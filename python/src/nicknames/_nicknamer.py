from __future__ import annotations

from typing import Dict, Iterable, Set

from nicknames._csvfile import NameTriplet, name_triplets

_LookupTable = Dict[str, Set[str]]


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
                nickname_lookup = self.default_lookup()
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

    @property
    def nickname_lookup(self) -> _LookupTable:
        """Returns the nickname lookup table."""
        return {k: set(v) for k, v in self._nickname_lookup.items()}

    @property
    def canonical_lookup(self) -> _LookupTable:
        """Returns the canonical lookup table."""
        return {k: set(v) for k, v in self._canonical_lookup.items()}

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
    def from_triplets(cls, lines: Iterable[NameTriplet]) -> NickNamer:
        """Load from an iterable of RDF triple lines.

        Each line should be in the format: (name1, relationship, name2)

        >>> lines = [
        >>>     ["alex", "has_nickname", "al"],
        >>>     ["alexander", "has_nickname", "al"],
        >>>     ["alexander", "has_nickname", "alex"],
        >>>     ["alexander", "is_translation_of:en-sp", "alejandro"],
        >>> ]
        >>> nn = NickNamer.from_lines(lines)
        >>> assert nn.nicknames_of("alex") == {"al"}
        >>> assert nn.nicknames_of("alexa") == {"al", "alex"}
        >>> assert nn.nicknames_of("al") == {}
        >>> assert nn.canonicals_of("alex") == {"alexa", "alexander"}
        >>> assert nn.canonicals_of("alexander") == {}
        """
        nickname_lookup = _lookup_from_triplets(lines)
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

    @classmethod
    def default_lookup(cls) -> _LookupTable:
        """The default lookup table, mapping canonical name to sets of nicknames.

        All names are lowercase and have no leading or trailing whitespace.

        You could use this to tweak the default lookup table:

        >>> lookup = NickNamer.default_lookup()
        >>> del lookup["alexander"]
        >>> nn = NickNamer(nickname_lookup=lookup)
        >>> assert nn.nicknames_of("alexander") == set()
        """
        return _lookup_from_triplets(name_triplets())


def _lookup_from_triplets(relationships: Iterable[NameTriplet]) -> _LookupTable:
    nicknames_of = {}
    for r in relationships:
        canonical, relationship, nickname = r
        if relationship != "has_nickname":
            continue
        if canonical not in nicknames_of:
            nicknames_of[canonical] = set()
        nicknames_of[canonical].add(nickname)
    return nicknames_of


def _inverted(lookup: _LookupTable) -> _LookupTable:
    inverted = {}
    for k, v in lookup.items():
        for new_key in v:
            inverted.setdefault(new_key, set()).add(k)
    return inverted
