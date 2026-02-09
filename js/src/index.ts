import { defaultNamesData } from "./data";
import { Relationship, NameTriple, RELATIONSHIPS } from "./types";

export {
  defaultNamesData,
  RELATIONSHIPS,
  type Relationship,
  type NameTriple,
};

/**
 * Lookup nicknames and canonical names for US given names.
 * 
 * If you don't pass in custom data, it uses the built-in dataset of
 * common US names and their nicknames from https://github.com/carltonnorthern/nicknames
 *
 * @example
 * ```typescript
 * import { NickNamer } from "nicknames-curated";
 *
 * const nickNamer = new NickNamer(withMyData);
 * nickNamer.nicknamesOf("nicholas"); // Set { "nick", "nik", ... }
 * ```
 * 
 * You can also pass in your own data, eg if you want to add more names or use a different dataset.
 * The data should be an array of triples of the form [canonical, "has_nickname", nickname].
 * You can merge your data with the default dataset by spreading defaultNamesData().
 * 
 * @example
 * ```typescript
 * import { NickNamer, defaultNamesData } from "nicknames-curated";
 *
 * const withMyData = [...defaultNamesData(), ["samantha", "has_nickname", "sam"]];
 * const nickNamer = new NickNamer(withMyData);
 * ```
 */
export class NickNamer {
  private nicknameMap: Map<string, Set<string>>;
  private canonicalMap: Map<string, Set<string>>;

  constructor(data?: ReadonlyArray<NameTriple>) {
    this.nicknameMap = new Map();
    this.canonicalMap = new Map();
    const namesData = data || defaultNamesData();
    for (const group of namesData) {
      const [canonical, relationship, nickname] = group;
      if (!RELATIONSHIPS.includes(relationship)) {
        throw new Error(`Invalid relationship: ${relationship}`);
      }
      const canonicalLower = canonical.toLowerCase();
      if (!this.nicknameMap.has(canonicalLower)) {
        this.nicknameMap.set(canonicalLower, new Set());
      }
      const nicknameLower = nickname.toLowerCase();
      this.nicknameMap.get(canonicalLower)!.add(nicknameLower);
      if (!this.canonicalMap.has(nicknameLower)) {
        this.canonicalMap.set(nicknameLower, new Set());
      }
      this.canonicalMap.get(nicknameLower)!.add(canonicalLower);
    }
  }

  /**
   * Returns a set of all the nicknames for a name.
   *
   * Case-insensitive. Ignores leading and trailing whitespace.
   * Results are always lowercase and have no leading or trailing whitespace.
   *
   * @example
   * ```ts
   * const nn = new NickNamer();
   * nn.nicknamesOf("nicholas"); // Set { "nick", "nik", ... }
   * nn.nicknamesOf("not a name"); // Set {}
   * ```
   */
  nicknamesOf(name: string): Set<string> {
    const key = name.toLowerCase().trim();
    const result = this.nicknameMap.get(key);
    return result ? new Set(result) : new Set();
  }

  /**
   * Returns a set of all the canonical names for a name.
   *
   * Case-insensitive. Ignores leading and trailing whitespace.
   * Results are always lowercase and have no leading or trailing whitespace.
   *
   * @example
   * ```ts
   * const nn = new NickNamer();
   * nn.canonicalsOf("nick"); // Set { "nicholas", "nikolas", ... }
   * nn.canonicalsOf("not a name"); // Set {}
   * ```
   */
  canonicalsOf(name: string): Set<string> {
    const key = name.toLowerCase().trim();
    const result = this.canonicalMap.get(key);
    return result ? new Set(result) : new Set();
  }
}
