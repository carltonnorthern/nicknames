"""Tool to normalize a CSV file.

The first name in each line is the canonical name. The rest of the names in that
line are nicknames for the canonical name.

"Normalized" means:

- All names are lowercase
- All names have no leading or trailing whitespace
- A line has at least 2 names, one canonical and at least one nickname
- A name doesn't appear in a line more than once
- There are no repeated lines
- All lines are sorted by the first name in the line
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable, Sequence

_THIS_DIR = Path(__file__).parent


def read_lines(path: str):
    with open(path) as f:
        return [line for line in csv.reader(f)]


def write_lines(path: str, lines: Iterable[Iterable[str]]):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(lines)


def normalize(lines: Iterable[Iterable[str]]) -> list[list[str]]:
    lines = (list(line) for line in lines)
    lines = (line for line in lines if len(line))
    lines = ([norm_name(name) for name in line] for line in lines)
    lines = merge_lines(lines)
    lines = check_integrity(lines)
    lines = (drop_duplicates(line) for line in lines)
    lines = unique_lines(lines)
    lines = sort_lines(lines)
    return lines


def merge_lines(lines: Iterable[Iterable[str]]) -> list[list[str]]:
    """if more than one line has the same canonical name, merge them into one."""
    m = {}
    for line in lines:
        canonical, nicknames = line[0], line[1:]
        if canonical in m:
            m[canonical].extend(nicknames)
        else:
            m[canonical] = list(nicknames)
    return [[canonical, *nicknames] for canonical, nicknames in m.items()]


def norm_name(name: str) -> str:
    return name.lower().strip()


def drop_duplicates(line: Iterable[str]):
    """Get a list of unique elements in a list, preserving order."""
    return list(dict.fromkeys(line))


def unique_lines(lines: Iterable[Sequence[str]]):
    seen = set()
    result = []
    for line in lines:
        canonical, nicknames = line[0], line[1:]
        key = (canonical, frozenset(nicknames))
        if key in seen:
            continue
        seen.add(key)
        result.append(line)
    return result


def check_integrity(lines: Iterable[Sequence[str]]) -> Iterable[Sequence[str]]:
    for i, line in enumerate(lines):
        if len(line) < 2:
            raise ValueError(f"Line  {i} ({line}) has less than 2 elements")
        yield line


def sort_lines(lines: Iterable[Iterable[str]]) -> list[list[str]]:
    lines = list(lines)
    lines.sort(key=lambda line: line[0])
    return lines


def parse_args(argv):
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


def cli(argv):
    args = parse_args(argv)
    lines = read_lines(args.input)
    normed = normalize(lines)
    write_lines(args.output, normed)


if __name__ == "__main__":
    cli(sys.argv[1:])
