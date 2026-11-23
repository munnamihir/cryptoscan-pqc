# Action version tags

## Current verified release

- `v1.1.0` is the tested, published patch-level Action release.
- At the time of this document, `v1` remains attached to a **previous published GitHub release**, pointing to older code.
- Do not suggest `@v1` as the default install snippet until its target is deliberately updated.
- The README uses `@v1.1.0` for repeatability and safety.

## About moving `v1`

GitHub recommends floating major tags such as `v1` **when the action author maintains them**. Moving a tag changes the Action code pulled by workflows that use it. In this repository, `v1` is also the tag of an older published GitHub release; force-moving it would change the commit associated with that historical release.

Before deciding to move `v1`:

1. Confirm backward compatibility for every published `action.yml` input and behavior.
2. Review any existing users depending on `@v1`; announce the change if appropriate.
3. Decide whether preserving the historical `v1` release reference is more important than a floating major tag.
4. Re-run tests and pin the target to the known `v1.1.0` commit.
5. Obtain explicit maintainer approval **before force-updating any tag**.

Do not reassign the immutable semver tag `v1.1.0`. Never force-move major tags automatically without a documented release policy. Consumers who want immutable, auditable dependencies can pin a full commit SHA.

GitHub reference: https://docs.github.com/en/actions/how-tos/create-and-publish-actions/manage-custom-actions
