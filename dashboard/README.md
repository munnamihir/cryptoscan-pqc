# CryptoScan PQC — CBOM Intelligence Dashboard

A local-first, no-backend interactive viewer for **CycloneDX 1.6** CBOM JSON.

## What it does

- Distinguishes quantum-vulnerable, classically broken, review, informational and quantum-safe algorithm detections.
- Shows file contexts (application source, dependency metadata, documentation, vendor, tests), file locations and a review-first triage queue.
- Explores algorithm recommendations and potential migration replacements.
- Searches/filter findings and exports a CSV review list.
- Optional `owner/repo` text box links file and line references to GitHub for manual review.
- No telemetry, hosted APIs, or external JavaScript. JSON stays in your browser.

**Important:** Algorithm references are heuristic matches, **not confirmed vulnerabilities, compliance determinations, or proof of effective deployment**. A CBOM is a snapshot, not a trend or security score.

## Open a CBOM locally

Open [index.html](index.html) in Chrome, Firefox or Safari, then choose **Load CBOM JSON** and select a report.

Or build an HTML file that already includes a CBOM:

```bash
python3 dashboard/build_dashboard.py cbom.json -o cryptoscan-dashboard.html
```

Open the generated HTML in any browser. The HTML is self-contained, can be archived, and needs no network access. The original CBOM remains unchanged.

## GitHub Actions

When you run this repository's **Scan public GitHub repository** workflow after this change is merged, you receive two artifacts:

- `github-repository-cbom` — the original machine-readable CycloneDX 1.6 JSON.
- `github-repository-dashboard` — the self-contained `github-repository-dashboard.html` that opens directly in a browser.

The repository's **PQC demo** workflow also uploads a self-contained dashboard.

The published Marketplace Action `@v1.1.0` **does not yet auto-generate dashboards** for third-party repositories. This repository's Action source has an opt-out dashboard step prepared for **`v1.2.0`** (release pending). When published, consumers will receive `<artifact-name>` for JSON and `<artifact-name>-dashboard` for HTML by default. Use `dashboard: "false"` to disable or `dashboard-output: "custom-name.html"` to customize the output path. Don't use `@v1.2.0` until the versioned release exists.

## Privacy

Opening a dashboard locally does not send the CBOM to a server. However, generated HTML **contains the source CBOM inline**, including file names and line references. Do not publish or forward it if those paths are sensitive. The viewer only builds GitHub links if a user types an optional repository identifier.
