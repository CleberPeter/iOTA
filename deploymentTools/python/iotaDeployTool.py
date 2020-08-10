import sys
import os
import json
import time
import paho.mqtt.client as _mqtt
from parser import _parser
from manifest import _manifest

class iotaDeployTool:
    def __init__(self, qos = 2):
      self.qos = qos
      self.args = _parser().arguments
      self.printDebug("parsed parameters.")
      self.mqttObject = _mqtt.Client()
      self.mqttObject.on_connect = self.onConnectWithBroker
      self.mqttObject.on_publish = self.onPublishTopic
      self.sm = 'manifest'

      while(True):
        try:
            self.printDebug("trying connection with broker ...")
            self.mqttObject.connect(self.args.hostnameBroker, 1883, 60)
            break
        except:
            self.printDebug("connection failed ...")
            time.sleep(3)
      
      self.mqttObject.loop_forever()
    
    def onConnectWithBroker(self, client, userdata, flags, rc):
      if rc == _mqtt.MQTT_ERR_SUCCESS:
        self.printDebug("connected with broker.")
        self.publishManifest()
      else:
        print("can't connect with broker.")
        sys.exit()

    def publishManifest(self):
      topicManifest = "iota/" + self.args.uuid + "/" + self.args.version + "/manifest"
      manifestObject = _manifest(self.args.fileExtension, self.args.dateExpiration, self.args.incrementalNumber)
      manifestJson = json.dumps(manifestObject.__dict__)
      
      (rc, mid) = self.mqttObject.publish(topicManifest, manifestJson, self.qos, True)
      
      if not rc == _mqtt.MQTT_ERR_SUCCESS:
        print("can't publish manifest file.")
        sys.exit()

    def onPublishTopic(self, client, obj, mid):
      
      if self.sm == 'manifest':
        self.printDebug("manifest published.")
        self.sm = 'firmware'
        self.publishUpdate()
      elif self.sm == 'firmware':
        print('update published with SUCCESS')
        sys.exit()
      else:
        print('state invalid')
        sys.exit()

    def publishUpdate(self):
      topicFirmware = "iota/" + self.args.uuid + "/" + self.args.version + "/firmware"
      
      try:
        dirPath = os.path.dirname(os.path.realpath(__file__)) + "/"
        file = open(dirPath+self.args.file, "rb")
      except:
        print("can't open file.")
        sys.exit()

      fileString = file.read()

      (rc, mid) = self.mqttObject.publish(topicFirmware, fileString, self.qos, True)
      
      if not rc == _mqtt.MQTT_ERR_SUCCESS:
        print("can't publish firmware file.")
        sys.exit()

    def printDebug(self, msg):
      if self.args.debug:
          print('iotaDeployTool: ',  msg)

def main():
  iotaDeployTool()  

if __name__ == "__main__":
  main()
