#!/usr/bin/env python3
"""Validate a coordinated GoreeCloud platform release manifest fail closed.

A release manifest selects component revisions and references evidence. It never manufactures
component-domain truth: producer conformance must already exist and remain revision-bound.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "goreecloud.platform-release.schema.json"
RULES_PATH = ROOT / "contracts" / "goreecloud.release-rules.v1.json"


class ReleaseValidationError(ValueError):
    pass


def load_data(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReleaseValidationError(f"could not read {path}: {exc}") from exc

    try:
        if path.suffix.lower() == ".json":
            value = json.loads(text)
        else:
            value = yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ReleaseValidationError(f"could not parse {path}: {exc}") from exc

    if not isinstance(value, dict):
        raise ReleaseValidationError(f"{path} must contain one mapping/object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReleaseValidationError(message)


def schema_validate(manifest: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda item: list(item.absolute_path))
    if not errors:
        return

    formatted: list[str] = []
    for error in errors[:20]:
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        formatted.append(f"{location}: {error.message}")
    suffix = "" if len(errors) <= 20 else f" (+{len(errors) - 20} more)"
    raise ReleaseValidationError("schema validation failed: " + "; ".join(formatted) + suffix)


def semantic_validate(manifest: dict[str, Any], rules: dict[str, Any]) -> dict[str, Any]:
    release = manifest["release"]
    components = manifest["components"]
    compatibility = manifest["compatibility"]
    gates = manifest["release_gates"]
    evidence = manifest["evidence"]
    certification = manifest["certification"]

    require(
        manifest["platform_contract"]["schema_version"] == rules["platform_contract_schema_version"],
        "release manifest platform-contract schema version does not match release rules",
    )
    require(
        manifest["platform_contract"]["rules_version"] == rules["rules_version"],
        "release manifest platform-contract rules version does not match release rules",
    )

    component_ids = [item["id"] for item in components]
    require(len(component_ids) == len(set(component_ids)), "component identifiers must be unique")
    component_map = {item["id"]: item for item in components}

    platform_systems = [
        item["platform_system"]
        for item in components
        if item["platform_system"] is not None
    ]
    require(len(platform_systems) == len(set(platform_systems)), "platform-system assignments must be unique")
    for component in components:
        if component["role"] == "platform_system":
            require(
                component["platform_system"] is not None,
                f"platform-system component {component['id']} must declare platform_system",
            )
        else:
            require(
                component["platform_system"] is None,
                f"non-platform-system component {component['id']} must not claim a platform_system slot",
            )
        if component["selection_status"] == "excluded":
            require(not component["required"], f"required component {component['id']} cannot be excluded")
        for dependency in component["dependencies"]:
            require(
                dependency in component_map,
                f"component {component['id']} declares dependency outside the release matrix: {dependency}",
            )
            require(dependency != component["id"], f"component {component['id']} cannot depend on itself")

    evidence_ids = [item["id"] for item in evidence]
    require(len(evidence_ids) == len(set(evidence_ids)), "evidence identifiers must be unique")
    evidence_map = {item["id"]: item for item in evidence}

    gate_ids = [item["id"] for item in gates]
    require(len(gate_ids) == len(set(gate_ids)), "release gate identifiers must be unique")
    gate_map = {item["id"]: item for item in gates}
    for required_gate in rules["mandatory_release_gates"]:
        require(required_gate in gate_map, f"missing mandatory release gate: {required_gate}")
        require(gate_map[required_gate]["mandatory"], f"mandatory release gate {required_gate} must declare mandatory=true")

    gates_allowing_na = set(rules["gates_allowing_not_applicable"])
    for gate in gates:
        for evidence_id in gate["evidence"]:
            require(evidence_id in evidence_map, f"gate {gate['id']} references unknown evidence {evidence_id}")
        if gate["status"] == "pass":
            require(gate["evidence"], f"passing gate {gate['id']} must cite evidence")
        if gate["status"] == "not_applicable":
            require(gate["id"] in gates_allowing_na, f"gate {gate['id']} may not be marked not_applicable")
            require(bool(gate.get("justification")), f"not-applicable gate {gate['id']} requires justification")

    relationship_keys: set[tuple[str, str, str]] = set()
    relationship_pairs: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for relationship in compatibility["relationships"]:
        key = (relationship["consumer"], relationship["provider"], relationship["requirement"])
        require(key not in relationship_keys, f"duplicate compatibility relationship: {key}")
        relationship_keys.add(key)
        require(relationship["consumer"] in component_map, f"relationship consumer is not in release components: {relationship['consumer']}")
        require(relationship["provider"] in component_map, f"relationship provider is not in release components: {relationship['provider']}")
        relationship_pairs.setdefault((relationship["consumer"], relationship["provider"]), []).append(relationship)
        for evidence_id in relationship["evidence"]:
            require(evidence_id in evidence_map, f"compatibility relationship references unknown evidence {evidence_id}")
        if relationship["status"] == "compatible":
            require(relationship["evidence"], "compatible relationships must cite evidence")
        if relationship["status"] == "not_applicable":
            require(bool(relationship.get("justification")), "not-applicable compatibility relationships require justification")

    for component in components:
        conformance = component["conformance"]
        evidence_ref = conformance["evidence_ref"]
        if evidence_ref is not None:
            require(evidence_ref in evidence_map, f"component {component['id']} references unknown conformance evidence {evidence_ref}")
            require(
                evidence_map[evidence_ref]["kind"] == "conformance_result",
                f"component {component['id']} conformance evidence must have kind conformance_result",
            )
        if conformance["source_revision"] is not None and component["source_revision"] is not None:
            require(
                conformance["source_revision"] == component["source_revision"],
                f"component {component['id']} conformance revision does not match selected source revision",
            )

    is_certified_state = release["state"] == "certified"
    declares_certified = certification["declared_result"] == "certified"
    require(
        is_certified_state == declares_certified,
        "release.state=certified and certification.declared_result=certified must be declared together",
    )

    if not is_certified_state:
        require(release["certified_at"] is None, "non-certified release must not declare certified_at")
        require(not certification["compatible"], "non-certified release must not declare platform compatibility as certified truth")
    else:
        require(release["certified_at"] is not None, "certified release requires certified_at")
        require(certification["compatible"], "certified release must declare compatible=true")
        require(not certification["blockers"], "certified release cannot retain blockers")
        require(compatibility["matrix_state"] == "verified", "certified release requires a verified compatibility matrix")

        required_platform_systems = set(rules["required_platform_systems"])
        selected_platform_systems = {
            item["platform_system"]
            for item in components
            if item["selection_status"] == "selected" and item["platform_system"] is not None
        }
        missing_systems = sorted(required_platform_systems - selected_platform_systems)
        require(not missing_systems, "certified release is missing selected Integral Platform Systems: " + ", ".join(missing_systems))

        for component in components:
            if not component["required"]:
                continue
            require(component["selection_status"] == "selected", f"required component {component['id']} is not selected")
            require(component["version"] is not None, f"selected required component {component['id']} has no version")
            require(component["source_revision"] is not None, f"selected required component {component['id']} has no exact source revision")
            require(component["lifecycle"] is not None, f"selected required component {component['id']} has no lifecycle")
            require(
                component["compatibility_input_status"] == "declared",
                f"selected required component {component['id']} does not have producer-declared compatibility inputs",
            )
            conformance = component["conformance"]
            require(conformance["result"] == "conformant", f"selected required component {component['id']} is not conformant")
            require(conformance["stable_eligible"], f"selected required component {component['id']} is not Stable eligible")
            require(conformance["evidence_ref"] is not None, f"selected required component {component['id']} lacks conformance evidence")
            require(
                conformance["source_revision"] == component["source_revision"],
                f"selected required component {component['id']} conformance evidence is not revision-bound",
            )

            for dependency in component["dependencies"]:
                provider = component_map[dependency]
                require(
                    provider["selection_status"] == "selected",
                    f"selected required component {component['id']} depends on unselected component {dependency}",
                )
                pair = relationship_pairs.get((component["id"], dependency), [])
                require(
                    pair,
                    f"selected dependency has no compatibility relationship: {component['id']} -> {dependency}",
                )
                require(
                    any(item["status"] == "compatible" and item["evidence"] for item in pair),
                    f"selected dependency is not evidence-backed compatible: {component['id']} -> {dependency}",
                )

        for gate_id in rules["mandatory_release_gates"]:
            gate = gate_map[gate_id]
            if gate["status"] == "not_applicable":
                require(gate_id in gates_allowing_na, f"mandatory gate {gate_id} cannot be not_applicable")
            else:
                require(gate["status"] == "pass", f"mandatory gate {gate_id} is not passing")
                require(gate["evidence"], f"mandatory passing gate {gate_id} lacks evidence")

        for relationship in compatibility["relationships"]:
            consumer = component_map[relationship["consumer"]]
            provider = component_map[relationship["provider"]]
            if consumer["selection_status"] != "selected" or provider["selection_status"] != "selected":
                continue
            if relationship["status"] == "not_applicable":
                continue
            require(relationship["status"] == "compatible", f"selected compatibility relationship is not verified compatible: {relationship['consumer']} -> {relationship['provider']}")
            require(relationship["evidence"], "verified compatibility relationship lacks evidence")

    unresolved_required = [
        component["id"]
        for component in components
        if component["required"] and component["selection_status"] != "selected"
    ]
    failed_gates = [gate["id"] for gate in gates if gate["mandatory"] and gate["status"] in {"fail", "pending"}]
    incompatible_relationships = [
        f"{item['consumer']}->{item['provider']}"
        for item in compatibility["relationships"]
        if item["status"] == "incompatible"
    ]

    return {
        "result_version": "1.0",
        "release_id": release["id"],
        "release_state": release["state"],
        "declared_result": certification["declared_result"],
        "certified": is_certified_state,
        "compatible": certification["compatible"],
        "component_count": len(components),
        "selected_component_count": sum(item["selection_status"] == "selected" for item in components),
        "unresolved_required_components": unresolved_required,
        "failed_or_pending_mandatory_gates": failed_gates,
        "incompatible_relationships": incompatible_relationships,
        "declared_blockers": certification["blockers"],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="YAML or JSON platform release manifest")
    parser.add_argument("--output", type=Path, help="optional JSON validation result path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        manifest = load_data(args.manifest)
        schema = load_data(SCHEMA_PATH)
        rules = load_data(RULES_PATH)
        schema_validate(manifest, schema)
        result = semantic_validate(manifest, rules)
    except ReleaseValidationError as exc:
        print(f"GoreeCloud platform release validation failed: {exc}", file=sys.stderr)
        return 1

    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(
        "GoreeCloud platform release manifest validated: "
        f"{result['release_id']} state={result['release_state']} certified={str(result['certified']).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
