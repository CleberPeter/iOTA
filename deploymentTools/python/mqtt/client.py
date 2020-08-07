import paho.mqtt.client as mqtt
import time

class mqttClient:

    def __init__(self, debug = True):
        self.client = mqtt.Client()
        self.debug = debug
        self.client.on_connect = self.on_connect

        while(True):
            try:
                self.plotDebug("Trying connection with broker ...")
                self.client.connect("localhost", 1883, 60)
                break
            except:
                self.plotDebug("Connection Failed ...")
                time.sleep(3)

        self.loop()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        self.plotDebug("Connected with result code "+str(rc))

    def plotDebug(self, msg):
        if self.debug:
            print('mqttClient: ',  msg)

    def loop(self):
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        self.client.loop_forever()