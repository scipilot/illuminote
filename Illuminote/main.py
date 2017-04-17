#
from os import path
import sys

# Test: just show a fretboard from the Fretboard sources - which aren't really an API...
#sys.path.append(path.abspath('../Modules'))

# TODO: the git-backed requirements: how do you import them after pip install? can't seem to find this online
#sys.path.append(path.abspath('../src'))

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
Fretboard.show_fretboard(Tunings.tuning_dict, Notes.notes_sharp, Notes.notes_flat, valid_notes, bool_flat=True, bool_scale=True, bool_interval=False)
