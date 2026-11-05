"""Testes unitários das regras de domínio e limites de recursos."""

import unittest

from binlab.domain import analyze_bits, calculate, convert_integer, format_integer, parse_integer
from binlab.domain.analysis import MAX_BIT_WIDTH
from binlab.domain.numeric import MAX_NUMERIC_DIGITS
from binlab.domain.operations import MAX_NOT_WIDTH, MAX_SHIFT_DISTANCE


class NumericTests(unittest.TestCase):
    def test_parse_prefixed_hex_and_separators(self):
        self.assertEqual(parse_integer("0x2A_FF", 16), 0x2AFF)
        self.assertEqual(parse_integer("-0b1010_0011", 2), -0b10100011)

    def test_rejects_misplaced_numeric_separators(self):
        invalid_values = ("_10", "10_", "1__0", "+_10", "-_10", "0x_FF")
        for value in invalid_values:
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_integer(value, 2 if not value.lower().startswith("0x") else 16)

    def test_convert_hexadecimal_to_binary(self):
        self.assertEqual(convert_integer("0x2A", 16, 2), "101010")

    def test_format_negative_value(self):
        self.assertEqual(format_integer(-10, 16), "-A")

    def test_reject_invalid_base_and_digits(self):
        for call in (lambda: parse_integer("10", 3), lambda: parse_integer("102", 2)):
            with self.assertRaises(ValueError):
                call()

    def test_numeric_runtime_types_and_size(self):
        for call in (
            lambda: parse_integer(10, 2),
            lambda: parse_integer("10", True),
            lambda: format_integer(True, 2),
            lambda: format_integer("10", 2),
            lambda: parse_integer("1" * (MAX_NUMERIC_DIGITS + 1), 2),
        ):
            with self.assertRaises(ValueError):
                call()


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

    def test_bool_and_non_integer_operands_are_rejected(self):
        for call in (
            lambda: calculate(True, "+", 1),
            lambda: calculate(1, "+", False),
            lambda: calculate("1", "+", 1),
            lambda: calculate(1, None, 1),
        ):
            with self.assertRaises(ValueError):
                call()

    def test_not_and_shift_limits(self):
        for call in (
            lambda: calculate(0, "NOT", width=MAX_NOT_WIDTH + 1),
            lambda: calculate(1, "NOT", width=True),
            lambda: calculate(1, "<<", MAX_SHIFT_DISTANCE + 1),
            lambda: calculate(1, ">>", -1),
        ):
            with self.assertRaises(ValueError):
                call()


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
        for value in ("10x1", 100, "1" * (MAX_BIT_WIDTH + 1)):
            with self.assertRaises(ValueError):
                analyze_bits(value)


if __name__ == "__main__":
    unittest.main()
