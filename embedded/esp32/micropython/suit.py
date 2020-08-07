import _thread
import time
import json
from umqtt.robustModified import MQTTClient

class fotaSuit:
    def __init__(self, uuid, version, hostBroker, typeDelivery = 'Push', debug = True):
        self.hostBroker = hostBroker
        self.debug = debug
        self.uuid = uuid
        self.version = version
        self.typeDelivery = typeDelivery
        self.mqttClient = MQTTClient("fotaSuit-" + uuid, self.hostBroker)
        self.mqttClient.DEBUG = self.debug
        self.mqttClient.set_callback(self.mqttPublishReceived)
        
        if not (self.typeDelivery == 'Push' or self.typeDelivery == 'Pull'):
            raise ValueError("'type' variable not supported. Try 'Pull' or 'Push'.")

        while (not self.connectOnBroker(True)):
            self.plotDebug("trying connection with broker...")
            time.sleep(3)
        
        self.subscribeOnTopic("metadata") # waiting for metadata
        _thread.start_new_thread(self.loop, ())
        self.plotDebug("initialized.")
        
    def connectOnBroker(self, cleanSession):
        try:
            if not self.mqttClient.connect(clean_session=cleanSession):
                self.plotDebug("connected on broker.")
                return True
        except:
            return False

    def plotDebug(self, msg):
        if self.debug:
            print('fotasuit: ',  msg)

    def subscribeOnTopic(self, topic):
        self.mqttClient.subscribe(("iota/"+self.uuid+"/"+topic).encode())
        self.plotDebug("subscribed on topic: " + topic)

    def loop(self):
        while True:
            self.mqttClient.wait_msg()

    def mqttPublishReceived(self, topic, msg):
        
        topicStr = topic.decode("utf-8")
        msgStr = msg.decode("utf-8")

        self.plotDebug("topic received: " + topicStr)
        self.plotDebug("msg received: " + msgStr)

        msgType = self.parseTopic(topicStr)
        
        if (msgType == 'metadata'):
            self.plotDebug("metadata identified.")
            self.parseMetada(msgStr)

        elif (msgType == 'firmware'):
            self.plotDebug("firmware received.")
        else:
            self.plotDebug("topic not recognitzed: " + msgType)

    
    def parseTopic(self, topicStr):
        topicSplitted = topicStr.split("/")
        
        # /iota/uuid/type
        if (len(topicSplitted) == 3 and topicSplitted[1] == self.uuid): # is for me?
            return topicSplitted[2]
        else:
            return ""

    def parseMetada(self, msgStr):

        """
            {
            "version": 800,
            "incrementalNumber": 12,
            "dateExpiration": "2021-05-06",
            "sizeOfBlocks": 512,
            "numberOfBlocks": 1024,
            }
        """
        
        try:
            msg_data = json.loads(msgStr)
        except:
            self.plotDebug("error. Json invalid.")
            return False
        
        # TODO: check others informations like dateExpiration and incrementalNumber
        if (msg_data['version'] > self.version):
            self.plotDebug('new version avaliable.')
            self.subscribeOnTopic("firmware")

        return True
    