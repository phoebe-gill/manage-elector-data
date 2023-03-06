"""
Data from our current spreadsheet.
"""
from typing import Iterable
import openpyxl


def get_known_electors(electoral_roll_file_path: str) -> Iterable[dict]:
    workbook = openpyxl.load_workbook(electoral_roll_file_path, read_only=True)
    worksheet = workbook.active
    rows = worksheet.iter_rows(values_only=True)

    headers = get_header_names(next(rows))

    for row in rows:
        yield {key: value for (key, value) in zip(headers, row)}


def get_header_names(row: tuple) -> list[str]:
    """One column doesn't have a header."""
    return [element or "Notes" for element in row]
