from ST7735 import TFT,TFTColor
from machine import SPI,Pin
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
#  def __init__( self, spi, aDC, aReset, aCS) :
tft=TFT(spi, 27, 33, 14)
tft.initr()
tft.rgb(True)
tft.fill(TFT.BLACK)

fn='KduinoLogo'
f=open(fn+'.bmp', 'rb')
g=open(fn+'.b16', 'wb')
if f.read(2) == b'BM':  #header
  dummy = f.read(8) #file size(4), creator bytes(4)
  offset = int.from_bytes(f.read(4), 'little')
  hdrsize = int.from_bytes(f.read(4), 'little')
  width = int.from_bytes(f.read(4), 'little')
  height = int.from_bytes(f.read(4), 'little')
  if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
    depth = int.from_bytes(f.read(2), 'little')
    if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
      print("Image size:", width, "x", height)
      rowsize = (width * 3 + 3) & ~3
      if height < 0:
        height = -height
        flip = False
      else:
        flip = True
      w, h = width, height
      if w > 128: w = 128
      if h > 128: h = 128
      tft._setwindowloc((0,0),(w - 1,h - 1))
      header = bytearray([w,0,h,0])
      g.write(header)
      for row in range(h):
        if flip:
          pos = offset + (height - 1 - row) * rowsize
        else:
          pos = offset + row * rowsize
        if f.tell() != pos:
          dummy = f.seek(pos)
        data = list(bytearray(2*w))
        frow = list(f.read(3*w))
        ix = 0
        iy = 0
        for col in range(w):
          aColor=TFTColor(frow[ix], frow[ix+1], frow[ix+2])
          ix = ix + 3
          data[iy] = aColor >> 8
          data[iy+1] = aColor and 8
          iy = iy +2
        tft.dc(1)
        tft.cs(0)
        data=bytearray(data)
        tft.spi.write(data) # display one row
        tft.cs(1)
        g.write(data) # add row data to the .b16 file

spi.deinit()
