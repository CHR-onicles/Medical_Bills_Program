import os
import openpyxl
from openpyxl.styles import colors, PatternFill
from icecream import ic
from datetime import datetime





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
        Function to get staff names connected with their spouse and children.

        :param workbook: Staff list workbook

        :return: dictionary of staff names, their spouse and children.
        """
        staff_details = {}
        # sheet = workbook.active
        sheet = workbook['2020 STAFF LIST']
        start = datetime.now()
        for row in range(3, 581):  # ignoring header labels
            for col in range(1, 5):  # 1st to 4th column
                cell = sheet.cell(row=row, column=col)
                staff_cell = sheet.cell(row=row, column=1)  # cell with staff name

                if col == 1 and cell.value is not None and cell.font.b is True:  # staff name
                    backup_staff_cell = sheet.cell(row=row, column=1)
                    staff_details[cell.value] = []

                if col == 2 and cell.value is not None:
                    staff_details[staff_cell.value].append(cell.value)

                if col == 3 and cell.value is None:  # means no spouse
                    if staff_cell.value is not None:  # there was a staff name in first cell
                        staff_details[staff_cell.value].append(None)
                    else:
                        continue

                if col == 3 and cell.value is not None:  # has a spouse
                    staff_details[staff_cell.value].append(cell.value)

                if col == 4 and cell.value is None:  # doesn't have a child
                    if staff_cell.value is not None:
                        staff_details[staff_cell.value].append(None)
                    else:
                        continue

                if col == 4 and cell.value is not None:  # has a child
                    if (staff_cell.value and sheet.cell(row=row, column=2)
                            and sheet.cell(row=row, column=3)) is None:  # first 3 columns are empty means staff has multiple children
                        staff_details[backup_staff_cell.value].append(cell.value)
                    else:
                        staff_details[staff_cell.value].append(cell.value)

        stop = datetime.now()
        ic('Time elapsed for extracting:', (stop-start))
        # For Debugging -------------------------
        # for k, v in staff_details.items():
        #     #     print(k,'->', v)
        #     pass
        # print(staff_details)
        # print(len(staff_details))

        # for x in staff_details.keys():
        #     if 'ABIGAIL' in x:
        #         print(x)
        #         print(staff_details[x])
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
            ic.enable()
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
            ic.disable()


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
