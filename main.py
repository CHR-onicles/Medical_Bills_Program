from PyQt5.QtCore import (QSize, Qt, pyqtSignal, pyqtSlot, QTimer)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QWidget, QSizePolicy, QCompleter,
                             QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox, QStatusBar, QListView,
                             QStyledItemDelegate)
import sys


# Local imports
import resources_rc, styles
from UI_main_window import UIMainWindow
from med_bills_functions import MBillsFunctions




class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.UI = UIMainWindow()
        self.setCentralWidget(self.UI)
        self.setStyleSheet(styles.main_window_style())
        self.resize(1300, 800)
        # self.resize(1000, 800)  # for testing purposes
        self.setMinimumSize(QSize(1000, 720))


        med_bills_wkbk, staff_list_wkbk = MBillsFunctions.initializeFiles('test_med_bills_20.xlsx', 'test_staff_list.xlsx')
        self.all_names = MBillsFunctions.getAllMedBillsNames(med_bills_wkbk)
        self.all_names.extend(MBillsFunctions.getAllDependantNames(staff_list_wkbk))

        # Completer configs -----------------------------------------------------------------------------
        self.completer = QCompleter(self.all_names)
        self.com_delegate = QStyledItemDelegate(self)  # have to do this to set style cuz of some bs thingy...
        self.completer.popup().setItemDelegate(self.com_delegate)  # Source: (https://www.qtcentre.org/threads/39268-Styling-a-QAbstractItemView-item)
        self.completer.popup().setStyleSheet("""
        QListView {
            font: 10pt century gothic;
            background-color: silver;
            border: 1px solid #444;
            border-radius: 3px;
            margin-left: 3px;
            color: black;
        }

        QListView::item:hover {
            background: #3d8ec9;
            color: #FFFFFF;
        }
        
        QListView::item:selected {
            background: #78879b;
            outline: 0;
            color: #FFFFFF;
        }
        """)


        self.UIComp()

    def UIComp(self):
        self.widgets()

    def widgets(self):
        self.UI.entry_staff_or_dependant.setCompleter(self.completer)


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
