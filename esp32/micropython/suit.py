"""
Implementation of OTA with MQTT Broker according to the SUIT specification for IoT devices.
"""
import os
import time
from umqttIota.robust import MQTTClient
from memory_esp32 import Memory
from manifest import Manifest
from security import Security

def unpad(s):
    while(s[-1] == 0):
        s = s[0:len(s)-1]
    return s

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
            _pubkey (string): public key from server.
            _delivery_type (string, optional): update search strategy pass: 'Pull' or 'Push'.
                                                Default is 'Push'.
            _debug (boolean, optional): enable debug from class. Default is True.
        Returns:
            object from class
    """
    def __init__(self, _uuid_project, _id_device, _version, _host_broker, \
                    _callback_on_receive_update, _private_key=None, _public_key=None, _delivery_type='Push', _debug=True):
        self.host_broker = _host_broker
        self.debug = _debug
        self.delivery_type = _delivery_type
        self.id_device = _id_device
        self.private_key = _private_key
        self.public_key = _public_key
        self.security = Security()
        self.message_incoming = bytes()
        self.do_decrypt = False
        self.aes_random_key = ''

        _id_on_broker = "FotaSuit-" + _uuid_project + "-" + self.id_device
        self.mqtt_client = MQTTClient(_id_on_broker, self.host_broker)
        self.mqtt_client.DEBUG = self.debug
        self.mqtt_client.set_callback(self.publish_received)

        self.update_file_size = 0
        self.update_file_index = 0
        self.update_file_handle = 0
        self.memory = Memory(self.debug)
        _next_partition = self.memory.get_next_partition_name()

        self.callback_on_receive_update = _callback_on_receive_update

        if not (self.delivery_type == 'Push' or self.delivery_type == 'Pull'):
            raise ValueError("'type' variable not supported. Try 'Pull' or 'Push'.")

        while not self.connect_on_broker(True):
            self.print_debug("trying connection with broker...")
            time.sleep(3)

        self.manifest = Manifest(_next_partition, _public_key)
        self.manifest.load(_uuid_project, _version)

        files = os.listdir()
        if '_updated.iota' in files: #have an update ?

            # notify the upgrade
            _version = str(self.manifest.version)
            _msg = '{"idDevice":"'+self.id_device+'", "uuidProject":"'+_uuid_project+'"'
            _msg += ', "version":'+_version+', "date": ""}'

            #TODO: insert other informations in message like date
            self.publish_on_topic(_version, "updated", _msg)
            os.remove('_updated.iota')
            
        self.subscribe_task = "manifest" # waiting for manifest file
        self.print_debug("initialized.")

        # _thread.start_new_thread(self.loop, ())
        

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

    def get_name_topic(self, _topic):
        return 

    def unsubscribe_from_topic(self, _topic):
        """
            unsubscribe from iota topic: iota/<uuidProject>/<version>/_topic

            Args:
                _topic (string): topic name to unsubscribe.
            Returns:
                void.
        """
        _next_version = str(self.manifest.get_next_version())
        _topic = "iota/"+self.manifest.uuid_project+"/"+_next_version+"/"+_topic

        self.mqtt_client.unsubscribe(_topic.encode())
        self.print_debug("unsubscribed on topic: " + _topic)

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

    def verify_file(self):

        """
            verifies the signature from upgrade file

            Args:
                void.
            Returns:
                boolean indicating the success of the signature verification.
        """

        _file_data = self.security.sha256_ret()

        if self.upgrade_is_secure():

            _sign_str = self.manifest.new['files'][self.update_file_index]['sign']
            
            try: 
                if self.security.ecdsa_secp256k1_verifiy_sign(self.public_key, _file_data, _sign_str):
                    return True
            except Exception as error:
                print(error)

            return False

        else:
            return True
    
    def upgrade_is_secure(self):
        return 'key' in self.manifest.new

    def publish_received(self, _topic, _message, _size_msg):
        """
            publish received on iota topic: iota/<uuid>/<version>/_topic

            Args:
                _topic (bytes): topic name from received message.
                _message (bytes): message received.
                _size_msg (int): total message size
            Returns:
                void.
        """
        _topic_str = _topic.decode("utf-8")
        _topic_name = self.parse_topic(_topic_str)
        
        if _topic_name == 'manifest':
            
            self.message_incoming += _message
            
            if len(self.message_incoming) == _size_msg:
                
                _msg_str = self.message_incoming.decode("utf-8")
                self.print_debug("topic received: " + _topic_str)
                self.print_debug("msg received: " + _msg_str)

                if self.manifest.save_new(_msg_str):
                    self.print_debug('new version avaliable.')
    
                    self.update_file_size = 0
                    self.update_file_index = 0
                    _name_new_file = self.manifest.new['files'][self.update_file_index]['name']

                    if self.manifest.new['type'] == 'py':
                        self.update_file_handle = open("_" + _name_new_file, "a")

                    if self.upgrade_is_secure():
                        self.do_decrypt = True # starts decryption only when this callback is closed
                        
                    self.subscribe_task = _name_new_file # subscribe to receive update file

                self.message_incoming = bytes()
             
        elif _topic_name == self.manifest.new['files'][self.update_file_index]['name']:

            self.update_file_size += len(_message)
            self.print_progress_download()

            if self.upgrade_is_secure():

                self.message_incoming += _message
                
                _chunks = int(len(self.message_incoming)/16)
                _message = self.message_incoming[0:_chunks*16]
                
                self.message_incoming = self.message_incoming[_chunks*16:]
                _message = self.security.aes_256_cbc_decrypt(_message)

                if self.update_file_size == self.manifest.new['files'][self.update_file_index]['size']: # finish download file
                    _message = unpad(_message)

            self.security.sha256_update(_message)
            
            if self.manifest.new['type'] == 'bin':
                self.memory.write(_message)
            else:
                self.update_file_handle.write(_message)
            
            if self.update_file_size == self.manifest.new['files'][self.update_file_index]['size']: # finish download file
                
                if self.manifest.new['type'] == 'bin':
                    self.memory.flush() # save remaining bytes
                else:
                    self.update_file_handle.close() # close update file

                if self.verify_file():

                    if self.upgrade_is_secure():
                        self.print_debug("signature verification successfully.")

                    self.update_file_index += 1 # another file received
                    self.update_file_size = 0

                    if self.update_file_index == len(self.manifest.new['files']): # downloaded all files ?
                        
                        for _file in self.manifest.new['files']:
                            self.unsubscribe_from_topic(_file['name'])
                        
                        self.callback_on_receive_update()
                    else:
                        _name_new_file = self.manifest.new['files'][self.update_file_index]['name']
                        self.update_file_handle = open("_" + _name_new_file, "a") # open another file
                        self.subscribe_task = _name_new_file # subscribe to receive update file
                        
                        if self.upgrade_is_secure():
                            self.security.aes_256_cbc_init(self.aes_random_key)

                else:
                    
                    self.print_debug("signature verify failed.")
                    
                    self.update_file_index = 0
                    self.update_file_size  = 0
                    self.message_incoming = bytes()

                    files = os.listdir()

                    for _file in self.manifest.new['files']:
                        self.unsubscribe_from_topic(_file['name'])

                    for file in files: # removes garbage
                        if file[0] == '_': # is an update file (_xxx)
                            os.remove(file)

                self.message_incoming = bytes()
            
        else:
            self.print_debug("topic not recognitzed: " + _topic_name)
            self.message_incoming = bytes()
        
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
        _progress = str(100*self.update_file_size/self.manifest.new['files'][self.update_file_index]['size'])
        _name_file = str(self.manifest.new['files'][self.update_file_index]['name'])
        self.print_debug("downloading update file: '"+_name_file+"' - progress: "+_progress+"%")

    def loop(self):
        """
            eternal loop necessary to process MQTT stack.

            Args:
                void.
            Returns:
                never returns.
        """

        if self.do_decrypt == True: # decryption have priority

            self.do_decrypt = False
            try:
                self.aes_random_key = self.security.rsa_decrypt(self.private_key, self.manifest.new['key'])
            except Exception:
                self.print_debug('decryption AES key failed.')
                self.subscribe_task = '' # cancel upgrade
                return
            
            print('aes secret random key: ', self.aes_random_key)
            self.security.aes_256_cbc_init(self.aes_random_key)
                
        if not self.subscribe_task == '':
            self.subscribe_on_topic(self.subscribe_task)
            self.subscribe_task = ''

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
