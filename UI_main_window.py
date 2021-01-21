from PyQt5.QtCore import (QSize, Qt, QTimer, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QFont, QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTabWidget, QComboBox, QCompleter,
                             QLineEdit, QStyle, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox, QWidget,
                             QStatusBar)
import sys

# Local imports
import resources_rc, styles
from custom_widgets import QHSeparationLine, QVSeparationLine




class UIMainWindow(QMainWindow):

    def __init__(self):
        super(UIMainWindow, self).__init__()
        self.setWindowTitle('Med Bills App')
        self.setWindowIcon(QIcon(':/icon/cat'))
        self.resize(1200, 800)


        self.UIComponents()

    def UIComponents(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        self.central_widget = QWidget()

        # BIG TITLE ----------------------------------------------------------------------------------------
        self.lbl_title = QLabel('MEDICAL BILLS 2021')
        self.lbl_title.setAlignment(Qt.AlignHCenter)

        # STATUS BAR ---------------------------------------------------------------------------------------
        self.statusBar().showMessage('Welcome, this is the status bar...')

        # TABS ---------------------------------------------------------------------------------------------
        self.tabs = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()
        self.tabs.addTab(self.tab_1, 'RECEIPT ENTRY')  # may change later
        self.tabs.addTab(self.tab_2, 'Tab 2')
        self.tabs.addTab(self.tab_3, 'Tab 3')

        # TAB 1 WIDGETS ------------------------------------------------------------------------------------
        self.lbl_month = QLabel('Month')
        self.combo_months = QComboBox()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                  'October', 'November', 'December']



    def layouts(self):
        # MAIN WINDOW LAYOUT (CENTRAL WIDGET) --------------------------------------------------------------
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        self.central_layout.setContentsMargins(0, 10, 0, 0)
        self.central_layout.addWidget(self.lbl_title)
        self.central_layout.addWidget(self.tabs)

        # TAB 1 LAYOUTS ------------------------------------------------------------------------------------
        self.tab1_main_layout = QVBoxLayout()
        self.tab1_quick_search_layout = QHBoxLayout()
        self.tab1_month_layout = QHBoxLayout()
        self.tab1_entry_and_details_layout = QHBoxLayout()


        # Adding Widgets to TAB 1 Layout -------------------------------------------------------------------
        self.tab1_main_layout.addLayout(self.tab1_quick_search_layout)
        self.tab1_main_layout.addLayout(self.tab1_month_layout)














if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UIMainWindow()
    window.show()
    sys.exit(app.exec_())
