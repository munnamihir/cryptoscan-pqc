# Scan a public GitHub repository without installing Python

Repository maintainers can use [Scan public GitHub repository](../.github/workflows/scan-repository.yml) to scan another public repository. **GitHub requires write access to the CryptoScan repository to start its manual workflow.** If you are an external visitor, use [the copyable Action workflow](../examples/pqc-scan.yml) in a repository you own; this is the supported no-local-installation path.

[View the completed sample demo](https://github.com/munnamihir/cryptoscan-pqc/actions/runs/45247523530).

## Steps for CryptoScan maintainers

1. Open **Actions** in the CryptoScan PQC repository.
2. Select **Scan public GitHub repository** in the left workflow list.
3. Click **Run workflow** and paste a public repository, e.g. `octocat/Hello-World` or `https://github.com/munnamihir/cryptoscan-pqc`.
4. Run the workflow, then open the completed run.
5. Read the **Summary** for a human-readable cryptographic inventory.
6. Download the **github-repository-cbom** artifact for the CycloneDX 1.6 JSON output.

No local Python installation is needed. The workflow uses CryptoScan PQC `v1.1.0` and never executes code from the selected repository.

## What the public scan does

- Validates that the input is exactly `owner/repo` or an HTTPS GitHub repository URL
- Verifies that GitHub reports the repository as public
- Checks out its **default branch only** with no persisted credentials, without submodules or LFS
- Scans repository text using heuristic rules (it does **not** execute checked-out source)
- Uploads a CBOM and adds a Markdown inventory to the GitHub Actions Summary
- Runs in **inventory mode**: cryptographic findings do not fail the workflow

## Constraints and security

- **Public repositories only.** This is a deliberately read-only scanner, not a credentialed private-repository scanner. For private repositories, add the published Action to an authorized workflow in that repository.
- **Permissions:** workflow job has `contents: read` only. Checkout credentials are not persisted.
- **Duration:** job timeout is 15 minutes; very large repositories may time out. The scanner does not analyze compiled binaries or dependency graphs.
- **Accuracy:** regex detections can identify references in comments and documentation or miss cryptography used indirectly. Review results before treating them as vulnerabilities or compliance findings.
- **Privacy:** the resulting CBOM includes algorithm names and source file/line paths. Do not scan private or sensitive repositories with a publicly visible workflow report.

## Continuous scanning in your own repository (recommended for visitors)

Copy [`examples/pqc-scan.yml`](../examples/pqc-scan.yml) into your repository's `.github/workflows/pqc-scan.yml` to run the Action on every push and pull request. This does not require the manual on-demand workflow.
