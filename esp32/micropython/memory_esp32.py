"""
    Implementation of memory management for esp32.
"""
from esp32 import Partition

PAGE_SIZE = 4096 # page size memory of esp32

class Memory:
    """
        Implementation of memory management for esp32.

        Args:
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            If the firmware is adapted to OTA returns object from class, else return exception.
    """

    def __init__(self, _debug=True):
        self.debug = _debug
        self.update_file_pages_counter = 0
        self.update_file_page_data = bytearray()

        current_partition = Partition(Partition.RUNNING)
        current_partition_name = current_partition.info()[4]

        self.plot_debug("current partition:" + str(current_partition.info()))

        if not current_partition_name.startswith("ota_"): # firmware is adapted to OTA ?
            print("memory_esp32: skipping... Partition table not adapted to OTA")
            raise SystemExit

        self.partition = current_partition.get_next_update()
        self.plot_debug("next partition:" + str(self.partition.info()))

    def get_current_partition_name(self):
        """
            returns current partition name.

            Args:
                void.
            Returns:
                string with current partition name (ota_0 or ota_1).
        """
        cur = Partition(Partition.RUNNING)
        return cur.info()[4]

    def get_next_partition_name(self):
        """
            returns next partition name.
            next partition is the partition wich will be booted after upgrade.

            Args:
                void.
            Returns:
                string with next partition name (ota_0 or ota_1).
        """
        return self.partition.info()[4]

    def write_on_memory(self):
        """
            write one page on esp32 flash memory.

            Args:
                void
            Returns:
                void
        """
        self.partition.writeblocks(self.update_file_pages_counter, self.update_file_page_data)

    def write(self, _data):
        """
            write data on OTA slot memory.
            the partition module only allows the writing of entire pages in flash memory.
            then this function stores the data in RAM until it is possible to write an
            entire page.

            Args:
                _data (bytes): data to write on OTA slot.
            Returns:
                void.
        """

        bytes_remaining_on_page = PAGE_SIZE - len(self.update_file_page_data)

        if len(_data) >= bytes_remaining_on_page:
            self.update_file_page_data += _data[0:bytes_remaining_on_page]

            self.write_on_memory()

            self.update_file_page_data = bytearray()
            self.update_file_page_data += _data[bytes_remaining_on_page:]

            self.update_file_pages_counter += 1
        else:
            self.update_file_page_data += _data

    def flush(self):
        """
            write remaining data on OTA slot memory.
            to the remaining data, 0xFF bytes are added to complete a flash memory page.

            Args:
                void.
            Returns:
                void.
        """

        bytes_on_page = len(self.update_file_page_data)
        written_info = "written: " + str(self.update_file_pages_counter)
        written_info += " blocks of "+str(PAGE_SIZE)+" bytes"

        if bytes_on_page > 0:
            written_info += " and 1 block of: " + str(bytes_on_page) + " bytes"

        self.plot_debug(written_info)

        # fill with 0xFF
        for i in range(PAGE_SIZE - bytes_on_page):
            self.update_file_page_data.append(0xFF)

        self.write_on_memory()
        self.partition.set_boot()

    def plot_debug(self, _message):
        """
            print debug messages.

            Args:
                _message (string): message to plot.
            Returns:
                void.
        """

        if self.debug:
            print('memory_esp32: ', _message)
