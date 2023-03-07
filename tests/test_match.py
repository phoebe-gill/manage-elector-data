from tests.test_council_data import TEST_COUNCIL_ELECTOR
from tests.test_gp_data import TEST_SOURCE_ELECTOR
from towerhamlets.council import get_council_electors
from towerhamlets.source import get_known_electors


def test_identical_names():
    assert TEST_COUNCIL_ELECTOR.get_identifier() == TEST_SOURCE_ELECTOR.get_identifier()


def test_non_identical_names():
    elector = TEST_COUNCIL_ELECTOR
    elector.forename = "foo"

    assert TEST_COUNCIL_ELECTOR.get_identifier() != TEST_SOURCE_ELECTOR.get_identifier()
