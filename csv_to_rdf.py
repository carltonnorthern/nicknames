"""Convert CSV nicknames to RDF triples format."""

import csv
from pathlib import Path


def csv_to_rdf_triples(*, input_path: str | Path, output_path: str | Path) -> None:
    """Convert CSV format to RDF triples.

    Parameters
    ----------
    input_path : str | Path
        Path to input CSV file
    output_path : str | Path
        Path to output RDF triples file
    """
    with open(input_path) as f:
        reader = csv.reader(f)
        with open(output_path, "w") as out:
            for line in reader:
                canonical, *nicknames = line
                for nickname in nicknames:
                    out.write(f"{canonical},has_nickname,{nickname}\n")


if __name__ == "__main__":
    csv_to_rdf_triples(input_path="names.csv", output_path="names_rdf.csv")
