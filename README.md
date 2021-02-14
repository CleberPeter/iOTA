# SOTARU

An OTA framework for the IoT in compliance with the Internet Engineering Task Force (IETF) Secure Update Internet of Things (SUIT). 

## Topology

This framework uses a centralized approach for the storage of update files where the update procedure can be initiated either by the server, PUSH approach, or initiated by the device, PULL approach.

The hybrid strategy for disseminating the update is made possible through an MQTT broker which retains all files necessary for the update. A manifest file present in a Broker topic tells the device whether an update exists or not, as well as the parameters required to perform the update.

The PULL approach is used when devices subscribe to the manifest topic in order to check for updates, if there are no updates, but the devices remain subscribed to this topic, the PUSH approach is activated, after all as soon as an update becomes available the device is notified.

## Requeriments 

* This framework uses an MQTT broker as a file repository, as a consequence an MQTT broker must exist on the update server and the MQTT protocol must be implemented by the embedded device.

* In this structure, devices of the same model and manufacturer must have a unique identifier called the project's unique universal identifier \ <uuidProject \>, which can be composed through the company's domain + device model as follows:

```python
company_domain = "G3PD.com.br"
model_device = "temperature_sensor_A"
<uuidProject> = SHA4(company_domain + model_device)
``` 

* Each device within the same project must have a unique identifier called \ <idDevice \> which can be obtained as follows:

```python
serial_number_from_device = "12345"
<idDevice> = SHA4(<uuidProject> + serial_number_from_device)
``` 

* The software/firmware <version> of the devices is an incremental numeric value. The device always updates to the immediately later version, that is, for a device that is currently running version 101, it must be updated to version 102 regardless of the fact that there are already new versions (103, 104, ...) available. This strategy aims to make the strategy of differential updates viable.

## Topics in Broker

All topics present in the broker are intended for a set of specific devices mapped through its \<uuidProject\> that have a specific software/firmware version defined through the \<version\> field.

#### Manifest

A manifest file is used to signal the device for an update, as well as to pass the necessary parameters for the execution of the update procedure. The manifest file can be obtained by subscribing to the following topic through the MQTT broker.

  * **Topic:** 
  
     iota/\<uuidProject\>/\<version\>/manifest

