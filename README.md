[![CI](https://github.com/carltonnorthern/nicknames/actions/workflows/ci.yml/badge.svg)](https://github.com/carltonnorthern/nicknames/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/nicknames.svg)](https://badge.fury.io/py/nicknames)

# Nicknames

A hand-curated CSV file ([names.csv](./names.csv)) containing English given names (first names) and
their associated nicknames. There are Python and SQL bindings provided for convenience.

This currently contains roughly 1100 canonical names.
Any help from people to clean or add to it is greatly appreciated.
We store the names in [semantic triplets](https://en.wikipedia.org/wiki/Semantic_triple) of (name1, relationship, name2), for example
`("alexander", "has_nickname", "alex")` or `("alexander", "is_translation_of:en-sp", "alejandro")`.
As of July 2025, we only store the `has_nickname` relationship, but if you
want to add more relationships, please open a pull request (or file an issue first
if it is a lot of work to confirm that you are heading in the right direction).

This lookup file was initially created by mining this
[genealogy page](https://www.caagri.org/nicknames.html) from the
*Center for African American Research, Inc*.
Because the lookup originates from a dataset used for genealogy purposes there
are old names that aren't commonly used these days, but there are recent ones
as well. Examples are "gregory", "greg", or "geoffrey", "geoff". There was also
a significant effort to make it machine readable, i.e. separate it with commas,
remove human conventions like "rickie(y)" would need to be made into two
different names "rickie", and "ricky". Due to the source of the original data,
the dataset is heavily biased towards traditionally African American names.
Names from other groups may or may not be present.

This project was created by [Old Dominion University](https://www.odu.edu/) -
[Web Science and Digital Libraries Research Group](http://ws-dl.blogspot.com/).
More information about the creation of this lookup can be found on this
[blog post about the creation of this library](https://ws-dl.blogspot.com/2010/08/lookup-for-nicknames-and-diminutive.html)

## SQL API

See the [sql/](./sql/) directory.

## Python API

The Python parser is available on PyPI from

```bash
pip install nicknames
```

and then you can do:

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
