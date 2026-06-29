"""Build a CycloneDX 1.6 Cryptographic Bill of Materials (CBOM) from findings."""

import datetime
import uuid
from typing import List

from .knowledge import lookup
from .scanner import Finding

SPEC_VERSION = "1.6"
TOOL_NAME = "cryptoscan"
TOOL_VERSION = "0.1.0"


def _component(finding: Finding) -> dict:
    algo = lookup(finding.algo_key)
    name = algo.name if algo else finding.algo_key

    algo_props = {"primitive": algo.primitive if algo else "unknown"}
    if algo and algo.classical_bits is not None:
        algo_props["classicalSecurityLevel"] = algo.classical_bits
    algo_props["nistQuantumSecurityLevel"] = algo.nist_quantum_level if algo else 0

    crypto_props = {
        "assetType": "algorithm",
        "algorithmProperties": algo_props,
    }
    if algo and algo.oid:
        crypto_props["oid"] = algo.oid

    # cryptoscan-specific risk metadata, exposed as standard CycloneDX properties
    props = [
        {"name": "cryptoscan:quantumStatus",
         "value": algo.quantum_status if algo else "unknown"},
    ]
    if algo and algo.recommendation:
        props.append({"name": "cryptoscan:recommendation", "value": algo.recommendation})
    if algo and algo.replacement:
        props.append({"name": "cryptoscan:replacement", "value": algo.replacement})

    occurrences = [{"location": f"{o.path}:{o.line}"} for o in finding.occurrences]

    return {
        "type": "cryptographic-asset",
        "bom-ref": f"crypto/algorithm/{finding.algo_key}",
        "name": name,
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
            "timestamp": datetime.datetime.now(datetime.timezone.utc)
                                  .isoformat(timespec="seconds"),
            "tools": [{"vendor": "cryptoscan", "name": TOOL_NAME, "version": TOOL_VERSION}],
            "component": {"type": "application", "name": target_name},
        },
        "components": [_component(f) for f in findings],
    }
