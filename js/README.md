# nicknames-curated

A JavaScript/TypeScript library for looking up nicknames and diminutive names for US given names.

## Installation

```bash
npm install nicknames-curated
```

## Usage

```typescript
import { NickNamer } from "nicknames-curated";

const nickNamer = new NickNamer();
nickNamer.nicknamesOf("nicholas"); // Set { "nick", "nik", ... }
nickNamer.nicknamesOf("NICHOLAS"); // Set { "nick", "nik", ... }
nickNamer.nicknamesOf("not a Name"); // empty set
nickNamer.canonicalsOf("bob"); // Set {"robert", ...}
```

### Using Custom Data

You can pass in your own data or merge with the default dataset:

```typescript
import { NickNamer, defaultNamesData } from "nicknames-curated";

const customData = [
    ...defaultNamesData(),
  ["elizabeth", "has_nickname", "liz"],
];
const nickNamer = new NickNamer(customData);
```

## About

This package is a JavaScript binding for the [nicknames project](https://github.com/carltonnorthern/nicknames), which contains a hand-curated CSV file of English given names and their associated nicknames.

For more details about the dataset, relationship types, and other language bindings (Python, SQL), see the [main repository](https://github.com/carltonnorthern/nicknames).
