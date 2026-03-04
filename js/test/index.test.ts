import { describe, it, expect } from "vitest";
import { NickNamer, defaultNamesData } from "../src/index";
import { NameTriple } from "../src/types";

describe("NickNamer", () => {
  const nn = new NickNamer();

  describe("nicknamesOf", () => {
    it("returns nicknames for a canonical name", () => {
      const result = nn.nicknamesOf("gregory");
      expect(result).toBeInstanceOf(Set);
      expect(result.has("greg")).toBe(true);
    });

    it("is case-insensitive", () => {
      const lower = nn.nicknamesOf("gregory");
      const upper = nn.nicknamesOf("GREGORY");
      const mixed = nn.nicknamesOf("Gregory");
      expect(lower).toEqual(upper);
      expect(lower).toEqual(mixed);
    });

    it("ignores leading and trailing whitespace", () => {
      const normal = nn.nicknamesOf("gregory");
      const spaces = nn.nicknamesOf("  gregory  ");
      expect(normal).toEqual(spaces);
    });

    it("returns empty set for an unknown name", () => {
      const result = nn.nicknamesOf("xyznotaname");
      expect(result).toBeInstanceOf(Set);
      expect(result.size).toBe(0);
    });

    it("does not include the input name in the result", () => {
      const result = nn.nicknamesOf("gregory");
      expect(result.has("gregory")).toBe(false);
    });
  });

  describe("canonicalsOf", () => {
    it("returns canonical names for a nickname", () => {
      const result = nn.canonicalsOf("greg");
      expect(result).toBeInstanceOf(Set);
      expect(result.has("gregory")).toBe(true);
    });

    it("is case-insensitive", () => {
      const lower = nn.canonicalsOf("greg");
      const upper = nn.canonicalsOf("GREG");
      const mixed = nn.canonicalsOf("Greg");
      expect(lower).toEqual(upper);
      expect(lower).toEqual(mixed);
    });

    it("ignores leading and trailing whitespace", () => {
      const normal = nn.canonicalsOf("greg");
      const spaces = nn.canonicalsOf("  greg  ");
      expect(normal).toEqual(spaces);
    });

    it("returns empty set for an unknown name", () => {
      const result = nn.canonicalsOf("xyznotaname");
      expect(result).toBeInstanceOf(Set);
      expect(result.size).toBe(0);
    });

    it("does not include the input name in the result", () => {
      const result = nn.canonicalsOf("greg");
      expect(result.has("greg")).toBe(false);
    });
  });

  describe("custom data", () => {
    it("accepts custom data in the constructor", () => {
      const customData: Array<NameTriple> = [
        ["samantha", "has_nickname", "sam"],
        ["samantha", "has_nickname", "sammie"],
      ];
      const customNn = new NickNamer(customData);
      const nicknames = customNn.nicknamesOf("samantha");
      expect(nicknames.has("sam")).toBe(true);
      expect(nicknames.has("sammie")).toBe(true);
    });

    it("works with merged default and custom data", () => {
      const customData: ReadonlyArray<NameTriple> = [...defaultNamesData() as Array<NameTriple>, ["xyzname", "has_nickname", "xyz"]];
      const mergedNn = new NickNamer(customData);
      expect(mergedNn.nicknamesOf("gregory").has("greg")).toBe(true);
      expect(mergedNn.nicknamesOf("xyzname").has("xyz")).toBe(true);
    });

    it("throws on an invalid relationship", () => {
      const invalidData = [
        ["samantha", "invalid_relationship", "sam"],
      ];
      // @ts-expect-error - testing invalid relationship
      expect(() => new NickNamer(invalidData)).toThrow("Invalid relationship");
    });
  });
});

describe("defaultNamesData", () => {
  it("returns a fresh copy each call", () => {
    const first = defaultNamesData() as Array<NameTriple>;
    first.push(["tempname", "has_nickname", "temp"]);
    const second = defaultNamesData() as Array<NameTriple>;
    const tempEntries = second.filter(([canonical]) => canonical === "tempname");
    expect(tempEntries.length).toBe(0);
  });
});

describe("typechecking", () => {
  it("rejects invalid relationship types", () => {
    const invalid: Array<NameTriple> = [
      // @ts-expect-error - invalid relationship literal
      ["samantha", "invalid_relationship", "sam"],
    ];
    expect(invalid.length).toBe(1);
  });
});