"""Build a CycloneDX 1.6 Cryptographic Bill of Materials (CBOM)."""

import datetime
import uuid
from typing import List

from . import __version__
from .knowledge import lookup
from .scanner import Finding

SPEC_VERSION = "1.6"
TOOL_NAME = "cryptoscan-pqc"


def _component(finding: Finding) -> dict:
    algo = lookup(finding.algo_key)
    algo_props = {"primitive": algo.primitive if algo else "unknown"}
    if algo and algo.classical_bits is not None:
        algo_props["classicalSecurityLevel"] = algo.classical_bits
    algo_props["nistQuantumSecurityLevel"] = algo.nist_quantum_level if algo else 0
    crypto_props = {"assetType": "algorithm", "algorithmProperties": algo_props}
    if algo and algo.oid:
        crypto_props["oid"] = algo.oid
    props = [{"name": "cryptoscan:quantumStatus",
              "value": algo.quantum_status if algo else "unknown"}]
    if algo and algo.recommendation:
        props.append({"name": "cryptoscan:recommendation", "value": algo.recommendation})
    if algo and algo.replacement:
        props.append({"name": "cryptoscan:replacement", "value": algo.replacement})
    occurrences = [{"location": o.path, "line": o.line} for o in finding.occurrences]
    return {
        "type": "cryptographic-asset",
        "bom-ref": f"crypto/algorithm/{finding.algo_key}",
        "name": algo.name if algo else finding.algo_key,
        "cryptoProperties": crypto_props,
        "properties": props,
        "evidence": {"occurrences": occurrences},
    }


def build(findings: List[Finding], target_name: str) -> dict:
    return {
        "bomFormat": "CycloneDX",
        "specVersion": SPEC_VERSION,
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "tools": {"components": [
                {"type": "application", "name": TOOL_NAME, "version": __version__}
            ]},
            "component": {"type": "application", "name": target_name},
        },
        "components": [_component(f) for f in findings],
    }
