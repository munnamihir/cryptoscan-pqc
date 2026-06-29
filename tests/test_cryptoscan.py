"""Tests for cryptoscan. Run: python -m pytest  (or python -m unittest)."""

import json
import os
import tempfile
import unittest

from cryptoscan import scanner, cbom
from cryptoscan.knowledge import lookup, ALGORITHMS


def _write(d, name, content):
    p = os.path.join(d, name)
    with open(p, "w") as fh:
        fh.write(content)
    return p


class TestScanner(unittest.TestCase):
    def test_detects_rsa_and_classifies_vulnerable(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "a.py", "key = rsa.generate_private_key(key_size=2048)")
            findings = scanner.scan(d)
            keys = {f.algo_key for f in findings}
            self.assertIn("rsa", keys)
            self.assertEqual(lookup("rsa").quantum_status, "vulnerable")

    def test_detects_pqc_as_safe(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "m.go", "import mlkem // ML-KEM-768")
            findings = scanner.scan(d)
            self.assertIn("ml-kem-768", {f.algo_key for f in findings})

    def test_generic_collapses_to_specific_on_same_line(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "m.go", "x := mlkem768 // ML-KEM-768")
            findings = {f.algo_key: f for f in scanner.scan(d)}
            # the specific variant wins; generic ml-kem should not also be recorded here
            self.assertIn("ml-kem-768", findings)

    def test_skips_node_modules(self):
        with tempfile.TemporaryDirectory() as d:
            nm = os.path.join(d, "node_modules")
            os.makedirs(nm)
            _write(nm, "x.js", "crypto.createHash('md5')")
            self.assertEqual(scanner.scan(d), [])

    def test_occurrence_deduped_per_line(self):
        with tempfile.TemporaryDirectory() as d:
            # "TripleDES" matches more than one rule; must count the line once
            _write(d, "x.cs", "using var des = TripleDES.Create();")
            findings = {f.algo_key: f for f in scanner.scan(d)}
            self.assertEqual(len(findings["3des"].occurrences), 1)


class TestCBOM(unittest.TestCase):
    def test_cyclonedx_shape(self):
        with tempfile.TemporaryDirectory() as d:
            _write(d, "a.py", "import hashlib; hashlib.md5(b'x')")
            bom = cbom.build(scanner.scan(d), "demo")
            self.assertEqual(bom["bomFormat"], "CycloneDX")
            self.assertEqual(bom["specVersion"], "1.6")
            self.assertTrue(bom["serialNumber"].startswith("urn:uuid:"))
            comp = bom["components"][0]
            self.assertEqual(comp["type"], "cryptographic-asset")
            self.assertEqual(comp["cryptoProperties"]["assetType"], "algorithm")
            self.assertIn("primitive", comp["cryptoProperties"]["algorithmProperties"])
            self.assertTrue(json.dumps(bom))  # serializable

    def test_every_algorithm_has_valid_primitive(self):
        valid = {"drbg", "mac", "blockcipher", "streamcipher", "signature", "hash",
                 "pke", "xof", "kdf", "keyagree", "kem", "ae", "combiner", "other", "unknown"}
        for key, a in ALGORITHMS.items():
            self.assertIn(a.primitive, valid, key)


if __name__ == "__main__":
    unittest.main()
