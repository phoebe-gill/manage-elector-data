"""apply_postal_votes.py

Usage:
    apply_postal_votes.py [-h] GP_SPREADSHEET_PATH POSTAL_VOTE_PATH OUTPUT_PATH ELECTION_ROW_NAME
"""
from dataclasses import dataclass
import re
from docopt import docopt
import csv

from towerhamlets import create_output, load_electors


@dataclass(frozen=True)
class PostalVoteRecord:
    prefix: str
    number: int
    suffix: int


def get_postal_voters(path):
    with open(path, encoding="windows-1252") as f:
        reader = csv.DictReader(f)

        for row in reader:
            match = re.fullmatch(r"(\w\w\d)-(\d+)(/(\d+))?", row["ElectorNo"])
            prefix = match.group(1)
            number = match.group(2)
            suffix = match.group(4)
            yield PostalVoteRecord(
                prefix=prefix,
                number=int(number),
                suffix=int(suffix or 0),
            )


def main(
    gp_spreadsheet_path: str,
    postal_vote_path: str,
    output_path: str,
    election_row_name: str,
):
    (headers, electors) = load_electors(gp_spreadsheet_path)

    election_row_index = (
        headers.index(election_row_name) - 3
    )  # First three rows aren't included in data

    postal_voters = get_postal_voters(postal_vote_path)

    for postal_voter in postal_voters:
        identifier = (postal_voter.prefix, postal_voter.number, postal_voter.suffix)
        if identifier in electors:
            electors[identifier] = (
                electors[identifier][:election_row_index]
                + ["x"]
                + electors[identifier][election_row_index + 1 :]
            )

    create_output(headers, electors, output_path)


if __name__ == "__main__":
    arguments = docopt(__doc__)
    main(
        arguments["GP_SPREADSHEET_PATH"],
        arguments["POSTAL_VOTE_PATH"],
        arguments["OUTPUT_PATH"],
        arguments["ELECTION_ROW_NAME"],
    )
