from __future__ import annotations

from pathlib import Path

import pytest
from nicknames import NickNamer, default_lookup


@pytest.fixture
def csv_contents():
    return """
alex,al
alexa,alex,al
alexander,alex,al
""".strip()


@pytest.fixture
def csv_filename(tmp_path: Path, csv_contents):
    result = tmp_path / "names.csv"
    result.write_text(csv_contents)
    return result


@pytest.fixture
def nickname_lookup():
    return {
        "alex": {"al"},
        "alexa": {"alex", "al"},
        "alexander": {"alex", "al"},
    }


@pytest.fixture
def nickname_lookup_messy():
    # Has leading and trailing whitespace and some uppercase
    return {
        "alex": {"AL"},
        "   alexa  ": {"alex", "al"},
        "alexander": {"alex", "al"},
    }


@pytest.fixture
def canonical_lookup():
    return {
        "al": {"alex", "alexa", "alexander"},
        "alex": {"alexa", "alexander"},
    }


@pytest.fixture
def nicknamer(nickname_lookup):
    return NickNamer(nickname_lookup=nickname_lookup)


def _assert_equal(a: NickNamer, b: NickNamer):
    assert a._nickname_lookup == b._nickname_lookup
    assert a._canonical_lookup == b._canonical_lookup


def test_constructor(nickname_lookup, canonical_lookup, nickname_lookup_messy):
    nn1 = NickNamer(nickname_lookup=nickname_lookup)
    nn2 = NickNamer(canonical_lookup=canonical_lookup)
    nn3 = NickNamer(nickname_lookup=nickname_lookup, canonical_lookup=canonical_lookup)
    nn4 = NickNamer(nickname_lookup=nickname_lookup_messy)
    _assert_equal(nn1, nn2)
    _assert_equal(nn1, nn3)
    _assert_equal(nn1, nn4)
    _assert_equal(nn2, nn3)
    _assert_equal(nn2, nn4)
    _assert_equal(nn3, nn4)

    # Positional arguments are not allowed to prevent accidental misuse
    with pytest.raises(TypeError):
        NickNamer(nickname_lookup)


def test_nicknames(nicknamer: NickNamer):
    assert nicknamer.nicknames_of("alex") == {"al"}
    assert nicknamer.nicknames_of("alexa") == {"alex", "al"}
    assert nicknamer.nicknames_of("alexander") == {"alex", "al"}
    assert nicknamer.nicknames_of("al") == set()


def test_canonicals(nicknamer: NickNamer):
    assert nicknamer.canonicals_of("alex") == {"alexa", "alexander"}
    assert nicknamer.canonicals_of("al") == {"alex", "alexa", "alexander"}
    assert nicknamer.canonicals_of("alexa") == set()
    assert nicknamer.canonicals_of("alexander") == set()


def test_copied(nicknamer: NickNamer):
    nicknamer.nicknames_of("alexa").remove("al")
    after = nicknamer.nicknames_of("alexa")
    assert after == {"alex", "al"}


@pytest.mark.parametrize("function", ["nicknames_of", "canonicals_of"])
def test_weird(nicknamer: NickNamer, function):
    func = getattr(nicknamer, function)
    assert func("ALEX") == func("alex")
    assert func("  alex\t") == func("alex")
    assert func("not_present") == set()
    with pytest.raises(AttributeError):
        func(1)


def test_from_lines(csv_contents: str, nicknamer: NickNamer):
    lines = [line.split(",") for line in csv_contents.splitlines()]
    result = NickNamer.from_lines(lines)
    _assert_equal(result, nicknamer)


def test_from_lines_bad():
    fine = ["alex, al"]

    canonical_in_nicknames = [fine, ["al", "alex", "al"]]
    with pytest.raises(ValueError):
        NickNamer.from_lines(canonical_in_nicknames)

    too_short = [fine, []]
    with pytest.raises(ValueError):
        NickNamer.from_lines(too_short)

    too_short = [fine, ["al"]]
    with pytest.raises(ValueError):
        NickNamer.from_lines(too_short)


def test_from_csv(csv_filename, nicknamer: NickNamer):
    result = NickNamer.from_csv(csv_filename)
    _assert_equal(result, nicknamer)

    with pytest.raises(FileNotFoundError):
        NickNamer.from_csv("not_present.csv")


def test_default_load():
    denormer = NickNamer()
    assert len(denormer._nickname_lookup) > 0
    assert isinstance(denormer._nickname_lookup, dict)
    assert len(denormer._canonical_lookup) > 0
    assert isinstance(denormer._canonical_lookup, dict)
    assert "nick" in denormer.nicknames_of("nicholas")


def test_default_load_twice():
    # Test for https://github.com/carltonnorthern/nicknames/issues/46
    NickNamer()
    NickNamer()


def test_default_lookup():
    lookup = default_lookup()
    assert isinstance(lookup, dict)
    assert len(lookup) > 0
    assert "nick" in lookup["nicholas"]
    assert "nick" not in lookup


def test_default_lookup_copied():
    # Check that the default lookup is not modified
    lookup = default_lookup()
    lookup_original = lookup.copy()
    lookup.clear()
    lookup2 = default_lookup()
    assert lookup2 == lookup_original
