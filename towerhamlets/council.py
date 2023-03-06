"""
Data from the electoral register, as provided by the council.
"""
from dataclasses import dataclass
from typing import Iterable

import openpyxl


@dataclass
class CouncilElector:
    record_order: int
    number_prefix: str
    number: int
    marker: str
    surname: str
    forename: str
    address_1: str
    address_2: str
    postcode: str
    address_3: str
    address_4: str


def get_council_electors(electoral_roll_file_path: str) -> Iterable[CouncilElector]:
    workbook = openpyxl.load_workbook(electoral_roll_file_path, read_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, values_only=True):  # Skip header
        yield CouncilElector(*remove_duplicate_postcode(row))


def filter_out_fields_containing(element, rejection_string):
    if isinstance(element, str) and rejection_string in element:
        return None
    return element


def remove_duplicate_postcode(row: list) -> list:
    """
    Each elector has a postcode field, but also has the postcode in an address field.
    The latter are all of the form 'E1†1AA'. So let's de-duplicate.
    """
    return [filter_out_fields_containing(element, "†") for element in row]
