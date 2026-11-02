export type NumericBase = 2 | 8 | 10 | 16;

export function parseInteger(input: string, base: NumericBase): bigint {
  const normalized = input.trim().replaceAll("_", "");
  if (!normalized) throw new Error("Informe um valor.");
  const pattern: Record<NumericBase, RegExp> = {
    2: /^[+-]?[01]+$/,
    8: /^[+-]?[0-7]+$/,
    10: /^[+-]?\d+$/,
    16: /^[+-]?[\da-fA-F]+$/
  };
  if (!pattern[base].test(normalized)) throw new Error(`Valor inválido para a base ${base}.`);

  const negative = normalized.startsWith("-");
  const digits = normalized.replace(/^[+-]/, "").toLowerCase();
  let value = 0n;
  for (const char of digits) value = value * BigInt(base) + BigInt(parseInt(char, 16));
  return negative ? -value : value;
}

export function formatInteger(value: bigint, base: NumericBase): string {
  const prefix = base === 2 ? "0b" : base === 8 ? "0o" : base === 16 ? "0x" : "";
  const digits = (value < 0n ? -value : value).toString(base).toUpperCase();
  return `${value < 0n ? "-" : ""}${prefix}${digits}`;
}

export function convertInteger(input: string, source: NumericBase): Record<NumericBase, string> {
  const value = parseInteger(input, source);
  return { 2: formatInteger(value, 2), 8: formatInteger(value, 8), 10: formatInteger(value, 10), 16: formatInteger(value, 16) };
}

export function bitwiseOperation(a: bigint, operator: "&" | "|" | "^" | "<<", b: bigint): bigint {
  if (b < 0n || b > 4096n) throw new Error("Deslocamento deve estar entre 0 e 4096.");
  if (operator === "<<") return a << b;
  if (operator === "&") return a & b;
  if (operator === "|") return a | b;
  return a ^ b;
}