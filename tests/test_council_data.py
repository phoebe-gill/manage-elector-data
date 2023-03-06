from towerhamlets.council import CouncilElector, get_council_electors

TEST_COUNCIL_ELECTOR = CouncilElector(
    record_order=1,
    number_prefix="BW1",
    number=1,
    marker=None,
    surname="Bar",
    forename="Foo",
    address_1="1 Test Road",
    address_2="London",
    postcode="E1 1AA",
)


def test_import():
    assert list(get_council_electors("tests/test_council_data.xlsx")) == [TEST_COUNCIL_ELECTOR]
