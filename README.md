[![CI](https://github.com/carltonnorthern/nicknames/actions/workflows/ci.yml/badge.svg)](https://github.com/carltonnorthern/nicknames/actions/workflows/ci.yml)

# Nicknames

A hand-curated CSV file ([names.csv](./names.csv)) containing English given names (first names) and
their associated nicknames. There are Python, TypeScript/javascript, and SQL bindings provided for convenience.

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

## Client Libraries

- **Python**: See the [python/](./python/) directory.
- **TypeScript/javascript**: See the [js/](./js/) directory.
- **SQL**: See the [sql/](./sql/) directory.
