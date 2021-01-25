from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import (QPixmap, QIcon)
from PyQt5.QtWidgets import (QPushButton, QLabel, QTabWidget, QComboBox, QWidget, QSizePolicy, QApplication,
                             QLineEdit, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox)
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


        # TABS ---------------------------------------------------------------------------------------------
        self.tabs = QTabWidget()
        self.tab_1 = QWidget()
        self.tab_2 = QWidget()  # todo: Implement statistics or staff list here
        # self.tab_3 = QWidget()  # todo: Implement Later (for Graphs maybe)
        self.tabs.addTab(self.tab_1, 'Receipt Entry')  # may change later
        self.tabs.addTab(self.tab_2, 'Tab 2')
        # self.tabs.addTab(self.tab_3, 'Tab 3')

        # TAB 1 WIDGETS ------------------------------------------------------------------------------------
        self.lbl_month = QLabel('Month:')
        self.lbl_month.setObjectName('lbl_titles')
        self.combo_months = QComboBox()
        self.combo_months.setObjectName('combo_titles')

        self.lbl_quick_search = QLabel('Quick Search For Dependant or Staff:')
        self.entry_quick_search = QLineEdit()
        self.btn_quick_search = QPushButton('Search')
        self.btn_quick_search.setObjectName('btn_quick_search_and_refresh')

        # Entry from Receipt Widgets -----------------------------------------------------------------------
        self.lbl_entry_from_receipt = QLabel('<u>Entry From Receipt</u>')
        self.lbl_entry_from_receipt.setAlignment(Qt.AlignHCenter)
        self.lbl_entry_from_receipt.setObjectName('lbl_titles')

        self.lbl_staff_or_dependant = QLabel('Staff/Dependant Name:')
        self.entry_staff_or_dependant = QLineEdit()
        # self.entry_staff_or_dependant.setValidator(NameInputValidator())
        self.lbl_amount = QLabel('Amount:')
        self.entry_amount = QLineEdit('GH₵ ')
        self.entry_amount.setValidator(CurrencyInputValidator())
        self.entry_amount.setObjectName('entry_amount')
        self.btn_submit = QPushButton('Submit')
        self.btn_submit.setObjectName('btn_submit')

        self.vline = QVSeparationLine()
        self.vline.setStyleSheet('border: 1px solid gray;')

        self.hline = QHSeparationLine()
        self.hline.setStyleSheet('border: 1px solid gray;')


        # Staff Details widgets ----------------------------------------------------------------------------
        self.lbl_staff_details = QLabel('<u>Staff Details</u>')
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
        self.lbl_cur_amount = QLabel('Current Amount\nFor Month:')
        self.lbl_cur_amount.setWordWrap(True)
        self.entry_cur_amount = QLineEdit('GH₵ ')
        self.entry_cur_amount.setReadOnly(True)
        self.entry_cur_amount.setObjectName('entry_amount')



    def UIlayouts(self):
        # MAIN WINDOW LAYOUT (CENTRAL WIDGET) --------------------------------------------------------------
        self.central_layout = QVBoxLayout()

        # TAB 1 LAYOUTS ------------------------------------------------------------------------------------
        self.tab1_main_layout = QVBoxLayout()
        self.tab1_quick_search_layout = QHBoxLayout()
        self.tab1_month_layout = QHBoxLayout()

        self.tab1_entry_and_details_main_layout = QHBoxLayout()
        self.tab1_entry_and_details_main_layout.setContentsMargins(0, 50, 0, 0)
        self.entry_from_receipt_layout = QVBoxLayout()
        self.entry_form = QFormLayout()

        self.staff_details_layout = QVBoxLayout()
        self.staff_form = QFormLayout()


        # Adding Widgets to TAB 1 Layout -------------------------------------------------------------------
        self.tab1_quick_search_layout.addWidget(self.lbl_quick_search)
        self.tab1_quick_search_layout.addWidget(self.entry_quick_search)
        self.tab1_quick_search_layout.addWidget(self.btn_quick_search)

        self.tab1_month_layout.addStretch()
        self.tab1_month_layout.addWidget(self.lbl_month)
        self.tab1_month_layout.addWidget(self.combo_months)
        self.tab1_month_layout.addStretch()

        self.tab1_entry_and_details_main_layout.addLayout(self.entry_from_receipt_layout, 48)
        self.tab1_entry_and_details_main_layout.addWidget(self.vline, 4)
        self.tab1_entry_and_details_main_layout.addLayout(self.staff_details_layout, 48)

        self.entry_from_receipt_layout.addWidget(self.lbl_entry_from_receipt, 20)
        self.entry_from_receipt_layout.addLayout(self.entry_form, 80)
        self.entry_form.addRow(self.lbl_staff_or_dependant, self.entry_staff_or_dependant)
        self.entry_form.addRow(self.lbl_amount, self.entry_amount)
        self.entry_form.addRow('', self.btn_submit)
        self.entry_form.setVerticalSpacing(25)

        self.staff_details_layout.addWidget(self.lbl_staff_details, 20)
        self.staff_details_layout.addLayout(self.staff_form, 80)
        self.staff_form.addRow(self.lbl_staff_name, self.entry_staff_name)
        self.staff_form.addRow(self.lbl_department, self.entry_department)
        self.staff_form.addRow(self.lbl_spouse, self.entry_spouse)
        self.staff_form.addRow(self.lbl_children, self.combo_children)
        self.staff_form.addRow(self.lbl_cur_amount, self.entry_cur_amount)
        self.staff_form.setVerticalSpacing(25)

        self.tab1_main_layout.addLayout(self.tab1_quick_search_layout, 18)
        self.tab1_main_layout.addLayout(self.tab1_month_layout, 18)
        self.tab1_main_layout.addWidget(self.hline, 4)
        self.tab1_main_layout.addLayout(self.tab1_entry_and_details_main_layout, 60)
        self.tab_1.setLayout(self.tab1_main_layout)

        self.central_layout.setContentsMargins(0, 10, 0, 0)
        self.central_layout.addWidget(self.lbl_title)
        self.central_layout.addWidget(self.tabs)
        self.setLayout(self.central_layout)


    # ---------------------------------------- TODO --------------------------------------------------------
    # TODO:
    #   1. Set Tooltips [Optional]
    #   2. Set entry_staff_or_dependant to have launch focus [Optional]
