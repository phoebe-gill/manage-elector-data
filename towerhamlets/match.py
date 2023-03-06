from towerhamlets.council import CouncilElector


def is_same_person(council_elector: CouncilElector, gp_elector: dict) -> bool:
    """We assume that the same address with the same name is the same person."""
    return (
        (
            gp_elector["Elector Name"]
            == f"{council_elector.surname} {council_elector.forename}"
        )
        and gp_elector["Address1"] == council_elector.address_1
        and gp_elector["Address2"] == council_elector.address_2
        and gp_elector["Address3"] == council_elector.address_3
        and gp_elector["Address4"] == council_elector.address_4
    )
