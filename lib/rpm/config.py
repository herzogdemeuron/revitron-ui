import pyrevit
import os

RPM_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RPM_PYREVIT_DIR = pyrevit.HOME_DIR
RPM_PYREVIT_BIN = pyrevit.ROOT_BIN_DIR + '\\pyrevit.exe'
RPM_EXTENSIONS_DIR = RPM_PYREVIT_DIR + '\\extensions'