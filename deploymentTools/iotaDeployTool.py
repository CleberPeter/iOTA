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
      
      topicManifest = "iota/" + self.args.uuidProject + "/" + str(self.args.version) + "/manifest"
      
      manifestClass = _manifest(self.args.uuidProject, self.args.version, self.args.type, self.args.dateExpiration, self.args.filesNames, self.args.filesSizes)
      manifestObject = manifestClass.__dict__

      try:
        manifestJson = json.dumps(manifestObject)
      except Exception as e:
        print("can't create manifest JSON. Error:")
        print(e)
        sys.exit()

      (rc, mid) = self.mqttObject.publish(topicManifest, manifestJson, self.qos, True)
      
      if not rc == _mqtt.MQTT_ERR_SUCCESS:
        print("can't publish manifest file.")
        sys.exit()

    def onPublishTopic(self, client, obj, mid):
      
      if self.sm == 'manifest':
        self.printDebug("manifest published.")
        self.sm = 'firmware'
        self.indexFiles = 0
        self.publishUpdate(self.indexFiles)
        self.indexFiles += 1
      elif self.sm == 'firmware':
        if self.indexFiles < len(self.args.filesNames):
          self.publishUpdate(self.indexFiles)
          self.indexFiles += 1
        else:
          print('update published with SUCCESS')
          sys.exit()
      else:
        print('state invalid')
        sys.exit()

    def publishUpdate(self, filesIndex):
        topicFirmware = "iota/" + self.args.uuidProject + "/" + str(self.args.version) + "/" + self.args.filesNames[filesIndex]
        (rc, mid) = self.mqttObject.publish(topicFirmware, self.args.filesData[filesIndex], self.qos, True)
        
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
