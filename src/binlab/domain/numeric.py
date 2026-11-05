"""Parsing, conversão e formatação de inteiros em bases posicionais."""

BASE_PREFIXES = {2: "0b", 8: "0o", 10: "0d", 16: "0x"}
MAX_NUMERIC_DIGITS = 4096
MAX_FORMAT_BITS = 16384


def _validate_base(base: int) -> None:
    if isinstance(base, bool) or not isinstance(base, int) or base not in BASE_PREFIXES:
        raise ValueError("A base deve ser 2, 8, 10 ou 16.")


def parse_integer(text: str, base: int) -> int:
    """Interpreta inteiro em base 2, 8, 10 ou 16, aceitando prefixos e '_'."""
    _validate_base(base)
    if not isinstance(text, str):
        raise ValueError("O valor deve ser texto.")
    if len(text) > (MAX_NUMERIC_DIGITS * 2) + 3:
        raise ValueError("O valor excede o limite de {} dígitos.".format(MAX_NUMERIC_DIGITS))

    value = text.strip()
    sign = ""
    if value.startswith(("+", "-")):
        sign, value = value[0], value[1:]
    if value.lower().startswith(BASE_PREFIXES[base]):
        value = value[2:]

    digit_count = len(value.replace("_", ""))
    if not value or digit_count > MAX_NUMERIC_DIGITS:
        raise ValueError("Informe um número com até {} dígitos.".format(MAX_NUMERIC_DIGITS))
    try:
        # int() already enforces Python's strict underscore grammar:
        # separators must occur between valid digits, never at either edge.
        return int(sign + value, base)
    except ValueError as error:
        raise ValueError("Valor inválido para a base {}.".format(base)) from error


def format_integer(value: int, base: int, uppercase: bool = True) -> str:
    """Formata inteiro com sinal em uma base suportada, sem prefixo."""
    _validate_base(base)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("O valor a formatar deve ser um inteiro.")
    if value.bit_length() > MAX_FORMAT_BITS:
        raise ValueError("O valor excede o limite de {} bits.".format(MAX_FORMAT_BITS))
    if not isinstance(uppercase, bool):
        raise ValueError("uppercase deve ser booleano.")
    if base == 10:
        return str(value)
    digits = format(abs(value), {2: "b", 8: "o", 16: "X" if uppercase else "x"}[base])
    return ("-" if value < 0 else "") + digits


def convert_integer(text: str, source_base: int, target_base: int) -> str:
    """Converte texto entre bases sem expor detalhes de interface."""
    value = parse_integer(text, source_base)
    return format_integer(value, target_base)
