from towerhamlets.council import (
    CouncilElector,
    get_council_electors,
    filter_out_post_code,
)

TEST_COUNCIL_FILE_PATH = "tests/test_council_data.xlsx"


TEST_COUNCIL_ELECTOR = CouncilElector(
    number_prefix="BW1",
    number=1,
    suffix=0,
    markers=None,
    date_of_birth=None,
    surname="A",
    forename="B",
    address_1="2 Foo Road",
    address_2="London",
    address_3="E1 1AA",
    address_4=None,
    address_5=None,
    address_6=None,
    postcode="E1 1AA",
)


def test_import():
    assert next(get_council_electors(TEST_COUNCIL_FILE_PATH)) == TEST_COUNCIL_ELECTOR


def test_is_post_code():
    assert filter_out_post_code("E1 1AA") is None


def test_is_not_post_code():
    assert filter_out_post_code("E1 Rose House") == "E1 Rose House"
