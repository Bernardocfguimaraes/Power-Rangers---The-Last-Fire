import cx_Freeze
from cx_Freeze import setup, Executable

executaveis = [Executable(script="main.py", icon="recursos/icon.png")]

build_exe_options = {
    "packages": [
        "pygame", "random", "os", "tkinter", "json", "math", "datetime",
        "speech_recognition", "pyttsx3", "sys", "pyaudio", "aifc", "chunk"
    ],
    "includes": ["aifc", "chunk"],
    "include_files": ["recursos", "log.dat"]
}

setup(
    name="Power Rangers The Last Fire",
    version="1.0",
    description="Jogo desenvolvido com Pygame",
    options={"build_exe": build_exe_options},
    executables=executaveis
)