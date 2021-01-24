from PyQt5.QtCore import (QSize, Qt, pyqtSignal, pyqtSlot, QThread, QThreadPool, QRunnable, QObject)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QWidget, QSizePolicy,
                             QCompleter,
                             QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox, QStatusBar, QListView,
                             QStyledItemDelegate)
import sys
from icecream import ic
import openpyxl
from datetime import datetime

# Local imports
import resources_rc, styles
from UI_main_window import UIMainWindow
from med_bills_functions import MBillsFunctions





# icecream debugging configs
ic.configureOutput(includeContext=True)


class ExtractionRunner(QRunnable):

    def __init__(self, workbook):
        super(ExtractionRunner, self).__init__()
        ic('In runner')
        self.workbook = workbook
        self.signals = RunnerSignals()

    @pyqtSlot()
    def run(self):
        staff_details = MBillsFunctions.getDetailsOfPermanentStaff(self.workbook)
        self.signals.signal_staff_details.emit(staff_details)
        ic('run in Runner')
        # ic('Size of Staff details:', len(staff_details))


class RunnerSignals(QObject):
    """
    Class inheriting from QObject to create signals because QRunnables cannot create signals.
    """
    signal_staff_details = pyqtSignal(dict)




class MainApp(QMainWindow):
    """
    Main Controls of App
    """
    # signal_wkbk_staff_list = pyqtSignal(openpyxl.workbook.workbook.Workbook)
    signal_wkbk_staff_list = pyqtSignal(object)

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
        self.wkbk_med_bills, self.wkbk_staff_list = MBillsFunctions.initializeFiles('test_med_bills_20.xlsx',
                                                                                    'test_staff_list.xlsx')
        self.signal_wkbk_staff_list.emit(self.wkbk_staff_list)
        self.all_names = MBillsFunctions.getAllMedBillsNames(self.wkbk_med_bills)
        self.all_names.extend(MBillsFunctions.getAllDependantNames(self.wkbk_staff_list))

        # Completer configs -----------------------------------------------------------------------------
        self.completer = QCompleter(self.all_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.com_delegate = QStyledItemDelegate(self)  # have to do this to set style cuz of some bs thingy...
        self.completer.popup().setItemDelegate(
            self.com_delegate)  # Source: (https://www.qtcentre.org/threads/39268-Styling-a-QAbstractItemView-item)
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

        # Threading here -----------------------------------
        s1 = datetime.now()
        ic('Starting thread')
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(5)
        self.worker = ExtractionRunner(self.wkbk_staff_list)
        self.worker.signals.signal_staff_details.connect(self.on_signal_details)
        self.threadpool.start(self.worker)

        s2 = datetime.now()
        ic('Finished thread:', s2 - s1)

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


    @pyqtSlot(dict)
    def on_signal_details(self, det):
        self.staff_details = det
        ic('grab details called')
        ic('Length of staff details:', len(self.staff_details))

    def populateStaffDetails(self, person):
        ic.enable()
        # self.clearStaffDetails()

        # ic('Finished staff Details')
        details = MBillsFunctions.searchForPerson(person.upper(),
                                                  self.staff_details)  # all names in staff list are uppercase
        # print('Extracted searched person\'s details')

        if details is not None:
            self.UI.entry_staff_name.setText(details[0].title())
            self.UI.entry_department.setText(details[1][0])

        else:
            pass
            # todo: show message box here


        # ic.disable()




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
    #   2. Let status bar show status of long processes
