"""Build an offline interactive HTML dashboard from a CycloneDX 1.6 CBOM.

This program performs no network activity. Embedded JSON is escaped to prevent
</script> data from becoming executable markup in the generated report.
"""

import argparse
import json
from pathlib import Path

SCRIPT_MARKER = '<script id="bootstrap-data" type="application/json">null</script>'
MAX_CBOM_BYTES = 30 * 1024 * 1024


def build_dashboard(cbom_path, output_path, template_path=None):
    cbom_path = Path(cbom_path)
    output_path = Path(output_path)
    template_path = Path(template_path) if template_path else Path(__file__).with_name("index.html")

    if cbom_path.stat().st_size > MAX_CBOM_BYTES:
        raise ValueError("CBOM exceeds 30 MB offline viewer limit")
    data = json.loads(cbom_path.read_text(encoding="utf-8"))
    if (
        not isinstance(data, dict)
        or data.get("bomFormat") != "CycloneDX"
        or data.get("specVersion") != "1.6"
        or not isinstance(data.get("components"), list)
    ):
        raise ValueError("Expected a CycloneDX 1.6 JSON CBOM with components")

    # JSON text inside a script element must escape the literal '<' character.
    safe_payload = json.dumps(data, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")
    template = template_path.read_text(encoding="utf-8")
    if template.count(SCRIPT_MARKER) != 1:
        raise ValueError("Dashboard template is missing its bootstrap marker")
    rendered = template.replace(
        SCRIPT_MARKER,
        '<script id="bootstrap-data" type="application/json">' + safe_payload + "</script>",
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cbom", help="CycloneDX 1.6 CBOM JSON file")
    parser.add_argument("-o", "--output", default="cryptoscan-dashboard.html", help="Self-contained output HTML")
    args = parser.parse_args()
    result = build_dashboard(args.cbom, args.output)
    print("Dashboard generated:", result)


if __name__ == "__main__":
    main()
