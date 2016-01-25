import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "sys", "pygame"], "excludes": ["tkinter"],
                     "include_files": ["data/", "images/", "sounds/"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Zombi game",
      version="1.0",
      description="A cool survival game!",
      options={"build_exe": build_exe_options},
      executables=[Executable("Zombi mäng.py", base=base)])
