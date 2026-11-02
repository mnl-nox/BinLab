import { describe, expect, it } from "vitest";
import { bitwiseOperation, convertInteger, parseInteger } from "./numbers";

describe("numeric domain", () => {
  it("converts decimal values across bases", () => {
    expect(convertInteger("255", 10)).toEqual({
      2: "0b11111111",
      8: "0o377",
      10: "255",
      16: "0xFF"
    });
  });

  it("parses hexadecimal and preserves integers beyond JavaScript safe-number range", () => {
    expect(parseInteger("FF", 16)).toBe(255n);
    expect(parseInteger("9007199254740993", 10)).toBe(9007199254740993n);
  });

  it("rejects digits outside the selected base", () => {
    expect(() => parseInteger("102", 2)).toThrow();
  });

  it("executes bounded bitwise operations", () => {
    expect(bitwiseOperation(0b1100n, "&", 0b1010n)).toBe(0b1000n);
    expect(bitwiseOperation(3n, "<<", 2n)).toBe(12n);
    expect(() => bitwiseOperation(1n, "<<", 4097n)).toThrow();
  });
});