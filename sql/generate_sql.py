"""Script to auto-generate SQL scripts from the canonical CSV file."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Iterable

_THIS_DIR = Path(__file__).parent


def cli(argv: list[str]):
    args = parse_argv(argv)
    generate_sql(args.type, args.output)


def generate_sql(typ: str = "all", out_path: Path | None = None):
    if typ == "all" and out_path is not None:
        raise ValueError("Cannot specify '--output' with '--type=all'")
    repo_root = _THIS_DIR.parent
    max_nicknames, rows = read_csv(repo_root / "names.csv")
    builders: dict[str, list[BaseBuilder]] = {
        "nicknames": [NicknamesBuilder(out_path)],
        "normalized": [NormalizedBuilder(out_path)],
    }
    builders["all"] = builders["nicknames"] + builders["normalized"]
    for builder in builders[typ]:
        builder.build(max_nicknames, rows)


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


def read_csv(file_name: str) -> tuple[int, list[list[str]]]:
    with open(file_name) as f:
        r = csv.reader(f)
        rows = [row for row in r]
    max_nicknames = max(len(row) for row in rows) - 1
    return max_nicknames, rows


class BaseBuilder:
    DEFAULT_OUT_PATH: Path
    table_name: str
    template: str

    def __init__(self, out_path: Path | None = None):
        if out_path is None:
            out_path = self.DEFAULT_OUT_PATH
        self.output_file = Path(out_path)

    def build(self, max_nicknames: int, rows: list[list[str]]):
        sql = self._make_sql(max_nicknames, rows)
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.output_file.write_text(sql)

    def _make_sql(self, max_nicknames: int, rows: list[list[str]]) -> str:
        create_statement = self._create_statement(max_nicknames)
        insert_statements = self._insert_statements(rows)
        return self.template.format(
            create_statement=create_statement,
            insert_statements=insert_statements,
        )

    def _create_statement(self, max_nicknames: int) -> str:
        raise NotImplementedError

    def _insert_statements(self, rows: list[list[str]]) -> str:
        raise NotImplementedError

    def _format_insert_statement(self, fields: list[str], values: list[str]) -> str:
        quoted_values = [f"'{v}'" for v in values]
        v = ", ".join(quoted_values)
        f = ", ".join(fields)
        return f"insert into {self.table_name} ({f}) values ({v});"


class NicknamesBuilder(BaseBuilder):
    DEFAULT_OUT_PATH = _THIS_DIR / "names.sql"
    table_name = "nicknames"
    template = """\
-- This creation script should work in most flavors of SQL.
-- Logically, canonical_name is a primary key although no
-- constraint or index is included.
{create_statement}
-- These insert statements are verbose, but they could not be simpler to use.
{insert_statements}
"""

    def _create_statement(self, max_nicknames: int) -> str:
        sql = f"create table {self.table_name} (\n"
        sql += "  canonical_name varchar(255),\n"
        for i in range(max_nicknames):
            sql += f"  nickname_{i+1} varchar(255)"
            if i < max_nicknames - 1:
                sql += ","
            sql += "\n"
        sql += ");"
        return sql

    def _insert_statements(self, rows: list[list[str]]) -> str:
        return "\n".join(self._one_row_insert_statement(row) for row in rows)

    def _one_row_insert_statement(self, row: list[str]) -> str:
        n_nicknames = len(row) - 1
        field_names = ["canonical_name"] + [
            f"nickname_{i+1}" for i in range(n_nicknames)
        ]
        return self._format_insert_statement(field_names, row)


class NormalizedBuilder(BaseBuilder):
    DEFAULT_OUT_PATH = _THIS_DIR / "names_normalized.sql"
    table_name = "nicknames_normalized"
    template = """\
-- This creation script should work in most flavors of SQL.
{create_statement}
-- These insert statements are verbose, but they could not be simpler to use.
{insert_statements}
"""

    def _create_statement(self, max_nicknames: int) -> str:
        return f"""\
create table {self.table_name} (
  canonical_name varchar(255),
  nickname varchar(255)
);"""

    def _insert_statements(self, rows: list[list[str]]) -> str:
        statements = (s for row in rows for s in self._one_row_insert_statements(row))
        return "\n".join(statements)

    def _one_row_insert_statements(self, row: list[str]) -> Iterable[str]:
        canonical, *nicknames = row
        fields = ["canonical_name", "nickname"]
        for nickname in nicknames:
            vals = [canonical, nickname]
            yield self._format_insert_statement(fields, vals)


if __name__ == "__main__":
    cli(sys.argv[1:])
