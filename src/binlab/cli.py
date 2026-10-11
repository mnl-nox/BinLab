#!/usr/bin/env python3
"""Calculadora didática para conversões e operações com números binários."""

from .artifact_reader import read_artifact
from . import __version__


def read_binary(prompt: str) -> int:
    """Lê um número binário não negativo e retorna seu valor inteiro."""
    value = input(prompt).strip().replace("_", "")
    if not value or any(bit not in "01" for bit in value):
        raise ValueError("Digite somente 0 e 1 (sublinhados são aceitos como separadores).")
    return int(value, 2)


def parse_number(text: str, base: int) -> int:
    """Interpreta um inteiro em base 2, 8, 10 ou 16, com prefixo opcional."""
    value = text.strip().replace("_", "")
    prefixes = {2: "0b", 8: "0o", 10: "0d", 16: "0x"}
    sign = ""
    if value.startswith(("+", "-")):
        sign, value = value[0], value[1:]
    if value.lower().startswith(prefixes[base]):
        value = value[2:]
    if not value:
        raise ValueError("Informe um número.")
    try:
        return int(sign + value, base)
    except ValueError as error:
        raise ValueError(f"Valor inválido para a base {base}.") from error


def binary(value: int) -> str:
    """Formata um inteiro com sinal em base 2."""
    return ("-" if value < 0 else "") + format(abs(value), "b")


def show_result(label: str, value: int) -> None:
    """Exibe o resultado decimal e binário."""
    print(f"{label}: {binary(value)} (binário) = {value} (decimal)")


def arithmetic() -> None:
    """Executa operações aritméticas entre dois binários."""
    a = read_binary("Primeiro número binário: ")
    b = read_binary("Segundo número binário: ")
    print("Operações: +  -  *  //  %")
    operator = input("Operador: ").strip()
    operations = {
        "+": lambda: a + b,
        "-": lambda: a - b,
        "*": lambda: a * b,
        "//": lambda: a // b,
        "%": lambda: a % b,
    }
    if operator not in operations:
        raise ValueError("Operador inválido.")
    if operator in ("//", "%") and b == 0:
        raise ValueError("Não é possível dividir por zero.")
    show_result("Resultado", operations[operator]())


def bitwise() -> None:
    """Executa AND, OR, XOR ou NOT com largura definida pelo usuário."""
    a = read_binary("Primeiro número binário: ")
    operator = input("Operação (AND, OR, XOR, NOT): ").strip().upper()
    if operator == "NOT":
        width = input("Largura em bits [padrão: tamanho de A]: ").strip()
        bits = int(width) if width else max(1, a.bit_length())
        if bits < 1 or a >= (1 << bits):
            raise ValueError("A largura deve ser positiva e comportar o primeiro número.")
        result = (~a) & ((1 << bits) - 1)
    else:
        b = read_binary("Segundo número binário: ")
        operations = {"AND": lambda: a & b, "OR": lambda: a | b, "XOR": lambda: a ^ b}
        if operator not in operations:
            raise ValueError("Operação inválida.")
        result = operations[operator]()
    show_result("Resultado", result)


def shift() -> None:
    """Desloca os bits para a esquerda ou direita."""
    value = read_binary("Número binário: ")
    direction = input("Direção (E para esquerda, D para direita): ").strip().upper()
    places_text = input("Quantidade de posições: ").strip()
    if not places_text.isdigit():
        raise ValueError("A quantidade deve ser um inteiro não negativo.")
    places = int(places_text)
    if direction == "E":
        result = value << places
    elif direction == "D":
        result = value >> places
    else:
        raise ValueError("Direção inválida.")
    show_result("Resultado", result)


def conversion() -> None:
    """Converte um valor informado entre bases binária, octal, decimal e hexadecimal."""
    bases = {"2": (2, "binário"), "8": (8, "octal"), "10": (10, "decimal"), "16": (16, "hexadecimal")}
    print("Bases disponíveis: 2 (binário), 8 (octal), 10 (decimal), 16 (hexadecimal)")
    source = input("Base de origem: ").strip()
    target = input("Base de destino: ").strip()
    if source not in bases or target not in bases:
        raise ValueError("Use as bases 2, 8, 10 ou 16.")
    value = parse_number(input("Valor: "), bases[source][0])
    formats = {2: lambda n: binary(n), 8: lambda n: ("-" if n < 0 else "") + format(abs(n), "o"),
               10: str, 16: lambda n: ("-" if n < 0 else "") + format(abs(n), "X")}
    base = bases[target][0]
    print(f"{value} decimal = {formats[base](value)} base {base} ({bases[target][1]}).")


def analyze_binary() -> None:
    """Interpreta bits como valor, campos estatísticos, sinal e bytes ASCII."""
    raw = input("Sequência binária (ex.: 0100_0001): ").strip().replace("_", "")
    if not raw or any(bit not in "01" for bit in raw):
        raise ValueError("Digite uma sequência contendo somente 0 e 1.")
    value = int(raw, 2)
    width = len(raw)
    signed = value - (1 << width) if raw[0] == "1" else value
    hex_value = format(value, f"0{(width + 3) // 4}X")
    print(f"Largura: {width} bits")
    print(f"Valor sem sinal: {value}")
    print(f"Complemento de dois ({width} bits): {signed}")
    print(f"Hexadecimal: 0x{hex_value}")
    print(f"Quantidade de bits 1: {raw.count('1')}")
    print(f"Quantidade de bits 0: {raw.count('0')}")
    if width % 8 == 0:
        data = bytes(int(raw[index:index + 8], 2) for index in range(0, width, 8))
        decoded = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)
        print(f"Bytes (hex): {' '.join(f'{byte:02X}' for byte in data)}")
        print(f"ASCII imprimível (bytes não imprimíveis como '.'): {decoded}")
    else:
        print("ASCII: indisponível (a sequência precisa ter múltiplos de 8 bits).")


def truth_table() -> None:
    """Imprime a tabela verdade das portas lógicas básicas de um bit."""
    print("A B | AND OR XOR | NOT(A) NOT(B)")
    print("----+------------+-------------")
    for a in (0, 1):
        for b in (0, 1):
            print(f"{a} {b} |  {a & b}   {a | b}   {a ^ b}  |    {1 - a}      {1 - b}")


def main() -> None:
    """Apresenta o menu e trata erros de entrada sem encerrar o programa."""
    menu = {
        "1": ("Aritmética binária", arithmetic),
        "2": ("Operações bit a bit", bitwise),
        "3": ("Deslocamento de bits", shift),
        "4": ("Conversão de bases", conversion),
        "5": ("Tabela verdade", truth_table),
        "6": ("Análise de sequência binária", analyze_binary),
        "7": ("Leitor de arquivos C/assembly/binário/hex", read_artifact),
    }
    print(r"""
 ____  _       _           _
| __ )(_)_ __ | |    __ _| |__
|  _ \| | '_ \| |   / _` | '_ \
| |_) | | | | | |__| (_| | |_) |
|____/|_|_| |_|_____\__,_|_.__/
      BINARY LAB  ·  v""" + __version__)
    while True:
        print("\n=== Calculadora e leitor de dados binários ===")
        for key, (description, _) in menu.items():
            print(f"{key}. {description}")
        print("0. Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "0":
            print("Até logo!")
            return
        selected = menu.get(choice)
        if selected is None:
            print("Opção inválida. Escolha um número de 0 a 7.")
            continue
        try:
            selected[1]()
        except (ValueError, EOFError) as error:
            print(f"Erro: {error}")


if __name__ == "__main__":
    main()
