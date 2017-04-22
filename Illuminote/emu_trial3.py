# Trial3: Try to render a scale on the Fret Emu
# injects the I2C Emu into the Adafruit RGB Driver.

import logging
from i2c_emu  import i2c_emu
from Adafruit_LED_Backpack import BicolorMatrix8x8
from i2c_emu.i2c_emu import consoleFretboardOutputDriver


# simple logging setup
logging.basicConfig(filename='debug.log',level=logging.DEBUG,filemode='w')

# Inject our ic2 emulation in
# Create display instance on default I2C address (0x70) and bus number.
# note: you could pass in an i2c_interface() which returns a Device?
display = BicolorMatrix8x8.BicolorMatrix8x8(address=0x70, busnum=0, i2c=i2c_emu)

# Initialize the display. Must be called once before using the display.
display.begin()


from fretboard import Fretboard
from fretboard import Tunings
from fretboard import Notes
from fretboard import Scales
from fretboard import Settings

scale_interval = ""
scale_steps = ""

for Scale in Scales.ListScales:
    # Find the Index of the chosen scale
    if Scale["Scale"] == Settings.string_scale:  # if the scale matches a scale in ListScales
        scale_steps = Scale["H_Steps"]
        scale_interval = Scale["L_Steps"]
        break

valid_notes = Fretboard.return_scale_notes(Settings.root_note, scale_interval)
notes = Fretboard.show_fretboard(Tunings.tuning_dict, Notes.notes_sharp, Notes.notes_flat, valid_notes, bool_flat=True, bool_scale=True, bool_interval=False)
# Note: Fretboard (my mod!) returns an 2D array of strings, then frets.

# some test sets
# notes = [[0 for i in range(12)] for j in range(6)]
# just the first F on E string 1. This is note #0. LED Matrix position [0][0]
# notes[0][0] = 'F'
# just the first F on E string 6. This is note #5. LED Matrix position [0][5]. Register x01, Value b00010000 (d16)
#notes[5][0] = 'F'
# just the first F# on E string 6. This is note #11. LED Matrix position [1][5]. Register x03, Value b00010000 (d16)
# notes[5][1] = 'F#'
# notes[4][0] = 'C'
# notes[1][2] = 'C'
# notes[2][1] = 'C'

# The notes returned are in a 6-string-array, of 13-fret arrays (configurable)
# So we need to transform that into the 8x8 pixel array

# needed for matrix mapping functions
driver = consoleFretboardOutputDriver
data = [[0 for i in range(8)] for j in range(8)]

# Build the 64 note representation.
# todo: move this into a "Fretboard to BicolorMatrix8x8 mapper"? if we keep "Fretboard" that is...
string_no = 1
for string in notes:
    fret_no = 1
    for fret in string:
        # we're limited to what we can display: only 4 notes on the 11th fret (64 notes)
        if fret_no < 11:     # doesn't work unless we went backwards! or (string_no < 5 and fret_no == 11):
            # just show red for "fret here" for the moment. Could use RGY for e.g. R=root, G=3,5,7, Y=others?
            data = driver.putFretxel(data, string_no, fret_no, BicolorMatrix8x8.OFF if fret == 0 else BicolorMatrix8x8.RED)
        fret_no += 1
    string_no += 1

# Iterate through all positions x and y.
for x in range(8):
    for y in range(8):
        display.set_pixel(x, y, data[y][x])
display.write_display()


