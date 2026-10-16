import os
import sys

dwsim_path = r"C:\Users\morit\AppData\Local\DWSIM7"

os.add_dll_directory(dwsim_path)
sys.path.append(dwsim_path)