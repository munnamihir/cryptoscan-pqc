"""
Detection rules. Each rule maps a regex (matched against source text) to a
normalized algorithm key in knowledge.ALGORITHMS.

These are high-signal patterns across the ecosystems a typical enterprise estate
contains: Python, JavaScript/TypeScript, Java, Go, C/C++/OpenSSL, .NET/C#, and
config/PEM material. The set is intentionally extensible — add a rule, not code.
"""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    algo: str          # key into knowledge.ALGORITHMS
    pattern: str       # regex
    lang: str          # label for evidence
    note: str = ""

    def compiled(self):
        return re.compile(self.pattern, re.IGNORECASE)


RULES = [
    # ---------------- Python ----------------
    Rule("rsa", r"\brsa\.generate_private_key|RSA\.generate|from\s+cryptography.*rsa", "python"),
    Rule("ecdsa", r"\bec\.(SECP|generate_private_key)|ECDSA\b", "python"),
    Rule("ed25519", r"ed25519\.|Ed25519PrivateKey", "python"),
    Rule("x25519", r"x25519\.|X25519PrivateKey", "python"),
    Rule("dh", r"\bdh\.generate_parameters|DHParameterNumbers", "python"),
    Rule("md5", r"hashlib\.md5|MD5\.new", "python"),
    Rule("sha1", r"hashlib\.sha1\b|SHA1\.new", "python"),
    Rule("sha256", r"hashlib\.sha256\b", "python"),
    Rule("3des", r"TripleDES|DES3\.new", "python"),
    Rule("rc4", r"\bARC4\b|Cipher\.ARC4", "python"),

    # ---------------- JS / TS ----------------
    Rule("rsa", r"generateKeyPair(?:Sync)?\(\s*['\"]rsa['\"]|['\"]RS(?:256|384|512)['\"]", "javascript"),
    Rule("ecdsa", r"['\"]ES(?:256|384|512)['\"]|createSign\(\s*['\"]SHA\d+['\"]\)|['\"]ec['\"]", "javascript"),
    Rule("ed25519", r"['\"]ed25519['\"]|EdDSA", "javascript"),
    Rule("aes-128", r"createCipheriv\(\s*['\"]aes-128", "javascript"),
    Rule("aes-256", r"createCipheriv\(\s*['\"]aes-256", "javascript"),
    Rule("md5", r"createHash\(\s*['\"]md5['\"]", "javascript"),
    Rule("sha1", r"createHash\(\s*['\"]sha1['\"]", "javascript"),
    Rule("bcrypt", r"\bbcrypt\b", "javascript"),

    # ---------------- Java ----------------
    Rule("rsa", r'getInstance\(\s*"RSA|"SHA\d+withRSA"', "java"),
    Rule("ecdsa", r'"SHA\d+withECDSA"|getInstance\(\s*"EC"', "java"),
    Rule("dsa", r'"SHA\d+withDSA"|getInstance\(\s*"DSA"', "java"),
    Rule("aes", r'Cipher\.getInstance\(\s*"AES', "java"),
    Rule("3des", r'"DESede"|"TripleDES"', "java"),
    Rule("md5", r'MessageDigest\.getInstance\(\s*"MD5"', "java"),
    Rule("sha1", r'MessageDigest\.getInstance\(\s*"SHA-?1"', "java"),

    # ---------------- Go ----------------
    Rule("rsa", r'crypto/rsa|rsa\.GenerateKey', "go"),
    Rule("ecdsa", r'crypto/ecdsa|ecdsa\.GenerateKey', "go"),
    Rule("ed25519", r'crypto/ed25519', "go"),
    Rule("md5", r'crypto/md5', "go"),
    Rule("sha1", r'crypto/sha1', "go"),
    Rule("3des", r'crypto/des', "go"),

    # ---------------- C / C++ / OpenSSL ----------------
    Rule("rsa", r'RSA_generate_key|EVP_PKEY_RSA|PEM_read.*RSA', "c"),
    Rule("ecdsa", r'EC_KEY_new|ECDSA_|EVP_PKEY_EC', "c"),
    Rule("md5", r'\bMD5_Init\b|EVP_md5', "c"),
    Rule("sha1", r'\bSHA1_Init\b|EVP_sha1', "c"),
    Rule("3des", r'DES_ede3|EVP_des_ede3', "c"),

    # ---------------- .NET / C# ----------------
    Rule("rsa", r'RSACryptoServiceProvider|RSA\.Create|new\s+RSA', "csharp"),
    Rule("ecdsa", r'ECDsa(?:Cng|\.Create)|new\s+ECDsa', "csharp"),
    Rule("aes", r'Aes\.Create|RijndaelManaged|new\s+AesManaged', "csharp"),
    Rule("3des", r'TripleDESCryptoServiceProvider|TripleDES\.Create', "csharp"),
    Rule("md5", r'MD5\.Create|MD5CryptoServiceProvider|new\s+MD5', "csharp"),
    Rule("sha1", r'SHA1\.Create|SHA1Managed|SHA1CryptoServiceProvider', "csharp"),

    # ---------------- TLS / config / certs ----------------
    Rule("sha1", r'sha1WithRSAEncryption|Signature Algorithm:\s*sha1', "x509"),
    Rule("rsa", r'BEGIN RSA PRIVATE KEY|rsaEncryption', "pem"),
    Rule("ecdsa", r'BEGIN EC PRIVATE KEY|id-ecPublicKey', "pem"),
    Rule("3des", r'ssl_ciphers.*3DES|:DES-CBC3-', "config"),
    Rule("rc4", r'ssl_ciphers.*RC4|:RC4-', "config"),

    # ---------------- Post-quantum (good findings) ----------------
    Rule("ml-kem-768", r'\bML-?KEM-?768\b|Kyber768', "pqc"),
    Rule("ml-kem-1024", r'\bML-?KEM-?1024\b|Kyber1024', "pqc"),
    Rule("ml-kem-512", r'\bML-?KEM-?512\b|Kyber512', "pqc"),
    Rule("ml-kem", r'\bML-?KEM\b|\bKyber\b', "pqc"),
    Rule("ml-dsa", r'\bML-?DSA\b|Dilithium', "pqc"),
    Rule("slh-dsa", r'\bSLH-?DSA\b|SPHINCS', "pqc"),
    Rule("falcon", r'\bFalcon(?:512|1024)?\b|FN-?DSA', "pqc"),
    Rule("hqc", r'\bHQC\b', "pqc"),
]

COMPILED = [(r, r.compiled()) for r in RULES]

# Directories and extensions we never read
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist",
             "build", ".next", "target", "bin", "obj", ".idea", ".vscode"}
TEXT_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".c", ".h",
             ".cpp", ".cc", ".cs", ".rb", ".php", ".rs", ".pem", ".crt", ".cer",
             ".conf", ".cfg", ".ini", ".yaml", ".yml", ".json", ".txt", ".md"}
