from dataclasses import dataclass
from typing import Optional
from towerhamlets.council import CouncilElector
from towerhamlets.source import SourceData


@dataclass(frozen=True)
class DestinationElector:
    number_prefix: str
    number: int
    markers: Optional[str]
    forename: str
    surname: str
    address_1: str
    address_2: Optional[str]
    address_3: Optional[str]
    address_4: Optional[str]
    postcode: str

    month_first_seen: Optional[str] = None
    ward_walk_reference: Optional[int] = None
    gla_2021: Optional[str] = None
    local_2022: Optional[str] = None
    gp_member: Optional[str] = None
    do_not_knock: Optional[str] = None
    do_not_leaflet: Optional[str] = None
    displayed_poster: Optional[str] = None
    rag: Optional[str] = None
    parties_considered: Optional[str] = None
    likelihood_to_vote_green: Optional[str] = None
    notes: Optional[str] = None
    date_last_knocked: Optional[str] = None

    @classmethod
    def create(
        cls,
        council_elector: CouncilElector,
        source_data: SourceData,
    ) -> "DestinationElector":
        source_elector = source_data.get_elector(council_elector.get_identifier()) or {}
        return DestinationElector(
            number_prefix=council_elector.number_prefix,
            number=council_elector.number,
            markers=council_elector.markers,
            surname=council_elector.surname,
            forename=council_elector.forename,
            address_1=council_elector.address_1,
            address_2=council_elector.address_2,
            address_3=council_elector.address_3,
            address_4=council_elector.address_4,
            postcode=council_elector.postcode,
            month_first_seen=(
                "2022 December"
                if not source_elector
                else "2021 May"
                if source_elector.get("GLA") == "NEW"
                else None
            ),
            ward_walk_reference=source_elector.get("Ward wark ref"),
            gla_2021=get_gla_2021_vote(source_elector.get("GLA")),
            local_2022=source_elector.get("Local 2022"),
            gp_member=(
                "y"
                if source_elector.get("GLA") and "v GPMem" in source_elector.get("GLA")
                else None
            ),
            do_not_knock="DNK" if source_elector.get("DNK?") else None,
            do_not_leaflet="DNL" if source_elector.get("No leaflets?") else None,
            displayed_poster="y" if source_elector.get("Poster?") else None,
            rag=source_elector.get("RAG"),
            parties_considered=source_elector.get("Parties considered"),
            likelihood_to_vote_green=source_elector.get("1-5"),
            notes=source_elector.get("Notes"),
            date_last_knocked=source_elector.get("Date Last Knocked"),
        )


def get_gla_2021_vote(source_entry) -> str:
    match source_entry:
        case None | 0 | "x" | "v":
            return source_entry
        case "v GPMem":
            return "v"
        case "x GPMem":
            return "x"
        case "NEW":
            return None
    raise Exception(f"Unexpected GLA 2021 voting record entry: {source_entry}")
