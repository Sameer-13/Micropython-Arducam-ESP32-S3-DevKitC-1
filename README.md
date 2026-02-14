# Arducam Mini Plus MicroPython Driver

A MicroPython driver for the Arducam Mini Plus camera module (OV5642 or OV2640) on ESP32-S3 DevKitC-1.

## Hardware Requirements

- ESP32-S3 DevKitC-1
- Arducam Mini Plus (OV5642 or OV2640)

Note: 
- The example code have been tested on the OV5642 module.
- If you are going to use the OV2640, make sure to find and download the register map ```OV264_reg.py``` from the internet.

## Wiring

| Arducam Pin | ESP32-S3 Pin |
|-------------|--------------|
| CS          | GPIO 9       |
| MOSI        | GPIO 10      |
| MISO        | GPIO 11      |
| SCK         | GPIO 12      |
| SDA         | GPIO 13      |
| SCL         | GPIO 14      |
| VCC         | 3.3V         |
| GND         | GND          |

## Installation

### Option A: Using esptool and mpremote (Command Line)

- Download the MicroPython firmware for ESP32-S3 from: [[https://micropython.org/download](https://micropython.org/download/)](https://micropython.org/download/ESP32_GENERIC_S3/)

Install the required tools:
```bash
pip install esptool mpremote
```

1. Flash MicroPython firmware to your ESP32-S3:
   ```bash
   esptool.py --chip esp32s3 --port /dev/ttyUSB0 erase_flash
   esptool.py --chip esp32s3 --port /dev/ttyUSB0 write_flash -z 0 ESP32_GENERIC_S3-xxxxxxxx.bin
   ```

2. Create a `lib` directory on the ESP32-S3:
   ```
   /lib/
       Arducam.py
       OV5642_reg.py
   ```

3. Upload the driver files:
   ```bash
   mpremote mkdir lib
   mpremote cp Arducam.py :lib/Arducam.py
   mpremote cp OV5642_reg.py :lib/OV5642_reg.py
   ```

4. Upload your main script:
   ```bash
   mpremote cp main_example.py :main.py
   ```

### Option B: Using Thonny (GUI)

1. Download and install Thonny from: [https://thonny.org](https://thonny.org/)

2. Download the MicroPython firmware for ESP32-S3 from: [[https://micropython.org/download](https://micropython.org/download/)](https://micropython.org/download/ESP32_GENERIC_S3/)

3. Open Thonny, go to **Tools → Options → Interpreter** and select "MicroPython (ESP32)".

4. Click "Install or update MicroPython" to flash the firmware to your ESP32-S3.

5. Connect to your ESP32-S3.

6. In the file browser, create a `lib` folder on the device.

7. Upload `Arducam.py` and `OV5642_reg.py` to the `lib` folder.

8. Upload your main script as `main.py` to the root of the device.

## Quick Start

Checkout ```main_example.py``` file

## File Structure

```
/
├── lib/
│   ├── Arducam.py      # Main camera driver
│   └── OV5642_reg.py   # OV5642 register definitions
└── main.py             # Your application code
```

## Supported Resolutions (OV5642)

- 320x240
- 640x480
- 1024x768
- 1280x960
- 1600x1200
- 2048x1536
- 2592x1944
- 1920x1080

You can easily set config the captured image using the helper functions in ```image_config.py```

## Troubleshooting

- **SPI interface Error**: Check wiring and ensure correct GPIO pins are used.
- **Can't find OV5642 module**: Verify I2C connections (SDA/SCL) and power supply.
- **Empty JPEG data**: Allow warm-up time after `init()` before capturing.

## License

MIT
