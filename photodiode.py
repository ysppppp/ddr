import spidev
import time

spi = spidev.SpiDev()
spi.open(0,0)    # SPI Port 0, Chip Select 0
# Run SPI bus at low speed so we can capture everything in piscope
spi.max_speed_hz = 7629 
# Send these bytes on the MOSI line and read the MISO line
#resp = spi.xfer2([0b00000001, 0b10000000, 0b00000000])

#for b in resp:
while 1:
    resp = spi.xfer2([0b00000001, 0b10000000, 0b00000000])
    print(format(resp[2], '#010b'))
    time.sleep(1)