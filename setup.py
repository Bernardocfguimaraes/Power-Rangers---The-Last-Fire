import cx_Freeze
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="recursos/icon.png") ]
cx_Freeze.setup(
    name = "Power Rangers The Last Fire",
    options={
        "build_exe":{
            "packages":["pygame", "random", "os", "tkinter", "json", "math", "datetime",
        "speech_recognition", "pyttsx3", "sys", "pyaudio", "aifc"],
            "include_files": ["recursos", "log.dat"],
            "includes": ["aifc", "json"]
        }
    }, executables = executaveis
)