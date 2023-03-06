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


def get_council_electors(electoral_roll_file_path: str) -> Iterable[CouncilElector]:
    workbook = openpyxl.load_workbook(electoral_roll_file_path, read_only=True)
    worksheet = workbook.active

    for row in worksheet.iter_rows(min_row=2, values_only=True):  # Skip header
        yield CouncilElector(*row)
