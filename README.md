# Illuminote Guitar Tutor App.

Authors: Pip Jones, Dylan Hoelzel

Status: Early prototype / POC

## Requirements (PoC)

* Currently intended to run on a Raspberry Pi, with the necessary hardware attached via I2C.
* Currently that hardware is a "Adafruit Bicolor LED Square Pixel 8x8 Matrix with I2C Backpack"
* Python3
* Pip3

## Installation

    git clone https://github.com/scipilot/illuminote.git
    cd illuminote
    pip3 install -r Illuminote/requirements.txt

To test it in the console LED emulator:

    python3 Illuminote/trial.py
    python3 Illuminote/trial2.py
    python3 Illuminote/trial3.py

To test the hardware LED:

    TBC - coming soon
