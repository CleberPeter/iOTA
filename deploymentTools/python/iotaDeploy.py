# -u 1 -f firmware -v 800 -sb 512 -h localhost -p 1883 -split -d 2021-05-06 -n 11
import getopt
import sys
from mqtt.client import mqttClient

debug = True

argv = sys.argv[1:] 

try:
    opts, args = getopt.getopt(argv, 'u:f:v:sb:h:p:d:n', ['uuid', 'firmwareFile', 'version', 'sizeOfBlocks', 'hostnameOfBroker', 'portOfBroker', 'dateExpiration', 'incrementalNumber'])
    print(opts)
    print(args)
    
    # Check if the options' length is 2 (can be enhanced)
    """f len(opts) == 0 and len(opts) > 2:
      print ('usage: add.py -a <first_operand> -b <second_operand>')
    else:
      # Iterate the options and get the corresponding values
      for opt, arg in opts:
         sum += int(arg)
      print('Sum is {}'.format(sum))
      """

except getopt.GetoptError:
    # Print something useful
    print ('usage: iotaDeploy.py -u 1 -f firmware -v 800 -sb 512 -h localhost -p 1883 -split -d 2021-05-06 -n 11')
    sys.exit(2)



#_mqttClient = mqttClient(debug)
