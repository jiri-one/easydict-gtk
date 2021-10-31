#!/bin/python

from os import system
from pathlib import Path

easydict_main_file = str(Path(__file__).parent / "easydict.py")

system(f"python {easydict_main_file}")
