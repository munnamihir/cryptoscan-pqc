"""cryptoscan command-line interface."""

import argparse
import json
import os
import sys

from . import scanner, cbom, report
from .knowledge import lookup

EXIT_CLEAN = 0
EXIT_FINDINGS = 1   # quantum-vulnerable assets present (useful for CI gating)
EXIT_ERROR = 2


def _run_scan(args) -> int:
    if not os.path.exists(args.path):
        print(f"error: path not found: {args.path}", file=sys.stderr)
        return EXIT_ERROR

    findings = scanner.scan(args.path)
    target = os.path.basename(os.path.abspath(args.path.rstrip("/"))) or args.path
    bom = cbom.build(findings, target)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(bom, fh, indent=2)
        print(f"CBOM written to {args.output}", file=sys.stderr)

    if args.format == "json":
        print(json.dumps(bom, indent=2))
    elif args.format == "md":
        print(report.markdown(findings, target))
    else:
        print(report.terminal(findings, target, color=not args.no_color))

    if args.fail_on_vulnerable:
        for f in findings:
            a = lookup(f.algo_key)
            if a and a.quantum_status in ("vulnerable", "broken_classical"):
                return EXIT_FINDINGS
    return EXIT_CLEAN


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cryptoscan",
        description="Discover cryptographic assets in a codebase and emit a "
                    "CycloneDX CBOM with post-quantum risk classification.")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("scan", help="scan a file or directory")
    s.add_argument("path", help="file or directory to scan")
    s.add_argument("-o", "--output", help="write CycloneDX CBOM JSON to this file")
    s.add_argument("-f", "--format", choices=["terminal", "md", "json"],
                   default="terminal", help="report written to stdout")
    s.add_argument("--no-color", action="store_true", help="disable ANSI colors")
    s.add_argument("--fail-on-vulnerable", action="store_true",
                   help="exit non-zero if quantum-vulnerable assets are found (CI gate)")
    s.set_defaults(func=_run_scan)
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
