"""Human-readable reporting: a terminal summary and a markdown report."""

from typing import List

from .knowledge import lookup, SEVERITY
from .scanner import Finding

LABEL = {
    "vulnerable": "QUANTUM-VULNERABLE",
    "broken_classical": "BROKEN (classical)",
    "review": "REVIEW",
    "informational": "INFO",
    "safe": "QUANTUM-SAFE",
}

# ANSI colors for the terminal
COLOR = {
    "vulnerable": "\033[91m", "broken_classical": "\033[95m", "review": "\033[93m",
    "informational": "\033[90m", "safe": "\033[92m",
}
RESET = "\033[0m"


def _counts(findings: List[Finding]):
    c = {}
    for f in findings:
        algo = lookup(f.algo_key)
        status = algo.quantum_status if algo else "unknown"
        c[status] = c.get(status, 0) + 1
    return c


def terminal(findings: List[Finding], target: str, color: bool = True) -> str:
    out = [f"\ncryptoscan — cryptographic inventory for {target}\n" + "=" * 60]
    c = _counts(findings)
    vuln = c.get("vulnerable", 0) + c.get("broken_classical", 0)
    out.append(f"{len(findings)} crypto assets found · "
               f"{vuln} need migration · {c.get('safe',0)} already quantum-safe\n")

    for f in findings:
        algo = lookup(f.algo_key)
        status = algo.quantum_status if algo else "unknown"
        tag = LABEL.get(status, status.upper())
        if color:
            tag = f"{COLOR.get(status,'')}{tag}{RESET}"
        name = algo.name if algo else f.algo_key
        out.append(f"[{tag}] {name}  ({len(f.occurrences)} occurrence"
                   f"{'s' if len(f.occurrences) != 1 else ''})")
        if algo and algo.recommendation:
            out.append(f"    → {algo.recommendation}")
        for o in f.occurrences[:3]:
            out.append(f"      {o.path}:{o.line}")
        if len(f.occurrences) > 3:
            out.append(f"      … and {len(f.occurrences) - 3} more")
        out.append("")
    return "\n".join(out)


def markdown(findings: List[Finding], target: str) -> str:
    c = _counts(findings)
    vuln = c.get("vulnerable", 0) + c.get("broken_classical", 0)
    lines = [
        f"# Cryptographic inventory — {target}",
        "",
        f"- **{len(findings)}** cryptographic assets detected",
        f"- **{vuln}** require migration (quantum-vulnerable or broken)",
        f"- **{c.get('safe', 0)}** already quantum-safe",
        "",
        "| Asset | Status | Occurrences | Recommendation |",
        "|---|---|---|---|",
    ]
    for f in findings:
        algo = lookup(f.algo_key)
        status = algo.quantum_status if algo else "unknown"
        name = algo.name if algo else f.algo_key
        rec = (algo.recommendation if algo else "").replace("|", "/")
        lines.append(f"| {name} | {LABEL.get(status, status)} | "
                     f"{len(f.occurrences)} | {rec} |")
    lines.append("")
    return "\n".join(lines)
