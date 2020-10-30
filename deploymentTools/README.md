## Usage Example

### Monolithic
python3 iotaDeployTool.py -uuid 1 -files application_ota.bin -type bin -version 12 -dateExpiration 2020-06-05 -debug true

### Diferential
python3 iotaDeployTool.py -uuid 1 -files ../esp32/micropython/suit.py,../esp32/micropython/main.py -type py -version 78 -dateExpiration 2020-06-05 -debug true

### With Authentication
python3 iotaDeployTool.py -uuid 1 -files ../esp32/micropython/suit.py,../esp32/micropython/main.py -type py -version 78 -dateExpiration 2020-06-05 -debug true -privateKey 7964370f8571a7a63b519b4067e3e364100804a0f0b285e1292bf6d8636b168a
