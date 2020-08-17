"""
Implementation of OTA with MQTT Broker according to the SUIT specification for IoT devices.
"""
import time
import json
import _thread
from umqttIota.robust import MQTTClient
from memory_esp32 import Memory

class FotaSuit:
    """
        Implementation of OTA with MQTT Broker according to the SUIT specification for IoT devices.

        Args:
            _uuid (string): universal unique id from device.
            _version (integer): current version from device.
            _host_broker (string): address from broker.
            _callback_on_receive_update (function): called when upgrade file received.
            _delivery_type (string, optional): update search strategy pass: 'Pull' or 'Push'.
                                                Default is 'Push'.
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            object from class
    """
    def __init__(self, _uuid, _version, _host_broker, _callback_on_receive_update, \
                    _delivery_type='Push', _debug=True):
        self.host_broker = _host_broker
        self.debug = _debug
        self.uuid = _uuid
        self.version = _version+1 # search by next version
        self.delivery_type = _delivery_type
        self.mqtt_client = MQTTClient("fotaSuit-" + _uuid, self.host_broker)
        self.mqtt_client.DEBUG = self.debug
        self.mqtt_client.set_callback(self.publish_received)
        self.update_file_size = 0
        self.manifest = None
        self.memory = Memory(self.debug)
        self.callback_on_receive_update = _callback_on_receive_update

        if not (self.delivery_type == 'Push' or self.delivery_type == 'Pull'):
            raise ValueError("'type' variable not supported. Try 'Pull' or 'Push'.")

        while not self.connect_on_broker(True):
            self.plot_debug("trying connection with broker...")
            time.sleep(3)

        self.subscribe_on_topic("manifest") # waiting for manifest file
        _thread.start_new_thread(self.loop, ())
        self.plot_debug("initialized.")

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
                self.plot_debug("connected on broker.")
                return True
        except:
            self.plot_debug("fail to connect with broker.")
            return False

    def subscribe_on_topic(self, _topic):
        """
            subscribe on iota topic: iota/<uuid>/<version>/_topic

            Args:
                _topic (string): topic name to subscribe.
            Returns:
                void.
        """

        self.mqtt_client.subscribe(("iota/"+self.uuid+"/"+str(self.version)+"/"+_topic).encode())
        self.plot_debug("subscribed on topic: " + _topic)

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
        msg_type = self.parse_topic(topic_str)

        if msg_type == 'manifest':
            self.plot_debug("topic received: " + topic_str)
            msg_str = _message.decode("utf-8")
            self.plot_debug("msg received: " + msg_str)

            self.plot_debug("manifest identified.")
            self.parse_manifest(msg_str)

        elif msg_type == 'firmware':

            size_message = len(_message)
            self.update_file_size += size_message
            self.print_progress_download()
            self.memory.write(_message)

            if self.update_file_size == self.manifest['fileSize']:
                self.memory.flush() # save remaining bytes
                self.update_file_size = 0
                self.callback_on_receive_update()

        else:
            self.plot_debug("topic not recognitzed: " + msg_type)

    def print_progress_download(self):
        """
            writes the update file download progress

            Args:
                void
            Returns:
                void.
        """
        progress = 100*self.update_file_size/self.manifest['fileSize']
        self.plot_debug("downloading update: "+str(progress)+"%")

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

        # is for me and version is the desired one?
        if (len(topic_splitted) == 4 and topic_splitted[1] == self.uuid \
                and topic_splitted[2] == str(self.version)):
            return topic_splitted[3]
        else:
            return ""

    def parse_manifest(self, _manifest_str):
        """
            parse manifest file:
                {
                "dateExpiration": "2021-05-06",
                "type": "bin",
                "fileSize": 1408512,
                }

            Args:
                _manifest_str (string): manifest file in string format.
            Returns:
                boolean indicating status of parsing.
        """

        try:
            self.manifest = json.loads(_manifest_str)
        except ValueError:
            self.plot_debug("error. Json invalid.")
            return False

        # TODO: check others informations like dateExpiration
        if self.manifest['type'] == "bin":
            self.plot_debug('new version avaliable.')
            self.subscribe_on_topic("firmware")

        return True

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

    def plot_debug(self, _message):
        """
            print debug messages.

            Args:
                _message (string): message to plot.
            Returns:
                void.
        """

        if self.debug:
            print('fotasuit: ', _message)
