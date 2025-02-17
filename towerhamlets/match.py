"""match.py

Usage:
    match.py [-h] COUNCIL_ELECTORAL_ROLL_PATH GP_ELECTORAL_ROLL_PATH OUTPUT_PATH

"""
from datetime import date, datetime
from docopt import docopt

from dataclasses import astuple, dataclass
from typing import Literal, Optional

from openpyxl import Workbook
from towerhamlets.council import (
    CouncilElector,
    get_council_electors,
    filter_out_post_code,
)
from towerhamlets.source import SourceData


@dataclass(frozen=True)
class DestinationElector:
    number_prefix: str
    number: int
    suffix: int
    markers: Optional[str]
    date_of_birth: Optional[str]
    surname: str
    forename: str
    address_1: Optional[str]
    address_2: Optional[str]
    address_3: Optional[str]
    address_4: Optional[str]
    postcode: Optional[str]
    month_first_seen: Optional[str] = None
    ward_walk_reference: Optional[int] = None
    # Key:
    #  v = voted in person
    #  x = voted by post
    #  0 = did not vote
    #  None = was not on the electoral register at the time this vote took place
    gla_2021: Literal["v", "x", 0, None] = None
    local_2022: Literal["v", "x", 0, None] = None
    gp_member: Optional[str] = None
    do_not_knock: Optional[str] = None
    do_not_leaflet: Optional[str] = None
    displayed_poster: Optional[str] = None
    rag: Optional[str] = None
    parties_considered: Optional[str] = None
    likelihood_to_vote_green: Optional[str] = None
    notes: Optional[str] = None
    date_last_knocked: Optional[date] = None

    @classmethod
    def headers(cls):
        return (
            "Elector Number Prefix",
            "Elector Number",
            "Elector Number Suffix",
            "Elector Markers",
            "Elector DOB",
            "Surname",
            "Forename",
            "Address1",
            "Address2",
            "Address3",
            "Address4",
            "PostCode",
            "Month first seen on roll",
            "Ward walk ref",
            "GLA 2021",
            "Local 2022",
            "GP member",
            "Do not knock",
            "Do not leaflet",
            "Displayed poster",
            "RAG",
            "Parties considered",
            "Likelihood to vote Green (1-5)",
            "Notes",
            "Date Last Knocked",
        )

    @classmethod
    def create(
        cls,
        council_elector: CouncilElector,
        source_data: SourceData,
    ) -> "DestinationElector":
        source_elector = source_data.get_elector(council_elector.get_identifier()) or {}

        if not source_elector:
            print(f"New elector: {council_elector.forename} {council_elector.surname}")

        return DestinationElector(
            number_prefix=council_elector.number_prefix,
            number=council_elector.number,
            suffix=council_elector.suffix,
            markers=council_elector.markers,
            date_of_birth=council_elector.date_of_birth,
            surname=council_elector.surname.strip(),
            forename=council_elector.forename.strip(),
            address_1=council_elector.address_1,
            address_2=council_elector.address_2,
            address_3=filter_out_post_code(council_elector.address_3),
            address_4=filter_out_post_code(council_elector.address_4),
            postcode=council_elector.postcode,
            month_first_seen=source_elector.get("Month first seen on roll")
            if source_elector
            else "2024 December",
            ward_walk_reference=source_elector.get("Ward walk ref"),
            gla_2021=source_elector.get("GLA 2021"),
            local_2022=(source_elector.get("Local 2022") or 0)
            if source_elector
            else None,
            gp_member=source_elector.get("GP member"),
            do_not_knock=source_elector.get("Do not knock"),
            do_not_leaflet=source_elector.get("Do not leaflet"),
            displayed_poster=source_elector.get("Displayed poster"),
            rag=source_elector.get("RAG"),
            parties_considered=source_elector.get("Parties considered"),
            likelihood_to_vote_green=source_elector.get(
                "Likelihood to vote Green (1-5)"
            ),
            notes=source_elector.get("Notes"),
            date_last_knocked=(
                last_knocked.date()
                if (last_knocked := source_elector.get("Date Last Knocked"))
                and isinstance(last_knocked, datetime)
                else last_knocked
            ),
        )


def get_gla_2021_vote(source_entry) -> str:
    match source_entry:
        case None | 0 | "x" | "v":
            return source_entry
        case "v GPMem":
            return "v"
        case "x GPMem":
            return "x"
        case "NEW" | "NEW ":
            return None
    raise Exception(f"Unexpected GLA 2021 voting record entry: '{source_entry}'")


def main(council_electoral_roll_path, gp_electoral_roll_path, output_path):
    council_electors = get_council_electors(council_electoral_roll_path)
    gp_electors = SourceData(gp_electoral_roll_path)
    combined_electors = [
        DestinationElector.create(council_elector, gp_electors)
        for council_elector in council_electors
    ]

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(DestinationElector.headers())
    for elector in combined_electors:
        worksheet.append(astuple(elector))
    workbook.save(output_path)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(
        arguments["COUNCIL_ELECTORAL_ROLL_PATH"],
        arguments["GP_ELECTORAL_ROLL_PATH"],
        arguments["OUTPUT_PATH"],
    )
