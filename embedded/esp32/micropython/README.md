# iota at esp32

Implementation of the iota framework in micropython for esp32

## Requeriments

Below are listed the necessary adjustments so that this OTA implementation can be used in esp32

1) Micropython Firmware

The micropython firmware applied to esp32 needs to be adapted to run OTA. The suitability refers mainly to the partition table of esp32, by default the table used by micropython is shown below:

```csv
Name,   Type, SubType, Offset,  Size, Flags
nvs,      data, nvs,     0x9000,  0x6000,
phy_init, data, phy,     0xf000,  0x1000,
factory,  app,  factory, 0x10000, 0x180000,
vfs,      data, fat,     0x200000, 0x200000,
```

However, for the API provided by espressif for the use of OTA, it is necessary to provide for at least two sections for OTA, as follows:

```csv
Name,   Type, SubType, Offset,   Size,     Flags
nvs,      data, nvs,     0x9000,   0x4000,
otadata,  data, ota,     0xd000,   0x2000,
phy_init, data, phy,     0xf000,   0x1000,
ota_0,    app,  ota_0,   0x10000,  0x180000,
ota_1,    app,  ota_1,   0x190000, 0x180000,
vfs,      data, fat,     0x310000, 0x0f0000,
```

For the partition table to be changed it is necessary that the micropython firmware is recompiled, unfortunately so far the micropython does not have on its page (https://micropython.org/download/esp32/) a pre-compiled binary compatible with the OTA. Therefore it is necessary that your firmware is compiled manually through its source available at: (https://github.com/micropython/micropython/tree/master) 

A procedure for the compilation is detailed in: (https://github.com/micropython/micropython/tree/master/ports/esp32), however for the resulting firmware to be adapted for OTA it is necessary that the compilation command is compiled as follows:

```console
$ make BOARD=GENERIC_OTA
```

Another alternative is the use of micropython firmware adapted to OTA, available at: (https://github.com/CleberPeter/iota/blob/master/embedded/esp32/micropython/firmware_ota.bin), which is based on version 1.12 of micropython and was used for testing the implementation of this framework.

2) MQTT library for Micropython

The standard library for MQTT in micropython umqtt available at: (https://github.com/micropython/micropython-lib) has some flaws.

The first, discussed here: (https://github.com/CleberPeter/micropython-lib/commit/b56e600f131f88e325ffe7d6e55d2a19d336999d) refers to the attempt to reconnect with the broker which after some time results in an IOError error (23) and makes it impossible for the device to making new connections.

The second, discussed here (https://github.com/CleberPeter/micropython-lib/commit/a55d72d21d4d2a985fab3ae81b5d40d40d6a0d6a), refers to the fact that the original implementation does not provide for receiving a message larger than the device's TCP window. However, a firmware update for micropython usually has more than 1MB.

Alternatively a fork of the library maintained here: (https://github.com/CleberPeter/micropython-lib) fix these problems.
