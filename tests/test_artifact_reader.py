"""Testes de segurança e regressão do leitor estático de artefatos."""

import sys
import tempfile
import unittest
from pathlib import Path

from binlab import artifact_reader as reader


def intel_record(address, kind, data=b""):
    body = bytes((len(data),)) + address.to_bytes(2, "big") + bytes((kind,)) + data
    checksum = (-sum(body)) & 0xFF
    return ":" + (body + bytes((checksum,))).hex().upper()


class HexReaderTests(unittest.TestCase):
    def test_parse_plain_hex(self):
        self.assertEqual(reader.parse_hex_text("0xDE, 0xAD BE_EF"), bytes.fromhex("DE AD BE EF"))

    def test_parse_intel_hex_records_and_checksum(self):
        intel_hex = ":0400000001020304F2\n:00000001FF\n"
        self.assertEqual(reader.parse_hex_text(intel_hex), bytes((1, 2, 3, 4)))
        with self.assertRaisesRegex(ValueError, "Checksum"):
            reader.parse_hex_text(":0400000001020304F3\n:00000001FF\n")

    def test_eof_is_mandatory_and_terminal(self):
        data = intel_record(0, 0, b"\xAA")
        eof = intel_record(0, 1)
        with self.assertRaisesRegex(ValueError, "sem registro EOF"):
            reader.parse_hex_text(data)
        with self.assertRaisesRegex(ValueError, "após EOF"):
            reader.parse_hex_text(data + "\n" + eof + "\n" + data)
        with self.assertRaisesRegex(ValueError, "EOF"):
            reader.parse_hex_text(data + "\n" + intel_record(1, 1))

    def test_record_types_require_exact_fields(self):
        invalid_records = [
            intel_record(1, 2, b"\x00\x01"),
            intel_record(0, 3, b"\x00\x00\x00"),
            intel_record(1, 4, b"\x00\x01"),
            intel_record(0, 5, b"\x00\x00"),
        ]
        for record in invalid_records:
            with self.subTest(record=record), self.assertRaises(ValueError):
                reader.parse_hex_text(record + "\n" + intel_record(0, 1))

    def test_overlap_is_rejected(self):
        text = "\n".join((
            intel_record(0, 0, b"AB"),
            intel_record(1, 0, b"CD"),
            intel_record(0, 1),
        ))
        with self.assertRaisesRegex(ValueError, "sobrepostos"):
            reader.parse_hex_text(text)

    def test_sparse_addresses_are_bounded(self):
        text = "\n".join((
            intel_record(0, 4, b"\x00\x01"),
            intel_record(1, 0, b"X"),
            intel_record(0, 1),
        ))
        with self.assertRaisesRegex(ValueError, "Intervalo esparso"):
            reader.parse_hex_text(text)

    def test_decoded_span_is_bounded(self):
        records = []
        for index in range(18):
            absolute = index * 65535
            upper = absolute >> 16
            offset = absolute & 0xFFFF
            records.append(intel_record(0, 4, upper.to_bytes(2, "big")))
            records.append(intel_record(offset, 0, b"X"))
        records.append(intel_record(0, 1))
        with self.assertRaisesRegex(ValueError, "Span Intel HEX"):
            reader.parse_hex_text("\n".join(records))

    def test_data_record_address_overflow_is_rejected(self):
        text = "\n".join((
            intel_record(0, 4, b"\xff\xff"),
            intel_record(0xFFFF, 0, b"XX"),
            intel_record(0, 1),
        ))
        with self.assertRaisesRegex(ValueError, "32 bits"):
            reader.parse_hex_text(text)

    def test_hex_dump_and_format_signature(self):
        self.assertIn("00000000", reader.format_hex_dump(b"ABCD"))
        self.assertEqual(reader.detect_format(b"\x7fELF"), "ELF")
        self.assertIn("Formato provável: ELF", reader.inspect_binary(b"\x7fELF", "demo", disassemble=False))

    def test_intel_hex_record_count_is_bounded(self):
        with self.assertRaisesRegex(ValueError, "limite de"):
            reader.parse_hex_text(chr(10) * (reader.MAX_HEX_RECORDS + 1))

    def test_raw_hex_size_is_bounded(self):
        with self.assertRaisesRegex(ValueError, "excede o limite"):
            reader.parse_hex_text("AA" * (reader.MAX_HEX_DECODED_BYTES + 1))

    def test_printable_strings_are_capped(self):
        data = b"\x00".join(("STRING{:02d}".format(index).encode("ascii") for index in range(100)))
        strings = reader.printable_strings(data)
        self.assertEqual(len(strings), reader.MAX_STRINGS)
        self.assertTrue(all(len(value) <= reader.MAX_STRING_LENGTH for value in strings))


class FileBoundaryTests(unittest.TestCase):
    def test_source_file_limit_is_enforced_during_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.c"
            path.write_bytes(b"A" * (reader.MAX_SOURCE_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "Arquivo-fonte excede"):
                reader.inspect_source(path)

    def test_binary_file_limit_is_enforced_during_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.bin"
            path.write_bytes(b"\x00" * (reader.MAX_BINARY_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "Arquivo binário excede"):
                reader.inspect_file(path)

    def test_hex_file_limit_is_enforced_during_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.hex"
            path.write_bytes(b"0" * (reader.MAX_HEX_TEXT_BYTES + 1))
            with self.assertRaisesRegex(ValueError, "Arquivo HEX excede"):
                reader.inspect_file(path)


class ExternalToolBoundaryTests(unittest.TestCase):
    def test_objdump_output_is_bounded_while_running(self):
        output = reader._run_bounded(
            [sys.executable, "-c", "import sys; sys.stdout.write('X' * 1000000)"],
            timeout=5,
            output_limit=4096,
        )
        self.assertLessEqual(len(output.encode("utf-8")), 4096 + 100)
        self.assertIn("limite", output)

    def test_objdump_timeout_is_enforced(self):
        output = reader._run_bounded(
            [sys.executable, "-c", "import time; time.sleep(5)"],
            timeout=0.1,
            output_limit=1024,
        )
        self.assertIn("timeout", output)


class SourceReaderTests(unittest.TestCase):
    def test_c_source_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.c"
            path.write_text("#include <stdio.h>\nint main(void) { return 0; }\n", encoding="utf-8")
            report = reader.inspect_file(path)
        self.assertIn("Arquivo-fonte", report)
        self.assertIn("Includes: 1", report)
        self.assertIn("main", report)


if __name__ == "__main__":
    unittest.main()
