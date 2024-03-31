import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Running as a bundled application (packaged by PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # Running as a normal Python script
        return os.path.abspath(os.path.dirname(__file__))