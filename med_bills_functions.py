import os
import openpyxl
from openpyxl.styles import colors, PatternFill
from icecream import ic
from datetime import datetime



# Global variables
staff_details = {}

class MBillsFunctions:
    """
    Class which contains operations to be carried out on medical bills files.
    """

    @staticmethod
    def initializeFiles(med_bill_file=None, staff_list_file=None):
        """
        Loads med bills file and staff list file.

        :param med_bill_file: Medical Bills File
        :param staff_list_file: Staff List File
        :return: Both workbooks, one of them or None if one is type: None
        """
        if med_bill_file and staff_list_file is not None:
            workbook1 = openpyxl.load_workbook(med_bill_file)
            workbook2 = openpyxl.load_workbook(staff_list_file, read_only=True)
            return workbook1, workbook2
        elif med_bill_file is None:
            workbook = openpyxl.load_workbook(staff_list_file, read_only=True)
            return workbook
        elif staff_list_file is None:
            workbook = openpyxl.load_workbook(med_bill_file)
            return workbook
        else:
            return None


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

        :param workbook: Staff List Workbook
        :return: list of all dependants from Staff list workbook
        """

        d_names = []

        for sheet in workbook.sheetnames:
            for row in workbook[sheet].iter_rows(min_row=3, max_row=600, min_col=3, max_col=4):
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
    def getDetailsOfPermanentStaff(workbook):
        """
        Optimized function to extract details of staff members from the staff list file.

        :param workbook: Staff list workbook

        :return: dictionary of staff names, their spouse and children.
        """
        sheet = workbook.active

        start = datetime.now()

        def row_any(row):
            """
            Reimplementation of python's any() function but for rows.

            :param row: Row to be checked.

            :return: Returns False if all cells in a row are empty. True otherwise.
            """
            non_empty_cells = [x for x in row if x.value is not None]
            return any(non_empty_cells)

        helper_staff_name = ''

        def process_row(_row):
            """
            Function to process rows and create dictionary of staff details.

            :param _row: rows from staff list sheet

            :return: dictionary containing all permanent staff details
            """
            global helper_staff_name, staff_details
            if _row[0].value is not None:
                helper_staff_name = _row[0].value

            # Assigning dept, spouse and child to staff name if staff is not empty
            # (meaning staff has multiple children according to the format of the file)
            if _row[0].value is not None:
                staff_details[_row[0].value] = [cell for cell in [_row[1].value, _row[2].value, _row[3].value]]
            else:
                if helper_staff_name == '':
                    raise Exception('Staff name provided was None!!')
                else:
                    staff_details[helper_staff_name].append(_row[-1].value)

            return staff_details

        # Filtering out rows which are empty which is ~40% of all rows...improving performance
        rows = [x for x in sheet.iter_rows(min_row=3, max_row=600, min_col=1, max_col=4) if row_any(x)]
        for row in rows:
            process_row(row)

        stop = datetime.now()
        ic('Time elapsed for extracting:', (stop - start))
        # For Debugging -------------------------
        # for k, v in staff_details.items():
        #     #     print(k,'->', v)
        #     pass
        # print(staff_details)
        # print(len(staff_details))
        # End Debugging -------------------------

        return staff_details


    @staticmethod
    def searchForPerson(person, staff_details):
        """
        Function to search for anyone using staff list. If found, returns staff's details...if not returns none for
        those particulars in the details(For casuals and guests).

        :param staff_details: dictionary of staff with details

        :param person: person to search for

        :return: tuple of staff with dependant(s)
        """
        start = datetime.now()
        for staff, dependants in staff_details.items():
            ic.disable()
            if staff == person:
                ic('Found with key:', staff, dependants)
                stop = datetime.now()
                ic('Time for Search elapsed:', stop - start)
                return staff, dependants
            else:
                for d in dependants:
                    if d == person:
                        ic('Found with value:', staff, dependants)
                        stop = datetime.now()
                        ic('Time for Search elapsed:', stop - start)
                        return staff, dependants
            # ic.disable()


    @staticmethod
    def saveFile(workbook, new_name):
        """

        :param workbook:
        :param new_name:
        :return: Boolean whether save was successful or not
        """
        return workbook.save(new_name)



    # ---------------------------------------- TODO --------------------------------------------------------
    # TODO:
    #   1. Make documentation more comprehensible
