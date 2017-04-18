# Trial: inject the IC2 Emu into the Adafruit RGB Driver.

import time
import logging
from ic2_emu  import ic2_emu
from Adafruit_LED_Backpack import BicolorMatrix8x8

# simple logging setup
logging.basicConfig(filename='debug.log',level=logging.DEBUG,filemode='w')

# Inject our ic2 emulation in
# Create display instance on default I2C address (0x70) and bus number.
display = BicolorMatrix8x8.BicolorMatrix8x8(address=0x70, busnum=0, i2c=ic2_emu)

# Initialize the display. Must be called once before using the display.
display.begin()

# Run through each color and pixel.
# Iterate through all colors.
for c in [BicolorMatrix8x8.RED, BicolorMatrix8x8.GREEN, BicolorMatrix8x8.YELLOW]:
    logging.debug("Setting colour {0}".format(c))
    # Iterate through all positions x and y.
    for x in range(8):
        for y in range(8):
            logging.debug("Setting X,Y={0},{1}".format(x,y))
            # Clear the display buffer.
            logging.debug("Clearing display...")
            display.clear()
            # Set pixel at position i, j to appropriate color.
            logging.debug("Setting pixel...")
            display.set_pixel(x, y, c)
            # Write the display buffer to the hardware.  This must be called to
            # update the actual display LEDs.
            logging.debug("Writing display...")
            display.write_display()
            # Delay for a quarter second.
            # time.sleep(0.025)



"""
From looking at the output:
- First there are three setup calls to: write_i2c_block_data to register 0x21, register 0x81, register 0xEF
- During the loop above, nothing happens in the bus until write_display is called. 
- This triggers 16 calls to Device.write8 / AsciiBus:write_byte_data
- This means the emulator would have to update the output display per-pixel change (there is no "frame")
- Also means I'm not capturing the "clear" signal, so we have to process R=R, then 0+G = G, R+G=Y (i.e. don't "remember" G)  
- all are 0's except:
DEBUG:root:Setting colour 2 (RED?)
DEBUG:root:Setting X,Y=0,0
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x01
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,1,1)
DEBUG:root:Setting X,Y=0,1
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x03
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,3,1)
DEBUG:root:Setting X,Y=0,2
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x05
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,5,1)
...
DEBUG:root:Setting X,Y=0,7
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x0F
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,15,1)

DEBUG:root:Setting X,Y=1,0
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x02 to register 0x01
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,1,2)
...
DEBUG:root:Setting X,Y=1,7
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x02 to register 0x0F
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,15,2)
...
DEBUG:root:Setting X,Y=2,0
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x04 to register 0x01
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,1,4)
DEBUG:root:Setting X,Y=2,1
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x04 to register 0x03
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,3,4)
...
DEBUG:root:Setting X,Y=7,7
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x80 to register 0x0F
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,15,128)

DEBUG:root:Setting colour 1 (GREEN)
DEBUG:root:Setting X,Y=0,0
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x00
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,0,1)
...
DEBUG:root:Setting X,Y=0,1
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x02
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,2,1)
...
DEBUG:root:Setting X,Y=7,7
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x80 to register 0x0E
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,14,128)

DEBUG:root:Setting colour 3
DEBUG:root:Setting X,Y=0,0
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x00
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,0,1)
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x01 to register 0x01
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,1,1)
...
DEBUG:root:Setting X,Y=7,7
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x80 to register 0x0E
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,14,128)
DEBUG:I2C_Emu.Device.Bus.0.Address.0X70:.write8:Writing value:0x80 to register 0x0F
DEBUG:I2C_Emu.AsciiBus:write_byte_data(112,15,128)

So the rows/columns are represented by register/value combinations.
- R00 = Green pixels in row 1
- R01 = Red pixels in row 1
- R0E = Green pixels in row 8
- R0F = Red pixels in row 8

The columns are set/cleared by bits in the data: 
- 00 = all off, 
- 01, 02, 04 ... 80 = individual pixels
- FF = all on

Address = 112

"""