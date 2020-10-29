## Usage Example

### Binary file
python3 iotaDeployTool.py -uuid 1 -files application_ota.bin -type bin -version 12 -dateExpiration 2020-06-05 -debug true

### Python files
python3 iotaDeployTool.py -uuid 1 -files ../esp32/micropython/suit.py,../esp32/micropython/main.py -type py -version 78 -dateExpiration 2020-06-05 -debug true

### With Authentication
python3 iotaDeployTool.py -uuid 1 -files ../esp32/micropython/suit.py,../esp32/micropython/main.py -type py -version 78 -dateExpiration 2020-06-05 -debug true -privateKey a039169eb60af31b3bf291fab39a15a2f1300663370ff8c6dcc5a8e2fe3c3690
