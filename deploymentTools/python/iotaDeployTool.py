import sys
import json
from mqtt.client import _mqttClient
from parser import _parser
from manifest import _manifest

class iotaDeployTool:
    def __init__(self, debug = True, qos = 2):
      self.debug = debug
      self.qos = qos
      self.parserObject = _parser(self.debug)
      self.printDebug("parsed parameters.")
      self.mqttClientObject = _mqttClient(self.onConnectWithBroker, self.debug)

    def onConnectWithBroker(self, success):
      if success:
        if self.publishManifest():
          self.printDebug("manifest published")
        else:
          print("can't publish manifest.")
          exit   
      else:
        print("can't connect with broker.")
        exit

    def publishManifest(self):
      topicManifest = "iota/" + self.parserObject.arguments.uuid + "/" + self.parserObject.arguments.version + "/manifest"
      manifestObject = _manifest(self.parserObject.arguments.fileExtension, self.parserObject.arguments.dateExpiration, self.parserObject.arguments.incrementalNumber)
      manifestJson = json.dumps(manifestObject.__dict__)

      if self.mqttClientObject.publish(topicManifest, manifestJson, self.qos, True):
        return True
      else:
        return False

    def printDebug(self, msg):
      if self.debug:
          print('iotaDeployTool: ',  msg)

def main():
  debug = True
  iotaDeployTool(debug)  

if __name__ == "__main__":
  main()
