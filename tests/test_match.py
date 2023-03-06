from tests.test_council_data import TEST_COUNCIL_ELECTOR
from tests.test_gp_data import TEST_SOURCE_ELECTOR
from towerhamlets.council import get_council_electors
from towerhamlets.match import is_same_person
from towerhamlets.source import get_known_electors


def test_identical_names():
    assert is_same_person(TEST_COUNCIL_ELECTOR, TEST_SOURCE_ELECTOR)


def test_non_identical_names():
    elector = TEST_COUNCIL_ELECTOR
    elector.forename = "foo"

    assert not is_same_person(elector, TEST_SOURCE_ELECTOR)
