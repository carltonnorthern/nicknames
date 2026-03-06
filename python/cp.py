#!/usr/bin/env python3
import shutil
from pathlib import Path

HERE = Path(__file__).parent.absolute()
NAMES_CSV = HERE.parent / "names.csv"
DEST = HERE / "src" / "nicknames" / "names.csv"
print("Copying names.csv from", NAMES_CSV, "to", DEST)
shutil.copyfile(NAMES_CSV, DEST)
