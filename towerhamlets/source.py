"""
Data from our current spreadsheet.
"""
from typing import Iterable, Optional
import openpyxl


class SourceElector(dict):
    def get_identifier(self) -> tuple:
        """We assume that the same address with the same name is the same person."""
        return (
            self["Surname"],
            self["Forename"],
            self["Address1"],
            self["Address2"],
            self["Address3"],
            self["Address4"],
            None,
            None,
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

    headers = next(rows)

    for row in rows:
        if not row[0]:
            # All electors have a prefix, so this must be an empty row
            continue
        yield SourceElector(
            {
                key: value.strip() if isinstance(value, str) else value
                for (key, value) in zip(headers, row)
            }
        )
