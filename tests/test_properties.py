"""Property-based regression tests for numeric and artifact boundaries."""

import unittest

from hypothesis import given, settings, strategies as st

from binlab.artifact_reader import parse_hex_text
from binlab.domain.numeric import format_integer, parse_integer
from binlab.domain.operations import calculate


def intel_record(address, kind, data=b""):
    body = bytes((len(data),)) + address.to_bytes(2, "big") + bytes((kind,)) + data
    checksum = (-sum(body)) & 0xFF
    return ":" + (body + bytes((checksum,))).hex().upper()


class NumericPropertyTests(unittest.TestCase):
    @settings(max_examples=150, deadline=None)
    @given(
        value=st.integers(min_value=-(1 << 512), max_value=1 << 512),
        base=st.sampled_from((2, 8, 10, 16)),
    )
    def test_format_parse_round_trip(self, value, base):
        encoded = format_integer(value, base)
        self.assertEqual(parse_integer(encoded, base), value)

    @settings(max_examples=150, deadline=None)
    @given(
        left=st.integers(min_value=0, max_value=(1 << 256) - 1),
        right=st.integers(min_value=0, max_value=(1 << 256) - 1),
    )
    def test_bitwise_operations_match_integer_semantics(self, left, right):
        self.assertEqual(calculate(left, "AND", right), left & right)
        self.assertEqual(calculate(left, "OR", right), left | right)
        self.assertEqual(calculate(left, "XOR", right), left ^ right)


class ArtifactPropertyTests(unittest.TestCase):
    @settings(max_examples=150, deadline=None)
    @given(payload=st.binary(min_size=1, max_size=4096))
    def test_raw_hex_round_trip(self, payload):
        self.assertEqual(parse_hex_text(payload.hex()), payload)

    @settings(max_examples=100, deadline=None)
    @given(
        address=st.integers(min_value=0, max_value=4096),
        payload=st.binary(min_size=1, max_size=128),
    )
    def test_intel_hex_data_records_round_trip(self, address, payload):
        data = intel_record(address, 0, payload)
        eof = intel_record(0, 1)
        self.assertEqual(parse_hex_text(data + "\n" + eof), bytes(address) + payload)

    @settings(max_examples=100, deadline=None)
    @given(payload=st.binary(min_size=1, max_size=128))
    def test_intel_hex_checksum_mutation_is_rejected(self, payload):
        record = intel_record(0, 0, payload)
        replacement = "0" if record[-1] != "0" else "1"
        corrupted = record[:-1] + replacement
        with self.assertRaisesRegex(ValueError, "Checksum"):
            parse_hex_text(corrupted + "\n" + intel_record(0, 1))


if __name__ == "__main__":
    unittest.main()
