"""
Author = CHR-onicles
Date: 20/01/21
"""

from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QFrame, QSizePolicy, QWidget
from icecream import ic




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
    Custom validator class to validate currency input in line edits.
    """

    def validate(self, v_string: str, index: int):
        ic.disable()
        # invalid_chars = """
        # `~!@#$%^&*()-_=+{[}]|\\'",<>/?
        # """  # Might need them in future
        state = None
        if len(v_string) < 4 or v_string[:4] != 'GH₵ ':
            ic('Less than 4 or not GHC - invalid')
            state = QValidator.Invalid

        if len(v_string) >= 4:
            ic('Greater than 4 - VALID')
            state = QValidator.Intermediate

        if (v_string[4:].isdigit()) is True:
            ic('All digits - VALID')
            state = QValidator.Acceptable

        for x in v_string[4:]:
            if ((x.isdigit() is False) and '.' not in v_string[4:]) or x.isalpha():
                ic('Alpha or Anything else - invalid')
                state = QValidator.Invalid

        nums = v_string[4:].split('.')
        if '.' in v_string[4:]:
            if (nums[0].isdigit() and nums[1].isdigit()) is True:
                ic('Has period and both numbers are legit - VALID')
                state = QValidator.Acceptable
            if '.' in v_string[4:] and len(v_string.split('.')[1]) >= 1:
                if (nums[0].isdigit() is True) and (nums[1].isdigit() is False):
                    ic('Has period, but other chars too - invalid')
                    state = QValidator.Invalid
            if len(nums[1]) > 2:
                ic('More than 2 digits after period - invalid')
                state = QValidator.Invalid

        if v_string.count('.') > 1:
            ic('More than one period - invalid')
            state = QValidator.Invalid

        return state, v_string, index


# class NameInputValidator(QValidator):
#     """
#     Custom validator class to validate entries of names
#     """
#
#     def validate(self, v_string, index):
#         state = None
#
#         for x in v_string:
#             if x.isdigit():
#                 state = QValidator.Invalid
#
#         if '.' or '-' in v_string:
#             state = QValidator.Intermediate
#
#         if v_string.isalpha():
#             state = QValidator.Acceptable
#
#         return state, v_string, index
     # don't think I need a validator for names
