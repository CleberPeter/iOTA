# iota

An OTA framework for the IoT in compliance with the Internet Engineering Task Force (IETF) Secure Update Internet of Things (SUIT). 

## Topology

This framework uses a centralized approach for the storage of update files where the update procedure can be initiated either by the server, PUSH approach, or initiated by the device, PULL strategy.

The hybrid strategy for disseminating the update is made possible through an MQTT broker which retains all files necessary for the update. A manifest file present in a Broker topic tells the device whether an update exists or not, as well as the parameters required to perform the update.

The PULL approach is used when devices subscribe to the manifest topic in order to check for updates, if there are no updates, but the devices remain subscribed to this topic, the PUSH approach is activated, after all as soon as an update becomes available the device is notified.

## Requeriments 

* This framework uses an MQTT broker as a file repository, as a consequence an MQTT broker must exist on the update server and the MQTT protocol must be implemented by the embedded device.

* In this framework devices of the same model and manufacturer must have a unique identifier called unique universal identifier \<uuid\>, which can be composed through the company domain + device model as follows:

```python
<uuid> = SHA256("G3PD.com.br" + "temperature_sensor_A")
``` 

* The software/firmware <version> of the devices is an incremental numeric value. The device always updates to the immediately later version, that is, for a device that is currently running version 101, it must be updated to version 102 regardless of the fact that there are already new versions (103, 104, ...) available. This strategy aims to make the strategy of differential updates viable.

## Topics in Broker

All topics present in the broker are intended for a set of specific devices mapped through its \<uuid\> that have a specific software/firmware version defined through the \<version\> field.

#### Manifest

A manifest file is used to signal the device for an update, as well as to pass the necessary parameters for the execution of the update procedure. The manifest file can be obtained by subscribing to the following topic through the MQTT broker.

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/manifest

The current implementation for the manifest file uses the JSON standard and follows:

  * **Message:** 
     ```json 
     {
     "dateExpiration": "2021-05-06",
     "uuid": "\<uuid\>",
     "version": \<version\>,
     "type": "bin",
     "fileSize": 1408512,
     }
     ```

The dateExpiration field defines the cut-off date for the update to be applied and aims to protect against security attacks on eclipsed devices.

The type field defines the type of update. Currently two types **bin** and **py** are provided. A bin type update indicates to the device a monolithic update in which the firmware is updated. On the other hand, a py update indicates a modular update in which only a particular module or application is updated.

The fileSize field indicates the size in bytes of the update file.

#### Firmware

After discovering the existence of an update the device must subscribe to this topic through which it can obtain the update file in binary format

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/firmware

  * **Message:** 
  
     binary file.

## Implementations

The front end implementations that perform the interaction between the developer and the framework can be found at:

https://github.com/CleberPeter/iota/tree/master/deploymentTools

The embedded implementations that perform the interaction between the devices and the framework can be found at:

https://github.com/CleberPeter/iota/tree/master/embedded
