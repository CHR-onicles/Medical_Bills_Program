from PyQt5.QtCore import (QSize, Qt, pyqtSignal, pyqtSlot, QTimer)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QWidget, QSizePolicy,
                             QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox, QStatusBar)
import sys


# Local imports
import resources_rc, styles
from UI_main_window import UIMainWindow




class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.UI = UIMainWindow()
        self.setCentralWidget(self.UI)
        self.setStyleSheet(styles.main_window_style())
        self.resize(1300, 800)
        # self.resize(1000, 800)  # for testing purposes
        self.setMinimumSize(QSize(1000, 720))



        self.UIComp()

    def UIComp(self):
        self.widgets()

    def widgets(self):


        # STATUS BAR ---------------------------------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Welcome, this is the status bar...')
        self.btn_refresh = QPushButton('Refresh')
        self.btn_refresh.setObjectName('btn_quick_search_and_refresh')
        self.status_bar.addPermanentWidget(self.btn_refresh)
        self.status_bar.setFixedHeight(60)
        self.setContentsMargins(0, 0, 20, 0)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
