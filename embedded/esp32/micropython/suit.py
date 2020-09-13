"""
Implementation of OTA with MQTT Broker according to the SUIT specification for IoT devices.
"""
import time
import _thread
from umqttIota.robust import MQTTClient
from memory_esp32 import Memory
from manifest import Manifest

class FotaSuit:
    """
        Implementation of OTA with MQTT Broker according to the SUIT specification for IoT devices.

        Args:
            _uuid_project (string): universal unique id from project
                            (only used if not exists an local manifest).
            _id_device (string): id from device inside project.
            _version (integer): Current version of device
                            (only used if not exists an local manifest).
            _host_broker (string): address from broker.
            _callback_on_receive_update (function): called when upgrade file received.
            _delivery_type (string, optional): update search strategy pass: 'Pull' or 'Push'.
                                                Default is 'Push'.
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            object from class
    """
    def __init__(self, _uuid_project, _id_device, _version, _host_broker, \
                    _callback_on_receive_update, _delivery_type='Push', _debug=True):
        self.host_broker = _host_broker
        self.debug = _debug
        self.delivery_type = _delivery_type
        self.id_device = _id_device

        _id_on_broker = "FotaSuit-" + _uuid_project + "-" + self.id_device
        self.mqtt_client = MQTTClient(_id_on_broker, self.host_broker)
        self.mqtt_client.DEBUG = self.debug
        self.mqtt_client.set_callback(self.publish_received)

        self.update_file_size = 0
        self.memory = Memory(self.debug)
        _current_partition = self.memory.get_current_partition_name()
        _next_partition = self.memory.get_next_partition_name()

        self.callback_on_receive_update = _callback_on_receive_update

        if not (self.delivery_type == 'Push' or self.delivery_type == 'Pull'):
            raise ValueError("'type' variable not supported. Try 'Pull' or 'Push'.")

        while not self.connect_on_broker(True):
            self.print_debug("trying connection with broker...")
            time.sleep(3)

        self.manifest = Manifest(_current_partition, _next_partition)

        if self.manifest.load_and_update(_uuid_project, _version): # notify the upgrade

            #TODO: insert other informations in message like date
            _version = str(self.manifest.version)
            _msg = '{"idDevice":"'+self.id_device+'", "uuidProject":"'+_uuid_project+'"'
            _msg += ', "version":'+_version+', "date": ""}'
            self.publish_on_topic(_version, "updated", _msg)

        self.subscribe_on_topic("manifest") # waiting for manifest file
        _thread.start_new_thread(self.loop, ())
        self.print_debug("initialized.")

    def connect_on_broker(self, _clean_session):
        """
            try connection with MQTT broker.

            Args:
                _clean_session (boolean): clean session with broker.
            Returns:
                boolean indicating status of connection.
        """

        try:
            if not self.mqtt_client.connect(clean_session=_clean_session):
                self.print_debug("connected on broker.")
                return True
        except:
            self.print_debug("fail to connect with broker.")
            return False

    def subscribe_on_topic(self, _topic):
        """
            subscribe on iota topic: iota/<uuidProject>/<version>/_topic

            Args:
                _topic (string): topic name to subscribe.
            Returns:
                void.
        """
        _next_version = str(self.manifest.get_next_version())
        _topic = "iota/"+self.manifest.uuid_project+"/"+_next_version+"/"+_topic

        self.mqtt_client.subscribe(_topic.encode())
        self.print_debug("subscribed on topic: " + _topic)

    def publish_on_topic(self, _version, _topic, _msg):
        """
            publish on iota topic: iota/<uuidProject>/<idDevice>/<version>/_topic

            Args:
                _version (string): version to publish.
                _topic (string): topic name to publish.
                _msg (string): message to publish.
            Returns:
                void.
        """
        _topic = "iota/"+self.manifest.uuid_project+"/"+self.id_device+"/"+_version+"/"+_topic

        self.mqtt_client.publish(_topic.encode(), _msg.encode(), True) # retain this message!
        self.print_debug("published on topic: " + _topic + " msg:" + _msg)

    def publish_received(self, _topic, _message):
        """
            publish received on iota topic: iota/<uuid>/<version>/_topic

            Args:
                _topic (bytes): topic name from received message.
                _message (bytes): message received.
            Returns:
                void.
        """

        topic_str = _topic.decode("utf-8")
        topic_type = self.parse_topic(topic_str)

        if topic_type == 'manifest':
            self.print_debug("topic received: " + topic_str)
            msg_str = _message.decode("utf-8")
            self.print_debug("msg received: " + msg_str)

            if self.manifest.save_new(msg_str):
                self.print_debug('new version avaliable.')
                _name_new_file = self.manifest.new_files[0]['name']
                self.subscribe_on_topic(_name_new_file) # subscribe to receive update files

        elif topic_type == self.manifest.new_files[0]['name']:

            size_message = len(_message)
            self.update_file_size += size_message
            self.print_progress_download()
            self.memory.write(_message)

            if self.update_file_size == self.manifest.new_files[0]['size']:
                self.memory.flush() # save remaining bytes
                self.update_file_size = 0
                self.callback_on_receive_update()

        else:
            self.print_debug("topic not recognitzed: " + topic_type)

    def parse_topic(self, _topic_str):
        """
            parse iota topic: iota/<uuid>/<version>/<type>.
            Check if topic is valid and from iota.

            Args:
                _topic_str (string): topic name.
            Returns:
                <type> of topic.
        """

        topic_splitted = _topic_str.split("/")

        # message is from IOTA ?
        if len(topic_splitted) == 4 and topic_splitted[0] == "iota":
            # is for me ?
            if topic_splitted[1] == self.manifest.uuid_project:
                # version is the desired one
                if topic_splitted[2] == str(self.manifest.get_next_version()):
                    return topic_splitted[3]

                if topic_splitted[2] == str(self.manifest.version):
                    self.print_debug("device up to date")

        return ""

    def print_progress_download(self):
        """
            print the update file download progress

            Args:
                void
            Returns:
                void.
        """
        progress = 100*self.update_file_size/self.manifest.new_files[0]['size']
        self.print_debug("downloading update: "+str(progress)+"%")

    def loop(self):
        """
            eternal loop necessary to process MQTT stack.

            Args:
                void.
            Returns:
                never returns.
        """

        while True:
            self.mqtt_client.wait_msg()

    def print_debug(self, _message):
        """
            print debug messages.

            Args:
                _message (string): message to plot.
            Returns:
                void.
        """

        if self.debug:
            print('fotasuit: ', _message)
