"""Testes do serviço de leitura estática de arquivos."""

import tempfile
import unittest
from pathlib import Path

from binlab.artifact_reader import (
    detect_format,
    format_hex_dump,
    inspect_binary,
    inspect_file,
    parse_hex_text,
)


class HexReaderTests(unittest.TestCase):
    def test_parse_plain_hex(self):
        self.assertEqual(parse_hex_text("0xDE, 0xAD BE_EF"), bytes.fromhex("DE AD BE EF"))

    def test_parse_intel_hex_records_and_checksum(self):
        intel_hex = ":0400000001020304F2\n:00000001FF\n"
        self.assertEqual(parse_hex_text(intel_hex), bytes((1, 2, 3, 4)))
        with self.assertRaises(ValueError):
            parse_hex_text(":0400000001020304F3\n")

    def test_hex_dump_and_format_signature(self):
        self.assertIn("00000000", format_hex_dump(b"ABCD"))
        self.assertEqual(detect_format(b"\x7fELF"), "ELF")
        self.assertIn("Formato provável: ELF", inspect_binary(b"\x7fELF", "demo", disassemble=False))


class SourceReaderTests(unittest.TestCase):
    def test_c_source_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.c"
            path.write_text("#include <stdio.h>\nint main(void) { return 0; }\n", encoding="utf-8")
            report = inspect_file(path)
        self.assertIn("Arquivo-fonte", report)
        self.assertIn("Includes: 1", report)
        self.assertIn("main", report)


if __name__ == "__main__":
    unittest.main()
