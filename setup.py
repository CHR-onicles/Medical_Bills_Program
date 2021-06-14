import os
import sys

from cx_Freeze import setup, Executable
from _version import __version__




# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'zip_include_packages': ['PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore', 'openpyxl'],
                 'excludes': ['PySide2', 'tkinter', 'PIL', 'multiprocessing', 'email', 'numpy', 'scipy', 'setuptools',
                              'distutils', 'unittest', 'packaging', 'cffi', 'html', 'http', 'pycparser', 'icecream',
                              'lxml'
                              ],  # had to yeet all these out as it made the executable folder huge af...
                 'include_files': ['test med bills 2021.xlsx', 'STAFF DEPENDANT LIST 2020.xlsx']
                 # todo: change these files to work with different databases
                 }

base = 'Win32GUI' if sys.platform == 'win32' else None
# base = None  # for debugging (it displays console)

executables = [
    Executable('src/main.py', base=base, icon='rc/cat.ico', target_name='Med Bills')
]

setup(
    name="Medical Bills Entry App",
    version=__version__,
    license='MIT',
    author='Divine Anum',
    author_email='tpandivine48@gmail.com',
    url='https://github.com/CHR-onicles/Medical_Bills_Program',
    description='App to speed up entry of medical bills claims/receipts into a preformatted excel database.',
    options={'build_exe': build_options},
    executables=executables)

def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)
