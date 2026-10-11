"""Operações inteiras, lógicas e deslocamentos da calculadora."""

from typing import Optional, Tuple

ARITHMETIC_OPERATORS = {"+", "-", "*", "//", "%"}
BITWISE_OPERATORS = {"AND", "OR", "XOR", "NOT"}
SHIFT_OPERATORS = {"<<", ">>"}
OPERATORS = ARITHMETIC_OPERATORS | BITWISE_OPERATORS | SHIFT_OPERATORS


def calculate(a: int, operator: str, b: Optional[int] = None, width: Optional[int] = None) -> int:
    """Aplica uma operação validada a inteiros e retorna o resultado.

    `b` é o segundo operando ou a quantidade de posições nos deslocamentos.
    `width` define o complemento finito para NOT.
    """
    operator = operator.strip()
    if operator.isalpha():
        operator = operator.upper()
    if operator not in OPERATORS:
        raise ValueError(f"Operador não suportado: {operator}.")
    if operator == "NOT":
        if width is None or width < 1:
            raise ValueError("NOT requer uma largura positiva em bits.")
        if a < 0 or a >= (1 << width):
            raise ValueError("A largura deve comportar o operando não negativo.")
        return (~a) & ((1 << width) - 1)
    if b is None:
        raise ValueError(f"O operador {operator} requer um segundo operando.")
    if operator in {"//", "%"} and b == 0:
        raise ValueError("Não é possível dividir por zero.")
    if operator in BITWISE_OPERATORS | SHIFT_OPERATORS and (a < 0 or b < 0):
        raise ValueError("Operações bit a bit e deslocamentos requerem operandos não negativos.")
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
