export type NumericBase = 2 | 8 | 10 | 16;
export type BitwiseOperator = "&" | "|" | "^" | "<<";

const MAX_INPUT_DIGITS = 4096;
const MAX_OPERAND_BITS = 4096;

const digitPatterns: Record<NumericBase, RegExp> = {
  2: /^[01]+(?:_[01]+)*$/,
  8: /^[0-7]+(?:_[0-7]+)*$/,
  10: /^\d+(?:_\d+)*$/,
  16: /^[\da-fA-F]+(?:_[\da-fA-F]+)*$/
};

function assertBase(base: number): asserts base is NumericBase {
  if (![2, 8, 10, 16].includes(base)) {
    throw new Error("A base deve ser 2, 8, 10 ou 16.");
  }
}

function bitLength(value: bigint): number {
  return (value < 0n ? -value : value).toString(2).length;
}

export function parseInteger(input: string, base: NumericBase): bigint {
  assertBase(base);
  if (typeof input !== "string") throw new Error("O valor deve ser texto.");

  const trimmed = input.trim();
  if (!trimmed) throw new Error("Informe um valor.");

  const sign = /^[+-]/.test(trimmed) ? trimmed[0] : "";
  const digits = sign ? trimmed.slice(1) : trimmed;
  if (!digits || !digitPatterns[base].test(digits)) {
    throw new Error(`Valor inválido para a base ${base}.`);
  }

  const normalizedDigits = digits.replaceAll("_", "");
  if (normalizedDigits.length > MAX_INPUT_DIGITS) {
    throw new Error(`Entrada excede ${MAX_INPUT_DIGITS} dígitos.`);
  }

  let value = 0n;
  for (const char of normalizedDigits.toLowerCase()) {
    const digit = Number.parseInt(char, 16);
    value = value * BigInt(base) + BigInt(digit);
  }

  if (bitLength(value) > MAX_OPERAND_BITS) {
    throw new Error(`Operando excede ${MAX_OPERAND_BITS} bits.`);
  }
  return sign === "-" ? -value : value;
}

export function formatInteger(value: bigint, base: NumericBase): string {
  assertBase(base);
  if (typeof value !== "bigint") throw new Error("O valor deve ser BigInt.");
  const prefix = base === 2 ? "0b" : base === 8 ? "0o" : base === 16 ? "0x" : "";
  const digits = (value < 0n ? -value : value).toString(base).toUpperCase();
  return `${value < 0n ? "-" : ""}${prefix}${digits}`;
}

export function convertInteger(input: string, source: NumericBase): Record<NumericBase, string> {
  const value = parseInteger(input, source);
  return {
    2: formatInteger(value, 2),
    8: formatInteger(value, 8),
    10: formatInteger(value, 10),
    16: formatInteger(value, 16)
  };
}

export function bitwiseOperation(a: bigint, operator: BitwiseOperator, b: bigint): bigint {
  if (typeof a !== "bigint" || typeof b !== "bigint") {
    throw new Error("Os operandos devem ser BigInt.");
  }
  if (bitLength(a) > MAX_OPERAND_BITS || bitLength(b) > MAX_OPERAND_BITS) {
    throw new Error(`Operandos excedem ${MAX_OPERAND_BITS} bits.`);
  }

  if (operator === "<<") {
    if (b < 0n || b > 4096n) {
      throw new Error("Deslocamento deve estar entre 0 e 4096.");
    }
    const result = a << b;
    if (bitLength(result) > MAX_OPERAND_BITS) {
      throw new Error(`Resultado excede ${MAX_OPERAND_BITS} bits.`);
    }
    return result;
  }

  switch (operator) {
    case "&": return a & b;
    case "|": return a | b;
    case "^": return a ^ b;
    default: throw new Error("Operação bit a bit não suportada.");
  }
}
