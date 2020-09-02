# iota
An OTA framework for the IoT in compliance with the Internet Engineering Task Force (IETF) Secure Update Internet of Things (SUIT).

#### Manifest

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/manifest

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
  
#### Firmware

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/firmware

  * **Message:** 
  
     binary file.
