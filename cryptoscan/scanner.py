"""Walk a target path, apply detection rules, and collect findings."""

import os
from dataclasses import dataclass, field
from typing import List

from . import detectors
from .knowledge import lookup, SEVERITY


@dataclass
class Occurrence:
    path: str
    line: int
    evidence: str


@dataclass
class Finding:
    algo_key: str
    occurrences: List[Occurrence] = field(default_factory=list)


# Generic keys that should yield to a more specific sibling on the same line
# (e.g. drop "ml-kem" if "ml-kem-768" also matched, drop "aes" if "aes-256" did)
GENERICS = {"ml-kem", "ml-dsa", "aes"}


def _collapse(keys: set) -> set:
    out = set(keys)
    for g in GENERICS:
        if g in out and any(k != g and k.startswith(g) for k in out):
            out.discard(g)
    return out


def _is_text_file(path: str) -> bool:
    ext = os.path.splitext(path)[1].lower()
    if ext in detectors.TEXT_EXTS:
        return True
    # allow extensionless config-like files but cap size
    return ext == "" and os.path.getsize(path) < 256 * 1024


def scan(target: str) -> List[Finding]:
    """Return findings aggregated by algorithm, sorted by severity then name."""
    findings = {}  # algo_key -> Finding

    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in detectors.SKIP_DIRS]
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                if not _is_text_file(fpath):
                    continue
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    lines = fh.readlines()
            except (OSError, ValueError):
                continue

            rel = os.path.relpath(fpath, target)
            for lineno, text in enumerate(lines, 1):
                matched = {rule.algo for rule, rx in detectors.COMPILED if rx.search(text)}
                for algo_key in _collapse(matched):
                    f = findings.setdefault(algo_key, Finding(algo_key))
                    f.occurrences.append(Occurrence(rel, lineno, text.strip()[:160]))

    def sort_key(f: Finding):
        algo = lookup(f.algo_key)
        sev = SEVERITY.get(algo.quantum_status, 0) if algo else 0
        return (-sev, algo.name if algo else f.algo_key)

    return sorted(findings.values(), key=sort_key)
