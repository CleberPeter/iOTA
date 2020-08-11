import os
import argparse
import datetime

class _parser:
    def __init__(self):
        self.debug = True
        parser = argparse.ArgumentParser(description = 'python tool for iota deployment')
        parser.add_argument('-uuid', action = 'store', dest = 'uuid', required = True,
                                help = 'universal unique identifier (uuid) of devices')
        parser.add_argument('-file', action = 'store', dest = 'file', required = True,
                            help = 'file to deploy (.bin or .py)')
        parser.add_argument('-version', action = 'store', dest = 'version', required = True,
                            help = 'version to deploy')
        parser.add_argument('-hostnameBroker', action = 'store',  dest = 'hostnameBroker', required = False, 
                             help = 'hostname broker', default = 'localhost')
        parser.add_argument('-portBroker', action = 'store',  dest = 'portBroker', required = False, 
                             help = 'port broker', default = 1883)
        parser.add_argument('-dateExpiration', action = 'store',  dest = 'dateExpiration', required = True, 
                             help = 'date expiration')
        parser.add_argument('-debug', action = 'store',  dest = 'debug', required = False, 
                             help = 'port broker', default = "False")
        self.arguments = parser.parse_args()
        
        if not self.doParse():
            raise Exception("can't parse parameters.")
    
    def printDebug(self, msg):
        if self.debug:
            print('parseArguments: ',  msg)

    def parseFileExtension(self, extensions):
        fileSplitted = self.arguments.file.split(".")
        if len(fileSplitted) > 1 : # have extension ?
            self.arguments.fileExtension = fileSplitted[1]
            if self.arguments.fileExtension in extensions:
                return True
            else:
                return False
        else:
            return False

    def doParse(self):
        if self.arguments.debug.lower() == 'true':
            self.debug = True
        elif self.arguments.debug.lower() == 'false':
            self.debug = False
        else:
            print("debug need to be true or false.")
            return False
        
        self.arguments.debug = self.debug
        self.printDebug("parsing parameters ...")
        self.printDebug("uuid: " + self.arguments.uuid)

        if not self.parseFileExtension(["bin","py"]):
            print("extension not supported.")
            return False
        
        self.printDebug("file: " + self.arguments.file)

        try:
            dirPath = os.path.dirname(os.path.realpath(__file__)) + "/"
            file = open(dirPath+self.arguments.file, "rb")
        except:
            print("can't open file.")
            return False
        
        self.arguments.fileData = file.read()
        self.arguments.fileSize = len(self.arguments.fileData)

        self.printDebug("file size: " + str(self.arguments.fileSize))
        
        try:
            self.arguments.version = int(self.arguments.version)
        except:
            print("version need to be an integer.")
            return False
        
        self.printDebug("version: " + str(self.arguments.version))
        self.printDebug("hostnameBroker: " + self.arguments.hostnameBroker)
        
        try:
            self.arguments.portBroker = int(self.arguments.portBroker)
        except:
            print("port broker need to be an integer.")
            return False
        
        self.printDebug("portBroker: " + str(self.arguments.portBroker))

        try:
            datetime.datetime.strptime(self.arguments.dateExpiration, '%Y-%m-%d')
        except ValueError:
            print("incorrect data expiration format, should be YYYY-MM-DD.")
            return False

        self.printDebug("dateExpiration: " + str(self.arguments.dateExpiration))

        return True        
        