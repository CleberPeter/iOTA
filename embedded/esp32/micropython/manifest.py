"""
Implementation of manifest function from IOTA framework.
"""
import os
import json

class Manifest:
    """
        load the current device manifest.
        Will be loaded from the last downloaded manifest or a default manifest will be created
        with the uuid and versions passed as a parameter by the user

        Args:
            _uuid (string): universal unique id from device to create a default manifest
                            (only used if not exists an local manifest).
            _version (integer): current version of device to create a default manifest
                            (only used if not exists an local manifest).
            _current_partition_name (string): used to verify an success of upgrade,
                                              must be the same as determined by the update manifest
            _next_partition_name (string): attached to the manifest to determine which
                                           partition should be booted after the upgrade
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            boolean indicating status of requisition.
    """
    def __init__(self, _uuid, _version, _current_partition_name, \
                _next_partition_name, _debug=True):

        self.debug = _debug
        self.current_partition_name = _current_partition_name
        self.next_partition_name = _next_partition_name

        self.update(_uuid, _version)

        _manifest_file = open('manifest.json', 'r')
        _manifest_str = _manifest_file.read()
        _manifest_file.close()

        self.load(_manifest_str)
        self.print_debug("current manifest:\n" + _manifest_str)

    def update(self, _uuid, _version):
        """
            update manifest to newest version if necessary.

            Args:
                _uuid (string): universal unique id from device to create a default manifest
                                (only used if not exists an local manifest).
                _version (integer): current version of device to create a default manifest
                                (only used if not exists an local manifest).
            Returns:
                void.
        """
        files = os.listdir()

        # create default manifest, if necessary. (only in first execution)
        if not 'manifest.json' in files:
            _manifest_file = open('manifest.json', 'x')
            _manifest_str = self.get_default(_uuid, _version)
            _manifest_file.write(_manifest_str)
            _manifest_file.close()

        if '_manifest.json' in files: # have an new manifest ? make upgrade

            _manifest_file = open('_manifest.json', 'r')
            _manifest_str = _manifest_file.read()
            _manifest_file.close()

            try:
                _manifest_object = json.loads(_manifest_str)

                if _manifest_object['ota'] == self.current_partition_name: # changed OTA partition ?
                    _manifest_file = open('manifest.json', 'w')
                    _manifest_file.write(_manifest_str)
                    _manifest_file.close()
                    self.print_debug('update manifest with success.')
                else:
                    self.print_debug('failed to update.')
            except ValueError:
                self.print_debug("error. invalid manifest file.")
                return False

            os.remove('_manifest.json')
        else:
            self.print_debug('manifest already up to date.')

    def save(self, _new_manifest_object):
        """
            saves the new manifest file to the file system.
            NOT update the RAM manifest.

            Args:
                _new_manifest_str (object): manifest in dict format.
            Returns:
                boolean indicating success of operation.
        """
        try:
            _new_manifest_str = json.dumps(_new_manifest_object)
        except ValueError:
            self.print_debug("error. invalid manifest file.")
            return False

        _manifest_file = open('_manifest.json', 'x')
        _manifest_file.write(_new_manifest_str)
        _manifest_file.close()

        return True

        #TODO: check this question!
        # self.load(_new_manifest_str) # for now, only reloads manifest in RAM when reboot.

    def save_new(self, _str):
        """
            set new manifest file:
                {
                "dateExpiration": "2021-05-06",
                "uuid": "uuid",
                "version": version,
                "type": "bin",
                "fileSize": 1408512,
                }

            Args:
                _str (string): manifest file in string format.
            Returns:
                boolean indicating status of parsing.
        """

        try:
            _manifest_object = json.loads(_str)
        except ValueError:
            self.print_debug("error. invalid manifest file.")
            return False

        # is for this device and is the desired version ?
        if _manifest_object['uuid'] == self.uuid and \
           _manifest_object['version'] == self.get_next_version():

            # TODO: check others informations like dateExpiration
            if _manifest_object['type'] == "bin":

                # sets parition wich must be booted after upgrade
                # used to verify sucessfull of upgrade
                _manifest_object['ota'] = self.next_partition_name

                return self.save(_manifest_object)

        return False

    def load(self, _manifest_str):
        """
            load manifest object from string.

            Args:
                _manifest_str (string): manifest file in string format.
            Returns:
                boolean indicating loading status.
        """
        try:
            _manifest_object = json.loads(_manifest_str)
            self.uuid = _manifest_object['uuid']
            self.version = _manifest_object['version']
            self.date_expiration = _manifest_object['dateExpiration']
            self.type = _manifest_object['type']
            self.file_size = _manifest_object['fileSize']
        except ValueError:
            raise ValueError("can't load manifest file.")

    def get_default(self, _uuid, _version):
        """
            returns default manifest file with _uuid and _version provided.

            Args:
                _uuid (string): universal unique id from device.
                _version (integer): Current version of device.
            Returns:
                string with minimal manifest.
        """
        _default_manifest = '{"uuid":"' + _uuid + '", "version":' + str(_version)
        _default_manifest += ', "dateExpiration": "", type: "", fileSize: 0}'

        return _default_manifest

    def get_next_version(self):
        """
            returns the new version based on the standard established
            by IOTA framework for version management.

            Args:
                void.
            Returns:
                integer with new version.
        """
        return self.version+1

    def print_debug(self, _message):
        """
            print debug messages.

            Args:
                _message (string): message to plot.
            Returns:
                void.
        """

        if self.debug:
            print('manifest: ', _message)
    