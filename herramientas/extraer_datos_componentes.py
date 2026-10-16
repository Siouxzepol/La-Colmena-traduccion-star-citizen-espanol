#!/usr/bin/env python3
"""Export ship component metadata and resource rates from extracted DataCore JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")).get("_RecordValue_", {})
    except (OSError, json.JSONDecodeError):
        return {}


def table(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if "=" in line and not line.lstrip().startswith((";", "#")):
            key, value = line.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def find_rates(node, state="Online"):
    found = []
    if isinstance(node, dict):
        if node.get("_Type_") == "ItemResourceState":
            state = node.get("name", state)
        if node.get("_Type_") in ("ItemResourceDeltaConversion", "ItemResourceDeltaConsumption"):
            for direction in ("consumption", "generation"):
                amount = node.get(direction)
                if not isinstance(amount, dict):
                    continue
                unit = amount.get("resourceAmountPerSecond", {})
                number = next((v for k, v in unit.items() if k not in ("_Type_",) and isinstance(v, (int, float))), None)
                if number is not None:
                    found.append({"estado": state, "direccion": direction, "recurso": amount.get("resource"), "cantidad_por_segundo": number, "unidad": unit.get("_Type_")})
        for value in node.values():
            found.extend(find_rates(value, state))
    elif isinstance(node, list):
        for value in node:
            found.extend(find_rates(value, state))
    return found


def main() -> int:
    if len(sys.argv) != 5:
        print("Uso: python extraer_datos_componentes.py <DataCore-json> <english.ini> <spanish.ini> <output.json>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]) / "libs" / "foundry" / "records"
    en, es = table(Path(sys.argv[2])), table(Path(sys.argv[3]))
    output = Path(sys.argv[4])
    categories = ("cooler", "shieldgenerator", "powerplant", "quantumdrive", "radar", "jumpdrive", "thrusters", "weapons", "countermeasures", "fuelnozzle")
    entries = []
    for category in categories:
        folder = root / "entities" / "scitem" / "ships" / category
        if not folder.exists():
            continue
        for path in folder.rglob("*.json"):
            record = load(path)
            components = [c for c in record.get("Components", []) if isinstance(c, dict)]
            definitions = [c.get("AttachDef", {}) for c in components if c.get("_Type_") == "SAttachableComponentParams"]
            for item in definitions:
                if not item or item.get("Type") in (None, "UNDEFINED"):
                    continue
                loc = item.get("Localization", {})
                name_key = loc.get("Name")
                name_key = name_key.lstrip("@") if isinstance(name_key, str) else None
                mass = None
                for component in components:
                    phys = component.get("PhysType", {}) if component.get("_Type_") == "SEntityPhysicsControllerParams" else {}
                    if isinstance(phys, dict) and isinstance(phys.get("Mass"), (int, float)):
                        mass = phys["Mass"]
                        break
                entries.append({
                    "id": path.stem,
                    "tipo": item.get("Type"),
                    "subtipo": item.get("SubType"),
                    "tamano": item.get("Size"),
                    "grado": item.get("Grade"),
                    "nombre_loc_id": name_key,
                    "nombre_es": es.get(name_key) if name_key else None,
                    "nombre_ingles": en.get(name_key) if name_key else None,
                    "fabricante_id": item.get("Manufacturer"),
                    "masa": mass,
                    "flujos_recursos": find_rates(components),
                })
    entries.sort(key=lambda x: (x["tipo"] or "", x["tamano"] or 0, x["nombre_es"] or x["nombre_ingles"] or x["id"]))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "fuente": "DataCore extraído de la instalación local de Star Citizen",
        "nota": "Valores de recursos tal como están configurados en el juego; pueden cambiar con los parches. Se incluyen nombre localizado, tipo, tamaño, grado, masa y flujos declarados.",
        "total_componentes": len(entries),
        "componentes": entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(entries)} componentes escritos en {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
