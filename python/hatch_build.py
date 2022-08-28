"""Copies the root names.csv into the python package so it is included as a data file.

If you ever change names.csv, you will need to re-run this by deleting and
re-creating the hatch environment with
```
hatch env prune
hatch shell
```

This is maybe a little clunky, but I couldn't find an easier way to do it, because
most of the supported workflows assume that the data files live INSIDE the python
package. But in our case, we want to keep the data file at the root so the other
languages can share it.

If the data file was inside the package, it would be quite
simple:
[tool.hatch.build.force-include]
"src/data" = "mypackage/data"

but this method didn't work with editable installs. See
https://stackoverflow.com/q/73466480/5156887

This post https://stackoverflow.com/q/61624018/5156887
makes it seem like a custom setuptools script is the only way. So that's what I did,
but using hatch.
"""
import shutil

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        shutil.copyfile("../names.csv", "./src/us_nicknames/names.csv")
