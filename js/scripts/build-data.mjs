// Reads ../names.csv and generates src/data.ts with embedded name data.

import { readFileSync, writeFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const csvPath = resolve(__dirname, "../../names.csv");
const outPath = resolve(__dirname, "../src/data.ts");

const csv = readFileSync(csvPath, "utf-8");
const rows = csv
  .split("\n")
  .map((line) => line.trim())
  .filter((line) => line.length > 0)
  .slice(1)
  .map((line) => line.split(",").map((name) => name.trim()))

const json = "[\n" + rows.map((row) => `  ${JSON.stringify(row)}`).join(",\n") + "\n]";

const output = `// Auto-generated from names.csv — do not edit by hand.
// Regenerate with: npm run build:data

import { NameTriple } from "./types";

/**
 * Semantic triples of eg ("robert","has_nickname","bob").
 * 
 * You can use this as a base before passing to a NickNamer instance, eg
 * \`\`\`typescript
 * import { NickNamer, defaultNamesData } from "nicknames-curated";
 * 
 * const withMyData = [...defaultNamesData(), ["samantha", "has_nickname", "sam"]];
 * const nickNamer = new NickNamer(withMyData);
 * \`\`\`
 */
const DEFAULT_NAMES_DATA: Array<NameTriple> = ${json};

export const defaultNamesData = (): Array<NameTriple> =>
  DEFAULT_NAMES_DATA.map((triple) => [triple[0], triple[1], triple[2]]);
`;

writeFileSync(outPath, output, "utf-8");
console.log(`Generated src/data.ts with ${rows.length} name groups.`);
