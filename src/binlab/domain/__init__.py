"""API de domínio pura do BinLab, reutilizável por qualquer interface."""

from .analysis import BinaryAnalysis, analyze_bits
from .numeric import convert_integer, format_integer, parse_integer
from .operations import calculate, truth_table_rows

__all__ = [
    "BinaryAnalysis",
    "analyze_bits",
    "calculate",
    "convert_integer",
    "format_integer",
    "parse_integer",
    "truth_table_rows",
]
