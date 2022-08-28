"""Tool to ensure that the CSV data is normalized.

"Normalized" means:

- All names are lowercase
- A name doesn't appear in a line more than once
- There are no repeated lines
- All lines are sorted by the first name in the line
- No line is a subset of another line (eg alex,alexa is redundant if we already
  have alex,alexa,alexander)
"""
from __future__ import annotations

import argparse

import csv
import sys
from typing import Iterable


def read_lines(path: str):
    with open(path) as f:
        return [line for line in csv.reader(f)]


def write_lines(path: str, lines: Iterable[Iterable[str]]):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(lines)


def _is_subset_of_others(line: set, others: Iterable[set[str]]):
    for other in others:
        if line == other:
            continue
        if line.issubset(other):
            return True
    return False


def remove_subsets(lines: Iterable[Iterable[str]]):
    """Remove lines that are subsets of other lines.

    For instance, if we have

    alex,alexa,alexander
    alex,alexa

    then we can remove the second line, since the first line already says that
    alex and alexa are interchangaable.

    This is a naive O(n^2) search, but we aren't dealing with many names."""
    line_sets = [set(line) for line in lines]
    return [
        line
        for line, line_set in zip(lines, line_sets)
        if not _is_subset_of_others(line_set, line_sets)
    ]


def unique(line: Iterable[str]):
    """Get a list of unique elements in a list, preserving order."""
    return list(dict.fromkeys(line))


def unique_lines(lines: Iterable[list[str]]):
    seen = set()
    result = []
    for line in lines:
        key = frozenset(line)
        if key in seen:
            continue
        seen.add(key)
        result.append(line)
    return result


def normalize(lines: Iterable[Iterable[str]]) -> list[list[str]]:
    lines = [[name.lower() for name in line] for line in lines]
    lines = [unique(line) for line in lines]
    lines = unique_lines(lines)
    lines = remove_subsets(lines)
    lines = list(sorted(lines, key=lambda line: line[0]))
    return lines


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Normalize names.csv")
    parser.add_argument(
        "-i", "--input", help="Path to input CSV file", default="names.csv"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output CSV file",
        default="names.csv",
    )
    return parser.parse_args(argv)


def cli(argv):
    args = parse_args(argv)
    lines = read_lines(args.input)
    normed = normalize(lines)
    write_lines(args.output, normed)


if __name__ == "__main__":
    cli(sys.argv[1:])
