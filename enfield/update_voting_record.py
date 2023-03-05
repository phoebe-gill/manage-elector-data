#!/usr/bin/env python3
"""update_voting_record.py

Usage:
    update_voting_record.py [-h] FILENAME
"""
from docopt import docopt
import openpyxl


def main(filename):
    workbook = openpyxl.load_workbook(filename)
    worksheet = workbook.active

    for row in worksheet.rows:
        [house_number, _, _, first_name, surname, voting_record, *_] = row

        if first_name.value:
            print(
                f"{str(house_number.value)}: {surname.value.upper()}, {first_name.value}"
            )
            voted = input("Did they vote [(y)es/(n)o]?")

            if voted and voted in ["yes", "y"]:
                if voting_record.value:
                    voting_record.value = voting_record.value.rstrip("/") + "/V18"
                else:
                    voting_record.value = "V18"

    workbook.save("processed_" + filename)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(arguments["FILENAME"])
