from dataclasses import replace
from datetime import datetime
import openpyxl
from tests.test_council_data import TEST_COUNCIL_ELECTOR, TEST_COUNCIL_FILE_PATH
from tests.test_gp_data import TEST_SOURCE_ELECTOR, TEST_SOURCE_FILE_PATH
from towerhamlets.council import get_council_electors
from towerhamlets.match import DestinationElector
from towerhamlets.source import SourceData


TEST_COMBINED_FILE_PATH = "tests/test_combined_data.xlsx"

TEST_SOURCE_DATA = SourceData(TEST_SOURCE_FILE_PATH)


def get_test_destination_electors():
    workbook = openpyxl.load_workbook(TEST_COMBINED_FILE_PATH, read_only=True)
    worksheet = workbook.active
    rows = worksheet.iter_rows(values_only=True, min_row=2)  # Skip header

    for row in rows:
        elector = DestinationElector(*row[:25:])
        if isinstance(elector.date_last_knocked, datetime):
            elector = replace(
                elector, date_last_knocked=elector.date_last_knocked.date()
            )
        yield elector


def test_identical_names():
    assert TEST_COUNCIL_ELECTOR.get_identifier() == TEST_SOURCE_ELECTOR.get_identifier()


def test_non_identical_names():
    elector = replace(TEST_COUNCIL_ELECTOR, forename="foo")

    assert elector.get_identifier() != TEST_SOURCE_ELECTOR.get_identifier()


def test_create_destination_elector():
    assert DestinationElector.create(TEST_COUNCIL_ELECTOR, TEST_SOURCE_DATA) == next(
        get_test_destination_electors()
    )


def test_create_destination_electors():
    assert [
        DestinationElector.create(council_elector, TEST_SOURCE_DATA)
        for council_elector in get_council_electors(TEST_COUNCIL_FILE_PATH)
    ] == list(get_test_destination_electors())
