# CryptoScan PQC Action v1.2.0 — release candidate

**Status: prepared for review, not published.** The current tagged Marketplace release remains `v1.1.0`.

## Customer-facing improvement

When the v1.2.0 Action is published, third-party workflows will automatically receive:

- `cbom` (or the custom `artifact-name`) — original CycloneDX 1.6 JSON
- `cbom-dashboard` (or `<artifact-name>-dashboard`) — a self-contained interactive HTML report for browsing evidence and reviewing migration recommendations

Dashboard processing is offline; the Action performs **no data upload to a dashboard server**. GitHub Actions artifacts are stored in the consumer repository according to that repository's permissions/retention policy.

### Inputs added (only present in source on `main` until v1.2.0 is published)

| Input | Default | Description |
| --- | --- | --- |
| `dashboard` | `true` | Generate and upload HTML alongside JSON |
| `dashboard-output` | `cryptoscan-dashboard.html` | Output HTML file path |

The dashboard artifact name is automatically derived from the JSON artifact name, with `-dashboard`.

### Example for the future release (do not use until published)

```yaml
- uses: munnamihir/cryptoscan-pqc@v1.2.0
  with:
    path: .
    artifact-name: cbom
    dashboard: "true"
    fail-on-vulnerable: "false"
```

Even with `fail-on-vulnerable: "true"`, the Action attempts to upload the JSON and HTML **after scanner returns exit status 1 due to findings**. A missing/invalid CBOM is a build error and may prevent dashboard output.

## Release checks

- [ ] CI: tests pass on Python 3.9 and 3.12
- [ ] CI: Action integration succeeds with HTML embedded from the exact CBOM
- [ ] CI: failing vulnerability gate still uploads both JSON and dashboard
- [ ] CI: no-dashboard setting still uploads JSON but no dashboard
- [ ] CI: potentially hostile file paths cannot become shell commands
- [ ] CI: all expected GitHub Actions artifacts visible
- [ ] Verify automatic dashboard generation works from Action source in third-party-style integration job
- [ ] Verify new release tag targets the tested `main` commit
- [ ] Review new source code, permissions and privacy implications
- [ ] **Explicit maintainer approval required** to create/publish release `v1.2.0` and Marketplace listing
- [ ] Update README and copyable workflow to `@v1.2.0` only **after** release publication
- [ ] Manual smoke test on an outside repository using the tagged version

Do not move legacy `v1` (an earlier published release) or rewrite the immutable `v1.1.0` tag.
