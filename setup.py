import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["tkinter"], "include_files": 
                     [
    "cores.py","criarbd.py","dados.db","view.py","logo.png","images.png", "delete.png", "teste.ico"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Controle Financeiro",
    version="1.0",
    description="Controle de finanças",
    options={"build_exe": build_exe_options},
    executables=[Executable(script="main.py", base=base, icon="teste.ico")]
)