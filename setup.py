import sys

from cx_Freeze import setup, Executable




__version__ = '1.0.0'
# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'zip_include_packages': ['PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore', 'openpyxl'],
                 'excludes': ['PySide2', 'tkinter', 'multiprocessing', 'email', 'numpy', 'scipy', 'setuptools',
                              'distutils', 'unittest', 'packaging', 'cffi', 'html', 'http', 'pycparser'
                              ]
                 }

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, icon='rc/cat.ico', target_name='Med Bills App')
]

setup(
    name="Medical Bills Entry App",
    version=__version__,
    license='MIT',
    author='Divine Anum',
    author_email='tpandivine48@gmail.com',
    url='https://github.com/CHR-onicles/Medical_Bills_Program',
    description='App to speed up the process of entering medical bills claims/receipts into a preformatted excel database.',
    options={'build_exe': build_options},
    executables=executables)
