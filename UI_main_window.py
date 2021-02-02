"""
Author: CHR-onicles
Date: 20/01/21
"""
from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (QPushButton, QLabel, QTabWidget, QComboBox, QWidget, QSizePolicy, QApplication,
                             QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox, QTableWidget,
                             QHeaderView)
import sys
from icecream import ic

# Local imports
from custom_widgets import (QHSeparationLine, QVSeparationLine, CurrencyInputValidator)




class UIMainWindow(QWidget):

    def __init__(self):
        super().__init__()
        # self.setStyleSheet(styles.main_window_style())  # Not needed here anymore


        self.UIComponents()
        # self.show()

    def UIComponents(self):
        self.UIwidgets()
        self.UIlayouts()

    def UIwidgets(self):
        # BIG TITLE ----------------------------------------------------------------------------------------
        self.lbl_title = QLabel('MEDICAL BILLS 2021')  # todo: link this to the excel file name somehow
        # self.lbl_title = QLabel('Medical Bills 2021')
        self.lbl_title.setObjectName('lbl_header')
        self.lbl_title.setAlignment(Qt.AlignHCenter)
        # END BIG TITLE ------------------------------------------------------------------------------------


        # TABS ---------------------------------------------------------------------------------------------
        self.tabs = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()  # todo: Implement statistics or staff list here
        # self.tab_3 = QWidget()  # todo: Implement Later (for Graphs maybe or utility stuff: like resetting all entries)
        self.tabs.addTab(self.tab_1, 'Receipt Entry')  # may change later
        self.tabs.addTab(self.tab_2, 'Tab 2')
        # self.tabs.addTab(self.tab_3, 'Tab 3')

        # TAB 1 WIDGETS ------------------------------------------------------------------------------------
        self.lbl_month = QLabel('Month:')
        self.lbl_month.setObjectName('lbl_titles')
        self.combo_months = QComboBox()
        self.combo_months.setObjectName('combo_titles')

        self.entry_quick_search = QLineEdit()
        self.entry_quick_search.setPlaceholderText('Quick Search For Dependant/Staff')
        self.entry_quick_search.setFixedWidth(500)
        self.entry_quick_search.setClearButtonEnabled(True)
        search_icon = QIcon(':/icon/search')
        self.entry_quick_search.addAction(search_icon, QLineEdit.LeadingPosition)
        self.btn_quick_search = QPushButton('Search')
        self.btn_quick_search.setObjectName('btn_quick_search_and_refresh')

        # Menu buttons ------------------------------------------------------------------------------------
        self.btn_undo = QPushButton()
        self.btn_undo.setIcon(QIcon(':/icon/undo'))
        self.btn_undo.setToolTip('Undo last entry')
        self.btn_undo.setObjectName('menu_button')
        self.btn_redo = QPushButton()
        self.btn_redo.setIcon(QIcon(':/icon/redo'))
        self.btn_redo.setToolTip('Redo recently undone entry')
        self.btn_redo.setObjectName('menu_button')
        self.btn_clear = QPushButton()
        self.btn_clear.setToolTip('Clear Staff details Summary')
        self.btn_clear.setIcon(QIcon(':/icon/clear'))
        self.btn_clear.setObjectName('menu_button')
        # END Menu buttons ---------------------------------------------------------------------------------


        # Entry from Receipt Widgets -----------------------------------------------------------------------
        self.lbl_entry_from_receipt = QLabel('<u>Entry For Bills/Claims</u>')
        self.lbl_entry_from_receipt.setAlignment(Qt.AlignHCenter)
        self.lbl_entry_from_receipt.setObjectName('lbl_titles')

        self.lbl_staff_or_dependant = QLabel('Staff/Dependant Name:')
        self.entry_staff_or_dependant = QLineEdit()
        self.entry_staff_or_dependant.setClearButtonEnabled(True)
        # self.entry_staff_or_dependant.setValidator(NameInputValidator())
        self.lbl_amount = QLabel('Amount:')
        self.entry_amount = QLineEdit('GH₵ ')
        self.entry_amount.setValidator(CurrencyInputValidator())
        self.entry_amount.setObjectName('entry_amount')
        self.btn_submit = QPushButton('Submit')
        self.btn_submit.setObjectName('btn_submit')

        # END Entry from Receipt Widgets -------------------------------------------------------------------


        # Staff Details widgets ----------------------------------------------------------------------------
        self.lbl_staff_details = QLabel('<u>Staff Details Summary</u>')
        self.lbl_staff_details.setAlignment(Qt.AlignHCenter)
        self.lbl_staff_details.setObjectName('lbl_titles')

        self.lbl_staff_name = QLabel('Staff Name:')
        self.entry_staff_name = QLineEdit()
        self.entry_staff_name.setReadOnly(True)
        self.lbl_department = QLabel('Department:')
        self.entry_department = QLineEdit()
        self.entry_department.setReadOnly(True)
        self.entry_department.setObjectName('entry_department')
        self.lbl_spouse = QLabel('Spouse:')
        self.entry_spouse = QLineEdit()
        self.entry_spouse.setReadOnly(True)
        self.lbl_children = QLabel('Child(ren):')
        self.combo_children = QComboBox()
        self.lbl_cur_amount = QLabel()
        self.lbl_cur_amount.setWordWrap(True)
        self.lbl_staff_amt = QLabel('Staff')
        self.lbl_staff_amt.setAlignment(Qt.AlignHCenter)
        self.lbl_spouse_amt = QLabel('Spouse')
        self.lbl_spouse_amt.setAlignment(Qt.AlignHCenter)
        self.lbl_child_amt = QLabel('Child')
        self.lbl_child_amt.setAlignment(Qt.AlignHCenter)
        self.entry_cur_amount1 = QLineEdit()
        self.entry_cur_amount1.setReadOnly(True)
        self.entry_cur_amount1.setObjectName('entry_amount')
        self.entry_cur_amount1.setAlignment(Qt.AlignHCenter)
        self.entry_cur_amount2 = QLineEdit()
        self.entry_cur_amount2.setReadOnly(True)
        self.entry_cur_amount2.setObjectName('entry_amount')
        self.entry_cur_amount2.setAlignment(Qt.AlignHCenter)
        self.entry_cur_amount3 = QLineEdit()
        self.entry_cur_amount3.setReadOnly(True)
        self.entry_cur_amount3.setObjectName('entry_amount')
        self.entry_cur_amount3.setAlignment(Qt.AlignHCenter)
        # END Staff Details widgets -----------------------------------------------------------------------


        # TABLE -------------------------------------------------------------------------------------------
        self.hline1 = QHSeparationLine()
        # self.hline1.setStyleSheet('border: 1px solid gray;')
        self.lbl_table_title = QLabel('Last Edit History:')

        self.table_last_edit = QTableWidget()
        self.table_last_edit.setRowCount(1)
        self.table_last_edit.setColumnCount(8)
        # self.table_last_edit.setSpan(0, 3, 1, 4)
        self.table_last_edit.setSpan(0, 5, 1, 3)
        table_lbl0 = QLabel('<i>Time</i>')
        table_lbl0.setAlignment(Qt.AlignHCenter)
        table_lbl1 = QLabel('<i>Staff Name</i>')
        table_lbl1.setAlignment(Qt.AlignHCenter)
        table_lbl2 = QLabel('<i>Dept.</i>')
        table_lbl2.setAlignment(Qt.AlignHCenter)
        table_lbl3 = QLabel('<i>Spouse</i>')
        table_lbl3.setAlignment(Qt.AlignHCenter)
        table_lbl4 = QLabel('<i>Child(ren)</i>')
        table_lbl4.setAlignment(Qt.AlignHCenter)
        table_lbl5 = QLabel('<i>New Amount</i>(<font color=\"#3d8ec9\">GH₵</font>) <i>added for</i>:')  # todo: get better name for this
        table_lbl5.setAlignment(Qt.AlignHCenter)
        table_lbl5.setWordWrap(True)

        # just using this to set column header resize
        self.table_last_edit.setHorizontalHeaderLabels(['Time', 'Staff Name', 'Department', 'Spouse Name', 'Children   ', 'New Amount for Month'])
        self.table_last_edit.setCellWidget(0, 0, table_lbl0)
        self.table_last_edit.setColumnWidth(0, 100)  # For time
        self.table_last_edit.setColumnWidth(5, 75)  # For Spanned amount columns
        self.table_last_edit.setColumnWidth(6, 100)  # For Spanned amount columns
        # self.table_last_edit.setColumnWidth(7, 90)  # For Spanned amount columns
        self.table_last_edit.setCellWidget(0, 1, table_lbl1)
        self.table_last_edit.setCellWidget(0, 2, table_lbl2)
        self.table_last_edit.setCellWidget(0, 3, table_lbl3)
        self.table_last_edit.setCellWidget(0, 4, table_lbl4)
        self.table_last_edit.setCellWidget(0, 5, table_lbl5)
        self.table_last_edit.setCellWidget(1, 4, QComboBox())
        self.table_last_edit.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_last_edit.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_last_edit.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table_last_edit.setRowHeight(0, 60)


        # END TABLE ----------------------------------------------------------------------------------------



    def UIlayouts(self):
        # TAB 1 LAYOUTS ------------------------------------------------------------------------------------
        self.tab1_main_layout = QVBoxLayout()
        self.tab1_quick_search_layout = QHBoxLayout()
        self.tab1_quick_search_layout.setContentsMargins(0, 0, 0, 6)
        self.tab1_month_layout = QHBoxLayout()

        self.tab1_entry_and_details_main_layout = QHBoxLayout()
        self.tab1_entry_and_details_main_layout.setContentsMargins(0, 10, 0, 10)
        self.entry_from_receipt_layout = QVBoxLayout()
        self.entry_from_receipt_layout.setContentsMargins(0, 0, 10, 0)
        self.entry_form = QFormLayout()
        self.entry_form.setVerticalSpacing(15)


        self.staff_details_layout = QVBoxLayout()
        self.staff_details_layout.setContentsMargins(10, 0, 0, 0)
        self.staff_form = QFormLayout()
        self.staff_form.setVerticalSpacing(8)
        self.lbl_cur_amount_layout = QHBoxLayout()
        # self.lbl_cur_amount_layout.setContentsMargins(20, 0, 0, 0)
        self.entry_cur_amount_layout = QHBoxLayout()
        self.entry_cur_amount_layout.setSpacing(15)
        self.entry_cur_amount_main_layout = QVBoxLayout()
        self.entry_cur_amount_main_layout.addLayout(self.lbl_cur_amount_layout)
        self.entry_cur_amount_main_layout.addLayout(self.entry_cur_amount_layout)



        # Adding Widgets to TAB 1 Layout -------------------------------------------------------------------
        self.tab1_quick_search_layout.addWidget(self.btn_undo)
        self.tab1_quick_search_layout.addWidget(self.btn_redo)
        self.tab1_quick_search_layout.addWidget(QLabel(' '), 1)
        self.tab1_quick_search_layout.addWidget(self.entry_quick_search)
        self.tab1_quick_search_layout.addWidget(self.btn_quick_search)
        self.tab1_quick_search_layout.addWidget(self.btn_clear)

        self.tab1_month_layout.addStretch()
        self.tab1_month_layout.addWidget(self.lbl_month)
        self.tab1_month_layout.addWidget(self.combo_months)
        self.tab1_month_layout.addStretch()

        self.tab1_entry_and_details_main_layout.addLayout(self.entry_from_receipt_layout, 48)
        self.tab1_entry_and_details_main_layout.addWidget(QVSeparationLine(), 4)
        self.tab1_entry_and_details_main_layout.addLayout(self.staff_details_layout, 48)

        self.entry_from_receipt_layout.addWidget(self.lbl_entry_from_receipt, 20)
        self.entry_from_receipt_layout.addLayout(self.entry_form, 80)
        self.entry_form.addRow(self.lbl_staff_or_dependant, self.entry_staff_or_dependant)
        self.entry_form.addRow(self.lbl_amount, self.entry_amount)
        self.entry_form.addRow('', self.btn_submit)

        self.staff_details_layout.addWidget(self.lbl_staff_details, 20)
        self.staff_details_layout.addLayout(self.staff_form, 80)
        self.staff_form.addRow(self.lbl_staff_name, self.entry_staff_name)
        self.staff_form.addRow(self.lbl_department, self.entry_department)
        self.staff_form.addRow(self.lbl_spouse, self.entry_spouse)
        self.staff_form.addRow(self.lbl_children, self.combo_children)

        self.lbl_cur_amount_layout.addWidget(self.lbl_staff_amt)
        self.lbl_cur_amount_layout.addWidget(self.lbl_spouse_amt)
        self.lbl_cur_amount_layout.addWidget(self.lbl_child_amt)
        self.entry_cur_amount_layout.addWidget(self.entry_cur_amount1)
        self.entry_cur_amount_layout.addWidget(self.entry_cur_amount2)
        self.entry_cur_amount_layout.addWidget(self.entry_cur_amount3)

        self.staff_form.addRow(self.lbl_cur_amount, self.entry_cur_amount_main_layout)

        self.tab1_main_layout.addLayout(self.tab1_quick_search_layout, 2)
        self.tab1_main_layout.addWidget(QHSeparationLine(), 1)
        self.tab1_main_layout.addLayout(self.tab1_month_layout, 5)
        self.tab1_main_layout.addWidget(QHSeparationLine(), 1)
        self.tab1_main_layout.addLayout(self.tab1_entry_and_details_main_layout, 50)
        self.tab1_main_layout.addWidget(QHSeparationLine(), 1)
        self.tab1_main_layout.addWidget(self.lbl_table_title, 5)
        self.tab1_main_layout.addWidget(self.table_last_edit, 35)
        self.tab_1.setLayout(self.tab1_main_layout)
        #   END TAB 1 LAYOUTS ------------------------------------------------------------------------------


        # MAIN WINDOW LAYOUT (CENTRAL WIDGET) --------------------------------------------------------------
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 10, 0, 0)
        self.central_layout.addWidget(self.lbl_title)
        self.central_layout.addWidget(self.tabs)
        self.setLayout(self.central_layout)
        # END MAIN WINDOW LAYOUT (CENTRAL WIDGET) ----------------------------------------------------------



    # ---------------------------------------- TODO --------------------------------------------------------
    # TODO:
    #   1. Set Tooltips [Optional]
