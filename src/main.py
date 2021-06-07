# Standard library imports
import os
import subprocess as sbp  # To terminate Excel processes before the app saves.
import sys
import time
from datetime import datetime

# 3rd Party imports
# from icecream import ic
from PyQt5.QtCore import (Qt, QSettings, QSize, QPoint)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QComboBox, QCompleter, QMessageBox, QTableWidgetItem,
                             QStyledItemDelegate, QAbstractItemView, QStatusBar, QAction, QRadioButton, QHBoxLayout)
from PyQt5.QtGui import (QIcon, QFont)

# Local imports
from _version import __version__
from src import styles
from src import med_bills_functions  # to access the global variables
from src import UIMainWindow, MBillsFunctions


sys.path.append("..")  # to include files one level up from this directory
import resources_rc



# icecream debugging configs
# ic.configureOutput(includeContext=True)


class Log:
    """
    Class to deal with logging of entries from app.
    """
    undo_called = False

    def __init__(self, log_file):
        self.initialized_already = False
        self.LOG_FILE = log_file  # this changes when working on test files.

    def initialize(self, file):
        """
        Method to signify start of batch entries by a timestamp and name of the database file.
        """
        if self.initialized_already is True:
            return
        with open(self.LOG_FILE, 'a') as f:
            f.write('== ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + f' -> {file}' + ' ==')
        self.initialized_already = True

    def add_entry(self, entry, is_redo=False):
        """
        Method to add an entry to log file.
        """
        with open(self.LOG_FILE, 'a') as f:
            # line below is not creating newline after undo on Win 8.1(Target PC)
            # f.write(str(entry)) if (is_redo or self.undo_called) is True else f.write('\n' + str(entry))
            f.write('\n' + str(entry))
        self.undo_called = False

    def undo_entry(self):
        """
        Deleting last line in file: (https://stackoverflow.com/questions/1877999/delete-final-line-in-file-with-python)
        """
        with open(self.LOG_FILE, "r+", ) as file:
            # Move the pointer to the end of the file
            file.seek(0, os.SEEK_END)
            # Go one step back from the last newline character at EOF
            pos = file.tell() - 1
            # Loop backwards searching for newline character
            while pos > 0 and file.read(1) != "\n":
                pos -= 1
                file.seek(pos, os.SEEK_SET)
            # Delete all the characters ahead of this position if we're not at the beginning
            if pos > 0:
                file.seek(pos, os.SEEK_SET)
                file.truncate()
                self.undo_called = True

    def undo_specific_entry(self):
        """
        Method to remove a specific row(entry) from a batch of entries.
        """
        global global_specific_row, global_all_entries
        row = global_specific_row - 1
        # print(global_all_entries)
        # print('Row:', row)
        # print(global_all_entries)
        with open(self.LOG_FILE, 'r') as file:
            lines = file.readlines()
        with open(self.LOG_FILE, 'w+') as file:
            for line in lines:
                if line.strip('\n') != str(global_all_entries[row]):
                    file.write(line)
            if row == len(global_all_entries) - 1:
                file.seek(0, os.SEEK_END)
                pos = file.tell()
                char = ']' if row != 0 else '='
                while pos > 0 and file.read(1) != char:
                    pos -= 1
                    file.seek(pos, os.SEEK_SET)
                if pos > 0:
                    file.seek(pos + 1, os.SEEK_SET)
                    file.truncate()
                    # fixme: bug here where it sometimes doesn't delete the first person after multiple entries
                    #   - bug not occuring on Win 8.1 VM (target PC)... so maybe ignore...

            del global_all_entries[row]

    def terminate(self):
        """
        Method to end signify end of a batch of entries with '='.
        """
        if self.initialized_already is True:
            with open(self.LOG_FILE, 'a') as f:
                f.write('=' * 150 + '\n\n') if self.undo_called is True else f.write('\n' + '=' * 150 + '\n\n')






# Global variables
global_specific_row = 0
global_all_entries = []


class MainApp(QMainWindow):
    """
    App configurations.
    """
    is_duplicate_toggle = False

    def __init__(self):
        super().__init__()

        # Window configs -------------------------------------------------------------------------------------
        self.setWindowTitle('Med Bills App' + ' v' + __version__)
        self.setWindowIcon(QIcon(':/icon/cat'))
        self.UI = UIMainWindow()
        self.setCentralWidget(self.UI)
        self.setStyleSheet(styles.main_window_style())

        # Factoring in size of app in other desktop resolutions
        if self.UI.desktop.width() == 1920 and self.UI.desktop.height() == 1080:
            self.APP_WIDTH, self.APP_HEIGHT = 1300, 950
            self.resize(self.APP_WIDTH, self.APP_HEIGHT)  # Seems like the perfect size for nice spacing among widgets.
            # self.resize(1000, 800)  # for testing purposes on 1920x1080 desktop
        else:
            # Resize app to maintain spacing between widgets for better look on all desktop resolutions
            WIDTH_RATIO, HEIGHT_RATIO = 1920 / 1300, 1080 / 950
            self.APP_WIDTH = int(round(self.UI.desktop.width() / WIDTH_RATIO, 1))
            self.APP_HEIGHT = int(round(self.UI.desktop.height() / HEIGHT_RATIO, 1))
            print('New res:', self.APP_WIDTH, self.APP_HEIGHT)
            self.resize(self.APP_WIDTH, self.APP_HEIGHT)
        # END Window configs ---------------------------------------------------------------------------------

        # App Settings ---------------------------------------------------------------------------------------
        self.settings = QSettings('CHR-onicles', 'Med Bills App')
        self.APP_XPOS, self.APP_YPOS = 0, 0  # Have to initialize to a 'not None' value for it to have effect
        try:
            self.resize(self.settings.value('app size', QSize(self.APP_WIDTH, self.APP_HEIGHT), type=QSize))
            self.move(self.settings.value('app position', QPoint(self.APP_XPOS, self.APP_YPOS), type=QPoint))
            # print(self.APP_XPOS, self.APP_YPOS)
        except:
            pass
        # END App Settings -----------------------------------------------------------------------------------

        # Medical Bills Files configs ------------------------------------------------------------------------
        self.months = {'January': 2, 'February': 3, 'March': 4, 'April': 5, 'May': 6, 'June': 7, 'July': 8,
                       'August': 9, 'September': 10, 'October': 11, 'November': 12, 'December': 13}

        # todo: Automatically check for the right files later [optional]
        # Files to use for faster reference:
        # test med bills 2021.xlsx
        # MEDICAL BILLS 2021.xlsx
        self.FILE_1, self.FILE_2 = 'test med bills 2021.xlsx', 'STAFF DEPENDANT LIST 2020.xlsx'
        self.wkbk_med_bills, self.wkbk_staff_list = MBillsFunctions.initialize_files(self.FILE_1, self.FILE_2)
        print(f'Working with: "{self.FILE_1}" and "{self.FILE_2}"')  # For testing and debugging
        self.all_names_and_dept = MBillsFunctions.get_all_med_bills_names_and_dept(self.wkbk_med_bills)
        self.all_names_and_dept.extend(MBillsFunctions.get_all_dependant_names(self.wkbk_staff_list))
        self.staff_details = MBillsFunctions.get_details_of_permanent_staff(self.wkbk_staff_list)
        # END Medical Bills Files configs --------------------------------------------------------------------


        # Auto Completer configs -----------------------------------------------------------------------------
        self.completer = QCompleter(set([name.split('|')[0] for name in self.all_names_and_dept]))
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
        # END Auto Completer configs -------------------------------------------------------------------------


        # Table info -----------------------------------------------------------------------------------------
        self.myrow_data = []

        self.UI.table_last_edit.setContextMenuPolicy(Qt.ActionsContextMenu)
        remove_action = QAction('Remove Entry \t',
                                self.UI.table_last_edit)  # '\t' quick fix for text not being centered automatically
        remove_action.setFont(QFont('segoe UI'))
        self.UI.table_last_edit.addAction(remove_action)
        remove_action.triggered.connect(self.remove_particular_entry)
        # END Table info -------------------------------------------------------------------------------------

        # Initializing log -----------------------------------------------------------------------------------
        if self.FILE_1 == 'MEDICAL BILLS 2021.xlsx':
            self.log = Log('entry_log.log')
            # No need to explicitly state that its "one level up" with "../",
            # because it's included in Path.
        else:
            self.log = Log('test_log.log')
        # END Initializing log -------------------------------------------------------------------------------

        self.ui_comp()


    def ui_comp(self):
        self.init_ui()


    def init_ui(self):
        """
        Initializing widgets for startup and connecting signals to slots.
        """
        # Disable these widgets on startup
        # self.UI.entry_staff_name.setDisabled(True)
        # self.UI.entry_department.setDisabled(True)
        # self.UI.entry_spouse.setDisabled(True)
        # self.UI.combo_children.setDisabled(True)
        # self.UI.entry_cur_amount1.setDisabled(True)
        self.UI.btn_submit.setEnabled(False)
        self.UI.btn_undo.setEnabled(False)
        self.UI.btn_redo.setEnabled(False)
        self.UI.btn_clear.setEnabled(False)
        self.UI.entry_staff_or_dependant.setFocus()

        # Dynamic widgets created for duplicate condition
        self.duplicate_btn1 = QRadioButton()
        self.duplicate_btn2 = QRadioButton()
        self.temp_layout = QHBoxLayout()

        self.UI.combo_months.addItems(list(self.months.keys()))
        try:
            self.UI.combo_months.setCurrentIndex(self.settings.value('current month', 0, type=int))
        except:
            pass
        self.mon = self.UI.combo_months.currentText()[0:3]
        self.UI.lbl_cur_amount.setText(
            'Current Amount For <u>' + self.mon + '</u>(<font color=\"#3d8ec9\">GH₵</font>):')

        self.UI.entry_staff_or_dependant.setCompleter(self.completer)

        self.UI.entry_quick_search.setCompleter(self.completer)

        self.UI.entry_quick_search.returnPressed.connect(
            lambda: self.populate_staff_details(self.UI.entry_quick_search.text().strip()))
        self.UI.btn_quick_search.clicked.connect(
            lambda: self.populate_staff_details(self.UI.entry_quick_search.text().strip()))

        self.UI.entry_staff_or_dependant.textChanged.connect(self.check_entry_staff_dep_state)
        self.UI.entry_amount.textChanged.connect(self.check_entry_staff_dep_state)
        self.UI.btn_submit.clicked.connect(self.insert_into_med_bills)

        self.UI.combo_months.currentTextChanged.connect(self.update_details_for_month)
        self.UI.combo_months.currentTextChanged.connect(self.update_cur_amount_label)
        self.UI.entry_staff_or_dependant.returnPressed.connect(self.UI.entry_amount.setFocus)
        self.UI.entry_amount.returnPressed.connect(self.insert_into_med_bills)

        self.UI.btn_clear.clicked.connect(self.control_clear_staff_details)
        self.UI.btn_undo.clicked.connect(self.undo)
        self.UI.btn_redo.clicked.connect(self.redo)
        self.UI.btn_save.clicked.connect(self.save_workbook)
        self.UI.btn_refresh.clicked.connect(self.refresh)

        # STATUS BAR ---------------------------------------------------------------------------------------
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setFont(QFont('century gothic', 12))
        self.status_bar.showMessage(f'Initializing files: "{self.FILE_1}" and "{self.FILE_2}"', 7000)
        # END STATUS BAR -----------------------------------------------------------------------------------

        # TABLE --------------------------------------------------------------------------------------------
        self.UI.table_last_edit.horizontalHeader().setVisible(False)
        self.UI.table_last_edit.verticalHeader().setVisible(False)
        self.UI.table_last_edit.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # END TABLE ----------------------------------------------------------------------------------------


    def update_cur_amount_label(self):
        """
        Method to update the Current Amount Label in accordance with the month it is set to.
        """
        self.mon = self.UI.combo_months.currentText()[0:3]
        self.UI.lbl_cur_amount.setText(
            'Current Amount For <u>' + self.mon + '</u>(<font color=\"#3d8ec9\">GH₵</font>):')


    def update_details_for_month(self):
        """
        Method to update all details of staff in accordance with the month it is set to.
        """
        if self.duplicate_btn1.isVisible():
            self.populate_staff_details(self.dup_name1, input_call='Entry') if self.duplicate_btn1.isChecked() \
                else self.populate_staff_details(self.dup_name2, input_call='Entry')
            return

        if self.UI.entry_quick_search.text() != '':
            self.populate_staff_details(self.UI.entry_quick_search.text())
        elif self.UI.entry_quick_search.text() == '' and self.UI.table_last_edit.rowCount() == 1:
            return
        elif self.UI.entry_staff_name.text() == self.UI.table_last_edit.item(self.UI.table_last_edit.rowCount() - 1,
                                                                             1).text():
            self.populate_staff_details(self.UI.entry_staff_name.text(), input_call='Entry')
            # without an else: return, it still does the job...DONT touch it! 😬 - might not actually be necessary


    def check_entry_staff_dep_state(self):
        """
        Method to enable/disable the submit button based on entry in Staff/Dependant & Amount line edits.
        """
        if len(self.UI.entry_staff_or_dependant.text()) >= 1 and \
                len(self.UI.entry_amount.text()) > 4:
            self.UI.btn_submit.setEnabled(True)
        else:
            self.UI.btn_submit.setEnabled(False)


    def populate_staff_details(self, person, input_call=None):
        """
        Method to populate various widgets with the details of a Staff(either permanent staff/Guest/Casual) or Dependant.

        :param person: Person whose details are to be populated.

        :param input_call: Random thingy to know which other method called this method and behave accordingly.
        """
        if (input_call is None) and (self.UI.entry_quick_search.text() == ''):
            # QMessageBox.critical(self, 'Search Error', 'Search box <b>cannot</b> be empty!')
            return
        else:
            person_status = ['Staff Name:', 'Guest Name:', 'Casual Name:']
            self.clear_staff_details()
            search_result = MBillsFunctions.search_for_staff_from_staff_list(person.upper(), self.staff_details)
            s_name = search_result[0][0]
            d_name = search_result[0][1]

            if search_result:  # not empty list
                if self.duplicate_btn1.isVisible() and s_name.split()[0] not in [self.duplicate_btn1.text(), self.duplicate_btn2.text()]:
                    # print(s_name.split()[0], 'not same as', self.duplicate_btn1.text(), 'or', self.duplicate_btn2.text())
                    self.remove_duplicate_btns()
                if len(search_result) > 1 and self.is_duplicate_toggle is False:
                    if not self.duplicate_btn1.isVisible():
                        self.setup_duplicate_btns(s_name, d_name[1].title(), self.UI.staff_form)
                        return
                if self.duplicate_btn1.isVisible() and len(search_result) == 1:  # searching for non-duplicate
                    self.remove_duplicate_btns()

                self.UI.lbl_staff_name.setText(person_status[0])
                self.UI.entry_staff_name.setText(s_name.title())
                if person == s_name.title():
                    self.set_border_highlight_switch(self.UI.entry_staff_name)
                self.UI.entry_department.setText(d_name[0])
                if d_name[1] != '-':  # Spouse name
                    self.UI.entry_spouse.setText(d_name[1].title())
                    if person == d_name[1].title():
                        self.set_border_highlight_switch(self.UI.entry_spouse)
                else:
                    self.UI.entry_spouse.setText('None')

                for child in d_name[2:]:
                    if child == '-':
                        self.UI.combo_children.addItem('None')
                        self.UI.combo_children.setEnabled(False)
                    else:
                        self.UI.combo_children.setEnabled(True)
                        self.UI.combo_children.addItem(child.title())
                        self.UI.combo_children.setCurrentText(person)
                        if person == child.title():
                            self.set_border_highlight_switch(self.UI.combo_children)

                staff_amt, child_amt, spouse_amt = MBillsFunctions. \
                    get_person_amount_for_month(self.wkbk_med_bills, s_name.title(), self.all_names_and_dept,
                                                self.months, self.UI.combo_months.currentText())
                self.UI.entry_cur_amount1.setText(str(staff_amt))
                self.UI.entry_cur_amount2.setText(str(spouse_amt))
                self.UI.entry_cur_amount3.setText(str(child_amt))

            else:  # means person is a guest or casual
                guest_or_casual = MBillsFunctions.search_for_casual_or_guest(self.all_names_and_dept, person)
                if guest_or_casual is not None:
                    staff_amt, child_amt, spouse_amt = MBillsFunctions. \
                        get_person_amount_for_month(self.wkbk_med_bills, guest_or_casual.split('|')[0],
                                                    self.all_names_and_dept, self.months,
                                                    self.UI.combo_months.currentText())
                    if 'GUEST' in guest_or_casual.split('|')[1]:
                        self.UI.lbl_staff_name.setText(person_status[1])
                        self.UI.entry_department.setText('GUEST')
                    elif 'CASUAL' in guest_or_casual.split('|')[1]:
                        self.UI.lbl_staff_name.setText(person_status[-1])
                        self.UI.entry_department.setText('CASUAL')

                    self.UI.entry_staff_name.setText(guest_or_casual.split('|')[0])
                    self.set_border_highlight_switch(self.UI.entry_staff_name)
                    self.UI.entry_spouse.setText('None')
                    self.UI.combo_children.addItem('None')
                    self.UI.combo_children.setEnabled(False)
                    self.UI.entry_cur_amount1.setText(str(staff_amt))
                    self.UI.entry_cur_amount2.setText(str(spouse_amt))
                    self.UI.entry_cur_amount3.setText(str(child_amt))

                else:
                    QMessageBox.critical(self, 'Search Error', 'The Person you searched for <b>cannot</b> be found!')
            self.UI.btn_clear.setEnabled(True)


    def control_clear_staff_details(self):
        self.clear_staff_details() if self.is_duplicate_toggle is False else self.clear_staff_details_with_duplicate()


    def clear_staff_details(self):
        """
        Method to clear widgets populated with staff details.
        """
        self.UI.entry_staff_name.clear()
        self.UI.entry_department.clear()
        self.UI.entry_spouse.clear()
        self.UI.combo_children.clear()
        self.UI.entry_cur_amount1.clear()
        self.UI.entry_cur_amount2.clear()
        self.UI.entry_cur_amount3.clear()
        self.UI.entry_amount.setText('GH₵ ')
        # self.UI.entry_staff_or_dependant.clear()
        self.UI.btn_clear.setEnabled(False)
        self.set_border_highlight_switch(None)


    def clear_staff_details_with_duplicate(self):
        self.clear_staff_details()
        self.remove_duplicate_btns()


    def insert_into_med_bills(self):
        """
        Method to insert amount entered for a Staff or Dependant into Med Bills workbook(The database).
        """
        # todo: add code to take care of duplicates
        if self.UI.entry_staff_or_dependant.text() in [names.split('|')[0] for names in self.all_names_and_dept]:
            # start = datetime.now()
            med_bills_functions.UNDO_ENTRY_HISTORY.clear()
            person_typed = self.UI.entry_staff_or_dependant.text()
            amount = str(self.UI.entry_amount.text()[4:])
            offset_col = self.months[self.UI.combo_months.currentText()]
            # ic.disable()
            # ic(offset_col)

            if person_typed.upper() in self.staff_details.keys():  # check if permanent staff was typed
                dept = MBillsFunctions.get_department_from_name(person_typed, self.all_names_and_dept)
                # ic('entered staff')
                MBillsFunctions.insert_amount_into_med_bills(self.wkbk_med_bills, person_typed, dept, offset_col, 0,
                                                             amount)
                self.myrow_data.append([person_typed, self.staff_details[person_typed.upper()][0],
                                        self.staff_details[person_typed.upper()][1].title() if
                                        self.staff_details[person_typed.upper()][1] != '-' else 'None',
                                        [x.title() if x != '-' else 'None' for x in
                                         self.staff_details[person_typed.upper()][2:]],
                                        self.UI.combo_months.currentText()[0:3].upper(), 'STAFF', f'{float(amount):.2f}'
                                        ])
                self.update_table()
            else:  # person could be dependant or casual/guest
                search_result = MBillsFunctions.search_for_staff_from_staff_list(person_typed.upper(), self.staff_details)
                actual_staff, dependant, status = search_result[0][0], search_result[0][1], search_result[0][2]
                if actual_staff is not None:  # check if person is in staff list
                    actual_staff = actual_staff.title()
                    dependant = [x.title() for x in dependant if x is not None]
                    # ic(actual_staff, dependant, status)
                    # Checking for dependant
                    if status == 'v':  # found dependant
                        dept = MBillsFunctions.get_department_from_name(actual_staff, self.all_names_and_dept)
                        if dept is not None:
                            # global person_typed
                            # 2 if person is spouse of staff else 1 for child of staff
                            if self.UI.entry_staff_or_dependant.text() not in dependant[2:]:
                                offset_row = 2
                            else:
                                offset_row = 1
                            MBillsFunctions.insert_amount_into_med_bills(self.wkbk_med_bills, actual_staff,
                                                                         dept, offset_col, offset_row, amount)
                            self.myrow_data.append([actual_staff, self.staff_details[actual_staff.upper()][0],
                                                    self.staff_details[actual_staff.upper()][1].title() if
                                                    self.staff_details[actual_staff.upper()][1] != '-' else 'None',
                                                    [x.title() if x != '-' else 'None' for x in
                                                     self.staff_details[actual_staff.upper()][2:]],
                                                    self.UI.combo_months.currentText()[0:3].upper(),
                                                    'CHILD' if offset_row == 1 else 'SPOUSE',
                                                    f'{float(amount):.2f}'
                                                    ])
                            self.update_table()

                else:  # person is guest/casual
                    # ic('entered guest')
                    dept = MBillsFunctions.get_department_from_name(person_typed, self.all_names_and_dept)
                    MBillsFunctions.insert_amount_into_med_bills(self.wkbk_med_bills, person_typed, dept, offset_col, 0,
                                                                 amount)
                    self.myrow_data.append([person_typed, 'GUEST' if 'GUEST' in dept else 'CASUAL',
                                            'None', 'None', self.UI.combo_months.currentText()[0:3].upper(),
                                            'GUEST' if 'GUEST' in dept else 'CASUAL', f'{float(amount):.2f}'
                                            ])
                    self.update_table()

            self.populate_staff_details(self.UI.entry_staff_or_dependant.text(), input_call='Entry')
            self.UI.entry_staff_or_dependant.clear()
            self.UI.entry_quick_search.clear()
            self.UI.entry_amount.setText('GH₵ ')
            self.UI.btn_undo.setEnabled(True)
            self.UI.btn_redo.setEnabled(False)
            self.undo_clicked_already = 0
            self.UI.entry_staff_or_dependant.setFocus()
            self.remove_hidden_rows()

            self.status_bar.showMessage('Entry entered successfully...', 2000)

            # stop = datetime.now()
            # print('Time taken to insert:', stop - start)

        else:
            QMessageBox.critical(self, 'Entry Error', 'No record found!')


    def undo(self):
        """
        Method to undo an entry.
        """
        if MBillsFunctions.undo_entry():
            self.hidden_row = self.UI.table_last_edit.rowCount() - 1
            self.UI.table_last_edit.hideRow(self.hidden_row)
            if len(med_bills_functions.UNDO_ENTRY_HISTORY) == 0:
                self.UI.btn_undo.setEnabled(False)
            self.status_bar.showMessage('Last entry has been undone...', 3000)
            self.UI.btn_redo.setEnabled(True)
            self.populate_staff_details(self.myrow_data_for_undo_redo[1], 'Entry')
            self.UI.entry_quick_search.clear()
            self.UI.table_last_edit.setCurrentCell(self.UI.table_last_edit.rowCount() - 2, 7)
            self.set_border_highlight_switch(None)
            self.log.undo_entry()


    def redo(self):
        """
        Method to redo a previously undone entry.
        """
        if MBillsFunctions.redo_entry():
            self.UI.table_last_edit.showRow(self.hidden_row)
            self.status_bar.showMessage('Entry redone successfully...', 3000)
            self.UI.btn_redo.setEnabled(False)
            self.UI.btn_undo.setEnabled(False)
            self.populate_staff_details(self.myrow_data_for_undo_redo[1], input_call='Entry')
            self.UI.entry_quick_search.clear()
            self.UI.table_last_edit.setCurrentCell(self.UI.table_last_edit.rowCount() - 1, 7)
            self.log.add_entry(self.myrow_data_for_undo_redo, is_redo=True)
            status = self.UI.table_last_edit.item(self.UI.table_last_edit.rowCount() - 1, 6).text()
            if status == 'STAFF':
                self.set_border_highlight_switch(self.UI.entry_staff_name)
            elif status == 'SPOUSE':
                self.set_border_highlight_switch(self.UI.entry_spouse)
            elif status == 'CHILD':
                self.set_border_highlight_switch(self.UI.combo_children)
            # No else statement to prevent unforeseen occurences.


    def update_table(self):
        """
        Method to update the table after an insertion to the Med Bills workbook has been made.
        """
        global global_all_entries
        start = datetime.now()  # DONT COMMENT OUT
        if self.myrow_data:  # check if row data is not empty
            self.UI.table_last_edit.insertRow(self.UI.table_last_edit.rowCount())  # add row at location of last row
            row = self.UI.table_last_edit.rowCount() - 1
            self.myrow_data[0].insert(0, str(start.strftime('%H:%M:%S')))
            for col, data in enumerate(self.myrow_data[0]):
                if col == 4:
                    combo_temp = QComboBox()
                    if 'None' in self.myrow_data[0][4]:
                        combo_temp.addItem('None')
                        combo_temp.setDisabled(True)
                    else:
                        if 'CHILD' in self.myrow_data[0]:
                            temp_index = self.myrow_data[0][4].index(self.UI.entry_staff_or_dependant.text())
                            self.myrow_data[0][4][0], self.myrow_data[0][4][temp_index] \
                                = self.myrow_data[0][4][temp_index], self.myrow_data[0][4][0]

                        combo_temp.addItems(self.myrow_data[0][4])
                    self.UI.table_last_edit.setCellWidget(row, 4, combo_temp)
                else:
                    self.UI.table_last_edit.setItem(row, col, QTableWidgetItem(data))
            self.UI.table_last_edit.item(row, 5).setFont(QFont('century gothic', 11))
            self.UI.table_last_edit.item(row, 5).setTextAlignment(Qt.AlignTop)
            self.UI.table_last_edit.item(row, 6).setFont(QFont('century gothic', 11))
            self.UI.table_last_edit.item(row, 6).setTextAlignment(Qt.AlignTop)
            self.UI.table_last_edit.setCurrentCell(row, 7)

        self.myrow_data_for_undo_redo = self.myrow_data[0]  # a copy of the list for undo and redo functions to use
        global_all_entries.append(self.myrow_data[0])

        # Logging added entry (for debugging)
        self.log.initialize(self.FILE_1)
        self.log.add_entry(self.myrow_data[0])

        self.myrow_data.clear()
        # stop = datetime.now()
        # print('Time taken to update table:', stop - start)


    def remove_particular_entry(self):
        """
        Method to remove/reverse/undo specific entries provided by a context menu.
        """
        global global_specific_row
        # start = datetime.now()
        selected_row = self.UI.table_last_edit.currentRow()
        global_specific_row = selected_row
        for col in range(self.UI.table_last_edit.columnCount()):
            if col == 1:
                staff_name = self.UI.table_last_edit.item(selected_row, col).text()
                # print('Staff:', staff_name)
            if col == 6:
                status = self.UI.table_last_edit.item(selected_row, col).text()
                # print('Status:', status)
        department = MBillsFunctions.get_department_from_name(staff_name, self.all_names_and_dept)
        # print('Department:', department)
        MBillsFunctions.undo_specific_entry(self.wkbk_med_bills, department, staff_name, status,
                                            self.months[self.UI.combo_months.currentText()])
        self.UI.table_last_edit.removeRow(selected_row)
        self.populate_staff_details(staff_name, 'Entry')
        self.log.undo_specific_entry()
        self.UI.btn_undo.setDisabled(True)
        self.UI.btn_redo.setDisabled(True)

        # stop = datetime.now()
        # ic('Time taken for specific undo:', stop-start)


    def refresh(self):
        self.clear_staff_details()
        self.UI.entry_quick_search.clear()
        # self.UI.combo_months.setCurrentIndex(0)
        self.UI.entry_staff_or_dependant.clear()
        self.UI.table_last_edit.setCurrentCell(0,
                                               0)  # just to make sure it doesn't remove this row as it is now set as active
        self.UI.table_last_edit.setRowCount(
            1)  # pro way of deleting rows, source: (https://stackoverflow.com/questions/15848086/how-to-delete-all-rows-from-qtablewidget)
        self.UI.btn_undo.setEnabled(False)
        self.UI.btn_redo.setEnabled(False)
        self.set_border_highlight_switch(None)
        self.remove_duplicate_btns()


    def save_workbook(self):
        """
        Method to save the Med Bills workbook.
        """
        # Check if Excel is opened and close it first to prevent file corruption:
        # todo: maybe notify user that all opened Excel files have been closed for above reason
        print('\nChecking if Excel is opened')
        tasklist = sbp.run('tasklist', shell=True, text=True, capture_output=True)
        if ('excel.exe' in tasklist.stdout) or ('EXCEL.EXE' in tasklist.stdout):
            print('Found Excel opened, closing it ASAP!')
            sbp.run(['taskkill', '/f', '/im', 'excel.exe', '/t'])
            print('Killed Excel successfully!')
        time.sleep(1)  # breather before app saves its version of the Excel file.

        if MBillsFunctions.save_file(self.wkbk_med_bills):
            self.status_bar.showMessage('Database saved and updated successfully...', 4000)


    def closeEvent(self, event):
        """
        Overriding PyQt's Close Event to save the workbook upon exit.

        :param event: Close event object.
        """
        # Save last size and position of app
        self.settings.setValue('app position', self.pos())
        self.settings.setValue('app size', self.size())
        self.settings.setValue('current month', self.UI.combo_months.currentIndex())

        self.hide()  # instantly hides app to prevent user from noticing delay(~2secs) in saving file when app exits.
        self.save_workbook()
        print('Saved workbook.')
        MBillsFunctions.close_file(self.wkbk_med_bills)
        MBillsFunctions.close_file(self.wkbk_staff_list)
        print('Closed workbooks.')

        # End logging
        self.log.terminate()

        event.accept()


    # Helper functions ------------------------------------------------------------------------------
    def set_border_highlight_switch(self, widget=None):
        """
        Helper function to highlight a widget which the 'searched for' person.

        :param widget: Widget to be highlighted.
        """
        self.UI.entry_staff_name.setStyleSheet('border: 1px solid #3A3939;')
        self.UI.entry_spouse.setStyleSheet('border: 1px solid #3A3939;')
        self.UI.combo_children.setStyleSheet('border: 1px solid #3A3939;')
        self.setStyleSheet(styles.main_window_style())

        if widget is not None:
            widget.setStyleSheet('border: 1px solid #78879b;')

    def remove_hidden_rows(self):
        """
        Helper function to remove hidden rows in table for accurate results in other calculations.
        """
        global global_all_entries
        for i in range(self.UI.table_last_edit.rowCount()):
            if self.UI.table_last_edit.isRowHidden(i):
                self.UI.table_last_edit.removeRow(i)
                del global_all_entries[i - 1]  # to keep visible rows and entries aligned

    def setup_duplicate_btns(self, name1, name2, location):
        """
        Helper function to toggle between the two instances of duplicate names.
        """
        self.UI.entry_quick_search.clear()
        self.dup_name1 = name1
        self.dup_name2 = name2  # in order to pass it to the update month details method
        self.duplicate_btn1.show()
        self.duplicate_btn1.setText(self.dup_name1.split()[0])
        self.duplicate_btn1.setChecked(True)
        self.duplicate_btn1.clicked.connect(lambda: self.on_dup_btn1_clicked(self.dup_name1))
        self.on_dup_btn1_clicked(self.dup_name1)
        self.duplicate_btn2.show()
        self.duplicate_btn2.setText(self.dup_name2.split()[0])
        self.duplicate_btn2.clicked.connect(lambda: self.on_dup_btn2_clicked(self.dup_name2))
        self.temp_layout = QHBoxLayout()
        self.temp_layout.addWidget(self.duplicate_btn1)
        self.temp_layout.addWidget(self.duplicate_btn2)
        location.insertRow(0, '', self.temp_layout)
        self.is_duplicate_toggle = True

    def on_dup_btn1_clicked(self, name):
        """
        Helper function to toggle to details of staff in the first option.
        """
        self.populate_staff_details(name, input_call='Entry')

    def on_dup_btn2_clicked(self, name):
        """
        Helper function to toggle to details of staff in the second option.
        """
        self.populate_staff_details(name, input_call='Entry')
        # Separated these one-liners into functions to potentially add more stuff later.

    def remove_duplicate_btns(self):
        """
        Helper function to remove buttons associated with the duplicate condition.
        """
        self.duplicate_btn1.hide()
        self.duplicate_btn2.hide()
        self.UI.staff_form.removeItem(self.temp_layout)
        self.is_duplicate_toggle = False






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


    # TODO/FIXME -------------------------------------------------------------------------------------------------------
    # TODO:
    #   - Bump version number to v1.2.0 (minor version update)
    #   - Change pink titles to groupboxes [optional -> New Feature]
    #   - Find a better way of doing "input_call='Entry'" [optional]
    #   - Properly evaluate boolean return value from functions [optional]
