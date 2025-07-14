"""Script to auto-generate SQL scripts from the RDF triples CSV file."""

import argparse
import csv
import sys
from pathlib import Path

_THIS_DIR = Path(__file__).parent


def cli(argv: list[str]):
    args = parse_argv(argv)
    generate_sql(args.type, args.output)


def generate_sql(typ: str = "all", out_path: Path | None = None):
    if typ == "all" and out_path is not None:
        raise ValueError("Cannot specify '--output' with '--type=all'")
    repo_root = _THIS_DIR.parent
    triples = read_rdf_csv(repo_root / "names.csv")

    generators = {
        "nicknames": lambda: generate_nicknames_sql(triples, out_path),
        "name_relationships": lambda: generate_name_relationships_sql(
            triples, out_path
        ),
    }

    if typ == "all":
        generators["nicknames"]()
        generators["name_relationships"]()
    else:
        generators[typ]()


def parse_argv(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type",
        choices=["nicknames", "normalized", "all"],
        help="The type of SQL to generate",
        default="all",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="The file to write the SQL to. Defaults are per-type.",
        default=None,
    )
    args = parser.parse_args(argv)
    if args.type == "all" and args.output is not None:
        raise ValueError("Cannot specify '--output' with '--type=all'")
    return args


def read_rdf_csv(file_name: str) -> list[tuple[str, str, str]]:
    with open(file_name) as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        return [(name1, relationship, name2) for name1, relationship, name2 in reader]


def generate_nicknames_sql(
    triples: list[tuple[str, str, str]], out_path: Path | None = None
):
    if out_path is None:
        out_path = _THIS_DIR / "create_nicknames.sql"

    rows = triples_to_rows(triples)
    max_nicknames = max(len(row) - 1 for row in rows) if rows else 0

    column_sql = ",\n".join(
        f"  nickname_{i + 1} varchar(255)" for i in range(max_nicknames)
    )
    insert_sql = "\n".join(insert_statement("nicknames", row) for row in rows)
    sql = f"""\
-- This creation script should work in most flavors of SQL.
-- Logically, canonical_name is a primary key although no
-- constraint or index is included.
create table nicknames (
canonical_name varchar(255),
{column_sql}
);
-- These insert statements are verbose, but they could not be simpler to use.
{insert_sql}
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(sql)


def generate_name_relationships_sql(
    triples: list[tuple[str, str, str]], out_path: Path | None = None
):
    if out_path is None:
        out_path = _THIS_DIR / "create_name_relationships.sql"

    insert_sql = "\n".join(
        insert_statement("name_relationships", values=t) for t in triples
    )
    sql = f"""\
-- This creation script should work in most flavors of SQL.
create table name_relationships (
name1 varchar(255),
relationship varchar(100),
name2 varchar(255)
);
-- These insert statements are verbose, but they could not be simpler to use.
{insert_sql}
"""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(sql)


def triples_to_rows(triples: list[tuple[str, str, str]]) -> list[list[str]]:
    nickname_map: dict[str, list[str]] = {}
    for canonical, relationship, nickname in triples:
        if relationship == "has_nickname":
            if canonical not in nickname_map:
                nickname_map[canonical] = []
            nickname_map[canonical].append(nickname)
    return [
        [canonical, *nicknames] for canonical, nicknames in sorted(nickname_map.items())
    ]


def insert_statement(table_name: str, values: list[str]) -> str:
    quoted_values = [f"'{v}'" for v in values]
    v = ", ".join(quoted_values)
    return f"insert into {table_name} values ({v});"


if __name__ == "__main__":
    cli(sys.argv[1:])
