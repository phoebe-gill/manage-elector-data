"""
Data from the electoral register, as provided by the council.
"""
from dataclasses import dataclass
import re
from typing import Iterable, Optional

import openpyxl

from towerhamlets.source import get_letters_only


@dataclass(frozen=True)
class CouncilElector:
    """Order of fields must match column order in source data."""

    number_prefix: str
    number: int
    suffix: int
    markers: Optional[str]
    date_of_birth: Optional[str]
    surname: str
    forename: str
    postcode: Optional[str]
    address_1: Optional[str]
    address_2: Optional[str]
    address_3: Optional[str]
    address_4: Optional[str]
    address_5: Optional[str]
    address_6: Optional[str]

    def get_identifier(self) -> tuple:
        """We assume that the same address with the same name is the same person."""
        return (
            get_letters_only(self.surname),
            get_letters_only(self.forename),
            self.address_1,
            self.address_2,
            filter_out_post_code(self.address_3),
            filter_out_post_code(self.address_4),
            filter_out_post_code(self.address_5),
            filter_out_post_code(self.address_6),
        )


def get_council_electors(electoral_roll_file_path: str) -> Iterable[CouncilElector]:
    workbook = openpyxl.load_workbook(electoral_roll_file_path, read_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, values_only=True):  # Skip header
        yield CouncilElector(
            *[item.strip() if isinstance(item, str) else item for item in row]
        )


def filter_out_post_code(address_component: Optional[str]):
    if address_component and re.fullmatch(r"E\d\W\d\w\w", address_component):
        return None
    return address_component
