import _thread
import time
import json
from umqtt.robust import MQTTClient

class fotaSuit:
    def __init__(self, UUID, version, hostBroker, typeDelivery = 'Push', debug = True):
        self.hostBroker = hostBroker
        self.debug = debug
        self.UUID = UUID
        self.version = version
        self.typeDelivery = typeDelivery
        self.mqttClient = MQTTClient("fotaSuit-" + UUID, self.hostBroker)
        self.mqttClient.DEBUG = self.debug
        self.mqttClient.set_callback(self.mqttPublishReceived)
        
        if not (self.typeDelivery == 'Push' or self.typeDelivery == 'Pull'):
            raise ValueError("'type' variable not supported. Try 'Pull' or 'Push'.")
        
        if not self.mqttClient.connect(clean_session=True):
            self.plotDebug("connected on broker.")
            self.mqttClient.subscribe(b"iota/metadata/"+self.UUID)

        _thread.start_new_thread(self.loop, ())
        self.plotDebug("initialized.")

    def plotDebug(self, msg):
        if self.debug:
            print('fotasuit: ',  msg)

    def mqttPublishReceived(self, topic, msg):
        
        topic_splitted = topic.decode("utf-8").split("/")
        
        if (topic_splitted[1] == 'metadata'):
            
            self.plotDebug("metadata received: " + msg.decode("utf-8"))
            msg_data = json.loads(msg.decode("utf-8"))
            
            if (msg_data['UUID'] == self.UUID and msg_data['version'] > self.version):
                self.plotDebug('new version avaliable.') 

    def loop(self):
        while True:
            self.mqttClient.wait_msg()