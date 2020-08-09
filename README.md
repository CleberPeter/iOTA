# iota
An OTA framework for the IoT in compliance with the Internet Engineering Task Force (IETF) Secure Update Internet of Things (SUIT).

#### Manifest

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/manifest

  * **Message:** 
     ```json 
     {
     "incrementalNumber": 12,
     "dateExpiration": "2021-05-06",
     "type": "bin",
     }
     ```
  
#### Firmware

  * **Topic:** 
  
     iota/\<uuid\>/\<version\>/firmware

  * **Message:** 
  
     binary file.
