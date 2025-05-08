import os
import platform

OBSIDIAN_APPDATA = os.path.join(os.getenv("APPDATA"), "obsidian")

if platform.system() == "Linux":
    OBSIDIAN_APPDATA = os.path.join(os.getenv("HOME"), ".config/obsidian")

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

KILL_HOLD_INTERVAL = 0.6