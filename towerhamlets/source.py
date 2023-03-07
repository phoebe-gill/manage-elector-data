"""
Data from our current spreadsheet.
"""
from typing import Iterable, Optional
import openpyxl


class SourceElector(dict):
    def get_identifier(self) -> tuple:
        """We assume that the same address with the same name is the same person."""
        return (
            self["Elector Name"],
            self["Address1"],
            self["Address2"],
            self["Address3"],
            self["Address4"],
        )


class SourceData:
    def __init__(self, electoral_roll_file_path: str) -> None:
        self.electors = {
            elector.get_identifier(): elector
            for elector in get_known_electors(electoral_roll_file_path)
        }

    def get_elector(self, identifier: tuple) -> Optional[SourceElector]:
        return self.electors.get(identifier)


def get_known_electors(electoral_roll_file_path: str) -> Iterable[dict]:
    workbook = openpyxl.load_workbook(electoral_roll_file_path, read_only=True)
    worksheet = workbook.active
    rows = worksheet.iter_rows(values_only=True)

    headers = get_header_names(next(rows))

    for row in rows:
        yield SourceElector({key: value for (key, value) in zip(headers, row)})


def get_header_names(row: tuple) -> list[str]:
    """One column doesn't have a header."""
    return [element or "Notes" for element in row]
