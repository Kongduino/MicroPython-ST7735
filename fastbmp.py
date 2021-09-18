from ST7735 import TFT,TFTColor
from machine import SPI,Pin
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
#  def __init__( self, spi, aDC, aReset, aCS) :
tft=TFT(spi, 27, 33, 14)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

f=open('KduinoLogo.b16', 'rb')
w = int.from_bytes(f.read(2), 'little')
h = int.from_bytes(f.read(2), 'little')
tft._setwindowloc((0,0),(w - 1,h - 1))
tft.dc(1)
tft.cs(0)
for row in range(h):
  row = f.read(2 * w)
  tft.spi.write(row) # send one row
tft.cs(1) # display
spi.deinit()
