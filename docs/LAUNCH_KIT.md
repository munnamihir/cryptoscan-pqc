# Launch kit: first 10 external CryptoScan PQC adopters

## Positioning

**One-line pitch:** Identify cryptographic algorithms in source code, prioritize potential post-quantum migration work, and produce a CycloneDX 1.6 CBOM in GitHub Actions.

**Best audience:** application security engineers, security-focused platform teams, DevSecOps maintainers and developers exploring post-quantum migration.

**Do not claim:** that the scanner proves a repository is quantum-safe, meets regulatory requirements, or performs deep dependency/binary analysis. Detection is regex-based and can produce false positives/negatives.

## Shareable links

- Repository: https://github.com/munnamihir/cryptoscan-pqc
- Tested release: https://github.com/munnamihir/cryptoscan-pqc/releases/tag/v1.1.0
- Demo workflow: https://github.com/munnamihir/cryptoscan-pqc/actions/workflows/demo.yml
- Integration example: https://github.com/munnamihir/cryptoscan-pqc/blob/main/examples/pqc-scan.yml
- Sample findings: https://github.com/munnamihir/cryptoscan-pqc/blob/main/docs/DEMO.md

## LinkedIn launch draft

> Open-sourced CryptoScan PQC: a small Python CLI and GitHub Action that finds cryptographic algorithms in source code and generates a CycloneDX 1.6 CBOM. It flags classical public-key cryptography, legacy hashes, and selected PQC primitives to help scope migration discussions.
>
> The Action now supports single-file scans, configurable CI gating, artifact uploads even when findings fail a job, and schema-validated CBOM output.
>
> This is heuristic discovery, not a certification. I'd appreciate feedback from AppSec and platform engineers: which algorithms or integrations should I support next?
>
> Repo + demo: https://github.com/munnamihir/cryptoscan-pqc

## Short developer-community launch draft

> I built an open-source GitHub Action for finding named cryptographic algorithms in application source code and emitting CycloneDX 1.6 CBOMs. Current rules cover Python, JS/TS, Java, Go, C/C++ and .NET. I've tested single-file scanning, CBOM schema validation, and CI failure/artifact behavior. It's heuristic rather than dependency-aware. What would make this useful in your CI workflow? https://github.com/munnamihir/cryptoscan-pqc

Only post where community rules permit self-promotion. Share the source, limitations and demo, not sensational claims.

## Adoption experiment

1. Ask 10 relevant **opt-in** engineers to try the example workflow (avoid mass DMs).
2. Give them a one-command local demo and a manual-only Action demo.
3. Request one concrete item per tester: false positive, missed algorithm, output-format issue, or feature request.
4. Log genuine outside-repo adoption separately from stars, forks, and page views.
5. Improve the top 1–2 user-blocking issues in a patch release and report what changed.

## What to measure

| Metric | Definition |
| --- | --- |
| External adopters | Outside-repo teams or developers who confirm running the Action |
| Retained users | People who intentionally keep it in CI after review |
| Issue quality | Reproducible bugs/feature requests |
| Detection quality | Verified false positives and missed algorithms from safe examples |
| Open-source interest | Non-author PRs, forks or stars (signals, not proof of usage) |

No traction figures are claimed until observed.
