from towerhamlets.source import SourceElector, get_header_names, get_known_electors


TEST_SOURCE_FILE_PATH = "tests/test_gp_data.xlsx"


TEST_SOURCE_ELECTOR = SourceElector(
    {
        "Elector Number Prefix": "BW1",
        "Elector Number": 1,
        "Elector Number (Absent Voter List)": "BW1-1",
        "Elector Number Suffix": 0,
        "Elector Markers": None,
        "Ward wark ref": 1,
        "Ward Walk #": "#1 Foo",
        "Voting Record": None,
        "GLA": None,
        "Local 2022": None,
        "Registered Postal Voter (March)": None,
        "Elector Name": "A B",
        "Address1": "1 Foo Road",
        "Address2": "London",
        "Address3": None,
        "Address4": None,
        "PostCode": "E1 1AA",
        "DNK?": None,
        "Poster?": None,
        "No leaflets?": None,
        "RAG": None,
        "Parties considered": None,
        "1-5": None,
        "Notes": None,
        "Date Last Knocked": None,
    }
)


def test_header_names():
    assert get_header_names(("foo", None)) == ["foo", "Notes"]


def test_import():
    assert next(get_known_electors(TEST_SOURCE_FILE_PATH)) == TEST_SOURCE_ELECTOR
