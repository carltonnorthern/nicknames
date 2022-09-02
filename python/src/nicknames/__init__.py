from __future__ import annotations

import csv
from importlib.resources import path
from pathlib import Path
from typing import Dict, Iterable, Set, Union

from nicknames._version import __version__  # noqa: F401

_LookupTable = Dict[str, Set[str]]
_PathLike = Union[str, Path]


class NickNamer:
    def __init__(
        self,
        *,
        nickname_lookup: _LookupTable | None = None,
        canonical_lookup: _LookupTable | None = None,
    ) -> None:
        """
        Create a NickNamer from lookup tables. If neither provided, the default is used.

        You probably want to use this with no arguments unless you know what
        you're doing. See the classmethods `from_csv` and `from_lines` if you need
        to parse your own custom data.

        >>> nn = NickNamer()
        >>> assert nn.nicknames_of("nicholas").issuperset({"nick", "nik"})
        >>> assert nn.canonicals_of("nick").issuperset({"nicholas", "nikolas"})
        """
        if canonical_lookup is None:
            if nickname_lookup is None:
                nickname_lookup = default_lookup()
            nickname_lookup = self._normalize_lookup(nickname_lookup)
            canonical_lookup = _inverted(nickname_lookup)
        else:
            canonical_lookup = self._normalize_lookup(canonical_lookup)
            if nickname_lookup is None:
                nickname_lookup = _inverted(canonical_lookup)
            else:
                nickname_lookup = self._normalize_lookup(nickname_lookup)
        self._nickname_lookup = nickname_lookup
        self._canonical_lookup = canonical_lookup

    def nicknames_of(self, name: str) -> set[str]:
        """Returns a set of all the nicknames for a name.

        Case-insensitive. Ignores leading and trailing whitespace.

        Results are always lowercase and have no leading or trailing whitespace.

        >>> nn = NickNamer()
        >>> assert nn.nicknames_of("nicholas").issuperset({"nick", "nik"})
        >>> assert "nicholas" not in nn.nicknames_of("nick")
        >>> assert nn.nicknames_of("nicholas") == nn.nicknames_of(" NICHOLAS ")
        >>> assert nn.nicknames_of("not a name") == set()
        """
        return self._get(name, self._nickname_lookup)

    def canonicals_of(self, name: str) -> set[str]:
        """Returns a set of all the canonical names for a name.

        Case-insensitive. Ignores leading and trailing whitespace.

        Results are always lowercase and have no leading or trailing whitespace.

        >>> nn = NickNamer()
        >>> assert nn.canonicals_of("nick").issuperset({"nicholas", "nikolas"})
        >>> assert "nick" not in n.canonicals_of("nicholas")
        >>> assert nn.canonicals_of("nick") == nn.canonicals_of(" NICK ")
        >>> assert nn.canonicals_of("not a name") == set()
        """
        return self._get(name, self._canonical_lookup)

    @classmethod
    def from_lines(cls, lines: Iterable[Iterable[str]]) -> NickNamer:
        """Load from an iterable of lines, where each line is an iterable of names.

        The first name in each line is the canonical name, and the rest are nicknames
        for that name.

        >>> lines = [
        >>>     ["alex", "al"],
        >>>     ["alexa", "al", "alex"],
        >>>     ["alexander", "al", "alex"],
        >>> ]
        >>> nn = NickNamer.from_lines(lines)
        >>> assert nn.nicknames_of("alex") == {"al"}
        >>> assert nn.nicknames_of("alexa") == {"al", "alex"}
        >>> assert nn.nicknames_of("al") == {}
        >>> assert nn.canonicals_of("alex") == {"alexa", "alexander"}
        >>> assert nn.canonicals_of("alexander") == {}
        """
        nickname_lookup = _lookup_from_lines(lines)
        return cls(nickname_lookup=nickname_lookup)

    @classmethod
    def from_csv(cls, path: _PathLike, reader_kwargs={}) -> NickNamer:
        """Load a NickNamer from a CSV file. See `from_lines` for details.

        >>> nn = NickNamer.from_csv("my_names.csv")
        """
        nickname_lookup = _lookup_from_csv(path, reader_kwargs=reader_kwargs)
        return cls(nickname_lookup=nickname_lookup)

    def _get(self, name: str, lookup: _LookupTable):
        name = self._normalize_name(name)
        try:
            result = lookup[name]
        except KeyError:
            return set()
        return result.copy()

    def _normalize_name(self, name: str) -> str:
        """Override this in a subclass to change how names are normalized."""
        return name.lower().strip()

    def _normalize_lookup(self, lookup: _LookupTable) -> _LookupTable:
        return {
            self._normalize_name(k): {self._normalize_name(v) for v in vs}
            for k, vs in lookup.items()
        }


def default_lookup() -> dict[str, set[str]]:
    """Returns the default lookup table, mapping canonical names to sets of nicknames.

    All names are lowercase and have no leading or trailing whitespace.

    You could use this to tweak the default lookup table:

    >>> lookup = default_nicknames_lookup()
    >>> del lookup["alexander]
    >>> nn = NickNamer(nickname_lookup=lookup)
    >>> assert nn.nicknames_of("alexander") == set()
    """
    with path(__package__, "names.csv") as f:
        return _lookup_from_csv(f)


def _lookup_from_csv(path: _PathLike, reader_kwargs={}) -> _LookupTable:
    path = Path(path)
    with path.open("r") as f:
        lines = csv.reader(f, **reader_kwargs)
        return _lookup_from_lines(lines)


def _lookup_from_lines(lines: Iterable[Iterable[str]]) -> _LookupTable:
    nicknames_of = {}
    for line in lines:
        if len(line) < 2:
            raise ValueError(
                "Each line must have one canonical name and at least one nickname"
            )
        line = [name.lower() for name in line]
        canonical, nicknames = line[0], set(line[1:])
        if canonical in nicknames:
            raise ValueError(f"{canonical} is in the nicknames for itself")
        nicknames_of[canonical] = nicknames
    return nicknames_of


def _inverted(lookup: _LookupTable) -> _LookupTable:
    inverted = {}
    for k, v in lookup.items():
        for new_key in v:
            inverted.setdefault(new_key, set()).add(k)
    return inverted
