from io import StringIO
from pathlib import Path

import pytest

from us_nicknames import NameDenormalizer


@pytest.fixture
def csv_contents():
    return """
alexa,alex
alexander,alex
"""


@pytest.fixture
def csv_fileio(csv_contents):
    return StringIO(csv_contents)


@pytest.fixture
def csv_filename(tmp_path: Path, csv_contents):
    result = tmp_path / "names.csv"
    result.write_text(csv_contents)
    return result


@pytest.fixture
def lookup_table():
    return {
        "alex": {"alexa", "alexander"},
        "alexa": {"alex"},
        "alexander": {"alex"},
    }


@pytest.fixture
def denormer(lookup_table):
    return NameDenormalizer(lookup_table)


def test_basic(denormer):
    assert denormer["alex"] == {"alexa", "alexander"}
    assert denormer["ALEX"] == {"alexa", "alexander"}
    assert denormer["alexa"] == {"alex"}
    assert denormer["alexander"] == {"alex"}
    with pytest.raises(KeyError):
        denormer["not_present"]


def test_copied(denormer: NameDenormalizer):
    denormer["alex"].remove("alexa")
    assert denormer["alex"] == {"alexa", "alexander"}


def test_get(denormer: NameDenormalizer):
    assert denormer.get("not_present") is None
    assert denormer.get("not_present", "default") == "default"


def test_from_fileio(csv_fileio, lookup_table):
    denormer2 = NameDenormalizer(csv_fileio)
    assert denormer2.lookup == lookup_table


def test_from_file(csv_filename, lookup_table):
    denormer2 = NameDenormalizer(csv_filename)
    assert denormer2.lookup == lookup_table
    with pytest.raises(FileNotFoundError):
        NameDenormalizer("not_present.csv")


def test_default_load():
    denormer = NameDenormalizer()
    assert len(denormer.lookup) > 0
    assert isinstance(denormer.lookup, dict)
    assert "nick" in denormer["nicholas"]
