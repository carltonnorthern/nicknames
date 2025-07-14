# Changelog

## [1.0.0] - 2025-07-14

### Changed

- Switched from a "wide" format in names.csv of `aaron, erin, ron, ronnie`
  to a "long" format with semantic triplets of
  `aaron, has_nickname, erin`
  `aaron, has_nickname, ron`
  `aaron, has_nickname, ronnie`
  This allows for describing other relationships besides canonical/nickname,
  such as translations.
  It also is more machine-readable, and has better diffs.
  See https://github.com/carltonnorthern/nicknames/pull/71#issuecomment-2176778678
  for more details.
- python: moved default_lookup() to be a class method of NickNamer, eg
  now use `NickNamer.default_lookup()`
- sql: renamed the generated tables names from `names` to `nicknames`
  and `names_normalized` to `name_relationships`.

### Removed

- I removed the perl, java, and R bindings. They were not maintained,
  I don't want to have to maintain them, and they are easy enough to generate
  with AI at this point.
- python: removed `load_resource()` function.
  Use `with_names_csv_path()` or `name_relationships()` instead.
- python: removed python 3.7 support. I will roughly follow the python
  [end-of-life schedule](https://peps.python.org/topic/release/).

### Added

- python: added `with_names_csv_path()` and `name_relationships()` for
  lower-level access to the CSV file, eg for loading into a database.