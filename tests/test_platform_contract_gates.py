#!/usr/bin/env python3
"""Regression tests for fail-closed Platform Contract 2.0 Anchor gates.

All acceptance paths and release IDs in this fixture are synthetic. These
tests validate metadata logic; they do not establish real release acceptance.
"""

from __future__ import annotations

import copy
from pathlib import Path
import tempfile
import unittest

import yaml

from scripts import evaluate_platform_conformance as evaluator
from scripts import validate_platform_manifest as validator


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "goreecloud.platform.example.yaml"
REVISION = "a" * 40
STALE_REVISION = "b" * 40
OBSERVED_AT = "2026-10-11T00:00:00Z"


def synthetic_anchor() -> dict:
    manifest = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    manifest["lifecycle"] = "anchor"
    metadata = manifest["lifecycle_metadata"]
    metadata["flags"] = []
    metadata["qualification_state"] = "passed"
    metadata["next_gate"] = "sunset"
    metadata["candidate_identity"] = {"source_revision": REVISION}
    metadata["evidence"] = ["tests/synthetic-qualification.md"]

    for entry in manifest["platform_systems"].values():
        entry["result"] = "not-applicable-justified"
        entry["evidence"] = ["tests/synthetic-system-evidence.md"]
        entry["notes"] = "Synthetic test justification; no real acceptance claimed."

    manifest["evidence"]["acceptance_tests"] = [
        {
            "id": "synthetic-" + category,
            "category": category,
            "path": "tests/synthetic-acceptance.md",
            "revision": REVISION,
            "result": "passed",
            "observed_at": OBSERVED_AT,
        }
        for category in sorted(validator.ANCHOR_ACCEPTANCE_CATEGORIES)
    ]
    manifest["evidence"]["release"] = [
        {
            "id": "synthetic-publication",
            "version": "0.0.0-test",
            "revision": REVISION,
            "path": "tests/synthetic-publication.md",
            "result": "published",
            "observed_at": OBSERVED_AT,
        }
    ]
    manifest["conformance"] = {
        "status": "conformant",
        "validated_at": OBSERVED_AT,
        "evidence": ["tests/synthetic-conformance.md"],
        "blockers": [],
    }
    return manifest


def validate_payload(payload: dict) -> dict:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.yaml"
        path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
        return validator.validate_manifest(path)


def evaluate_payload(payload: dict) -> dict:
    return evaluator.evaluate(
        payload,
        revision=REVISION,
        evaluator_revision=REVISION,
        evaluated_at=OBSERVED_AT,
    )


class AnchorEligibilityTests(unittest.TestCase):
    def test_exact_candidate_without_holds_is_metadata_eligible(self) -> None:
        manifest = synthetic_anchor()
        self.assertEqual(validate_payload(manifest), manifest)
        result = evaluate_payload(manifest)
        self.assertTrue(result["anchor_eligible"])
        self.assertEqual(result["computed_conformance"], "conformant")
        self.assertFalse(result["blockers"])

    def test_every_active_flag_blocks_anchor(self) -> None:
        for flag in (
            "blocked",
            "security-hold",
            "privacy-hold",
            "recovery-hold",
            "migration-required",
            "superseded",
        ):
            with self.subTest(flag=flag):
                manifest = synthetic_anchor()
                manifest["lifecycle_metadata"]["flags"] = [flag]
                with self.assertRaises(validator.ValidationError):
                    validate_payload(manifest)
                result = evaluate_payload(manifest)
                self.assertFalse(result["anchor_eligible"])
                self.assertIn("Active lifecycle flags: " + flag, result["blockers"])

    def test_missing_candidate_fails_closed(self) -> None:
        manifest = synthetic_anchor()
        manifest["lifecycle_metadata"]["candidate_identity"] = None
        with self.assertRaises(validator.ValidationError):
            validate_payload(manifest)
        result = evaluate_payload(manifest)
        self.assertFalse(result["anchor_eligible"])
        self.assertIn(
            "Candidate source revision does not match the evaluated revision",
            result["blockers"],
        )

    def test_candidate_and_release_cannot_refer_to_another_head(self) -> None:
        manifest = synthetic_anchor()
        manifest["lifecycle_metadata"]["candidate_identity"]["source_revision"] = STALE_REVISION
        manifest["evidence"]["release"][0]["revision"] = STALE_REVISION
        validate_payload(manifest)  # Internal consistency is not exact-head provenance.
        result = evaluate_payload(manifest)
        self.assertFalse(result["anchor_eligible"])
        self.assertIn(
            "Candidate source revision does not match the evaluated revision",
            result["blockers"],
        )
        self.assertIn(
            "Published release evidence for the evaluated revision is missing",
            result["blockers"],
        )

    def test_published_evidence_for_wrong_revision_fails_closed(self) -> None:
        manifest = synthetic_anchor()
        manifest["evidence"]["release"][0]["revision"] = STALE_REVISION
        with self.assertRaises(validator.ValidationError):
            validate_payload(manifest)
        result = evaluate_payload(manifest)
        self.assertFalse(result["anchor_eligible"])
        self.assertIn(
            "Published release evidence for the evaluated revision is missing",
            result["blockers"],
        )

    def test_candidate_release_is_not_published_release(self) -> None:
        manifest = synthetic_anchor()
        manifest["evidence"]["release"][0]["result"] = "candidate"
        with self.assertRaises(validator.ValidationError):
            validate_payload(manifest)
        self.assertFalse(evaluate_payload(manifest)["anchor_eligible"])


if __name__ == "__main__":
    unittest.main()
