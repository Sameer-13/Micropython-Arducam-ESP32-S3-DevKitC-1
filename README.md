# Arducam Mini 5MP Plus (OV5642) MicroPython Driver

A MicroPython driver for the Arducam Mini 5MP Plus camera module (OV5642) on ESP32-S3 DevKitC-1.

## Hardware Requirements

- ESP32-S3 DevKitC-1
- Arducam Mini 5MP Plus (OV5642)

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

1. Flash MicroPython firmware to your ESP32-S3.

2. Create a `lib` directory on the ESP32-S3:
   ```
   /lib/
       Arducam.py
       OV5642_reg.py
   ```

3. Upload the driver files using Thonny, mpremote, or ampy:
   ```bash
   mpremote mkdir lib
   mpremote cp Arducam.py :lib/Arducam.py
   mpremote cp OV5642_reg.py :lib/OV5642_reg.py
   ```

4. Upload your main script:
   ```bash
   mpremote cp main_example.py :main.py
   ```

## Quick Start

```python
from machine import Pin, SPI, I2C
import time
from Arducam import Arducam, JPEG, OV5642

# Configure SPI
spi = SPI(2, baudrate=2_000_000, polarity=0, phase=0,
          sck=Pin(12), mosi=Pin(10), miso=Pin(11))

# Configure I2C
i2c = I2C(0, scl=Pin(14), sda=Pin(13), freq=400_000)

# Initialize camera
cam = Arducam(spi=spi, cs_pin=9, i2c=i2c)
cam.CameraType = OV5642
cam.Set_Camera_mode(JPEG)

cam.Camera_Detection()
cam.Spi_Test(retries=5)
cam.init()
time.sleep(0.2)

# Capture image
cam.capture()
jpeg_data = cam.read_jpeg()

# Save to file
with open("photo.jpg", "wb") as f:
    f.write(jpeg_data)
```

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

## Troubleshooting

- **SPI interface Error**: Check wiring and ensure correct GPIO pins are used.
- **Can't find OV5642 module**: Verify I2C connections (SDA/SCL) and power supply.
- **Empty JPEG data**: Allow warm-up time after `init()` before capturing.

## License

MIT
