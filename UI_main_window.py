from PyQt5.QtCore import (QSize, Qt, QTimer, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QFont, QPixmap, QIcon)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTabWidget, QComboBox, QCompleter,
                             QLineEdit, QStyle, QGridLayout, QVBoxLayout, QFormLayout, QHBoxLayout, QFrame, QGroupBox,
                             QWidget, QSizePolicy)
import sys

# Local imports
import resources_rc, styles
from custom_widgets import QHSeparationLine, QVSeparationLine




class UIMainWindow(QMainWindow):

    def __init__(self):
        super(UIMainWindow, self).__init__()
        self.setWindowTitle('Med Bills App')
        self.setWindowIcon(QIcon(':/icon/cat'))
        self.resize(1200, 700)
        self.setStyleSheet(styles.main_window_style())


        self.UIComponents()

    def UIComponents(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        self.central_widget = QWidget()

        # BIG TITLE ----------------------------------------------------------------------------------------
        self.lbl_title = QLabel('MEDICAL BILLS 2021')
        # self.lbl_title = QLabel('Medical Bills 2021')
        self.lbl_title.setObjectName('lbl_title')
        self.lbl_title.setAlignment(Qt.AlignHCenter)

        # STATUS BAR ---------------------------------------------------------------------------------------
        self.statusBar().showMessage('Welcome, this is the status bar...')
        self.btn_refresh = QPushButton('Refresh')
        self.statusBar().addPermanentWidget(self.btn_refresh)

        # TABS ---------------------------------------------------------------------------------------------
        self.tabs = QTabWidget()
        self.tab_1 = QWidget()
        # self.tab_1.setStyleSheet(styles.tab1_style())
        self.tab_2 = QWidget()
        self.tab_3 = QWidget()
        self.tabs.addTab(self.tab_1, 'Receipt Entry')  # may change later
        self.tabs.addTab(self.tab_2, 'Tab 2')
        self.tabs.addTab(self.tab_3, 'Tab 3')

        # TAB 1 WIDGETS ------------------------------------------------------------------------------------
        self.lbl_month = QLabel('Month')
        self.combo_months = QComboBox()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                  'October', 'November', 'December']
        self.combo_months.addItems(months)

        self.lbl_quick_search = QLabel('Quick Search For Dependant or Staff:')
        self.entry_quick_search = QLineEdit()
        self.btn_quick_search = QPushButton('Search')

        # Entry from Receipt Widgets -----------------------------------------------------------------------
        self.lbl_entry_from_receipt = QLabel('Entry From Receipt')
        self.lbl_entry_from_receipt.setAlignment(Qt.AlignHCenter)
        self.lbl_staff_dependant = QLabel('Staff/Dependant Name:')
        self.entry_staff_dependant = QLineEdit()
        self.lbl_amount = QLabel('Amount:')
        self.entry_amount = QLineEdit()
        self.btn_submit = QPushButton('Submit')

        self.vline = QVSeparationLine()
        # self.vline.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # todo: make sure its ok
        self.vline.setStyleSheet('border: 1px solid gray;')

        # Staff Details widgets ----------------------------------------------------------------------------
        self.lbl_staff_details = QLabel('Staff Details')
        self.lbl_staff_details.setAlignment(Qt.AlignHCenter)
        self.lbl_staff_name = QLabel('Staff Name:')
        self.entry_staff_name = QLineEdit()  # todo: make them all read-only
        self.lbl_department = QLabel('Department:')
        self.entry_department = QLineEdit()
        self.lbl_spouse = QLabel('Spouse:')
        self.entry_spouse = QLineEdit()
        self.lbl_children = QLabel('Child(ren):')
        self.entry_children = QComboBox()
        self.lbl_cur_amount = QLabel('Current Amount For Month:')
        self.lbl_cur_amount.setWordWrap(True)
        self.entry_cur_amount = QLineEdit()



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

        self.tab1_entry_and_details_main_layout = QHBoxLayout()
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
        self.entry_form.addRow(self.lbl_staff_dependant, self.entry_staff_dependant)
        self.entry_form.addRow(self.lbl_amount, self.entry_amount)
        self.entry_form.addRow('', self.btn_submit)

        self.staff_details_layout.addWidget(self.lbl_staff_details, 20)
        self.staff_details_layout.addLayout(self.staff_form, 80)
        self.staff_form.addRow(self.lbl_staff_name, self.entry_staff_name)
        self.staff_form.addRow(self.lbl_department, self.entry_department)
        self.staff_form.addRow(self.lbl_spouse, self.entry_spouse)
        self.staff_form.addRow(self.lbl_children, self.entry_children)
        self.staff_form.addRow(self.lbl_cur_amount, self.entry_cur_amount)

        self.tab1_main_layout.addLayout(self.tab1_quick_search_layout, 20)
        self.tab1_main_layout.addLayout(self.tab1_month_layout, 20)
        self.tab1_main_layout.addLayout(self.tab1_entry_and_details_main_layout, 60)
        self.tab_1.setLayout(self.tab1_main_layout)















if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UIMainWindow()
    window.show()
    sys.exit(app.exec_())


    # ---------------------------------------- TODO --------------------------------------------------------
    # TODO:
    #   1. Set Tooltips
