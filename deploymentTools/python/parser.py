import argparse
import datetime

class parseArguments:
    def __init__(self, debug = True):
        self.debug = debug
        parser = argparse.ArgumentParser(description = 'python tool for iota deployment')
        parser.add_argument('-uuid', action = 'store', dest = 'uuid', required = True,
                                help = 'universal unique identifier (uuid) of devices')
        parser.add_argument('-file', action = 'store', dest = 'file', required = True,
                            help = 'file to deploy (.bin or .py)')
        parser.add_argument('-version', action = 'store', dest = 'version', required = True,
                            help = 'version to deploy')
        parser.add_argument('-blockSize', action = 'store', dest = 'blockSize', required = False,
                            help = 'size of blocks', default = 512)
        parser.add_argument('-hostnameBroker', action = 'store',  dest = 'hostnameBroker', required = False, 
                             help = 'hostname broker', default = 'localhost')
        parser.add_argument('-portBroker', action = 'store',  dest = 'portBroker', required = False, 
                             help = 'port broker', default = 1883)
        parser.add_argument('-dateExpiration', action = 'store',  dest = 'dateExpiration', required = True, 
                             help = 'date expiration')
        parser.add_argument('-incrementalNumber', action = 'store',  dest = 'incrementalNumber', required = True, 
                            help = 'incremental Number')
        self.arguments = parser.parse_args()
        
        if not self.doParse():
            raise Exception("can't parse parameters.")
    
    def printDebug(self, msg):
        if self.debug:
            print('parseArguments: ',  msg)

    def parseFileExtension(self, extensions):
        fileSplitted = self.arguments.file.split(".")
        if len(fileSplitted) > 1 : # have extension ?
            fileExtension = fileSplitted[1]
            if fileExtension in extensions:
                return True
            else:
                return False
        else:
            return False

    def doParse(self):
        self.printDebug("parsing parameters ...")
        self.printDebug("uuid: " + self.arguments.uuid)

        if not self.parseFileExtension(["bin","py"]):
            print("extension not supported.")
            return False
        
        self.printDebug("file: " + self.arguments.file)
        self.printDebug("version: " + self.arguments.version)
        
        try:
            self.arguments.blockSize = int(self.arguments.blockSize)
        except:
            print("block size need to be an integer.")
            return False
        
        self.printDebug("blockSize: " + str(self.arguments.blockSize))
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

        try:
            self.arguments.incrementalNumber = int(self.arguments.incrementalNumber)
        except:
            print("incremental number need to be an integer.")
            return False

        self.printDebug("incrementalNumber: " + str(self.arguments.incrementalNumber))

        return True        
        