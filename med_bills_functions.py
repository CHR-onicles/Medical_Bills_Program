import os
import openpyxl
from openpyxl.styles import colors, PatternFill




class MBillsFunctions:
    """
    Class which contains operations to be carried out on medical bills files.
    """

    @staticmethod
    def initializeFiles(med_bill_file, staff_list_file=None):
        """
        Loads med bills file and staff list file.

        :param med_bill_file: Medical Bills File
        :param staff_list_file: Staff List File
        :return: Both workbooks
        """
        workbook1 = openpyxl.load_workbook(med_bill_file)
        workbook2 = openpyxl.load_workbook(staff_list_file, read_only=True)
        return workbook1, workbook2


    @staticmethod
    def getAllMedBillsNames(workbook):
        """
        Function to get all names from Med Bills File

        :param workbook: Medical Bills workbook
        :return: list of all people in the medical bills workbook
        """
        people = []

        for sheet in workbook.sheetnames:
            for col in workbook[sheet].iter_cols(min_row=1, max_row=700, min_col=1, max_col=1):
                for cell in col:
                    # check for gray color, bold font, and whether cell is filled (not containing '0')
                    if cell.fill.start_color.index == 'FFD8D8D8' and cell.font.b is True \
                            and cell.value != 0:
                        people.append(cell.value.title())  # + ' | ' + workbook[sheet].title)

        # Debugging stuff ---------------------------------------------
        # print(f'Number of all people in Med Bills: {len(people)}\n')
        # staff.sort()
        # for c, sf in enumerate(people):
        #     print(c + 1, sf)
        # s = set(people)
        # len(s)
        # End Debugging -----------------------------------------------

        return people


    @staticmethod
    def getAllDependantNames(workbook):
        """
        Function to extract all spouse, and children's names from Staff List File.

        :param workbook:Staff List Workbook
        :return: list of all dependants from Staff list workbook
        """

        d_names = []

        for sheet in workbook.sheetnames:
            for row in workbook[sheet].iter_rows(min_row=3, max_row=700, min_col=3, max_col=4):
                for cell in row:
                    if cell.value is not None and cell.value.isupper() is True:  # check for upper case letters and not empty cell
                        d_names.append(cell.value.title())

        # For Debugging ---------------------------------------------
        # print(f'There are {len(d_names)} dependants for staff.\n')
        # for i in d_names:
        #     print(i)
        # End Debugging ---------------------------------------------

        return d_names



    @staticmethod
    def saveFile(workbook, new_name):
        """

        :param workbook:
        :param new_name:
        :return: Boolean whether save was successful or not
        """
        return workbook.save(new_name)




