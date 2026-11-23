"""Validate generated CBOMs against the official CycloneDX 1.6.2 JSON schema."""

import json
import os
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft7Validator, FormatChecker

from cryptoscan import cbom, scanner
from cryptoscan.knowledge import ALGORITHMS
from cryptoscan.scanner import Finding, Occurrence

SCHEMA_PATH = Path(__file__).parent / "schemas" / "bom-1.6.schema.json"


class TestCycloneDX16Schema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with SCHEMA_PATH.open(encoding="utf-8") as handle:
            cls.schema = json.load(handle)
        Draft7Validator.check_schema(cls.schema)
        cls.validator = Draft7Validator(cls.schema, format_checker=FormatChecker())

    def assert_schema_valid(self, document):
        errors = sorted(self.validator.iter_errors(document), key=lambda e: str(e.path))
        self.assertEqual(
            errors, [],
            "\n".join(f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors)
        )

    def test_empty_inventory_is_valid(self):
        self.assert_schema_valid(cbom.build([], "empty-project"))

    def test_source_inventory_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "example.py")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("hashlib.md5(b'x')\nrsa.generate_private_key(key_size=2048)\nML-KEM-768\n")
            self.assert_schema_valid(cbom.build(scanner.scan(directory), "example"))

    def test_every_algorithm_serializes(self):
        findings = [Finding(k, [Occurrence("sample.py", 1, k)]) for k in ALGORITHMS]
        self.assert_schema_valid(cbom.build(findings, "all-algorithms"))

    def test_rejects_invalid_primitive(self):
        document = cbom.build([Finding("aes-256", [Occurrence("a.py", 1, "AES")])], "bad")
        document["components"][0]["cryptoProperties"]["algorithmProperties"]["primitive"] = "blockcipher"
        self.assertFalse(self.validator.is_valid(document))


if __name__ == "__main__":
    unittest.main()
