"""Validate and normalize a GitHub repository for a read-only public scan."""

import re
import sys
from urllib.parse import urlsplit

OWNER = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?")
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]{1,100}")


def normalize_repository(value: str) -> str:
    """Accept owner/repo or https://github.com/owner/repo[.git]; reject others."""
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("Enter a public GitHub repository as owner/repo or its HTTPS URL.")

    if "://" in value:
        url = urlsplit(value)
        if (
            url.scheme != "https"
            or url.netloc.lower() != "github.com"
            or url.query
            or url.fragment
        ):
            raise ValueError("Only https://github.com/owner/repo URLs are supported.")
        value = url.path.strip("/")
        if value.endswith(".git"):
            value = value[:-4]
    elif value.startswith("github.com/"):
        raise ValueError("Include https:// for repository URLs, or use owner/repo.")

    pieces = value.split("/")
    if len(pieces) != 2:
        raise ValueError("Expected exactly owner/repo, without additional paths.")
    owner, name = pieces
    if (
        not OWNER.fullmatch(owner)
        or not REPOSITORY.fullmatch(name)
        or name in {".", ".."}
        or ".." in name
    ):
        raise ValueError("Invalid GitHub owner/repository identifier.")
    return f"{owner}/{name}"


def main() -> int:
    try:
        if len(sys.argv) != 2:
            raise ValueError("Expected one GitHub repository name or HTTPS URL.")
        repository = normalize_repository(sys.argv[1])
    except ValueError as exc:
        print(f"::error::{exc}", file=sys.stderr)
        return 2
    # Safe for direct append to GITHUB_OUTPUT: repository is strictly validated.
    print(f"repository={repository}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
