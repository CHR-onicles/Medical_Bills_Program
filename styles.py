def main_window_style():
    return """
    * {
        font-family: century gothic;
    }
    
    QLabel, QLineEdit, QLineEdit, QTabBar, QPushButton, QComboBox {
        font-size: 15pt;
    }
    
    QLabel#lbl_header {
        font: 32pt century gothic;
        color: rgb(0, 110, 161);
        background-color: rgb(147, 147, 147);
    }
    
    QLabel#lbl_titles {
        font: 75 20pt 'century gothic';
        color: rgb(255, 85, 255);
    }
    
    QComboBox#combo_titles {
        font-size: 18pt;
    }
    
    QPushButton#btn_quick_search_and_refresh {
        padding-top: 3px;
        padding-bottom: 3px;
        min-width: 4em;
    }
    
    QPushButton#btn_submit {
        padding-top: 7px;
        padding-bottom: 7px;
    }
    
    QLineEdit#entry_amount {
        /*color: #78879b; duller blue */
        color: #3d8ec9; /* brighter blue */
    }
    
    QLineEdit#entry_department {
        color: rgb(153, 80, 255); /* Dark purple*/
    }
    
    QMessageBox QLabel{
        font-size: 12pt;
    }
    
    QMessageBox QPushButton{
        font-size: 12pt; 
        min-width: 3em;
    }
    
    QTableWidget QLabel {
        font-size: 13pt;
        /* font: 75 12pt "century gothic"; # Doesn't work */
    }
    
    QTableWidget, QTableWidget QComboBox {
        font-size: 12pt;
        /*text-align: center; # doesnt work */
    }
    
    QPushButton#menu_button {
        border: none;
        padding-top: 8px;
        padding-bottom: 8px;
        padding-left: 7px;
        padding-right: 7px;
    }
    
    QPushButton#menu_button:hover {
        border: 2px solid #78879b;
        color: silver;
    }
    
    
/* QDarkStyle from here on ------------------------------------------------------------------------------------------ */
    
QProgressBar:horizontal {
    border: 1px solid #3A3939;
    text-align: center;
    padding: 1px;
    background: #201F1F;
}

QProgressBar::chunk:horizontal {
    background-color: qlineargradient(spread:reflect, x1:1, y1:0.545, x2:1, y2:0, stop:0 rgba(28, 66, 111, 255), stop:1 rgba(37, 87, 146, 255));
}

QToolTip
{   
    font: 9pt segoe UI;
    border: 1px solid #3A3939;
    /* background-color: rgb(90, 102, 117); original colour...not nice*/
    background-color: #444;
    color: white;
    padding: 3px;
    opacity: 200; /* the frick does this do? cuz I don't see anything*/
}

QWidget
{
    color: silver;
    background-color: #302F2F;
    selection-background-color:#3d8ec9;
    selection-color: black;
    background-clip: border;
    border-image: none;
    outline: 0;
}

QWidget:item:hover
{
    background-color: #78879b;
    color: black;
}

QWidget:item:selected
{
    background-color: #3d8ec9;
}

QCheckBox
{
    spacing: 5px;
    outline: none;
    color: #bbb;
    margin-bottom: 2px;
}

QCheckBox:disabled
{
    color: #777777;
}
QCheckBox::indicator,
QGroupBox::indicator
{
    width: 18px;
    height: 18px;
}
QGroupBox::indicator
{
    margin-left: 2px;
}

QCheckBox::indicator:unchecked,
QCheckBox::indicator:unchecked:hover,
QGroupBox::indicator:unchecked,
QGroupBox::indicator:unchecked:hover
{
    image: url(:/qss_icons/checkbox_unchecked.png);
}

QCheckBox::indicator:unchecked:focus,
QCheckBox::indicator:unchecked:pressed,
QGroupBox::indicator:unchecked:focus,
QGroupBox::indicator:unchecked:pressed
{
  border: none;
    image: url(:/qss_icons/checkbox_unchecked_focus.png);
}

QCheckBox::indicator:checked,
QCheckBox::indicator:checked:hover,
QGroupBox::indicator:checked,
QGroupBox::indicator:checked:hover
{
    image: url(:/qss_icons/checkbox_checked.png);
}

QCheckBox::indicator:checked:focus,
QCheckBox::indicator:checked:pressed,
QGroupBox::indicator:checked:focus,
QGroupBox::indicator:checked:pressed
{
  border: none;
    image: url(:/qss_icons/checkbox_checked_focus.png);
}

QCheckBox::indicator:indeterminate,
QCheckBox::indicator:indeterminate:hover,
QCheckBox::indicator:indeterminate:pressed
QGroupBox::indicator:indeterminate,
QGroupBox::indicator:indeterminate:hover,
QGroupBox::indicator:indeterminate:pressed
{
    image: url(:/qss_icons/checkbox_indeterminate.png);
}

QCheckBox::indicator:indeterminate:focus,
QGroupBox::indicator:indeterminate:focus
{
    image: url(:/qss_icons/checkbox_indeterminate_focus.png);
}

QCheckBox::indicator:checked:disabled,
QGroupBox::indicator:checked:disabled
{
    image: url(:/qss_icons/checkbox_checked_disabled.png);
}

QCheckBox::indicator:unchecked:disabled,
QGroupBox::indicator:unchecked:disabled
{
    image: url(:/qss_icons/checkbox_unchecked_disabled.png);
}

QRadioButton
{
    spacing: 5px;
    outline: none;
    color: #bbb;
    margin-bottom: 2px;
}

QRadioButton:disabled
{
    color: #777777;
}
QRadioButton::indicator
{
    width: 21px;
    height: 21px;
}

QRadioButton::indicator:unchecked,
QRadioButton::indicator:unchecked:hover
{
    image: url(:/qss_icons/radio_unchecked.png);
}

QRadioButton::indicator:unchecked:focus,
QRadioButton::indicator:unchecked:pressed
{
  border: none;
  outline: none;
    image: url(:/qss_icons/radio_unchecked_focus.png);
}

QRadioButton::indicator:checked,
QRadioButton::indicator:checked:hover
{
  border: none;
  outline: none;
    image: url(:/qss_icons/radio_checked.png);
}

QRadioButton::indicator:checked:focus,
QRadioButton::indicato::menu-arrowr:checked:pressed
{
  border: none;
  outline: none;
    image: url(:/qss_icons/radio_checked_focus.png);
}

QRadioButton::indicator:indeterminate,
QRadioButton::indicator:indeterminate:hover,
QRadioButton::indicator:indeterminate:pressed
{
        image: url(:/qss_icons/radio_indeterminate.png);
}

QRadioButton::indicator:checked:disabled
{
  outline: none;
  image: url(:/qss_icons/radio_checked_disabled.png);
}

QRadioButton::indicator:unchecked:disabled
{
    image: url(:/qss_icons/radio_unchecked_disabled.png);
}


QMenuBar
{
    background-color: #302F2F;
    color: silver;
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 1px solid #3A3939;
}

QMenuBar::item:pressed
{
    border: 1px solid #3A3939;
    background-color: #3d8ec9;
    color: black;
    margin-bottom:-1px;
    padding-bottom:1px;
}

QMenu
{
    border: 1px solid #3A3939;
    color: silver;
    margin: 1px;
}

QMenu::icon
{
    margin: 1px;
}

QMenu::item
{
    padding: 2px 2px 2px 25px;
    margin-left: 5px;
    border: 1px solid transparent; /* reserve space for selection border */
}

QMenu::item:selected
{
    color: black;
}

QMenu::separator {
    height: 2px;
    background: lightblue;
    margin-left: 10px;
    margin-right: 5px;
}

QMenu::indicator {
    width: 16px;
    height: 16px;
}

/* non-exclusive indicator = check box style indicator
   (see QActionGroup::setExclusive) */
QMenu::indicator:non-exclusive:unchecked {
    image: url(:/qss_icons/checkbox_unchecked.png);
}

QMenu::indicator:non-exclusive:unchecked:selected {
    image: url(:/qss_icons/checkbox_unchecked_disabled.png);
}

QMenu::indicator:non-exclusive:checked {
    image: url(:/qss_icons/checkbox_checked.png);
}

QMenu::indicator:non-exclusive:checked:selected {
    image: url(:/qss_icons/checkbox_checked_disabled.png);
}

/* exclusive indicator = radio button style indicator (see QActionGroup::setExclusive) */
QMenu::indicator:exclusive:unchecked {
    image: url(:/qss_icons/radio_unchecked.png);
}

QMenu::indicator:exclusive:unchecked:selected {
    image: url(:/qss_icons/radio_unchecked_disabled.png);
}

QMenu::indicator:exclusive:checked {
    image: url(:/qss_icons/radio_checked.png);
}

QMenu::indicator:exclusive:checked:selected {
    image: url(:/qss_icons/radio_checked_disabled.png);
}

QMenu::right-arrow {
    margin: 5px;
    image: url(:/qss_icons/right_arrow.png)
}


QWidget:disabled
{
    color: #808080;
    background-color: #302F2F;
}

QAbstractItemView
{
    alternate-background-color: #3A3939;
    color: silver;
    border: 1px solid 3A3939;
    border-radius: 2px;
    padding: 1px;
}

QWidget:focus, QMenuBar:focus
{
    border: 1px solid #78879b;
}

QTabWidget:focus, QCheckBox:focus, QRadioButton:focus, QSlider:focus
{
    border: none;
}

QLineEdit
{
    background-color: #201F1F;
    padding: 2px;
    border-style: solid;
    border: 1px solid #3A3939;
    border-radius: 2px;
    color: silver;
}

QGroupBox {
    border:1px solid #3A3939;
    border-radius: 2px;
    margin-top: 20px;
    background-color: #302F2F;
    color: silver;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 10px;
}

QAbstractScrollArea
{
    border-radius: 2px;
    border: 1px solid #3A3939;
    background-color: transparent;
}

QScrollBar:horizontal
{
    height: 15px;
    margin: 3px 15px 3px 15px;
    border: 1px transparent #2A2929;
    border-radius: 4px;
    background-color: #2A2929;
}

QScrollBar::handle:horizontal
{
    background-color: #605F5F;
    min-width: 5px;
    border-radius: 4px;
}

QScrollBar::add-line:horizontal
{
    margin: 0px 3px 0px 3px;
    border-image: url(:/qss_icons/right_arrow_disabled.png);
    width: 10px;
    height: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal
{
    margin: 0px 3px 0px 3px;
    border-image: url(:/qss_icons/left_arrow_disabled.png);
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::add-line:horizontal:hover,QScrollBar::add-line:horizontal:on
{
    border-image: url(:/qss_icons/right_arrow.png);
    height: 10px;
    width: 10px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}


QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on
{
    border-image: url(:/qss_icons/left_arrow.png);
    height: 10px;
    width: 10px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
{
    background: none;
}


QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{
    background: none;
}

QScrollBar:vertical
{
    background-color: #2A2929;
    width: 15px;
    margin: 15px 3px 15px 3px;
    border: 1px transparent #2A2929;
    border-radius: 4px;
}

QScrollBar::handle:vertical
{
    background-color: #605F5F;
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

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
{
    background: none;
}


QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
{
    background: none;
}

QTextEdit
{
    background-color: #201F1F;
    color: silver;
    border: 1px solid #3A3939;
}

QPlainTextEdit
{
    background-color: #201F1F;;
    color: silver;
    border-radius: 2px;
    border: 1px solid #3A3939;
}

QHeaderView::section
{
    background-color: #3A3939;
    color: silver;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
}

QSizeGrip {
    image: url(:/qss_icons/sizegrip.png);
    width: 12px;
    height: 12px;
}

QMainWindow
{
    background-color: #302F2F;

}

QMainWindow::separator
{
    background-color: #302F2F;
    color: white;
    padding-left: 4px;
    spacing: 2px;
    border: 1px dashed #3A3939;
}

QMainWindow::separator:hover
{

    background-color: #787876;
    color: white;
    padding-left: 4px;
    border: 1px solid #3A3939;
    spacing: 2px;
}


QMenu::separator
{
    height: 1px;
    background-color: #3A3939;
    color: white;
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}


QFrame
{
    border-radius: 2px;
    border: 1px solid #444;
}

QFrame[frameShape="0"]
{
    border-radius: 2px;
    border: 1px transparent #444;
}

QStackedWidget
{
    background-color: #302F2F;
    border: 1px transparent black;
}

QToolBar {
    border: 1px transparent #393838;
    background: 1px solid #302F2F;
    font-weight: bold;
}

QToolBar::handle:horizontal {
    image: url(:/qss_icons/Hmovetoolbar.png);
}
QToolBar::handle:vertical {
    image: url(:/qss_icons/Vmovetoolbar.png);
}
QToolBar::separator:horizontal {
    image: url(:/qss_icons/Hsepartoolbar.png);
}
QToolBar::separator:vertical {
    image: url(:/qss_icons/Vsepartoolbars.png);
}

QPushButton
{
    color: silver;
    background-color: #302F2F;
    border-width: 2px;
    border-color: #4A4949;
    border-style: solid;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 4px;
    /* outline: none; */
    /* min-width: 40px; */
}

QPushButton:disabled
{
    background-color: #302F2F;
    border-width: 2px;
    border-color: #3A3939;
    border-style: solid;
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 10px;
    padding-right: 10px;
    /*border-radius: 2px;*/
    color: #808080;
}

QPushButton:focus {
    background-color: #3d8ec9;
    color: white;
}

QComboBox
{
    selection-background-color: #3d8ec9;
    background-color: #201F1F;
    border-style: solid;
    border: 1px solid #3A3939;
    border-radius: 2px;
    padding: 2px;
    min-width: 75px;
}

QPushButton:checked{
    background-color: #4A4949;
    border-color: #6A6969;
}

QPushButton:hover {
    border: 2px solid #78879b;
    color: silver;
}

QComboBox:hover, QAbstractSpinBox:hover,QLineEdit:hover,QTextEdit:hover,QPlainTextEdit:hover,QAbstractView:hover,QTreeView:hover
{
    border: 1px solid #78879b;
    color: silver;
}

QComboBox:on
{
    background-color: #626873;
    padding-top: 3px;
    padding-left: 4px;
    selection-background-color: #4a4a4a;
}

QComboBox QAbstractItemView
{
    background-color: #201F1F;
    border-radius: 2px;
    border: 1px solid #444;
    selection-background-color: #3d8ec9;
    color: silver;
}

QComboBox::drop-down
{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 0px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow
{
    image: url(:/qss_icons/down_arrow_disabled);
}

QComboBox::down-arrow:on, QComboBox::down-arrow:hover,
QComboBox::down-arrow:focus
{
    image: url(:/qss_icons/down_arrow);
}

QPushButton:pressed
{
    background-color: #484846;
}

QAbstractSpinBox {
    padding-top: 2px;
    padding-bottom: 2px;
    border: 1px solid #3A3939;
    background-color: #201F1F;
    color: silver;
    border-radius: 2px;
    min-width: 75px;
}

QAbstractSpinBox:up-button
{
    background-color: transparent;
    subcontrol-origin: border;
    subcontrol-position: top right;
}

QAbstractSpinBox:down-button
{
    background-color: transparent;
    subcontrol-origin: border;
    subcontrol-position: bottom right;
}

QAbstractSpinBox::up-arrow,QAbstractSpinBox::up-arrow:disabled,QAbstractSpinBox::up-arrow:off {
    image: url(:/qss_icons/up_arrow_disabled.png);
    width: 10px;
    height: 10px;
}
QAbstractSpinBox::up-arrow:hover
{
    image: url(:/qss_icons/up_arrow.png);
}


QAbstractSpinBox::down-arrow,QAbstractSpinBox::down-arrow:disabled,QAbstractSpinBox::down-arrow:off
{
    image: url(:/qss_icons/down_arrow_disabled);
    width: 10px;
    height: 10px;
}
QAbstractSpinBox::down-arrow:hover
{
    image: url(:/qss_icons/down_arrow);
}


QLabel
{
    border: 0px solid black;
}

QTabWidget{
    border: 1px transparent black;
}

QTabWidget::pane {
    border: 1px solid #444;
    border-radius: 3px;
    padding: 3px;
}

QTabBar
{
    qproperty-drawBase: 0;
    left: 5px; /* move to the right by 5px */
}

QTabBar:focus
{
    border: 0px transparent black;
}

QTabBar::close-button  {
    image: url(:/qss_icons/close.png);
    background: transparent;
}

QTabBar::close-button:hover
{
    image: url(:/qss_icons/close-hover.png);
    background: transparent;
}

QTabBar::close-button:pressed {
    image: url(:/qss_icons/close-pressed.png);
    background: transparent;
}

/* TOP TABS */
QTabBar::tab:top {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-bottom: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;
}

QTabBar::tab:top:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-bottom: 1px transparent #4A4949;
    border-top-left-radius: 0px;
    border-top-right-radius: 0px;
}

QTabBar::tab:top:!selected:hover {
    background-color: #48576b;
}

/* BOTTOM TABS */
QTabBar::tab:bottom {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-top: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-bottom-left-radius: 2px;
    border-bottom-right-radius: 2px;
}

QTabBar::tab:bottom:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-top: 1px transparent #4A4949;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}

QTabBar::tab:bottom:!selected:hover {
    background-color: #78879b;
}

/* LEFT TABS */
QTabBar::tab:left {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-left: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-top-right-radius: 2px;
    border-bottom-right-radius: 2px;
}

QTabBar::tab:left:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-right: 1px transparent #4A4949;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
}

QTabBar::tab:left:!selected:hover {
    background-color: #48576b;
}


/* RIGHT TABS */
QTabBar::tab:right {
    color: #b1b1b1;
    border: 1px solid #4A4949;
    border-right: 1px transparent black;
    background-color: #302F2F;
    padding: 5px;
    border-top-left-radius: 2px;
    border-bottom-left-radius: 2px;
}

QTabBar::tab:right:!selected
{
    color: #b1b1b1;
    background-color: #201F1F;
    border: 1px transparent #4A4949;
    border-right: 1px transparent #4A4949;
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
}

QTabBar::tab:right:!selected:hover {
    background-color: #48576b;
}

QTabBar QToolButton::right-arrow:enabled {
     image: url(:/qss_icons/right_arrow.png);
 }

 QTabBar QToolButton::left-arrow:enabled {
     image: url(:/qss_icons/left_arrow.png);
 }

QTabBar QToolButton::right-arrow:disabled {
     image: url(:/qss_icons/right_arrow_disabled.png);
 }

 QTabBar QToolButton::left-arrow:disabled {
     image: url(:/qss_icons/left_arrow_disabled.png);
 }


QDockWidget {
    border: 1px solid #403F3F;
    titlebar-close-icon: url(:/qss_icons/close.png);
    titlebar-normal-icon: url(:/qss_icons/undock.png);
}

QDockWidget::close-button, QDockWidget::float-button {
    border: 1px solid transparent;
    border-radius: 2px;
    background: transparent;
}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background: rgba(255, 255, 255, 10);
}

QDockWidget::close-button:pressed, QDockWidget::float-button:pressed {
    padding: 1px -1px -1px 1px;
    background: rgba(255, 255, 255, 10);
}

QTreeView, QListView, QTextBrowser, AtLineEdit, AtLineEdit::hover {
    border: 1px solid #444;
    background-color: silver;
    border-radius: 3px;
    margin-left: 3px;
    color: black;
}

QTreeView:branch:selected, QTreeView:branch:hover {
    background: url(:/qss_icons/transparent.png);
}

QTreeView::branch:has-siblings:!adjoins-item {
    border-image: url(:/qss_icons/transparent.png);
}

QTreeView::branch:has-siblings:adjoins-item {
    border-image: url(:/qss_icons/transparent.png);
}

QTreeView::branch:!has-children:!has-siblings:adjoins-item {
    border-image: url(:/qss_icons/transparent.png);
}

QTreeView::branch:has-children:!has-siblings:closed,
QTreeView::branch:closed:has-children:has-siblings {
    image: url(:/qss_icons/branch_closed.png);
}

QTreeView::branch:open:has-children:!has-siblings,
QTreeView::branch:open:has-children:has-siblings  {
    image: url(:/qss_icons/branch_open.png);
}

QTreeView::branch:has-children:!has-siblings:closed:hover,
QTreeView::branch:closed:has-children:has-siblings:hover {
    image: url(:/qss_icons/branch_closed-on.png);
    }

QTreeView::branch:open:has-children:!has-siblings:hover,
QTreeView::branch:open:has-children:has-siblings:hover  {
    image: url(:/qss_icons/branch_open-on.png);
    }

QListView::item:!selected:hover, QListView::item:!selected:hover, QTreeView::item:!selected:hover  {
    background: rgba(0, 0, 0, 0);
    outline: 0;
    color: #FFFFFF
}

QListView::item:selected:hover, QListView::item:selected:hover, QTreeView::item:selected:hover  {
    background: #3d8ec9;
    color: #FFFFFF;
}

QSlider::groove:horizontal {
    border: 1px solid #3A3939;
    height: 8px;
    background: #201F1F;
    margin: 2px 0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
      stop: 0.0 silver, stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: -4px 0;
    border-radius: 2px;
}

QSlider::groove:vertical {
    border: 1px solid #3A3939;
    width: 8px;
    background: #201F1F;
    margin: 0 0px;
    border-radius: 2px;
}

QSlider::handle:vertical {
    background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 silver,
    stop: 0.2 #a8a8a8, stop: 1 #727272);
    border: 1px solid #3A3939;
    width: 14px;
    height: 14px;
    margin: 0 -4px;
    border-radius: 2px;
}

QToolButton {
    /*  background-color: transparent; */
    border: 2px transparent #4A4949;
    border-radius: 4px;
    background-color: dimgray;
    margin: 2px;
    padding: 2px;
}

QToolButton[popupMode="1"] { /* only for MenuButtonPopup */
 padding-right: 20px; /* make way for the popup button */
 border: 2px transparent #4A4949;
 border-radius: 4px;
}

QToolButton[popupMode="2"] { /* only for InstantPopup */
 padding-right: 10px; /* make way for the popup button */
 border: 2px transparent #4A4949;
}


QToolButton:hover, QToolButton::menu-button:hover {
    border: 2px solid #78879b;
}

QToolButton:checked, QToolButton:pressed,
    QToolButton::menu-button:pressed {
    background-color: #4A4949;
    border: 2px solid #78879b;
}

/* the subcontrol below is used only in the InstantPopup or DelayedPopup mode */
QToolButton::menu-indicator {
    image: url(:/qss_icons/down_arrow);
    top: -7px; left: -2px; /* shift it a bit */
}

/* the subcontrols below are used only in the MenuButtonPopup mode */
QToolButton::menu-button {
    border: 1px transparent #4A4949;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    /* 16px width + 4px for border = 20px allocated above */
    width: 16px;
    outline: none;
}

QToolButton::menu-arrow {
    image: url(:/qss_icons/down_arrow);
}

QToolButton::menu-arrow:open {
    top: 1px; left: 1px; /* shift it a bit */
    border: 1px solid #3A3939;
}

QPushButton::menu-indicator  {
    subcontrol-origin: padding;
    subcontrol-position: bottom right;
    left: 4px;
}

QTableView
{
    border: 1px solid #444;
    gridline-color: #6c6c6c;
    background-color: #201F1F;
}


QTableView, QHeaderView
{
    border-radius: 0px;
}

QTableView::item:pressed, QListView::item:pressed, QTreeView::item:pressed  {
    background: #78879b;
    color: #FFFFFF;
}

QTableView::item:selected:active, QTreeView::item:selected:active, QListView::item:selected:active  {
    background: #3d8ec9;
    color: #FFFFFF;
}


QHeaderView
{
    border: 1px transparent;
    border-radius: 2px;
    margin: 0px;
    padding: 0px;
}

QHeaderView::section  {
    background-color: #3A3939;
    color: silver;
    padding: 4px;
    border: 1px solid #6c6c6c;
    border-radius: 0px;
    text-align: center;
}

QHeaderView::section::vertical::first, QHeaderView::section::vertical::only-one
{
    border-top: 1px solid #6c6c6c;
}

QHeaderView::section::vertical
{
    border-top: transparent;
}

QHeaderView::section::horizontal::first, QHeaderView::section::horizontal::only-one
{
    border-left: 1px solid #6c6c6c;
}

QHeaderView::section::horizontal
{
    border-left: transparent;
}


QHeaderView::section:checked
 {
    color: white;
    background-color: #5A5959;
 }

 /* style the sort indicator */
QHeaderView::down-arrow {
    image: url(:/qss_icons/down_arrow);
}

QHeaderView::up-arrow {
    image: url(:/qss_icons/up_arrow.png);
}


QTableCornerButton::section {
    background-color: #3A3939;
    border: 1px solid #3A3939;
    border-radius: 2px;
}

QToolBox  {
    padding: 3px;
    border: 1px transparent black;
}

QToolBox::tab {
    color: #b1b1b1;
    background-color: #302F2F;
    border: 1px solid #4A4949;
    border-bottom: 1px transparent #302F2F;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

 QToolBox::tab:selected { /* italicize selected tabs */
    font: italic;
    background-color: #302F2F;
    border-color: #3d8ec9;
 }

QStatusBar::item {
    /*border: 1px solid #3A3939; # commented this out to remove border from invisible label*/
    border-radius: 2px;
 }


QFrame[height="3"], QFrame[width="3"] {
    background-color: #AAA;
}


QSplitter::handle {
    border: 1px dashed #3A3939;
}

QSplitter::handle:hover {
    background-color: #787876;
    border: 1px solid #3A3939;
}

QSplitter::handle:horizontal {
    width: 1px;
}

QSplitter::handle:vertical {
    height: 1px;
}

QListWidget {
    background-color: silver;
    border-radius: 5px;
    margin-left: 5px;
}

QListWidget::item {
    color: black;
}

ColorButton::enabled {
    border-radius: 0px;
    border: 1px solid #444444;
}

ColorButton::disabled {
    border-radius: 0px;
    border: 1px solid #AAAAAA;
}
    """
