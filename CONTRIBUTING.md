# Contributing

## Repository structure

- `names.csv` — the source data (one row per name group, comma-separated)
- `python/` — the `nicknames` python package
- `js/` — the `nicknames-curated` npm package (TypeScript)

## JavaScript / TypeScript package (`js/`)

### Prerequisites

- Node.js >= 18
- npm

### Setup

```bash
cd js
npm install
```

### Building

The build has two stages:

1. **Generate data** — reads `../names.csv` and produces `src/data.ts`
2. **Compile** — tsup bundles the TypeScript into CJS + ESM with type declarations

Run both with:

```bash
npm run build
```

Or run just the data generation step:

```bash
npm run build:data
```

### Testing

```bash
npm test
```

### After changing `names.csv`

If you modify `names.csv`, regenerate the JS data file and re-run tests:

```bash
cd js
npm run build:data
npm test
```

### Publishing to npm

1. Make sure you are logged in: `npm login`
2. Update the version in `js/package.json`
3. From the `js/` directory:

```bash
npm publish
```

`prepublishOnly` runs the full build automatically before publishing.
