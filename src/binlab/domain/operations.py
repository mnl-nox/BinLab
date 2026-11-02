"""Operações inteiras, lógicas e deslocamentos da calculadora."""

from typing import Optional, Tuple

MAX_OPERAND_BITS = 4096
MAX_NOT_WIDTH = 4096
MAX_SHIFT_DISTANCE = 4096

ARITHMETIC_OPERATORS = {"+", "-", "*", "//", "%"}
BITWISE_OPERATORS = {"AND", "OR", "XOR", "NOT"}
SHIFT_OPERATORS = {"<<", ">>"}
OPERATORS = ARITHMETIC_OPERATORS | BITWISE_OPERATORS | SHIFT_OPERATORS


def _require_integer(value: int, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("{} deve ser um inteiro (bool não é aceito).".format(label))
    if value.bit_length() > MAX_OPERAND_BITS:
        raise ValueError("{} excede o limite de {} bits.".format(label, MAX_OPERAND_BITS))


def calculate(a: int, operator: str, b: Optional[int] = None, width: Optional[int] = None) -> int:
    """Aplica operação limitada a inteiros.

    Operandos são limitados a 4096 bits, NOT a 4096 bits e shifts a 4096 posições.
    """
    _require_integer(a, "Operando A")
    if not isinstance(operator, str):
        raise ValueError("Operador deve ser texto.")
    operator = operator.strip()
    if operator.isalpha():
        operator = operator.upper()
    if operator not in OPERATORS:
        raise ValueError("Operador não suportado: {}.".format(operator))

    if operator == "NOT":
        if isinstance(width, bool) or not isinstance(width, int) or width < 1 or width > MAX_NOT_WIDTH:
            raise ValueError("NOT requer largura entre 1 e {} bits.".format(MAX_NOT_WIDTH))
        if a < 0 or a >= (1 << width):
            raise ValueError("A largura deve comportar o operando não negativo.")
        return (~a) & ((1 << width) - 1)

    if b is None:
        raise ValueError("O operador {} requer um segundo operando.".format(operator))
    _require_integer(b, "Operando B")

    if operator in {"//", "%"} and b == 0:
        raise ValueError("Não é possível dividir por zero.")
    if operator in BITWISE_OPERATORS | SHIFT_OPERATORS and (a < 0 or b < 0):
        raise ValueError("Operações bit a bit e deslocamentos requerem operandos não negativos.")
    if operator in SHIFT_OPERATORS and b > MAX_SHIFT_DISTANCE:
        raise ValueError("Deslocamento excede o limite de {} posições.".format(MAX_SHIFT_DISTANCE))

    operations = {
        "+": lambda: a + b,
        "-": lambda: a - b,
        "*": lambda: a * b,
        "//": lambda: a // b,
        "%": lambda: a % b,
        "AND": lambda: a & b,
        "OR": lambda: a | b,
        "XOR": lambda: a ^ b,
        "<<": lambda: a << b,
        ">>": lambda: a >> b,
    }
    return operations[operator]()


def truth_table_rows() -> Tuple[Tuple[int, int, int, int, int, int, int], ...]:
    """Retorna linhas (A, B, AND, OR, XOR, NOT A, NOT B) para um bit."""
    return tuple(
        (a, b, a & b, a | b, a ^ b, 1 - a, 1 - b)
        for a in (0, 1)
        for b in (0, 1)
    )
