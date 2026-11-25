"""Input-validation regression tests for the remote GitHub scanner."""

import unittest

from scripts.validate_repo_target import normalize_repository


class TestRemoteRepositoryValidation(unittest.TestCase):
    def test_owner_repo(self):
        self.assertEqual(
            normalize_repository("munnamihir/cryptoscan-pqc"),
            "munnamihir/cryptoscan-pqc",
        )

    def test_https_repository_url(self):
        self.assertEqual(
            normalize_repository("https://github.com/munnamihir/cryptoscan-pqc"),
            "munnamihir/cryptoscan-pqc",
        )

    def test_https_repository_git_clone_url(self):
        self.assertEqual(
            normalize_repository("https://github.com/octocat/Hello-World.git/"),
            "octocat/Hello-World",
        )

    def test_reject_unsafe_or_wrong_inputs(self):
        invalid = (
            "",
            " ",
            "owner/repo/extra",
            "https://github.com/owner/repo/tree/main",
            "https://github.com.evil.test/owner/repo",
            "http://github.com/owner/repo",
            "https://github.com/owner/repo?foo=bar",
            "https://github.com/owner/repo#readme",
            "owner/../evil",
            "owner/.",
            "owner/repo$(touch file)",
            "owner/repo\\nextra",
            "https://attacker@github.com/owner/repo",
            "https://github.com:8443/owner/repo",
        )
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_repository(value)


if __name__ == "__main__":
    unittest.main()
