# CryptoScan PQC — live demo and report guide

Use the checked-in deliberately vulnerable code, not a real production secret, to see how cryptographic findings are reported.

## 1. Run it on GitHub without installing anything

1. Open [Actions → PQC demo](../.github/workflows/demo.yml).
2. Click **Run workflow** and select `main` after this demo PR is merged.
3. Open the finished run's **Summary**. The job writes a Markdown inventory there.
4. Download the `demo-cbom` artifact from the same run to inspect the CycloneDX 1.6 JSON.

This workflow is **manual only**, uploads a CBOM (not the checked-out source), and uses the pinned `@v1.1.0` release.

## 2. Run it locally

```bash
git clone https://github.com/munnamihir/cryptoscan-pqc.git
cd cryptoscan-pqc
python -m pip install -e .
pqscan scan sample_vulnerable_app/auth.py --no-color
pqscan scan sample_vulnerable_app -f md
pqscan scan sample_vulnerable_app -o cbom.json
```

To try CI gating:

```bash
pqscan scan sample_vulnerable_app --fail-on-vulnerable -o cbom.json
# Expected: exit code 1 because the sample intentionally includes vulnerable crypto.
# The CBOM is written before the nonzero exit.
```

## 3. Example findings from `sample_vulnerable_app`

| Sample | Detected algorithm | Classification | Why review it |
| --- | --- | --- | --- |
| `auth.py` | RSA | Quantum-vulnerable | Classical public-key algorithm |
| `auth.py` | ECDSA | Quantum-vulnerable | Classical elliptic-curve signature algorithm |
| `auth.py` | MD5 | Broken (classical) | Collision attacks are practical |
| `tokens.js` | SHA-1 | Broken (classical) | Insecure for collision-resistant signatures/integrity |
| `nextgen.go` | ML-KEM-768 | Quantum-safe category in scanner | Example post-quantum key encapsulation algorithm |

The scanner reports algorithm occurrences, **not a confirmed exploitable vulnerability**. A rule may match a string, comment, or unused code. Results are a triage aid and require human confirmation.

## 4. What is in a CBOM?

The emitted CycloneDX 1.6 JSON includes a BOM identifier, tool information, cryptographic-asset components, normalized algorithm names, the algorithm primitive, a quantum-status property and occurrence locations.

For the actual schema, see [CycloneDX 1.6.2](https://github.com/CycloneDX/specification/blob/1.6.2/schema/bom-1.6.schema.json). CI validates the package output against this schema.

## 5. Try it in your own repository

Copy [`examples/pqc-scan.yml`](../examples/pqc-scan.yml) into `.github/workflows/pqc-scan.yml` on your own repository. On its next push or PR, you will get an inventory artifact. Keep `fail-on-vulnerable: "false"` until you've reviewed the findings.

If the scanner misses an algorithm or flags a false positive, please [open an issue](https://github.com/munnamihir/cryptoscan-pqc/issues) with a small non-sensitive example and the expected result.
