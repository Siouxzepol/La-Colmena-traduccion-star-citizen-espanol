#!/usr/bin/env python3
"""Build a compact mission reward reference from Star Citizen DataCore JSON.

Usage:
  python extraer_datos_misiones.py <DataCore-json-root> <english.ini> <spanish.ini> <output.json>

The input JSON is produced by extracting the game's DataCore with StarBreaker.
Only derived identifiers, reward amounts and blueprint-pool contents are emitted.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def load_record(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")).get("_RecordValue_", {})
    except (OSError, json.JSONDecodeError):
        return {}


def loc_table(path: Path) -> dict[str, str]:
    values = {}
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if not line or line.lstrip().startswith((";", "#")) or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def resolve_ref(ref: str, records_root: Path) -> Path | None:
    if not ref.startswith("file://"):
        return None
    rel = unquote(ref[7:]).replace("\\", "/")
    marker = "/libs/foundry/records/"
    if marker in f"/{rel.lstrip('./')}":
        rel = f"/{rel.lstrip('./')}".split(marker, 1)[1]
        return records_root / rel
    # Resolve relative file references against the JSON's common records root.
    parts = [p for p in rel.split("/") if p not in (".", "")]
    if "records" in parts:
        return records_root.joinpath(*parts[parts.index("records") + 1 :])
    return None


def token_value(token: str | None, strings: dict[str, str]) -> str | None:
    if not token:
        return None
    return strings.get(token.lstrip("@"), token)


def record_token(ref: str | None, field: str, records_root: Path) -> str | None:
    path = resolve_ref(ref or "", records_root)
    if not path or not path.exists():
        return None
    return load_record(path).get(field)


def walk_contracts(node, generator_name="", generator_params=None, source_file=""):
    if isinstance(node, dict):
        if node.get("_Type_") in ("Contract", "CareerContract"):
            yield node, generator_name, generator_params, source_file
        is_generator = node.get("_Type_") == "ContractGeneratorHandler_List"
        next_generator = node.get("debugName", generator_name) if is_generator else generator_name
        next_params = node.get("contractParams", generator_params) if is_generator else generator_params
        for value in node.values():
            yield from walk_contracts(value, next_generator, next_params, source_file)
    elif isinstance(node, list):
        for value in node:
            yield from walk_contracts(value, generator_name, generator_params, source_file)


def strings_for(params: dict) -> dict[str, str]:
    return {x.get("param", ""): x.get("value", "") for x in params.get("stringParamOverrides", [])}


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    english = loc_table(Path(sys.argv[2]))
    spanish = loc_table(Path(sys.argv[3]))
    out = Path(sys.argv[4])
    records_root = root / "libs" / "foundry" / "records"
    contracts_root = records_root / "contracts" / "contractgenerator"
    missions = []
    seen = set()
    for source in contracts_root.rglob("*.json"):
        generator_record = load_record(source)
        for contract, generator, generator_params, source_file in walk_contracts(generator_record, source_file=source.name):
            overrides = strings_for(contract.get("paramOverrides", {}))
            title = overrides.get("Title") or overrides.get("title")
            results = contract.get("contractResults", {}).get("contractResults", [])
            reputation = []
            blueprints = []
            for result in results:
                mask = result.get("missionResults") or []
                if not (mask and mask[0]):
                    continue
                amounts = result.get("contractResultReputationAmounts") or result.get("reputationAmounts")
                if amounts:
                    reward_ref = amounts.get("reward")
                    amount = None
                    reward_path = resolve_ref(reward_ref or "", records_root)
                    if reward_path and reward_path.exists():
                        amount = load_record(reward_path).get("reputationAmount")
                    faction_token = record_token(amounts.get("factionReputation"), "displayName", records_root)
                    scope_token = record_token(amounts.get("reputationScope"), "displayName", records_root)
                    reputation.append({
                        "faccion": token_value(faction_token, spanish),
                        "faccion_ingles": token_value(faction_token, english),
                        "faccion_loc_id": faction_token,
                        "ambito_loc_id": scope_token,
                        "cantidad": amount,
                        "fuente": Path((reward_ref or "").split("/")[-1]).stem,
                    })
                pool_ref = result.get("blueprintPool")
                if pool_ref:
                    pool_path = resolve_ref(pool_ref, records_root)
                    choices = []
                    if pool_path and pool_path.exists():
                        pool = load_record(pool_path)
                        for choice in pool.get("blueprintRewards", []):
                            bp_ref = choice.get("blueprintRecord")
                            bp_path = resolve_ref(bp_ref or "", records_root)
                            bp = load_record(bp_path) if bp_path and bp_path.exists() else {}
                            craft = bp.get("blueprint", {})
                            item_ref = craft.get("processSpecificData", {}).get("entityClass") if isinstance(craft.get("processSpecificData"), dict) else None
                            choices.append({
                                "id": Path((bp_ref or "").split("/")[-1]).stem,
                                "nombre_loc_id": craft.get("blueprintName"),
                                "objeto_id": Path((item_ref or "").split("/")[-1]).stem if item_ref else None,
                                "peso": choice.get("weight"),
                            })
                    blueprints.append({
                        "pool": Path((pool_ref or "").split("/")[-1]).stem,
                        "probabilidad": result.get("chance"),
                        "opciones": choices,
                    })
            if not reputation and not blueprints:
                continue
            identity = (contract.get("id") or contract.get("debugName"), title, source.as_posix())
            if identity in seen:
                continue
            seen.add(identity)
            giver = overrides.get("Contractor") or strings_for(generator_params or {}).get("Contractor")
            missions.append({
                "contrato_id": contract.get("debugName"),
                "titulo_loc_id": title,
                "titulo_es": token_value(title, spanish) if title and title.startswith("@") else title,
                "titulo_ingles": token_value(title, english) if title and title.startswith("@") else title,
                "contratista_loc_id": giver,
                "contratista_es": token_value(giver, spanish) if giver and giver.startswith("@") else giver,
                "contratista_ingles": token_value(giver, english) if giver and giver.startswith("@") else giver,
                "generador_id": generator,
                "plantilla_id": Path((contract.get("template") or "").split("/")[-1]).stem,
                "reputacion": reputation,
                "planos": blueprints,
            })
    missions.sort(key=lambda m: (m["contratista_es"] or m["contratista_ingles"] or "", m["titulo_es"] or m["titulo_ingles"] or "", m["contrato_id"] or ""))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "fuente": "DataCore extraído de la instalación local de Star Citizen",
        "formato": "StarBreaker JSON",
        "nota": "Datos de diseño del juego. La presencia en un pool no significa que todos sus planos se entreguen en cada contrato; puede ser una selección aleatoria.",
        "total_contratos": len(missions),
        "contratos": missions,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(missions)} contratos escritos en {out}")
    print(f"Con reputación: {sum(bool(m['reputacion']) for m in missions)}; con grupos de planos: {sum(bool(m['planos']) for m in missions)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