The current implementation of the manifest file uses the JWS(https://jwt.io/) standard to provide, when necessary, a digitally signed json file. Below are examples of signed and unsigned manifests:

  * **JWS signed:** 
  eyJ1dWlkUHJvamVjdCI6ICIxIiwgInZlcnNpb24iOiA4NywgInR5cGUiOiAicHkiLCAiZGF0ZUV4cGlyYXRpb24iOiAiMjAyMC0wNi0wNSIsICJmaWxlcyI6IFt7Im5hbWUiOiAic3VpdC5weSIsICJzaXplIjogMTQxMTIsICJzaWduIjogIjMwNDUwMjIwNTA5OGYyOWY4YzY0ZmZhNWYxNTQ2NTk4Y2I3NTBiOTIxMzBhYzk1MDczYzg1ZDA4MWMzYzRhMDYyZTExMGVhOTAyMjEwMGM1ZjE4ZTI0YTEzMzFkMDQ3OWYyMTNmODZkNmU2ZmEyMGQ4MzE4MWQzZDY3Njg4ZDlkMDg4OWE3ZDlkMGMyMDUifSwgeyJuYW1lIjogIm1haW4ucHkiLCAic2l6ZSI6IDQ1NjAsICJzaWduIjogIjMwNDUwMjIxMDBlMmE3NDZlMDc1MTQ4YTQxM2EyYzU1NmNkNGMzNjM1MjI0YmZkNjJhNzY0NzZlNjljYTYyNjg1NmNlNTExNDM3MDIyMDM3OWJhNmQzMTBmYjRhYjJlOTBmZjc1YjVlYTVmN2VkNGE5NmFhZTNmYjRlNzEzZWVjOWQ1MzVkMTExYzUzMTAifV0sICJrZXkiOiAiNDFhNjU2YTA2NTBiMjExZWM5OTBkMDQ3OTEzOTc5MjFmNDBlYzkyOWNiZmFkNGVmMTY5NTBjNzhiNGRlMjhhNTU1OGNhN2VkYjdjODYxMTg5NDgxMWMwNzg3ZjY5MDM2NTMwM2MyOTAyYmMxOTY4ZTBhYzQwNzJkNGJiY2VjN2UyZGQ5NjkzZWRmMjMyODA2YWQ0ZjZhZTgyMWUyODZkYzk3MWIxYTcyNjliOTE5OWUxOTliZDdlYTMwZTRmNDY1YzQ0YzE0YmE5ZGMyOWFhN2Q1ZTFlNmM2NTM2M2M0NDBjZGM2ODYyZDRmZTI5OTVjMmM1ZDU2M2E4ZGExZGU3NGNiYjNkYzZlZGVjZGY5ZDA2YWYyZDQ2MTFlN2Y5MmYzYTFkYmVhYzU3OTMwMzdkZjdjNGQ5OGFjMTA5OTNmOTQzMjI2YWQxNzA3ZWEyMzQ5ZjM4ZjhkNDJkMmUwNWE5YmI5OTRiNDIxODczNDY4Zjk1NDgwZjlkOWZkMjkxM2QzODk2M2ViNDgxMTQ3ZmQyOTljZmMyZjJmNmM2YTEyYTNhYzZmYzNlYzA3NWU1ZmFjYzRiNDNhODFmNDY4MWI1YjZkMjQzOGRhZWJlMzkyOGE0MWE5MzIyNzE2NjRkNjljYWYxOWQzYTE2NDY2ZGNhNzJiOTE3NThhNGJlYTA2MjcifQ==.eyJzaWduIjogIjMwNDUwMjIwMWFmZmExOWQyMmJjODM0YzBjYmNhMGQ4OGQwMDE3YmZiYTU0M2QyNjNkMTg0NGM1ODc5NGI4Nzc5YTU2NjI0ZTAyMjEwMGQ0YTc2ODdlMDIzNmM5MDRiZWIxNDgyOGUwNWY1NjkxOGU5NjQ5OGU4ZmQ1NGJjOGYzOTk1N2Q0ODFhOTViYWEifQ==
   
   The JWS standard provides, in addition to the conversion to base64 of the json object, the concatenation of the signature with the object signed using the character '.'
   
   * **Manifest object after base64 decode:**
   ```json
   {
   "uuidProject":"1",
   "version":87,
   "type":"py",
   "dateExpiration":"2020-06-05",
   "files":[
      {
         "name":"suit.py",
         "size":14112,
         "sign":"304502205098f29f8c64ffa5f1546598cb750b92130ac95073c85d081c3c4a062e110ea9022100c5f18e24a1331d0479f213f86d6e6fa20d83181d3d67688d9d0889a7d9d0c205"
      },
      {
         "name":"main.py",
         "size":4560,
         "sign":"3045022100e2a746e075148a413a2c556cd4c3635224bfd62a76476e69ca626856ce5114370220379ba6d310fb4ab2e90ff75b5ea5f7ed4a96aae3fb4e713eec9d535d111c5310"
      }
   ],
   "key":"41a656a0650b211ec990d04791397921f40ec929cbfad4ef16950c78b4de28a5558ca7edb7c8611894811c0787f690365303c2902bc1968e0ac4072d4bbcec7e2dd9693edf232806ad4f6ae821e286dc971b1a7269b9199e199bd7ea30e4f465c44c14ba9dc29aa7d5e1e6c65363c440cdc6862d4fe2995c2c5d563a8da1de74cbb3dc6edecdf9d06af2d4611e7f92f3a1dbeac5793037df7c4d98ac10993f943226ad1707ea2349f38f8d42d2e05a9bb994b421873468f95480f9d9fd2913d38963eb481147fd299cfc2f2f6c6a12a3ac6fc3ec075e5facc4b43a81f4681b5b6d2438daebe3928a41a932271664d69caf19d3a16466dca72b91758a4bea0627"
}
   ```
   
   * **Signature object after base64 decode:**
   ```json
   {
   "sign":"304502201affa19d22bc834c0cbca0d88d0017bfba543d263d1844c58794b8779a56624e022100d4a7687e0236c904beb14828e05f56918e96498e8fd54bc8f39957d481a95baa"
   }
   ```
   
   The sign attribute present in each of the update objects consists of the author's digital signature made with his private key through the ECDSA algorithm and with the SECP256K1 curve.
   
   The key attribute in the manifest represents the random key of the AES256 algorithm that was used to encrypt the update files. This key, in turn, is encrypted with the project's public key using the RSA-2048b algorithm.
   
   The dateExpiration field defines the cut-off date for the update to be applied and aims to protect against security attacks on eclipsed devices.

The type field defines the type of update. Currently two types **bin** and **py** are provided. A bin type update indicates to the device a monolithic update in which the firmware is updated. On the other hand, a py update indicates a modular update in which only a particular module or application is updated.

The fileSize field indicates the size in bytes of the update file.
   
   * **JWS unsigned:** 
  eyJ1dWlkUHJvamVjdCI6ICIxIiwgInZlcnNpb24iOiA4OCwgInR5cGUiOiAicHkiLCAiZGF0ZUV4cGlyYXRpb24iOiAiMjAyMC0wNi0wNSIsICJmaWxlcyI6IFt7Im5hbWUiOiAic3VpdC5weSIsICJzaXplIjogMTQwOTZ9LCB7Im5hbWUiOiAibWFpbi5weSIsICJzaXplIjogNDU0OX1dfQ==
  
  * **Manifest object after base64 decode:**
   ```json
   {
   "uuidProject":"1",
   "version":88,
   "type":"py",
   "dateExpiration":"2020-06-05",
   "files":[
      {
         "name":"suit.py",
         "size":14096
      },
      {
         "name":"main.py",
         "size":4549
      }
   ]
}
   ```

When the manifest file is digitally signed, the update is considered secure and all update files are encrypted with the AES256 algorithm using the random key provided key attribute of the manifest.

#### Monolithic Update

After discovering the existence of a **bin** update, the device must subscribe to this topic through which it can obtain the update file in binary format:

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/firmware

  * **Message:** 
  
     binary file.
     
#### Modular Update 

After discovering the existence of a **py** update, the device must subscribe to all topics listed in the manifest file, only after downloading all files can the device start the update.

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/file_1.py
     
     iota/\<uuid\>/\<version\>/file_2.py
     
     iota/\<uuid\>/\<version\>/file_x.py

  * **Messages:** 
  
     ASCII file.
     
#### Updated 

After an upgrade device notify the update server through the following topic:

  * **Topic:** 
  
     iota/\<uuidProject\>/\<idDevice\>/\<version\>/updated

  * **Messages:** 
  
     ```json 
     {
     "idDevice": "<idProject>",
     "uuidProject": "<uuidProject>",
     "version": <version>,
     "date": "<date_of_upgrade>",
     }
     ```

## Implementations

The front end implementations that perform the interaction between the developer and the framework can be found at:

https://github.com/CleberPeter/iOTA/tree/master/deploymentTools

The embedded implementations that perform the interaction between the devices and the framework can be found at:

https://github.com/CleberPeter/iOTA/tree/master/esp32/micropython
