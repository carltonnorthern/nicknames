# nickname-and-diminutive-names-lookup
A simple CSV file containing US given names (first name) and their associated nicknames or diminutive names.

This lookup file was initially created by mining this
<a href="http://www.caagri.org/nicknames.html">genealogy page</a>. Because the lookup originates from a dataset used for genealogy purposes there are old names that aren't commonly used these days, but there are recent ones as well. Examples are "gregory", "greg", or "geoffrey", "geoff". There was also a significant effort to make it machine readable, i.e. separate it with commas, remove human conventions like "rickie(y)" would need to be made into two different names "rickie", and "ricky".

There are Java, Perl, Python, and R parsers provided for convenience.

This is a relatively large list with roughly 1600 names. Any help from people to clean this list up and add to it is greatly appreciated.

This project was created by <a href="http://www.odu.edu/">Old Dominion University</a> - <a href="http://ws-dl.blogspot.com/">Web Science and Digital Libraries Research Group</a>. More information about the creation of this lookup can be found <a href="https://ws-dl.blogspot.com/2010/08/lookup-for-nicknames-and-diminutive.html">here</a>.

## Python API

The Python parser is available on PyPI from

```bash
pip install us-nicknames
```

and then you can do:

```python
from us_nicknames import NameDenormalizer

# Either use the included names.csv
denormer = NameDenormalizer()
# Or create from your own dataset
mapping = {
    "alex": {"alexa", "alexander"},
    "alexa": {"alex"},
    "alexander": {"alex"},
}
# denormer = NameDenormalizer("my_names.csv")
# denormer = NameDenormalizer.from_file(io.StringIO("alex,alexander"))

# Lookup a name. Return a set of strings. Note that the original name is not included.
assert denormer["aaron"] == {"ron", "erin", "ronnie"}
# Lookup is not case sensitive. Results are always lowercase.
assert denormer["AARON"] == {"ron", "erin", "ronnie"}

# Lookup on a missing name raises KeyError
try:
    denormer["missing"]
except KeyError:
    pass
# Use `.get` to handle missing names, like dict.get()
assert denormer.get("missing") is None
assert denormer.get("missing", "oops") == "oops"
```
