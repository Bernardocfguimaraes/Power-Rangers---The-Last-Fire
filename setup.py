from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base, icon="recursos/icon.png")]
build_exe_options = {
    "packages": ["pygame", "random", "math", "datetime", "tkinter", "json", "speech_recognition", "pyttsx3", "pyaudio"],  
    "include_files": ["log.dat", "recursos/"]}

setup(
    name="Power Rangers - The Last Fire",
    version="1.0",
    description="Jogo criado em Pygame",
    options={"build_exe": build_exe_options},
    executables=executables
)