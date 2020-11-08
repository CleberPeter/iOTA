import sys
import os
import json
import time
import paho.mqtt.client as _mqtt
from parser import _parser
from manifest import _manifest
import base64
import random
import string

def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

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
      
      _aes256_secret_random_key = None
      if self.args.authorPrivateKey:
        _aes256_secret_random_key = get_random_string(32).encode('utf8') # 32B -> aes256
        print('secret random key: ', _aes256_secret_random_key.decode('utf-8'))
      
      manifestClass = _manifest(self.args.uuidProject, self.args.version, self.args.type, self.args.dateExpiration, self.args.filesNames, self.args.filesSizes, self.args.filesData, self.args.authorPrivateKey, self.args.projectPublicKey, _aes256_secret_random_key)
      manifestObject = manifestClass.__dict__
      
      try:

        manifestJson = json.dumps(manifestObject).encode("utf-8")
        
        if self.args.authorPrivateKey:
          signObject = {
            "sign": manifestClass.sign_ecdsa(manifestJson, self.args.authorPrivateKey)
          }

          signJson = json.dumps(signObject).encode()
          manifestJson = base64.b64encode(manifestJson).decode("utf-8") + "." + base64.b64encode(signJson).decode("utf-8")
        
        else:
          manifestJson = base64.b64encode(manifestJson).decode("utf-8")
        
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
        
        try: 
          (rc, mid) = self.mqttObject.publish(topicFirmware, self.args.filesData[filesIndex], self.qos, True)
          
          if not rc == _mqtt.MQTT_ERR_SUCCESS:
            print("can't publish firmware file.")
            sys.exit()
        except Exception as error:
          print(error)

    def printDebug(self, msg):
      if self.args.debug:
          print('iotaDeployTool: ',  msg)

def main():
  iotaDeployTool()  

if __name__ == "__main__":
  main()
