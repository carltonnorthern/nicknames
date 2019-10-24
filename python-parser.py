import collections
import csv

class NameDenormalizer(object):
    def __init__(self, filename=None):
        filename = filename or 'names.csv'
        lookup = collections.defaultdict(list)
        with open(filename) as f:
            reader = csv.reader(f)
            for line in reader:
                matches = set(line)
                for match in matches:
                    lookup[match].append(matches)
        self.lookup = lookup

    def __getitem__(self, name):
        name = name.lower()
        if name not in self.lookup:
            raise KeyError(name)
        names = set().union(*self.lookup[name])
        if name in names:
            names.remove(name)
        return names

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default
