# iota
An OTA framework for the IoT in compliance with the Internet Engineering Task Force (IETF) Secure Update Internet of Things (SUIT).

### Manifest

  * **Topic:** iota/\<uuid\>/manifest

  * **Message:** 
  ```json 
  {
  "version": 800,
  "incrementalNumber": 12,
  "dateExpiration": "2021-05-06"
  "size": 512,
  "numberOfBlocks": 1024,
}
  ```
  

### Firmware

  * **Topic:** iota/\<uuid\>/firmware/0...\<numberOfBlocks\>

  * **Message:** binary block of \<size\> bytes.
