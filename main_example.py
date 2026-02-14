from machine import Pin, SPI, I2C
import time
from Arducam import Arducam, JPEG, OV5642, ARDUCHIP_TRIG, CAP_DONE_MASK, ARDUCHIP_TIM
import neopixel


# Config the Pins and IDs
SPI_ID   = 2

SPI_SCK  = 12
SPI_MOSI = 10
SPI_MISO = 11
CS_PIN   = 9

I2C_ID   = 0

I2C_SCL  = 14
I2C_SDA  = 13

led = neopixel.NeoPixel(Pin(38), 1)

# Config the camera
spi = SPI(SPI_ID, baudrate=2_000_000, polarity=0, phase=0,
          sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
i2c = I2C(I2C_ID, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400_000)

print("I2C scan:", [hex(x) for x in i2c.scan()])

cam = Arducam(spi=spi, cs_pin=CS_PIN, i2c=i2c)
cam.CameraType = OV5642
cam.Set_Camera_mode(JPEG)

cam.Camera_Detection()
cam.Spi_Test(retries=5)
cam.init()
time.sleep(0.2)

def capture_with_blinking(tag):
    # Flush the cam FIFO buffer
    cam.flush_fifo()
    cam.clear_fifo_flag()
    
    # blinking for 1 sec before start capturing
    for _ in range(5):
        led[0] = (255, 0, 0)  # Red
        led.write()
        time.sleep(0.1)

        led[0] = (0, 0, 0)    # Off
        led.write()
        time.sleep(0.1)
    
    # Start Capturing
    led[0] = (0, 255, 0)  # Green
    led.write()
    time.sleep(0.1)
    
    cam.start_capture()
    
    # Wait for 3s since the cam is asynchronized
    t0 = time.ticks_ms()
    while not cam.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK):
        if time.ticks_diff(time.ticks_ms(), t0) > 3000:
            print(tag, "timeout")
            return 0, b""
        time.sleep(0.01)

    length = cam.read_fifo_length()
    jpeg = cam.read_jpeg(max_size=None)
    
    # Print image detials
    print(tag, "TRIG:", hex(cam.Spi_read(ARDUCHIP_TRIG)[0]), "LEN:", length, "JPEG:", len(jpeg))
    
    # Finish Capturing
    led[0] = (0, 0, 0)    # Off
    led.write()
    time.sleep(0.1)
    
    return length, jpeg


# Setting timing bit for the cam vsync as active-low (since active-high (0) didn't work)
tim = 0x02 # 00000010
cam.Spi_write(ARDUCHIP_TIM, tim)
time.sleep(0.05)

# Capture the image
length, jpeg = capture_with_blinking("TIM=%s" % hex(tim))

# Save image
with open("test.jpg", "wb") as f:
    f.write(jpeg)
print("Saved test.jpg using", hex(tim))

