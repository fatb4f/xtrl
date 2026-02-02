#!/usr/bin/env python3
"""Generate derived binding views from PlantSpec + Ruleset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def derive_dag(ruleset: dict) -> dict:
    nodes = []
    edges = []
    start_id = "start"
    nodes.append({"id": start_id, "type": "start"})

    prev_id = start_id
    for idx, rule in enumerate(ruleset.get("order", [])):
        rid = f"rule-{idx:02d}"
        nodes.append({"id": rid, "type": "rule", "rule": rule})
        edges.append({"from": prev_id, "to": rid, "label": "next"})
        prev_id = rid
        if rule.get("decision") in {"DENY", "STOP"}:
            term_id = f"terminal-{idx:02d}"
            nodes.append(
                {
                    "id": term_id,
                    "type": "terminal",
                    "decision": rule.get("decision"),
                    "reason_code": rule.get("reason_code"),
                }
            )
            edges.append({"from": rid, "to": term_id, "label": rule.get("decision")})

    nodes.append({"id": "pass", "type": "pass"})
    edges.append({"from": prev_id, "to": "pass", "label": "ok"})
    return {"graph_version": "xtrl.binding.dag/v1", "nodes": nodes, "edges": edges}


def derive_mermaid(dag: dict) -> str:
    lines = ["flowchart TD", "  START([START])"]
    node_ids = {n["id"]: n for n in dag.get("nodes", [])}

    def label_for(node_id: str) -> str:
        node = node_ids.get(node_id, {})
        if node.get("type") == "rule":
            return node.get("rule", {}).get("id", node_id)
        if node.get("type") == "terminal":
            return f"{node.get('decision')}: {node.get('reason_code')}"
        if node.get("type") == "pass":
            return "PASS"
        return node_id

    # map start
    for edge in dag.get("edges", []):
        if edge["from"] == "start":
            lines.append(f"  START --> {edge['to']}")

    for edge in dag.get("edges", []):
        if edge["from"] == "start":
            continue
        src = edge["from"]
        dst = edge["to"]
        label = edge.get("label")
        src_label = label_for(src)
        dst_label = label_for(dst)
        src_id = src.replace("-", "_")
        dst_id = dst.replace("-", "_")
        lines.append(f"  {src_id}[{src_label}] -->|{label}| {dst_id}[{dst_label}]")

    return "\n".join(lines) + "\n"


def derive_plan_cards(plant_spec: dict) -> dict:
    cards = {}
    phases = plant_spec.get("phases", [])
    for phase in phases:
        cards[phase] = f"# PlanCard — {phase}\n\nTODO: describe 5W+H for {phase}.\n"
    return cards


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default="control/spec/binding/plant_spec.json")
    parser.add_argument("--ruleset", default="control/spec/binding/ruleset.json")
    parser.add_argument("--out-plant", default="control/plant")
    parser.add_argument("--out-cards", default="control/plan_cards")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    ruleset_path = Path(args.ruleset)
    out_plant = Path(args.out_plant)
    out_cards = Path(args.out_cards)

    plant_spec = read_json(spec_path)
    ruleset = read_json(ruleset_path)

    dag = derive_dag(ruleset)
    write_json(out_plant / "binding_dag.json", dag)
    write_text(out_plant / "binding_dag.mmd", derive_mermaid(dag))

    cards = derive_plan_cards(plant_spec)
    for phase, content in cards.items():
        write_text(out_cards / f"binding.{phase}.md", content)


if __name__ == "__main__":
    main()
