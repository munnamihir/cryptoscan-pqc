"""Walk a target file or directory, apply detection rules, and collect findings."""

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
    return ext == "" and os.path.getsize(path) < 256 * 1024


def _candidate_files(target: str):
    """Yield (filename, scan_root), supporting both files and directories."""
    scan_root = os.path.abspath(target)
    if os.path.isfile(scan_root):
        yield scan_root, os.path.dirname(scan_root)
        return
    for root, dirs, files in os.walk(scan_root):
        dirs[:] = [d for d in dirs if d not in detectors.SKIP_DIRS]
        for fname in files:
            yield os.path.join(root, fname), scan_root


def scan(target: str) -> List[Finding]:
    """Return findings aggregated by algorithm, sorted by severity then name."""
    findings = {}
    for fpath, scan_root in _candidate_files(target):
        try:
            if not _is_text_file(fpath):
                continue
            with open(fpath, "r", encoding="utf-8", errors="ignore") as handle:
                for lineno, line in enumerate(handle, 1):
                    matched = {rule.algo for rule, rx in detectors.COMPILED if rx.search(line)}
                    for algo_key in _collapse(matched):
                        finding = findings.setdefault(algo_key, Finding(algo_key))
                        finding.occurrences.append(
                            Occurrence(os.path.relpath(fpath, scan_root), lineno, line.strip()[:160])
                        )
        except (OSError, ValueError):
            continue

    def sort_key(finding: Finding):
        algo = lookup(finding.algo_key)
        severity = SEVERITY.get(algo.quantum_status, 0) if algo else 0
        return (-severity, algo.name if algo else finding.algo_key)

    return sorted(findings.values(), key=sort_key)
