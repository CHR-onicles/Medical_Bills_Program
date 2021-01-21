from PyQt5.QtCore import (QSize, Qt, QTimer, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QFont, QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTabWidget, QComboBox, QCompleter, QLineEdit, QStyle)
import sys

import resources_rc




class UIMainWindow(QMainWindow):

    def __init__(self):
        super(UIMainWindow, self).__init__()
        self.setWindowTitle('Med Bills App')
        self.setWindowIcon(QIcon(':/icon/cat'))
        self.resize(1200, 800)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UIMainWindow()
    window.show()
    sys.exit(app.exec_())