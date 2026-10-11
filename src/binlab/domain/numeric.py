"""Parsing, conversão e formatação de inteiros em bases posicionais."""

BASE_PREFIXES = {2: "0b", 8: "0o", 10: "0d", 16: "0x"}


def parse_integer(text: str, base: int) -> int:
    """Interpreta inteiro em base 2, 8, 10 ou 16, aceitando prefixos e `_`."""
    if base not in BASE_PREFIXES:
        raise ValueError("A base deve ser 2, 8, 10 ou 16.")
    value = text.strip().replace("_", "")
    sign = ""
    if value.startswith(("+", "-")):
        sign, value = value[0], value[1:]
    if value.lower().startswith(BASE_PREFIXES[base]):
        value = value[2:]
    if not value:
        raise ValueError("Informe um número.")
    try:
        return int(sign + value, base)
    except ValueError as error:
        raise ValueError(f"Valor inválido para a base {base}.") from error


def format_integer(value: int, base: int, uppercase: bool = True) -> str:
    """Formata inteiro com sinal em uma base suportada, sem prefixo."""
    if base not in BASE_PREFIXES:
        raise ValueError("A base deve ser 2, 8, 10 ou 16.")
    if base == 10:
        return str(value)
    digits = format(abs(value), {2: "b", 8: "o", 16: "X" if uppercase else "x"}[base])
    return ("-" if value < 0 else "") + digits


def convert_integer(text: str, source_base: int, target_base: int) -> str:
    """Converte texto entre bases sem expor detalhes de interface."""
    value = parse_integer(text, source_base)
    return format_integer(value, target_base)
