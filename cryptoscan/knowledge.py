"""
Cryptographic algorithm intelligence.

Maps a normalized algorithm key to its quantum-readiness profile. This is the
substance of the tool: it encodes *why* each algorithm is or isn't safe against
a cryptographically relevant quantum computer (CRQC), and what to migrate to.

Quantum status values:
  vulnerable        - broken by Shor's algorithm (all classical public-key crypto)
  review            - weakened by Grover but not broken; acceptable now, plan an upgrade
  broken_classical  - already broken/deprecated regardless of quantum (e.g. MD5, RC4)
  safe              - quantum-resistant (NIST PQC) or unaffected at current parameters
  informational     - not a quantum-relevant decision point (e.g. password hashing)

nist_quantum_level: NIST PQC security category (1,3,5). 0 = not quantum-safe.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Algo:
    name: str
    primitive: str            # CycloneDX 1.6 primitive enum
    family: str
    quantum_status: str
    classical_bits: Optional[int] = None
    nist_quantum_level: int = 0
    oid: Optional[str] = None
    recommendation: str = ""
    replacement: Optional[str] = None


# Severity ordering for sorting / summaries (higher = more urgent)
SEVERITY = {
    "vulnerable": 4,
    "broken_classical": 3,
    "review": 2,
    "informational": 1,
    "safe": 0,
}

_SHOR = "Public-key scheme broken by Shor's algorithm on a CRQC."
_GROVER = "Symmetric strength halved by Grover's algorithm; size the key accordingly."

ALGORITHMS = {
    # ---- Classical public-key: broken by Shor -------------------------------
    "rsa": Algo("RSA", "pke", "rsa", "vulnerable", 112, 0, "1.2.840.113549.1.1.1",
                _SHOR + " Migrate key exchange to ML-KEM and signatures to ML-DSA.",
                "ML-KEM-768 / ML-DSA-65"),
    "dsa": Algo("DSA", "signature", "dsa", "vulnerable", 112, 0, "1.2.840.10040.4.1",
                _SHOR + " Replace signatures with ML-DSA or SLH-DSA.", "ML-DSA-65"),
    "dh": Algo("Diffie-Hellman", "keyagree", "dh", "vulnerable", 112, 0, None,
               _SHOR + " Replace key agreement with ML-KEM.", "ML-KEM-768"),
    "ecdh": Algo("ECDH", "keyagree", "ecc", "vulnerable", 128, 0, None,
                 _SHOR + " Replace with ML-KEM (or a hybrid X25519+ML-KEM).", "ML-KEM-768"),
    "ecdsa": Algo("ECDSA", "signature", "ecc", "vulnerable", 128, 0, "1.2.840.10045.4.3.2",
                  _SHOR + " Replace with ML-DSA.", "ML-DSA-65"),
    "ecc": Algo("Elliptic-curve crypto", "pke", "ecc", "vulnerable", 128, 0, None,
                _SHOR + " Audit usage; migrate to ML-KEM / ML-DSA.", "ML-KEM-768 / ML-DSA-65"),
    "ed25519": Algo("Ed25519", "signature", "ecc", "vulnerable", 128, 0, None,
                    _SHOR + " Replace with ML-DSA, or use a hybrid signature.", "ML-DSA-65"),
    "x25519": Algo("X25519", "keyagree", "ecc", "vulnerable", 128, 0, None,
                   _SHOR + " Move to a hybrid X25519+ML-KEM-768 key agreement.", "ML-KEM-768"),
    "elgamal": Algo("ElGamal", "pke", "elgamal", "vulnerable", 112, 0, None,
                    _SHOR + " Replace with ML-KEM.", "ML-KEM-768"),

    # ---- Symmetric: weakened by Grover --------------------------------------
    "aes-128": Algo("AES-128", "blockcipher", "aes", "review", 128, 0, None,
                    _GROVER + " ~64-bit post-Grover; prefer AES-256.", "AES-256"),
    "aes-192": Algo("AES-192", "blockcipher", "aes", "safe", 192, 0, None,
                    "Adequate post-quantum margin."),
    "aes-256": Algo("AES-256", "blockcipher", "aes", "safe", 256, 0, None,
                    "Recommended symmetric baseline for the quantum era."),
    "aes": Algo("AES (unspecified key size)", "blockcipher", "aes", "review", None, 0, None,
                "Key size not detected; confirm AES-256 is used.", "AES-256"),
    "chacha20": Algo("ChaCha20", "streamcipher", "chacha", "safe", 256, 0, None,
                     "256-bit; adequate post-quantum margin."),
    "3des": Algo("Triple DES", "blockcipher", "des", "broken_classical", 112, 0, None,
                 "Deprecated by NIST independent of quantum risk. Replace with AES-256.", "AES-256"),
    "des": Algo("DES", "blockcipher", "des", "broken_classical", 56, 0, None,
                "Broken; remove immediately. Replace with AES-256.", "AES-256"),
    "rc4": Algo("RC4", "streamcipher", "rc4", "broken_classical", None, 0, None,
                "Broken stream cipher; remove. Replace with AES-256-GCM or ChaCha20.", "AES-256-GCM"),
    "blowfish": Algo("Blowfish", "blockcipher", "blowfish", "review", None, 0, None,
                     "Legacy 64-bit block cipher; migrate to AES-256.", "AES-256"),

    # ---- Hashes -------------------------------------------------------------
    "md5": Algo("MD5", "hash", "md5", "broken_classical", None, 0, "1.2.840.113549.2.5",
                "Collision-broken; never use for security. Replace with SHA-256+.", "SHA-256"),
    "sha1": Algo("SHA-1", "hash", "sha1", "broken_classical", None, 0, "1.3.14.3.2.26",
                 "Collision-broken; remove from signatures/certs. Replace with SHA-256+.", "SHA-256"),
    "sha256": Algo("SHA-256", "hash", "sha2", "safe", None, 0, None,
                   "Adequate; Grover leaves ~128-bit collision resistance."),
    "sha384": Algo("SHA-384", "hash", "sha2", "safe", None, 0, None, "Adequate post-quantum margin."),
    "sha512": Algo("SHA-512", "hash", "sha2", "safe", None, 0, None, "Adequate post-quantum margin."),
    "sha3": Algo("SHA-3", "hash", "sha3", "safe", None, 0, None, "Adequate post-quantum margin."),

    # ---- Password hashing / KDF (informational) -----------------------------
    "pbkdf2": Algo("PBKDF2", "kdf", "kdf", "informational", None, 0, None,
                   "Password KDF; not a quantum decision point. Ensure adequate iterations."),
    "bcrypt": Algo("bcrypt", "kdf", "kdf", "informational", None, 0, None,
                   "Password hashing; not quantum-relevant."),
    "scrypt": Algo("scrypt", "kdf", "kdf", "informational", None, 0, None,
                   "Password hashing; not quantum-relevant."),
    "argon2": Algo("Argon2", "kdf", "kdf", "informational", None, 0, None,
                   "Modern password hashing; not quantum-relevant."),

    # ---- Post-quantum (the migration targets) -------------------------------
    "ml-kem": Algo("ML-KEM (Kyber)", "kem", "ml-kem", "safe", None, 3, None,
                   "NIST FIPS 203 KEM. This is a migration target."),
    "ml-kem-512": Algo("ML-KEM-512", "kem", "ml-kem", "safe", None, 1, None, "NIST FIPS 203, category 1."),
    "ml-kem-768": Algo("ML-KEM-768", "kem", "ml-kem", "safe", None, 3, None, "NIST FIPS 203, category 3."),
    "ml-kem-1024": Algo("ML-KEM-1024", "kem", "ml-kem", "safe", None, 5, None, "NIST FIPS 203, category 5."),
    "ml-dsa": Algo("ML-DSA (Dilithium)", "signature", "ml-dsa", "safe", None, 3, None,
                   "NIST FIPS 204 signature. This is a migration target."),
    "slh-dsa": Algo("SLH-DSA (SPHINCS+)", "signature", "slh-dsa", "safe", None, 3, None,
                    "NIST FIPS 205 hash-based signature."),
    "falcon": Algo("Falcon", "signature", "falcon", "safe", None, 5, None,
                   "NIST-selected lattice signature (FN-DSA, draft)."),
    "hqc": Algo("HQC", "kem", "hqc", "safe", None, 3, None,
                "NIST code-based KEM backup to ML-KEM (selected 2025)."),
}


def lookup(key: str) -> Optional[Algo]:
    return ALGORITHMS.get(key)
