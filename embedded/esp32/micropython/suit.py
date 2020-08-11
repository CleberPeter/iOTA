import _thread
import time
import json
from umqttIota.robust import MQTTClient

class fotaSuit:
    def __init__(self, uuid, version, hostBroker, typeDelivery = 'Push', debug = True):
        self.hostBroker = hostBroker
        self.debug = debug
        self.uuid = uuid
        self.version = version+1 # search by next version
        self.typeDelivery = typeDelivery
        self.mqttClient = MQTTClient("fotaSuit-" + uuid, self.hostBroker)
        self.mqttClient.DEBUG = self.debug
        self.mqttClient.set_callback(self.mqttPublishReceived)
        self.firmwareBytes = 0
        
        if not (self.typeDelivery == 'Push' or self.typeDelivery == 'Pull'):
            raise ValueError("'type' variable not supported. Try 'Pull' or 'Push'.")

        while (not self.connectOnBroker(True)):
            self.plotDebug("trying connection with broker...")
            time.sleep(3)
        
        self.subscribeOnTopic("manifest") # waiting for manifest file
        _thread.start_new_thread(self.loop, ())
        self.plotDebug("initialized.")
    
    
    def connectOnBroker(self, cleanSession):
        try:
            if not self.mqttClient.connect(clean_session=cleanSession):
                self.plotDebug("connected on broker.")
                return True
        except:
            return False

    def subscribeOnTopic(self, topic):
        self.mqttClient.subscribe(("iota/"+self.uuid+"/"+str(self.version)+"/"+topic).encode())
        self.plotDebug("subscribed on topic: " + topic)

    def mqttPublishReceived(self, topic, msg):
        
        topicStr = topic.decode("utf-8")
        self.plotDebug("topic received: " + topicStr)
        msgType = self.parseTopic(topicStr)
        
        if (msgType == 'manifest'):
            msgStr = msg.decode("utf-8")
            self.plotDebug("msg received: " + msgStr)
            
            self.plotDebug("manifest identified.")
            self.parseManifest(msgStr)

        elif (msgType == 'firmware'):
            self.firmwareBytes += len(msg)
            self.plotDebug("firmware received: " + str(self.firmwareBytes))

        else:
            self.plotDebug("topic not recognitzed: " + msgType)
    
    def parseTopic(self, topicStr):
        topicSplitted = topicStr.split("/")
        
        # /iota/uuid/version/type
        if (len(topicSplitted) == 4 and topicSplitted[1] == self.uuid and topicSplitted[2] == str(self.version)): # is for me and version is the desired one?
            return topicSplitted[3]
        else:
            return ""

    def parseManifest(self, msgStr):

        """
        {
        "dateExpiration": "2021-05-06",
        "type": "bin",
        }
        """
        
        try:
            msgObject = json.loads(msgStr)
        except:
            self.plotDebug("error. Json invalid.")
            return False
        
        # TODO: check others informations like dateExpiration and incrementalNumber
        if (msgObject['type'] == "bin"):
            self.plotDebug('new version avaliable.')
            self.subscribeOnTopic("firmware")

        return True
    
    def loop(self):
        while True:
            self.mqttClient.wait_msg()

    def plotDebug(self, msg):
        if self.debug:
            print('fotasuit: ',  msg)
