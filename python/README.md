[![PyPI version](https://badge.fury.io/py/nicknames.svg)](https://badge.fury.io/py/nicknames)

# Nicknames

A hand-curated CSV file containing English given names (first names) and
their associated nicknames.

For more info on the source and format of the data, see https://github.com/carltonnorthern/nicknames.
In case that is useful to you, there are also SQL and typescript bindings there.

## Python API

The Python package is available on PyPI from

```bash
uv add nicknames
```

and then you can get to the csv data directly:

```python
from nicknames import name_triplets

# name_triplets() returns a list of a NamedTuples:
print(name_triplets()[:3])
# [NameTriplet(name1='aaron', relationship='has_nickname', name2='erin'), NameTriplet(name1='aaron', relationship='has_nickname', name2='ron'), NameTriplet(name1='aaron', relationship='has_nickname', name2='ronnie')]
```

Or, we have an NickNamer class which provides several convenience methods:

```python
from nicknames import NickNamer

nn = NickNamer()

# Get the nicknames for a given name as a set of strings
nicks = nn.nicknames_of("Alexander")
assert isinstance(nicks, set)
assert "al" in nicks
assert "alex" in nicks

# Note that the relationship isn't symmetric: al is a nickname for alexander,
# but alexander is not a nickname for al.
assert "alexander" not in nn.nicknames_of("al")

# Capitalization is ignored and leading and trailing whitespace is ignored
assert nn.nicknames_of("alexander") == nn.nicknames_of(" ALEXANDER ")

# Queries that aren't found return an empty set
assert nn.nicknames_of("not a name") == set()

# The other useful thing is to go the other way, nickname to canonical:
# It acts very similarly to nicknames_of.
can = nn.canonicals_of("al")
assert isinstance(can, set)
assert "alexander" in can
assert "alex" in can

assert "al" not in nn.canonicals_of("alexander")

# You can combine these to see if two names are interchangeable:
union = nn.nicknames_of("al") | nn.canonicals_of("al")
are_interchangeable = "alexander" in union
```

For more advanced usage, such as loading your own data, read the source code.