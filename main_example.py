from machine import Pin, SPI, I2C
import time
from Arducam import Arducam, JPEG, OV5642, ARDUCHIP_TRIG, CAP_DONE_MASK, ARDUCHIP_TIM

SPI_ID   = 2
SPI_SCK  = 12
SPI_MOSI = 10
SPI_MISO = 11
CS_PIN   = 9

I2C_ID   = 0
I2C_SCL  = 14
I2C_SDA  = 13

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

def try_capture(tag):
    cam.flush_fifo()
    cam.clear_fifo_flag()
    cam.start_capture()

    t0 = time.ticks_ms()
    while not cam.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK):
        if time.ticks_diff(time.ticks_ms(), t0) > 3000:
            print(tag, "timeout")
            return 0, b""
        time.sleep(0.01)

    length = cam.read_fifo_length()
    jpeg = cam.read_jpeg(max_size=None)
    print(tag, "TRIG:", hex(cam.Spi_read(ARDUCHIP_TRIG)[0]), "LEN:", length, "JPEG:", len(jpeg))
    return length, jpeg

for tim in (0x00, 0x02):
    cam.Spi_write(ARDUCHIP_TIM, tim)
    time.sleep(0.05)
    length, jpeg = try_capture("TIM=%s" % hex(tim))
    if len(jpeg) > 1000:
        with open("test.jpg", "wb") as f:
            f.write(jpeg)
        print("Saved test.jpg using", hex(tim))
        break

