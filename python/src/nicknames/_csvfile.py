import csv
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List, Literal, NamedTuple

try:
    from importlib.resources import as_file, files

    # This is the new way, but it's not available in Python 3.9+
    @contextmanager
    def with_resource(package: str, resource: str) -> Generator[Path, None, None]:
        """
        Load a resource from a package. Returns a context manager that yields a Path.
        """
        with as_file(files(package).joinpath(resource)) as f:
            yield f

except ImportError:
    from importlib.resources import path

    # This is the old way, deprecated starting in Python 3.11
    @contextmanager
    def with_resource(package: str, resource: str) -> Generator[Path, None, None]:
        """
        Load a resource from a package. Returns a context manager that yields a Path.
        """
        with path(package, resource) as f:
            yield f


@contextmanager
def with_names_csv_path() -> Generator[Path, None, None]:
    """
    Context manager for the names.csv file.

    This is a low-level function if you want to read the CSV file directly.
    You may be better off using the higher-level `NickNamer()` class or the
    `name_triplets()` function.

    Examples
    --------
    >>> import nicknames
    >>> with nicknames.with_names_csv_path() as path:
    ...     for line in path.read_text().splitlines()[:4]:
    ...         print(line)
    name1,relationship,name2
    aaron,has_nickname,erin
    aaron,has_nickname,ron
    aaron,has_nickname,ronnie

    Load into a database:

    >>> import duckdb  # doctest: +SKIP
    >>> con = duckdb.connect("my_database.duckdb") # doctest: +SKIP
    >>> with nicknames.with_names_csv_path() as path: # doctest: +SKIP
    ...     con.execute(f"CREATE TABLE names AS (SELECT * FROM read_csv_auto('{path}'))") # doctest: +SKIP
    """  # noqa: E501
    with with_resource("nicknames", "names.csv") as f:
        yield f


RELATIONSHIPS = frozenset(
    [
        "has_nickname",
        "is_translation_of:en-sp",
    ]
)
RelationshipType = Literal[
    "has_nickname",
    "is_translation_of:en-sp",
]


class NameTriplet(NamedTuple):
    """Represents a relationship between names.

    eg
    - ("robert", "has_nickname", "bob")
    - ("robert", "is_translation_of:en-sp", "roberto")
    """

    name1: str
    relationship: RelationshipType
    name2: str


def name_triplets() -> List[NameTriplet]:
    """NameTriplet objects from the names.csv file.

    Example usage:
    >>> import nicknames
    >>> print(nicknames.name_triplets()[0])
    NameTriplet(name1='aaron', relationship='has_nickname', name2='erin')
    """
    relationships = []
    with with_names_csv_path() as path, open(path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            relationships.append(NameTriplet(*row))
    return relationships
