"""Interpretação e métricas de sequências de bits."""

from dataclasses import dataclass
from typing import Optional


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
    """Valida e interpreta uma sequência, preservando zeros à esquerda."""
    bits = sequence.strip().replace("_", "")
    if not bits or any(bit not in "01" for bit in bits):
        raise ValueError("Digite uma sequência contendo somente 0 e 1.")
    width = len(bits)
    unsigned_value = int(bits, 2)
    signed_value = unsigned_value - (1 << width) if bits[0] == "1" else unsigned_value
    hex_digits = (width + 3) // 4
    hexadecimal = format(unsigned_value, f"0{hex_digits}X")
    byte_hex = None
    ascii_text = None
    if width % 8 == 0:
        data = bytes(int(bits[index:index + 8], 2) for index in range(0, width, 8))
        byte_hex = " ".join(f"{byte:02X}" for byte in data)
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
