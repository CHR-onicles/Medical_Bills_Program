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




class MainApp(QMainWindow):
    """
    Main App
    """

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
        self.all_names_and_dept = MBillsFunctions.getAllMedBillsNamesAndDept(self.wkbk_med_bills)
        self.all_names_and_dept.extend(MBillsFunctions.getAllDependantNames(self.wkbk_staff_list))
        self.staff_details = MBillsFunctions.getDetailsOfPermanentStaff(self.wkbk_staff_list)

        # Completer configs -----------------------------------------------------------------------------
        self.completer = QCompleter([name.split('|')[0] for name in self.all_names_and_dept])
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
        
        QScrollBar:vertical
        {
            background-color: #605F5F;
            width: 15px;
            margin: 15px 3px 15px 3px;
            border: 1px transparent #2A2929;
            border-radius: 4px;
        }

        QScrollBar::handle:vertical
        {
            background-color: #2A2929;
            min-height: 5px;
            border-radius: 4px;
        }
        
        QScrollBar::sub-line:vertical
        {
            margin: 3px 0px 3px 0px;
            border-image: url(:/qss_icons/up_arrow_disabled.png);
            height: 10px;
            width: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        
        QScrollBar::add-line:vertical
        {
            margin: 3px 0px 3px 0px;
            border-image: url(:/qss_icons/down_arrow_disabled);
            height: 10px;
            width: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        
        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on
        {
            border-image: url(:/qss_icons/up_arrow.png);
            height: 10px;
            width: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        
        
        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on
        {
            border-image: url(:/qss_icons/down_arrow);
            height: 10px;
            width: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        
        QScrollBar::down-arrow:vertical
        {
            background: none;
        }
        
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
        {
            background: none;
        }
        
        """)

        self.UIComp()


    def UIComp(self):
        self.widgets()

    def widgets(self):
        self.months = {'January': 2, 'February': 3, 'March': 4, 'April': 5, 'May': 6, 'June': 7, 'July': 8,
                       'August': 9, 'September': 10, 'October': 11, 'November': 12, 'December': 13}
        self.UI.combo_months.addItems(list(self.months.keys()))

        self.UI.entry_staff_or_dependant.setCompleter(self.completer)

        self.UI.entry_quick_search.setCompleter(self.completer)
        self.UI.entry_quick_search.returnPressed.connect(
            lambda: self.populateStaffDetails(self.UI.entry_quick_search.text().strip()))
        self.UI.btn_quick_search.clicked.connect(
            lambda: self.populateStaffDetails(self.UI.entry_quick_search.text().strip()))

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

        person_status = ['Staff Name:', 'Guest Name:', 'Casual Name:']
        self.clearStaffDetails()

        s_name, d_name = MBillsFunctions.searchForStaffFromStaffList(person.upper(),  # all names in staff list are uppercase
                                                                     self.staff_details)
        ic.enable()
        ic(s_name, d_name)

        if s_name and d_name is not None:
            self.UI.lbl_staff_name.setText(person_status[0])
            self.UI.entry_staff_name.setText(s_name.title())
            self.UI.entry_department.setText(d_name[0])
            if d_name[1] is not None:  # Spouse name
                self.UI.entry_spouse.setText(d_name[1].title())
            else:
                self.UI.entry_spouse.setText('None')

            for child in d_name[2:]:
                if child is None:
                    self.UI.combo_children.addItem('None')
                else:
                    self.UI.combo_children.addItem(child.title())
                    self.UI.combo_children.setCurrentText(person)

            amt = MBillsFunctions.getPersonAmountForMonth(self.wkbk_med_bills, s_name.title(), self.all_names_and_dept,
                                                          self.months, self.UI.combo_months.currentText())
            self.UI.entry_cur_amount.setText(self.UI.entry_cur_amount.text() + str(amt))

        else:  # means person is a guest or casual
            guest_or_casual = MBillsFunctions.searchForCasualOrGuest(self.all_names_and_dept, person)
            amt = MBillsFunctions.getPersonAmountForMonth(self.wkbk_med_bills, person, self.all_names_and_dept,
                                                          self.months, self.UI.combo_months.currentText())
            if 'GUEST' in guest_or_casual.split('|')[1]:
                self.UI.lbl_staff_name.setText(person_status[1])
                self.UI.entry_department.setText('GUEST')
            elif 'CASUAL' in guest_or_casual.split('|')[1]:
                self.UI.lbl_staff_name.setText(person_status[-1])
                self.UI.entry_department.setText('CASUAL')

            self.UI.entry_staff_name.setText(person)
            self.UI.entry_spouse.setText('None')
            self.UI.combo_children.addItem('None')
            self.UI.entry_cur_amount.setText(self.UI.entry_cur_amount.text() + str(amt))


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
    #   3. Update amount when months combo box changes
