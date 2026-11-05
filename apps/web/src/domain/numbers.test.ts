import { describe, expect, it } from "vitest";
import { bitwiseOperation, convertInteger, formatInteger, parseInteger } from "./numbers";

describe("numeric domain", () => {
  it("converts decimal values across bases", () => {
    expect(convertInteger("255", 10)).toEqual({
      2: "0b11111111",
      8: "0o377",
      10: "255",
      16: "0xFF"
    });
  });

  it("parses prefixed hexadecimal and preserves integers beyond JavaScript safe-number range", () => {
    expect(parseInteger("FF", 16)).toBe(255n);
    expect(parseInteger("0xFF", 16)).toBe(255n);
    expect(parseInteger("0b1010", 2)).toBe(10n);
    expect(parseInteger("9007199254740993", 10)).toBe(9007199254740993n);
  });

  it("accepts separators only between valid digits", () => {
    expect(parseInteger("  1111_0000  ", 2)).toBe(240n);
    expect(parseInteger("-A_B", 16)).toBe(-171n);
    for (const invalid of ["_10", "10_", "1__0", "1_A", "+", "--1"]) {
      expect(() => parseInteger(invalid, 2)).toThrow();
    }
  });

  it("rejects digits outside the selected base", () => {
    expect(() => parseInteger("102", 2)).toThrow();
    expect(() => parseInteger("8", 8)).toThrow();
    expect(() => parseInteger("0x10", 2)).toThrow();
  });

  it("validates runtime base values and input types", () => {
    expect(() => parseInteger("10", 3 as never)).toThrow();
    expect(() => parseInteger(10 as never, 10)).toThrow();
    expect(() => formatInteger(10n, 3 as never)).toThrow();
  });

  it("round-trips signed values in every supported base", () => {
    for (const base of [2, 8, 10, 16] as const) {
      for (const value of [0n, 1n, -1n, 255n, -255n, 9007199254740993n]) {
        expect(parseInteger(formatInteger(value, base), base)).toBe(value);
      }
    }
  });

  it("executes bounded bitwise operations", () => {
    expect(bitwiseOperation(0b1100n, "&", 0b1010n)).toBe(0b1000n);
    expect(bitwiseOperation(0b1100n, "|", 0b1010n)).toBe(0b1110n);
    expect(bitwiseOperation(0b1100n, "^", 0b1010n)).toBe(0b0110n);
    expect(bitwiseOperation(3n, "<<", 2n)).toBe(12n);
    expect(() => bitwiseOperation(1n, "<<", 4097n)).toThrow();
    expect(() => bitwiseOperation(1n, "invalid" as never, 1n)).toThrow();
  });
});
