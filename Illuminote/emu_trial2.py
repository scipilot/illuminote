# Trial: inject the IC2 Emu into the Adafruit RGB Driver.
# Draw a big X from 1,1 - 6,6

import time
import logging
from i2c_emu  import i2c_emu
from Adafruit_LED_Backpack import BicolorMatrix8x8
from PIL import Image
from PIL import ImageDraw

# simple logging setup
logging.basicConfig(filename='debug.log',level=logging.DEBUG,filemode='w')

# Inject our ic2 emulation in
# Create display instance on default I2C address (0x70) and bus number.
display = BicolorMatrix8x8.BicolorMatrix8x8(address=0x70, busnum=0, i2c=i2c_emu)

# Initialize the display. Must be called once before using the display.
display.begin()

# First create an 8x8 RGB image.
image = Image.new('RGB', (8, 8))

# Then create a draw instance.
draw = ImageDraw.Draw(image)

# Draw a filled yellow rectangle with red outline.
draw.rectangle((0, 0, 7, 7), outline=(255, 0, 0), fill=(255, 255, 0))

# Draw an X with two green lines.
draw.line((1, 1, 6, 6), fill=(0, 255, 0))
draw.line((1, 6, 6, 1), fill=(0, 255, 0))

# Draw the image on the display buffer.
display.set_image(image)

# Draw the buffer to the display hardware.
display.write_display()