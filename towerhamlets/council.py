"""
Data from the electoral register, as provided by the council.
"""
from dataclasses import dataclass
from typing import Iterable, Optional

import openpyxl


@dataclass(frozen=True)
class CouncilElector:
    """Order of fields must match column order in source data."""

    record_order: int
    number_prefix: str
    number: int
    markers: str
    surname: str
    forename: str
    address_1: str
    address_2: Optional[str]
    postcode: str
    address_3: Optional[str]
    address_4: Optional[str]

    def get_identifier(self) -> tuple:
        """We assume that the same address with the same name is the same person."""
        return (
            f"{self.surname} {self.forename}",
            self.address_1,
            self.address_2,
            self.address_3,
            self.address_4,
        )


def get_council_electors(electoral_roll_file_path: str) -> Iterable[CouncilElector]:
    workbook = openpyxl.load_workbook(electoral_roll_file_path, read_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, values_only=True):  # Skip header
        yield CouncilElector(
            *[
                item.strip() if isinstance(item, str) else item
                for item in remove_duplicate_postcode(row)
            ]
        )


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
