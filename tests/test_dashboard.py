"""Unit tests for offline CBOM report generation (no network)."""

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from dashboard.build_dashboard import SCRIPT_MARKER, build_dashboard


class DashboardBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)

    def write(self, data):
        path = self.root / "cbom.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_embeds_report_and_requires_no_external_assets(self):
        cbom = {
            "bomFormat": "CycloneDX", "specVersion": "1.6",
            "components": [{
                "name": "Ed25519", "type": "cryptographic-asset",
                "properties": [{"name": "cryptoscan:quantumStatus", "value": "vulnerable"}],
                "evidence": {"occurrences": [{"location": "src/security.py", "line": 42}]},
            }],
        }
        output = self.root / "dashboard.html"
        self.assertEqual(build_dashboard(self.write(cbom), output), output)
        content = output.read_text(encoding="utf-8")
        self.assertIn("CryptoScan PQC — CBOM Intelligence", content)
        self.assertIn('"name":"Ed25519"', content)
        self.assertIn('"line":42', content)
        self.assertNotIn(SCRIPT_MARKER, content)
        self.assertNotIn("https://cdn.", content)

    def test_script_injection_is_escaped(self):
        attack = '</script><script>window.injection = true</script>'
        cbom = {
            "bomFormat": "CycloneDX", "specVersion": "1.6",
            "components": [{"name": attack, "type": "cryptographic-asset"}],
        }
        output = self.root / "report.html"
        build_dashboard(self.write(cbom), output)
        html = output.read_text(encoding="utf-8")
        self.assertNotIn(attack, html)
        self.assertIn("\\u003c/script>", html)
        self.assertEqual(html.count('<script id="bootstrap-data" type="application/json">'), 1)

    def test_wrong_formats_are_rejected(self):
        for data in ([], {}, {"bomFormat": "CycloneDX", "specVersion": "1.5", "components": []}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                build_dashboard(self.write(data), self.root / "report.html")

    def test_dashboard_javascript_syntax(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node not installed")
        html = (Path(__file__).resolve().parents[1] / "dashboard" / "index.html").read_text(encoding="utf-8")
        script = html.split("<script>\n", 1)[1].split("\n</script>", 1)[0]
        js_file = self.root / "viewer.js"
        js_file.write_text(script, encoding="utf-8")
        subprocess.run([node, "--check", str(js_file)], check=True, capture_output=True, text=True)


if __name__ == "__main__":
    unittest.main()
