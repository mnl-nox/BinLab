"""Interpretação e métricas de sequências de bits."""

from dataclasses import dataclass
from typing import Optional


MAX_BIT_WIDTH = 4096
MAX_RAW_SEQUENCE_LENGTH = MAX_BIT_WIDTH * 2


@dataclass(frozen=True)
class BinaryAnalysis:
    """Resultado imutável da interpretação de uma sequência binária."""

    bits: str
    width: int
    unsigned_value: int
    signed_value: int
    hexadecimal: str
    ones: int
    zeros: int
    byte_hex: Optional[str]
    ascii_text: Optional[str]


def analyze_bits(sequence: str) -> BinaryAnalysis:
    """Valida e interpreta uma sequência limitada, preservando zeros à esquerda."""
    if not isinstance(sequence, str):
        raise ValueError("A sequência binária deve ser texto.")
    if len(sequence) > MAX_RAW_SEQUENCE_LENGTH:
        raise ValueError("A sequência excede o limite de {} caracteres.".format(MAX_RAW_SEQUENCE_LENGTH))
    bits = sequence.strip().replace("_", "")
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("Digite uma sequência contendo somente 0 e 1.")
    width = len(bits)
    if width > MAX_BIT_WIDTH:
        raise ValueError("A largura máxima permitida é de {} bits.".format(MAX_BIT_WIDTH))
    unsigned_value = int(bits, 2)
    signed_value = unsigned_value - (1 << width) if bits[0] == "1" else unsigned_value
    hex_digits = (width + 3) // 4
    hexadecimal = format(unsigned_value, "0{}X".format(hex_digits))
    byte_hex = None
    ascii_text = None
    if width % 8 == 0:
        data = bytes(int(bits[index:index + 8], 2) for index in range(0, width, 8))
        byte_hex = " ".join("{:02X}".format(byte) for byte in data)
        ascii_text = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in data)
    return BinaryAnalysis(
        bits=bits,
        width=width,
        unsigned_value=unsigned_value,
        signed_value=signed_value,
        hexadecimal=hexadecimal,
        ones=bits.count("1"),
        zeros=bits.count("0"),
        byte_hex=byte_hex,
        ascii_text=ascii_text,
    )
