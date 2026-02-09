# nicknames-curated

A JavaScript/TypeScript library for looking up nicknames and diminutive names for US given names.

## Installation

Install from [npm](https://www.npmjs.com/package/nicknames-curated):

```bash
npm install nicknames-curated
```

## Usage

```typescript
import { NickNamer } from "nicknames-curated";

const nn = new NickNamer();

// Get the nicknames for a given name as a Set of strings
const nicks = nn.nicknamesOf("alexander");
console.log(nicks.has("al")); // true
console.log(nicks.has("alex")); // true

// Note that the relationship isn't symmetric: al is a nickname for alexander,
// but alexander is not a nickname for al.
console.log(nn.nicknamesOf("al").has("alexander")); // false

// Capitalization is ignored and leading and trailing whitespace is ignored
console.log(nn.nicknamesOf("alexander").size === nn.nicknamesOf(" ALEXANDER ").size); // true

// Queries that aren't found return an empty set
console.log(nn.nicknamesOf("not a name").size); // 0

// The other useful thing is to go the other way, nickname to canonical:
// It acts very similarly to nicknamesOf.
const can = nn.canonicalsOf("al");
console.log(can.has("alexander")); // true
console.log(can.has("alex")); // false (alex is also a nickname, not canonical)

console.log(nn.canonicalsOf("alexander").has("al")); // false

// You can combine these to see if two names are interchangeable:
const union = new Set([...nn.nicknamesOf("al"), ...nn.canonicalsOf("al")]);
const areInterchangeable = union.has("alexander"); // true
```

### Using Custom Data

You can pass in your own data or merge with the default dataset:

```typescript
import { NickNamer, defaultNamesData } from "nicknames-curated";

const customData = [
    ...defaultNamesData(),
  ["elizabeth", "has_nickname", "liz"],
];
const nn = new NickNamer(customData);
```

## About

This package is a JavaScript binding for the [nicknames project](https://github.com/carltonnorthern/nicknames), which contains a hand-curated CSV file of English given names and their associated nicknames.

For more details about the dataset, relationship types, and other language bindings (Python, SQL), see the [main repository](https://github.com/carltonnorthern/nicknames).
