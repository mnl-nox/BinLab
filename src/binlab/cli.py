#!/usr/bin/env python3
"""Calculadora didática para conversões e operações com números binários."""

import os
import sys
from pathlib import Path

from . import __version__
from .artifact_reader import HEX_SUFFIXES, inspect_file
from .domain.analysis import analyze_bits
from .domain.numeric import format_integer, parse_integer
from .domain.operations import calculate, truth_table_rows


def read_binary(prompt: str) -> int:
    """Lê um número binário não negativo e retorna seu valor inteiro."""
    value = parse_integer(input(prompt), 2)
    if value < 0:
        raise ValueError("Informe um binário não negativo.")
    return value


def show_result(label: str, value: int) -> None:
    """Exibe o resultado decimal e binário."""
    print(f"{label}: {format_integer(value, 2)} (binário) = {value} (decimal)")


def arithmetic() -> None:
    """Executa operações aritméticas entre dois binários."""
    a = read_binary("Primeiro número binário: ")
    b = read_binary("Segundo número binário: ")
    print("Operações: +  -  *  //  %")
    operator = input("Operador: ").strip()
    show_result("Resultado", calculate(a, operator, b))


def bitwise() -> None:
    """Executa AND, OR, XOR ou NOT com largura definida pelo usuário."""
    a = read_binary("Primeiro número binário: ")
    operator = input("Operação (AND, OR, XOR, NOT): ").strip().upper()
    if operator == "NOT":
        width = input("Largura em bits [padrão: tamanho de A]: ").strip()
        bits = int(width) if width else max(1, a.bit_length())
        result = calculate(a, operator, width=bits)
    else:
        b = read_binary("Segundo número binário: ")
        result = calculate(a, operator, b)
    show_result("Resultado", result)


def shift() -> None:
    """Desloca os bits para a esquerda ou direita."""
    value = read_binary("Número binário: ")
    direction = input("Direção (E para esquerda, D para direita): ").strip().upper()
    places_text = input("Quantidade de posições: ").strip()
    if not places_text.isdigit():
        raise ValueError("A quantidade deve ser um inteiro não negativo.")
    places = int(places_text)
    if direction not in {"E", "D"}:
        raise ValueError("Direção inválida.")
    result = calculate(value, "<<" if direction == "E" else ">>", places)
    show_result("Resultado", result)


def conversion() -> None:
    """Converte um valor informado entre bases binária, octal, decimal e hexadecimal."""
    bases = {"2": (2, "binário"), "8": (8, "octal"), "10": (10, "decimal"), "16": (16, "hexadecimal")}
    print("Bases disponíveis: 2 (binário), 8 (octal), 10 (decimal), 16 (hexadecimal)")
    source = input("Base de origem: ").strip()
    target = input("Base de destino: ").strip()
    if source not in bases or target not in bases:
        raise ValueError("Use as bases 2, 8, 10 ou 16.")
    value = parse_integer(input("Valor: "), bases[source][0])
    base = bases[target][0]
    print(f"{value} decimal = {format_integer(value, base)} base {base} ({bases[target][1]}).")


def analyze_binary() -> None:
    """Interpreta bits como valor, campos estatísticos, sinal e bytes ASCII."""
    result = analyze_bits(input("Sequência binária (ex.: 0100_0001): "))
    print(f"Largura: {result.width} bits")
    print(f"Valor sem sinal: {result.unsigned_value}")
    print(f"Complemento de dois ({result.width} bits): {result.signed_value}")
    print(f"Hexadecimal: 0x{result.hexadecimal}")
    print(f"Quantidade de bits 1: {result.ones}")
    print(f"Quantidade de bits 0: {result.zeros}")
    if result.byte_hex is not None:
        print(f"Bytes (hex): {result.byte_hex}")
        print(f"ASCII imprimível (bytes não imprimíveis como '.'): {result.ascii_text}")
    else:
        print("ASCII: indisponível (a sequência precisa ter múltiplos de 8 bits).")


def truth_table() -> None:
    """Imprime a tabela verdade das portas lógicas básicas de um bit."""
    print("A B | AND OR XOR | NOT(A) NOT(B)")
    print("----+------------+-------------")
    for a, b, and_value, or_value, xor_value, not_a, not_b in truth_table_rows():
        print(f"{a} {b} |  {and_value}   {or_value}   {xor_value}  |    {not_a}      {not_b}")


def read_artifact() -> None:
    """Adapta perguntas do terminal ao serviço de inspeção de arquivos."""
    raw_path = input("Caminho do arquivo (C, assembly, binário ou .hex): ").strip()
    architecture = None
    if Path(raw_path).suffix.lower() in HEX_SUFFIXES:
        architecture = input("Arquitetura para objdump (vazio para ignorar): ").strip() or None
    print(inspect_file(raw_path, architecture))


def print_banner() -> None:
    """Imprime o logotipo com cores ANSI quando a saída é um terminal colorido."""
    colors_enabled = sys.stdout.isatty() and "NO_COLOR" not in os.environ
    palette = {
        "cyan": "\033[96m", "blue": "\033[94m", "green": "\033[92m",
        "yellow": "\033[93m", "reset": "\033[0m",
    }
    reset = palette["reset"] if colors_enabled else ""
    art = r""" ____  _       _           _
| __ )(_)_ __ | |    __ _| |__
|  _ \| | '_ \| |   / _` | '_ \
| |_) | | | | | |__| (_| | |_) |
|____/|_|_| |_|_____\__,_|_.__/"""
    colors = ["cyan", "blue", "blue", "green", "cyan"]
    for line, color in zip(art.splitlines(), colors):
        prefix = palette[color] if colors_enabled else ""
        print(f"{prefix}{line}{reset}")
    binary_label = f"{palette['blue']}BINARY{reset}" if colors_enabled else "BINARY"
    lab_label = f"{palette['green']}LAB{reset}" if colors_enabled else "LAB"
    version = f"{palette['yellow']}v{__version__}{reset}" if colors_enabled else f"v{__version__}"
    print(f"      {binary_label} · {lab_label}  {version}")
    print("      01 {cyan}·{reset} A-F {green}·{reset} C / ASM".format(
        cyan=palette["cyan"] if colors_enabled else "",
        green=palette["green"] if colors_enabled else "",
        reset=reset,
    ))


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
    print_banner()
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
