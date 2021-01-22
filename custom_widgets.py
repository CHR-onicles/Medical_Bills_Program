# ------------------------------------------------------------------------------
#
# AUTHOR: CHR-onicles (GitHub)
# PROJECT MADE WITH: PyQt5
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ------------------------------------------------------------------------------

from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QFrame, QSizePolicy, QWidget




class QHSeparationLine(QFrame):
    """
      Custom Class to create a horizontal separation line.
    """
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(1)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        return


class QVSeparationLine(QFrame):
    """
    Custom Class to create a vertical separation line.
    """
    def __init__(self):
        super().__init__()
        self.setFixedWidth(1)
        self.setMinimumHeight(1)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        return


class CurrencyInputValidator(QValidator):
    """
    Custom class to validate currency input in line edits
    """

    def validate(self, v_string: str, index: int):

        if len(v_string) < 4 or v_string[:4] != 'GH₵ ':
            state = QValidator.Invalid

        if len(v_string) >= 4:
            state = QValidator.Intermediate

        for x in v_string:
            if x.isalpha():
                state = QValidator.Invalid
                break

        if '.' in v_string:
            nums = v_string.split('.')
            if (nums[0].isdigit() and nums[1].isdigit()) is True:
                state = QValidator.Acceptable

        if v_string[4:].isdigit():
            state = QValidator.Acceptable


        return state, v_string, index


