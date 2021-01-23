from PyQt5.QtCore import (QSize, Qt, pyqtSignal, pyqtSlot, QThread, QThreadPool, QRunnable)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QWidget, QSizePolicy, QCompleter,
                             QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox, QStatusBar, QListView,
                             QStyledItemDelegate)
import sys
from icecream import ic

# Local imports
import resources_rc, styles
from UI_main_window import UIMainWindow
from med_bills_functions import MBillsFunctions




class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Med Bills App')
        self.setWindowIcon(QIcon(':/icon/cat'))
        self.UI = UIMainWindow()
        self.setCentralWidget(self.UI)
        self.setStyleSheet(styles.main_window_style())
        self.resize(1300, 800)
        # self.resize(1000, 800)  # for testing purposes
        self.setMinimumSize(QSize(1000, 720))

        # Medical Bills Files configs -------------------------------------------------------------------
        self.wkbk_med_bills, self.wkbk_staff_list = MBillsFunctions.initializeFiles('test_med_bills_20.xlsx', 'test_staff_list.xlsx')
        self.all_names = MBillsFunctions.getAllMedBillsNames(self.wkbk_med_bills)
        self.all_names.extend(MBillsFunctions.getAllDependantNames(self.wkbk_staff_list))

        # Completer configs -----------------------------------------------------------------------------
        self.completer = QCompleter(self.all_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
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

        self.UI.entry_quick_search.setCompleter(self.completer)
        # self.UI.entry_quick_search.returnPressed.connect(lambda: self.populateStaffDetails(self.UI.entry_quick_search.text().strip()))
        self.UI.btn_quick_search.clicked.connect(lambda: self.populateStaffDetails(self.UI.entry_quick_search.text()))



        # STATUS BAR ---------------------------------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Welcome, this is the status bar...')
        self.btn_refresh = QPushButton('Refresh')
        self.btn_refresh.setObjectName('btn_quick_search_and_refresh')
        self.btn_refresh.clicked.connect(self.clearStaffDetails)
        self.status_bar.addPermanentWidget(self.btn_refresh)
        self.status_bar.setFixedHeight(60)
        self.setContentsMargins(0, 0, 20, 0)


    def populateStaffDetails(self, person):
        ic.enable()
        ic('Entered populate function')

        # self.clearStaffDetails()
        self.staff_details = MBillsFunctions.getDetailsOfPermanentStaff(self.wkbk_staff_list)
        ic('Finished staff Details')
        details = MBillsFunctions.searchForPerson(person.upper(), self.staff_details)  # all names in staff list are uppercase
        print('Extracted searched person\'s details')

        if details is not None:
            self.UI.entry_staff_name.setText(details[0].title())

        else:
            pass
            # todo: show message box here


        ic.disable()




    def clearStaffDetails(self):
        self.UI.entry_staff_name.clear()
        self.UI.entry_department.clear()
        self.UI.entry_spouse.clear()
        self.UI.combo_children.clear()
        self.UI.entry_cur_amount.setText('GH₵ ')





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


    # ---------------------------------------- TODO --------------------------------------------------------
    # TODO:
    #   1. Difference between quick search and typing staff/dependant name directly???
    #   2.
