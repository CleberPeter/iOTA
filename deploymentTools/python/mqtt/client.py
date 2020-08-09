import paho.mqtt.client as mqtt
import time
import threading

class _mqttClient:

    def __init__(self, callbackOnConnect, debug = True):
        self.client = mqtt.Client()
        self.debug = debug
        self.client.on_connect = self.onConnect
        self.callbackOnConnect = callbackOnConnect

        while(True):
            try:
                self.printDebug("trying connection with broker ...")
                self.client.connect("localhost", 1883, 60)
                break
            except:
                self.printDebug("connection Failed ...")
                time.sleep(3)

        thread = threading.Thread(target=self.loop, args=())
        thread.start()

    def onConnect(self, client, userdata, flags, rc):
      if (rc == mqtt.MQTT_ERR_SUCCESS):
        self.printDebug("connected with broker.")
        self.callbackOnConnect(True)
      else:
        self.callbackOnConnect(False)
    
    def publish(self, topic, msg, qos, retain):
        (rc, mid) = self.client.publish(topic, msg, qos, retain)
        if rc == mqtt.MQTT_ERR_SUCCESS:
            return True
        else:
            return False

    def printDebug(self, msg):
        if self.debug:
            print('mqttClient: ',  msg)

    def loop(self):
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        self.client.loop_forever()