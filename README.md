# cryptoscan
![ci](https://github.com/munnamihir/cryptoscan/actions/workflows/ci.yml/badge.svg)

**Discover the cryptography in a codebase and emit a CycloneDX CBOM with post-quantum risk classification.**

You cannot migrate cryptography you cannot see. The June 2026 U.S. Executive Order on advanced cryptographic attacks set binding deadlines (2030 for key establishment, 2031 for signatures), extended them to federal contractors, and directed CISA and NIST to define the minimum elements of a **Cryptographic Bill of Materials (CBOM)**. Yet fewer than 5% of enterprises have a comprehensive cryptographic inventory, and existing discovery tooling tends to miss application-layer crypto, config, and firmware.

`cryptoscan` is a small, fast first step: point it at a repository and it produces (1) a prioritized, human-readable inventory and (2) a machine-readable CycloneDX 1.6 CBOM, with every asset classified by its resistance to a cryptographically relevant quantum computer and mapped to its NIST PQC replacement.

## Quick start

```bash
# scan a repo, print a prioritized report
python -m cryptoscan scan ./my-project

# write a CycloneDX 1.6 CBOM
python -m cryptoscan scan ./my-project -o cbom.json

# markdown report (for a PR comment or ticket)
python -m cryptoscan scan ./my-project -f md

# gate a CI pipeline: non-zero exit if quantum-vulnerable crypto is present
python -m cryptoscan scan ./my-project --fail-on-vulnerable
```

## What it finds

| Class | Examples | Verdict |
|---|---|---|
| Classical public-key | RSA, ECDSA, ECDH, DSA, Ed25519, X25519, DH | **Quantum-vulnerable** — broken by Shor's algorithm |
| Weakened symmetric | AES-128 | **Review** — halved by Grover; prefer AES-256 |
| Already broken | MD5, SHA-1, 3DES, RC4, DES | **Broken** — remove regardless of quantum |
| Post-quantum | ML-KEM (Kyber), ML-DSA (Dilithium), SLH-DSA, Falcon, HQC | **Quantum-safe** — migration targets |

Detectors cover Python, JavaScript/TypeScript, Java, Go, C/C++/OpenSSL, .NET/C#, and PEM/TLS config. Detection is rule-based and extensible — add a `Rule` in `detectors.py`, not code.

## Why CycloneDX

CycloneDX has carried cryptographic-asset components since v1.6, and the format is the one named in regulatory CBOM guidance. Emitting standards-compliant output means the result drops straight into existing SBOM/CBOM pipelines and tooling rather than living in a bespoke format.

## Architecture

```
detectors.py   rule set: regex -> normalized algorithm key
knowledge.py   algorithm intelligence: quantum status, NIST level, replacement
scanner.py     walk files, apply rules, collapse + dedupe -> findings
cbom.py        findings -> CycloneDX 1.6 CBOM
report.py      findings -> terminal / markdown
cli.py         `cryptoscan scan <path>`
```

## Honest limitations

This is rule-based static discovery, not a substitute for a validated commercial inventory platform. It finds *named* crypto in source and config; it does not resolve crypto reached only through deep dependency chains, dynamically selected algorithms, or compiled binaries without source. It reports where cryptography *is*, not where it is missing. Treat it as the fast 80% pass that scopes the harder work.

## Roadmap

- Dependency-aware detection (parse lockfiles; flag crypto libraries by version)
- Key/parameter extraction from PEM and X.509 (sizes, signature algorithms)
- Confidence scoring and false-positive suppression
- SARIF output for code-scanning UIs
- A web dashboard over the CBOM (trend the inventory over time — the "continuous" gap)

## License

MIT.
