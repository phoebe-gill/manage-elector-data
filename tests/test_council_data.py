from towerhamlets.council import CouncilElector, get_council_electors

TEST_COUNCIL_ELECTOR = CouncilElector(
    record_order=1,
    number_prefix="BW1",
    number=1,
    marker=None,
    surname="A",
    forename="B",
    address_1="1 Foo Road",
    address_2="London",
    postcode="E1 1AA",
    address_3="E1†1AA",
    address_4=None,
)


def test_import():
    assert next(get_council_electors("tests/test_council_data.xlsx")) == TEST_COUNCIL_ELECTOR
