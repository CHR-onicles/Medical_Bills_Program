from PyQt5.QtCore import (QSize, Qt, pyqtSignal, pyqtSlot, QThread, QThreadPool, QRunnable, QObject, QUrl,
                          QAbstractTableModel)
from PyQt5.QtGui import (QIcon, QFont, QStandardItemModel)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QWidget, QSizePolicy,
                             QCompleter, QMessageBox, QTableWidgetItem, QTableWidget, QStyledItemDelegate,
                             QAbstractItemView, QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QStatusBar, QListView)
from PyQt5.QtMultimedia import (QSoundEffect)
import sys
from icecream import ic
import openpyxl
from datetime import datetime

# Local imports
import resources_rc, styles
from UI_main_window import UIMainWindow, QVSeparationLine, QHSeparationLine
from med_bills_functions import MBillsFunctions





# icecream debugging configs
ic.configureOutput(includeContext=True)



class RecentlyEditedTableModel(QAbstractTableModel):

    def __init__(self):
        super(RecentlyEditedTableModel, self).__init__()





class MainApp(QMainWindow):
    """
    Main App configurations.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Med Bills App')
        self.setWindowIcon(QIcon(':/icon/cat'))
        self.UI = UIMainWindow()
        self.setCentralWidget(self.UI)
        self.setStyleSheet(styles.main_window_style())
        self.resize(1300, 930)
        # self.resize(1000, 800)  # for testing purposes
        self.setMinimumSize(QSize(1100, 850))  # todo: based on final program edit this

        # SFX -------------------------------------------------------------------------------------------
        self.sfx_player = QSoundEffect()
        self.sfx_player.setSource(QUrl.fromLocalFile(':/sfx/success'))

        # Medical Bills Files configs -------------------------------------------------------------------
        self.months = {'January': 2, 'February': 3, 'March': 4, 'April': 5, 'May': 6, 'June': 7, 'July': 8,
                       'August': 9, 'September': 10, 'October': 11, 'November': 12, 'December': 13}
        self.wkbk_med_bills, self.wkbk_staff_list = MBillsFunctions.initializeFiles('test_med_bills_20.xlsx',
                                                                                    'test_staff_list.xlsx')
        self.all_names_and_dept = MBillsFunctions.getAllMedBillsNamesAndDept(self.wkbk_med_bills)
        self.all_names_and_dept.extend(MBillsFunctions.getAllDependantNames(self.wkbk_staff_list))
        self.staff_details = MBillsFunctions.getDetailsOfPermanentStaff(self.wkbk_staff_list)

        # Completer configs -----------------------------------------------------------------------------
        self.completer = QCompleter([name.split('|')[0] for name in self.all_names_and_dept])
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
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
        self.initUI()

    def initUI(self):
        # Disable these widgets on startup
        # self.UI.entry_staff_name.setDisabled(True)
        # self.UI.entry_department.setDisabled(True)
        # self.UI.entry_spouse.setDisabled(True)
        # self.UI.combo_children.setDisabled(True)
        # self.UI.entry_cur_amount1.setDisabled(True)
        self.UI.btn_submit.setEnabled(False)

        self.UI.entry_staff_or_dependant.setFocus()

        self.UI.combo_months.addItems(list(self.months.keys()))
        self.mon = self.UI.combo_months.currentText()[0:3]
        self.UI.lbl_cur_amount.setText('Current Amount For <u>' + self.mon + '</u>(<font color=\"#3d8ec9\">GH₵</font>):')

        self.UI.entry_staff_or_dependant.setCompleter(self.completer)

        self.UI.entry_quick_search.setCompleter(self.completer)
        self.UI.entry_quick_search.returnPressed.connect(
            lambda: self.populateStaffDetails(self.UI.entry_quick_search.text().strip()))
        # self.UI.entry_quick_search.textChanged.connect(self.awakenStaffDetailsWidgets)
        self.UI.btn_quick_search.clicked.connect(
            lambda: self.populateStaffDetails(self.UI.entry_quick_search.text().strip()))

        # self.UI.entry_staff_or_dependant.returnPressed.connect(
        #     lambda: self.populateStaffDetails(self.UI.entry_staff_or_dependant.text().strip()))

        self.UI.entry_staff_or_dependant.textChanged.connect(self.checkEntryStaffDepState)
        self.UI.entry_amount.textChanged.connect(self.checkEntryStaffDepState)
        self.UI.btn_submit.clicked.connect(self.insertIntoMedBills)

        self.UI.combo_months.currentTextChanged.connect(self.updateDetailsForMonth)
        self.UI.combo_months.currentTextChanged.connect(self.updateCurAmountLabel)
        self.UI.entry_staff_or_dependant.returnPressed.connect(self.UI.entry_amount.setFocus)
        self.UI.entry_amount.returnPressed.connect(self.insertIntoMedBills)

        # STATUS BAR ---------------------------------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setFont(QFont('century gothic', 12, 0, True))
        self.status_bar.showMessage('Welcome, this is the status bar...', 5000)
        self.btn_refresh = QPushButton('Refresh')
        self.btn_refresh.setObjectName('btn_quick_search_and_refresh')  # just to apply that style to this too
        self.btn_refresh.clicked.connect(self.clearStaffDetails)
        self.status_bar.addPermanentWidget(self.btn_refresh)
        # self.status_bar.addPermanentWidget(QPushButton('Undo'))

        self.status_bar.setFixedHeight(60)
        self.setContentsMargins(0, 0, 20, 0)
        # END STATUS BAR -----------------------------------------------------------------------------------

        # TABLE --------------------------------------------------------------------------------------------
        self.UI.table_last_edit.horizontalHeader().setVisible(False)
        self.UI.table_last_edit.verticalHeader().setVisible(False)

        self.UI.table_last_edit.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.UI.table_last_edit.insertRow(self.UI.table_last_edit.rowCount())  # add row at location of last row
        # self.UI.table_last_edit.setSortingEnabled(True)  # dont need to sort for now
        # END TABLE ----------------------------------------------------------------------------------------



    def updateCurAmountLabel(self):
        self.mon = self.UI.combo_months.currentText()[0:3]
        self.UI.lbl_cur_amount.setText('Current Amount For <u>' + self.mon + '</u>(<font color=\"#3d8ec9\">GH₵</font>):')

    def updateDetailsForMonth(self):
        if len(self.UI.entry_quick_search.text()) > 0:
            self.populateStaffDetails(self.UI.entry_quick_search.text())

    # def awakenStaffDetailsWidgets(self):
    #     if len(self.UI.entry_quick_search.text()) > 0:
    #         self.UI.entry_staff_name.setDisabled(False)
    #         self.UI.entry_department.setDisabled(False)
    #         self.UI.entry_spouse.setDisabled(False)
    #         self.UI.combo_children.setDisabled(False)
    #         self.UI.entry_cur_amount1.setDisabled(False)
    #     else:
    #         self.UI.entry_staff_name.clear()
    #         self.UI.entry_department.clear()
    #         self.UI.entry_spouse.clear()
    #         self.UI.combo_children.clear()
    #         self.UI.entry_cur_amount1.setText('GH₵ ')
    #         self.UI.entry_staff_name.setDisabled(True)
    #         self.UI.entry_department.setDisabled(True)
    #         self.UI.entry_spouse.setDisabled(True)
    #         self.UI.combo_children.setDisabled(True)
    #         self.UI.entry_cur_amount1.setDisabled(True)


    def checkEntryStaffDepState(self):
        if len(self.UI.entry_staff_or_dependant.text()) >= 1 and \
                 len(self.UI.entry_amount.text()) > 4:
            self.UI.btn_submit.setEnabled(True)
        else:
            self.UI.btn_submit.setEnabled(False)


    def populateStaffDetails(self, person):
        if self.UI.entry_quick_search.text() != '':
            person_status = ['Staff Name:', 'Guest Name:', 'Casual Name:']
            self.clearStaffDetails()

            s_name, d_name, _ = MBillsFunctions.searchForStaffFromStaffList(person.upper(),
                                                                            # all names in staff list are uppercase
                                                                            self.staff_details)

            if (s_name and d_name) is not None:
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
                        self.UI.combo_children.setEnabled(False)
                    else:
                        self.UI.combo_children.setEnabled(True)
                        self.UI.combo_children.addItem(child.title())
                        self.UI.combo_children.setCurrentText(person)

                staff_amt, child_amt, spouse_amt = MBillsFunctions.\
                    getPersonAmountForMonth(self.wkbk_med_bills, s_name.title(), self.all_names_and_dept,
                                            self.months, self.UI.combo_months.currentText())
                self.UI.entry_cur_amount1.setText(str(staff_amt))
                self.UI.entry_cur_amount2.setText(str(spouse_amt))
                self.UI.entry_cur_amount3.setText(str(child_amt))

            else:  # means person is a guest or casual
                guest_or_casual = MBillsFunctions.searchForCasualOrGuest(self.all_names_and_dept, person)
                if guest_or_casual is not None:
                    staff_amt, child_amt, spouse_amt = MBillsFunctions.\
                        getPersonAmountForMonth(self.wkbk_med_bills, guest_or_casual.split('|')[0],
                                                self.all_names_and_dept, self.months,
                                                self.UI.combo_months.currentText())
                    if 'GUEST' in guest_or_casual.split('|')[1]:
                        self.UI.lbl_staff_name.setText(person_status[1])
                        self.UI.entry_department.setText('GUEST')
                    elif 'CASUAL' in guest_or_casual.split('|')[1]:
                        self.UI.lbl_staff_name.setText(person_status[-1])
                        self.UI.entry_department.setText('CASUAL')

                    self.UI.entry_staff_name.setText(guest_or_casual.split('|')[0])
                    self.UI.entry_spouse.setText('None')
                    self.UI.combo_children.addItem('None')
                    self.UI.combo_children.setEnabled(False)
                    self.UI.entry_cur_amount1.setText(str(staff_amt))
                    self.UI.entry_cur_amount2.setText(str(spouse_amt))
                    self.UI.entry_cur_amount3.setText(str(child_amt))

                else:
                    QMessageBox.critical(self, 'Search Error', 'The Person you searched for <b>cannot</b> be found!')
        else:
            QMessageBox.critical(self, 'Search Error', 'Search box <b>cannot</b> be empty!')

    def clearStaffDetails(self):
        self.UI.entry_staff_name.clear()
        self.UI.entry_department.clear()
        self.UI.entry_spouse.clear()
        self.UI.combo_children.clear()
        self.UI.entry_cur_amount1.clear()
        self.UI.entry_cur_amount2.clear()
        self.UI.entry_cur_amount3.clear()
        self.UI.entry_amount.setText('GH₵ ')
        # self.UI.entry_staff_or_dependant.clear()


    def insertIntoMedBills(self):
        if self.UI.entry_staff_or_dependant.text() in [names.split('|')[0] for names in self.all_names_and_dept]:
            # start = datetime.now()
            person_typed = self.UI.entry_staff_or_dependant.text()
            amount = str(self.UI.entry_amount.text()[4:])
            offset_col = self.months[self.UI.combo_months.currentText()]
            # ic.disable()
            # ic(offset_col)

            if person_typed.upper() in self.staff_details.keys():  # check if permanent staff was typed
                dept = MBillsFunctions.getDepartmentFromName(person_typed, self.all_names_and_dept)
                # ic('entered staff')
                MBillsFunctions.insertAmountIntoMedBills(self.wkbk_med_bills, person_typed, dept, offset_col, 0, amount)
            else:  # person could be dependant or casual/guest
                actual_staff, dependant, status = MBillsFunctions.searchForStaffFromStaffList(person_typed.upper(),
                                                                                              self.staff_details)
                if actual_staff is not None:  # check if person is in staff list
                    actual_staff = actual_staff.title()
                    dependant = [x.title() for x in dependant if x is not None]
                    # ic(actual_staff, dependant, status)
                    # Checking for dependant
                    if status == 'v':  # found dependant
                        dept = MBillsFunctions.getDepartmentFromName(actual_staff, self.all_names_and_dept)
                        if dept is not None:
                            # global person_typed
                            # 2 if person is spouse of staff else 1 for child of staff
                            if self.UI.entry_staff_or_dependant.text() not in dependant[2:]:
                                offset_row = 2
                                # ic('entered spouse')
                            else:
                                offset_row = 1
                                # ic('entered child')
                            MBillsFunctions.insertAmountIntoMedBills(self.wkbk_med_bills, actual_staff,
                                                                     dept, offset_col, offset_row, amount)

                else:  # person is guest/casual
                    # ic('entered guest')
                    dept = MBillsFunctions.getDepartmentFromName(person_typed, self.all_names_and_dept)
                    MBillsFunctions.insertAmountIntoMedBills(self.wkbk_med_bills, person_typed, dept, offset_col, 0,
                                                             amount)

            # self.UI.entry_staff_or_dependant.clear()
            self.UI.entry_amount.setText('GH₵ ')

            # stop = datetime.now()
            # ic('Time taken to insert:', stop-start)

            self.sfx_player.play()
            self.status_bar.showMessage('Entry saved successfully...', 3000)

        else:
            QMessageBox.critical(self, 'Entry Error', 'No record found!')






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


    # ---------------------------------------- TODO --------------------------------------------------------
    # TODO:
    #   1. Difference between quick search and typing staff/dependant name directly???
    #   2. Let status bar show status of long processes
