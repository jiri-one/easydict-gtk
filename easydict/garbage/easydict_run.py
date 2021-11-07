#!/bin/python

from os import system
from pathlib import Path
from time import sleep

easydict_main_file = str(Path(__file__).parent / "src" / "easydict.py")

#sleep(2) # on some DE is not needed (for on Plasma it works without it), but on Cinnamon i needed this delay to autostart EasyDict after PC started
system(f"python {easydict_main_file}")
