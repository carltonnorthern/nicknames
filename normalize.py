"""Tool to normalize the names.csv file of RDF triples.

Each line is in the format: (name1, relationship, name2)
For example:
    robert,has_nickname,bob
    robert,is_translation_of:en-sp,robertoxw

"Normalized" means:

- All names are lowercase
- All names have no leading or trailing whitespace
- There are no repeated lines
- All lines are sorted
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable, Sequence

_THIS_DIR = Path(__file__).parent
_HEADER = ["name1", "relationship", "name2"]


def read_lines(path: str) -> Iterable[list[str]]:
    with open(path) as f:
        reader = csv.reader(f)
        for line in reader:
            if line == _HEADER:
                continue
            yield list(line)


def write_lines(path: str, lines: Iterable[Sequence[str]]) -> None:
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(_HEADER)
        for line in lines:
            writer.writerow(line)


def normalize(lines: Iterable[Iterable[str]]) -> list[list[str]]:
    lines = (list(line) for line in lines)
    lines = (line for line in lines if len(line))
    lines = (norm_line(line) for line in lines)
    lines = check_integrity(lines)
    lines = (drop_duplicates(line) for line in lines)
    lines = unique_lines(lines)
    lines = sort_lines(lines)
    return list(lines)


def norm_line(line: list[str]) -> list[str]:
    return [field.lower().strip() for field in line]


def drop_duplicates(line: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(line))


def unique_lines(lines: Iterable[Sequence[str]]) -> list[list[str]]:
    d = dict.fromkeys(tuple(line) for line in lines)
    return [list(line) for line in d.keys()]


def check_integrity(lines: Iterable[Sequence[str]]) -> Iterable[Sequence[str]]:
    errors = []
    lines = list(lines)
    for i, line in enumerate(lines):
        if len(line) != 3:
            errors.append(f"Line {i} ({line}) needs 3 elements")
    if errors:
        raise ValueError("\n".join(errors))
    return lines


def sort_lines(lines: Iterable[Iterable[str]]) -> list[list[str]]:
    return sorted(lines)


def parse_args(argv) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize names.csv")
    parser.add_argument(
        "-i", "--input", help="Path to input CSV file", default=_THIS_DIR / "names.csv"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output CSV file",
        default=_THIS_DIR / "names.csv",
    )
    return parser.parse_args(argv)


def cli(argv) -> None:
    args = parse_args(argv)
    lines = read_lines(args.input)
    normed = normalize(lines)
    write_lines(args.output, normed)


if __name__ == "__main__":
    cli(sys.argv[1:])
