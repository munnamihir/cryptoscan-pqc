# CryptoScan PQC

[![Release](https://img.shields.io/github/v/release/munnamihir/cryptoscan-pqc)](https://github.com/munnamihir/cryptoscan-pqc/releases/tag/v1.1.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

![ci](https://github.com/munnamihir/cryptoscan-pqc/actions/workflows/ci.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/cryptoscan-pqc.svg)](https://pypi.org/project/cryptoscan-pqc/)

**Discover the cryptography in a codebase and emit a CycloneDX CBOM with post-quantum risk classification.**

You cannot migrate cryptography you cannot see. The [June 22, 2026 U.S. Executive Order](https://www.whitehouse.gov/presidential-actions/2026/06/securing-the-nation-against-advanced-cryptographic-attacks/) directs a post-quantum migration strategy for federal systems, targets high-value and high-impact federal assets for 2030/2031 transitions, calls for proposed contractor rules, and directs CISA and NIST to develop minimum CBOM guidance. A source-code inventory is a practical **first step** toward understanding migration work; it is not a compliance assessment.

`cryptoscan-pqc` is a small, fast first step: point it at a repository and it produces (1) a prioritized, human-readable inventory and (2) a machine-readable CycloneDX 1.6 CBOM, with every asset classified by its resistance to a cryptographically relevant quantum computer and mapped to its NIST PQC replacement.

## Install

```bash
python -m pip install cryptoscan-pqc
```

The CLI is released to PyPI separately. The GitHub Action uses the scanner bundled with the selected Action tag by default, so `@v1.1.0` contains its tested scanner code.

## Quick start

```bash
# scan a repo, print a prioritized report
pqscan scan ./my-project

# write a CycloneDX 1.6 CBOM
pqscan scan ./my-project -o cbom.json

# markdown report (for a PR comment or ticket)
pqscan scan ./my-project -f md

# gate a CI pipeline: non-zero exit if quantum-vulnerable crypto is present
pqscan scan ./my-project --fail-on-vulnerable
```

(The same entry point is available as `python -m cryptoscan scan ...`.)

## Run a reproducible demo

```bash
git clone https://github.com/munnamihir/cryptoscan-pqc.git
cd cryptoscan-pqc
python -m pip install -e .
pqscan scan sample_vulnerable_app --no-color
pqscan scan sample_vulnerable_app -f md
pqscan scan sample_vulnerable_app -o cbom.json
```

The bundled sample intentionally contains insecure and post-quantum cryptography. Try the [interactive GitHub Actions demo](.github/workflows/demo.yml) (Actions → **PQC demo** → Run workflow), read the [annotated findings](docs/DEMO.md), or explore the [copyable integration example](examples/pqc-scan.yml).

## Use it in GitHub Actions

```yaml
name: Cryptography inventory
on: [push, pull_request]

permissions:
  contents: read

jobs:
  scan:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: munnamihir/cryptoscan-pqc@v1.1.0
        with:
          path: .
          output: cbom.json
          artifact-name: cbom
          fail-on-vulnerable: "true"
```

**Note:** `fail-on-vulnerable: "true"` deliberately fails the job on detected risks; the CBOM is still uploaded under **Actions → run → Artifacts**. Start with `"false"` to inventory without gating. Prefer `@v1.1.0` over the older `@v1` tag until its compatibility review and tag update are complete.

The Action installs the **scanner bundled with the referenced Action commit/tag** by default, scans the target, and uploads the generated CycloneDX CBOM. With `fail-on-vulnerable: "true"`, the job fails on quantum-vulnerable or classically broken cryptography **while still uploading the CBOM**.

| Action input | Default | Meaning |
|---|---|---|
| `path` | `.` | File or directory to scan |
| `output` | `cbom.json` | CBOM output filename |
| `artifact-name` | `cbom` | Unique artifact name within a workflow run |
| `fail-on-vulnerable` | `false` | Return a nonzero exit code for vulnerable/broken cryptography |
| `version` | *(empty)* | Optional exact PyPI version instead of bundled source |

**Scope:** Cryptography discovery is heuristic. Findings require human review; matches in comments, configuration or dependencies do not prove exploitability. The CBOM artifact includes detected algorithm names and source file/line locations. See the [Marketplace release checklist](docs/MARKETPLACE_RELEASE.md).

## What it finds

| Class | Examples | Verdict |
|---|---|---|
| Classical public-key | RSA, ECDSA, ECDH, DSA, Ed25519, X25519, DH | **Quantum-vulnerable** — broken by Shor's algorithm |
| Weakened symmetric | AES-128 | **Review** — halved by Grover; prefer AES-256 |
| Already broken | MD5, SHA-1, 3DES, RC4, DES | **Broken** — remove regardless of quantum |
| Post-quantum | ML-KEM (Kyber), ML-DSA (Dilithium), SLH-DSA, Falcon, HQC | **Quantum-safe** — migration targets |

Detectors cover Python, JavaScript/TypeScript, Java, Go, C/C++/OpenSSL, .NET/C#, and PEM/TLS config. Detection is rule-based and extensible — add a `Rule` in `detectors.py`, not code.

## Why CycloneDX

CycloneDX 1.6 models cryptographic assets within a standardized BOM. CryptoScan generates this format and runs schema checks against the official CycloneDX 1.6.2 JSON schema. This helps downstream inventory workflows ingest the results; it does **not** mean every detection is verified or that a project is compliant with a regulation.

## Architecture

```
detectors.py   rule set: regex -> normalized algorithm key
knowledge.py   algorithm intelligence: quantum status, NIST level, replacement
scanner.py     walk files, apply rules, collapse + dedupe -> findings
cbom.py        findings -> CycloneDX 1.6 CBOM
report.py      findings -> terminal / markdown
cli.py         `pqscan scan <path>`
```

## Honest limitations

This is rule-based static discovery, not a substitute for a validated commercial inventory platform. It finds *named* crypto in source and config; it does not resolve crypto reached only through deep dependency chains, dynamically selected algorithms, or compiled binaries without source. It reports where cryptography *is*, not where it is missing. Treat the report as a review queue: inspect each finding, confirm whether the algorithm is actually used in a security-sensitive context, and prioritize remediation.

## Roadmap

- `--ignore` paths and comment/string awareness to cut false positives
- Dependency-aware detection (parse lockfiles; flag crypto libraries by version)
- Key/parameter extraction from PEM and X.509 (sizes, signature algorithms)
- SARIF output for code-scanning UIs
- A web dashboard over the CBOM (trend the inventory over time — the "continuous" gap)

## Get involved

Try the [live demo workflow](.github/workflows/demo.yml), check the [sample report](docs/DEMO.md), and [open an issue](https://github.com/munnamihir/cryptoscan-pqc/issues) with false positives, missing algorithms or integration questions. Feedback and reproductions are more useful than unverified security claims.

If you want to help grow the project, see the [community launch kit](docs/LAUNCH_KIT.md) and [version-tag guidance](docs/VERSIONING.md). This is an open-source heuristic scanner, not a certification or vulnerability exploit detector.

## License

[MIT](LICENSE).
