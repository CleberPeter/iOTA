import sys
from mqtt.client import mqttClient
from parser import parseArguments

debug = True

def printDebug(msg):
  if debug:
      print('iotaDeployTool: ',  msg)

_parser = parseArguments(debug)

printDebug(_parser.arguments.file)

#_mqttClient = mqttClient(debug)
