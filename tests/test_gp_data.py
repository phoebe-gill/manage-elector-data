from towerhamlets.source import SourceElector, get_known_electors


TEST_SOURCE_FILE_PATH = "tests/test_gp_data.xlsx"


TEST_SOURCE_ELECTOR = SourceElector(
    {
        "Elector Number Prefix": "BW1",
        "Elector Number": 1,
        "Elector Markers": None,
        "Surname": "O`A",
        "Forename": "B",
        "Address1": "2 Foo Road",
        "Address2": "London",
        "Address3": None,
        "Address4": None,
        "PostCode": "E1 1AA",
        "Month first seen on roll": "2022 December",
        "Ward walk ref": 1,
        "GLA 2021": None,
        "Local 2022": "x",
        "GP member": None,
        "Do not knock": None,
        "Do not leaflet": None,
        "Displayed poster": None,
        "RAG": None,
        "Parties considered": None,
        "Likelihood to vote Green (1-5)": None,
        "Notes": None,
        "Date Last Knocked": None,
    }
)


def test_import():
    assert next(get_known_electors(TEST_SOURCE_FILE_PATH)) == TEST_SOURCE_ELECTOR
