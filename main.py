from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTabWidget, QComboBox, QWidget, QSizePolicy,
                             QLineEdit, QGridLayout, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox)
import sys


# Local imports
from UI_main_window import UIMainWindow




class MainApp(UIMainWindow, QWidget):

    def __init__(self):
        super().__init__()


        self.UI()

    def UI(self):
        self.widgets()

    def widgets(self):
        pass







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    sys.exit(app.exec_())
