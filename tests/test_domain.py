"""Testes unitários das regras de domínio reutilizáveis."""

import unittest

from binlab.domain import analyze_bits, calculate, convert_integer, format_integer, parse_integer


class NumericTests(unittest.TestCase):
    def test_parse_prefixed_hex_and_separators(self):
        self.assertEqual(parse_integer("0x2A_FF", 16), 0x2AFF)

    def test_convert_hexadecimal_to_binary(self):
        self.assertEqual(convert_integer("0x2A", 16, 2), "101010")

    def test_format_negative_value(self):
        self.assertEqual(format_integer(-10, 16), "-A")

    def test_reject_invalid_base_and_digits(self):
        with self.assertRaises(ValueError):
            parse_integer("10", 3)
        with self.assertRaises(ValueError):
            parse_integer("102", 2)


class OperationTests(unittest.TestCase):
    def test_arithmetic_and_division(self):
        self.assertEqual(calculate(5, "+", 3), 8)
        self.assertEqual(calculate(13, "//", 2), 6)
        self.assertEqual(calculate(13, "%", 2), 1)

    def test_bitwise_and_width_limited_not(self):
        self.assertEqual(calculate(10, "AND", 3), 2)
        self.assertEqual(calculate(10, "XOR", 3), 9)
        self.assertEqual(calculate(10, "NOT", width=4), 5)

    def test_shift_and_invalid_operations(self):
        self.assertEqual(calculate(5, "<<", 2), 20)
        with self.assertRaises(ValueError):
            calculate(1, "//", 0)
        with self.assertRaises(ValueError):
            calculate(1, "NOT")
        with self.assertRaises(ValueError):
            calculate(-1, "AND", 1)


class AnalysisTests(unittest.TestCase):
    def test_analysis_preserves_width_and_twos_complement(self):
        result = analyze_bits("1111_1111")
        self.assertEqual(result.width, 8)
        self.assertEqual(result.unsigned_value, 255)
        self.assertEqual(result.signed_value, -1)
        self.assertEqual(result.hexadecimal, "FF")
        self.assertEqual(result.byte_hex, "FF")

    def test_ascii_and_invalid_sequence(self):
        self.assertEqual(analyze_bits("01000001").ascii_text, "A")
        with self.assertRaises(ValueError):
            analyze_bits("10x1")


if __name__ == "__main__":
    unittest.main()
