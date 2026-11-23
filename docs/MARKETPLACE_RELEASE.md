# Marketplace v1.1.0 — published release record

The GitHub release [v1.1.0](https://github.com/munnamihir/cryptoscan-pqc/releases/tag/v1.1.0) was published November 23, 2026 following passing tests on `main`. The owner selected GitHub Marketplace publishing in the release editor; independent Marketplace search visibility still needs verification. The PyPI package version is managed separately.

The original release checklist is preserved below as a historical record. See [version tag guidance](VERSIONING.md) before modifying the older published `v1` tag.

## Proposed release

- **Marketplace name:** cryptoscan-pqc (confirm availability when drafting the release)
- **GitHub Action tag:** `v1.1.0` (proposal only)
- **Python package version prepared in this PR:** `0.1.2`
- **Suggested categories:** Security; Continuous integration
- **Suggested title:** CryptoScan PQC v1.1.0 — Hardened Action and valid CBOMs

## Draft release notes

This release improves scanner reproducibility, GitHub Actions security and
CycloneDX 1.6 compatibility.

- Safely handle user-controlled Action inputs through environment variables.
- Install scanner bundled with the chosen Action ref by default; allow an exact
  PyPI version through the optional `version` input.
- Support individual file scans in addition to directory scans.
- Keep CBOM build artifacts even when the scan fails on vulnerable algorithms.
- Add `artifact-name` input to avoid collisions in multi-scan workflows.
- Correct CycloneDX 1.6 primitive names and tools metadata.
- Add offline validation against the official CycloneDX 1.6.2 JSON schema.
- Align version metadata and restore the complete MIT disclaimer.

## Release checklist — requires explicit approval

- [ ] Review the PR diff, test and integration logs.
- [ ] Confirm unit/schema tests pass on Python 3.9 and Python 3.12.
- [ ] Confirm the Action integration job passes (including fail gating and artifact upload).
- [ ] Confirm schema provenance (CycloneDX 1.6.2, Apache-2.0).
- [ ] Check the repository for secrets and verify dependency policies.
- [ ] Confirm the Action name is unique on Marketplace.
- [ ] Obtain approval to merge the PR to `main`.
- [ ] Optionally build and separately release PyPI package `0.1.2` after approval.
- [ ] Obtain approval before creating tag `v1.1.0` on the reviewed commit.
- [ ] Draft the GitHub release and select **Publish this Action to GitHub Marketplace**.
- [ ] Select categories, accept agreement if prompted and complete 2FA.
- [ ] Verify the published Marketplace listing and installation example.

## Reference

The schema at `tests/schemas/bom-1.6.schema.json` is an unmodified snapshot of:
https://github.com/CycloneDX/specification/blob/1.6.2/schema/bom-1.6.schema.json
(Apache License 2.0; development/test fixture only).
