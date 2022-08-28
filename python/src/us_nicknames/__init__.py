from __future__ import annotations

import collections
import csv
from importlib.resources import path
from io import StringIO, TextIOBase
from pathlib import Path
from typing import Dict, Set, Union

from us_nicknames._version import __version__  # noqa: F401

DEFAULT_NICKNAME_RESOURCE = path(__package__, "names.csv")

_LookupTable = Dict[str, Set[str]]

_FileLike = Union[str, Path, TextIOBase]


class NameDenormalizer:
    def __init__(self, lookup: _LookupTable | _FileLike | None = None) -> None:
        """Create a NameDenormalizer. Either uses the default file, or a custom file.

        `lookup` can be a

        - mapping, where keys are names, and values are all the names
          that are interchangeable for that key. For example,
          {
            "alex": {"alexa", "alexander"},
            "alexa": {"alex"},
            "alexander": {"alex"},
           }
        - CSV file path or file-like, with each row containing a
          set of names that are all interchangeable. For example,
          "alexa,alex\nalexander,alex".


        >>> denormer = NameDenormalizer()
        >>> assert denormer["alex"] == {"alexa", "alexander"}

        >>> mapping = {
        >>>     "alex": {"alexa", "alexander"},
        >>>     "alexa": {"alex"},
        >>>     "alexander": {"alex"},
        >>> }
        >>> denormer = NameDenormalizer(mapping)
        >>> assert denormer["alex"] == {"alexa", "alexander"}

        >>> denormer = NameDenormalizer("names.csv")
        >>> assert denormer["alex"] == {"alexa", "alexander"}

        >>> with open("names.csv") as f:
        ...     denormer = NameDenormalizer.from_file(f)
        ...
        >>> assert denormer["alex"] == {"alexa", "alexander"}
        """
        if lookup is None:
            lookup = self.load_lookup()
        elif isinstance(lookup, (str, Path, TextIOBase)):
            lookup = self.load_lookup(lookup)
        self.lookup = lookup

    def __getitem__(self, name: str) -> Set[str]:
        """Look up all the possible nicknames for a name. Case-insensitive.

        Raises KeyError if the name is not in the lookup table.

        >>> denormer = NameDenormalizer()
        >>> assert denormer["alex"] == {"alexa", "alexander"}
        """
        name = name.lower()
        names = self.lookup[name]
        names = names.copy()
        return names

    def get(self, name: str, default=None):
        """Similar to __getitem__, but returns `default` if the name is not found."""
        try:
            return self[name]
        except KeyError:
            return default

    @staticmethod
    def _lookup_from_filelike(file: StringIO) -> _LookupTable:
        lookup = collections.defaultdict(set)
        for line in csv.reader(file):
            names = {name.lower() for name in line}
            for name in names:
                lookup[name].update(names)

        # Don't include the original name in the results.
        lookup = {name: lookup[name] - {name} for name in lookup}
        # Remove empty sets
        lookup = {name: lookup[name] for name in lookup if lookup[name]}
        return lookup

    @classmethod
    def load_lookup(cls, filename: _FileLike | None = None) -> _LookupTable:
        """Load a lookup table from a CSV file path or file-like, or use the default.

        >>> denormer = NameDenormalizer.from_file("names.csv")
        >>> assert denormer["alex"] == {"alexa", "alexander"}

        >>> with open("names.csv") as f:
        ...     denormer = NameDenormalizer.from_file(f)
        ...
        >>> assert denormer["alex"] == {"alexa", "alexander"}
        """
        if filename is None:
            with DEFAULT_NICKNAME_RESOURCE as f:
                return cls.load_lookup(f)
        try:
            filename = Path(filename)
        except TypeError:
            return cls._lookup_from_filelike(filename)
        with filename.open("r") as f:
            return cls._lookup_from_filelike(f)
