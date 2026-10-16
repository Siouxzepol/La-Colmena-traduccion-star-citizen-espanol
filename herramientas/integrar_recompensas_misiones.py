#!/usr/bin/env python3
"""Add safe, static reputation/blueprint notes to localized mission descriptions.

The game localization file cannot inspect the active contract at runtime. This
tool only annotates descriptions when a title key maps unambiguously to one
reward signature in the extracted DataCore catalog and a matching description
key exists in global.ini.

Usage:
  python herramientas/integrar_recompensas_misiones.py [catalog.json] [global.ini]
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


MARKER = r"\n\nRECOMPENSAS DEL CONTRATO"


def reward_signature(contract: dict) -> tuple:
    reputation = tuple(sorted(
        (r.get("faccion_loc_id"), r.get("cantidad"), r.get("ambito_loc_id"))
        for r in contract.get("reputacion", [])
    ))
    blueprints = tuple(sorted(
        (p.get("pool"), p.get("probabilidad"))
        for p in contract.get("planos", [])
    ))
    return reputation, blueprints


def candidate_description_keys(title_key: str) -> list[str]:
    candidates = []
    for replacement in ("_Desc", "_desc"):
        candidate = re.sub(r"(?i)_title(?=_|$)", replacement, title_key)
        if candidate != title_key and candidate not in candidates:
            candidates.append(candidate)
    return candidates


def reward_text(contract: dict, strings: dict[str, str]) -> str:
    lines = []
    reputation = contract.get("reputacion", [])
    if reputation:
        parts = []
        for reward in reputation:
            faction = reward.get("faccion") or reward.get("faccion_ingles") or "facción"
            amount = reward.get("cantidad")
            if amount is not None:
                parts.append(f"+{amount} con {faction}")
        if parts:
            lines.append("Reputación: " + "; ".join(parts) + ".")

    pool_lines = []
    for pool in contract.get("planos", []):
        names = []
        for option in pool.get("opciones", []):
            item_id = option.get("objeto_id")
            if not item_id:
                continue
            name_key = f"item_Name{item_id}"
            name = strings.get(name_key) or strings.get(f"item_Name_{item_id}") or readable_item_name(item_id)
            if name not in names:
                names.append(name)
        if names:
            chance = pool.get("probabilidad")
            chance_text = f" ({chance * 100:g} % de probabilidad)" if isinstance(chance, (int, float)) and chance < 1 else ""
            pool_lines.append(" / ".join(names) + chance_text)
    if pool_lines:
        lines.append("Planos posibles (selección aleatoria): " + "; ".join(pool_lines) + ".")
    return r"\n".join(lines)


def readable_item_name(item_id: str) -> str:
    """Translate obvious item-type words while retaining manufacturer/model IDs."""
    manufacturers = {
        "amrs": "AMRS", "apar": "APAR", "asad": "ASAD", "banu": "Banu",
        "behr": "Behring", "grin": "Greycat", "gmni": "Gemini", "thcn": "Tachyon",
    }
    types = {
        "lasercannon": "cañón láser", "ballisticgatling": "ametralladora balística",
        "ballisticscattergun": "escopeta balística", "massdriver": "acelerador de masa",
        "distortionrepeater": "repetidor de distorsión", "tachyoncannon": "cañón de taquiones",
        "ballisticcannon": "cañón balístico", "ballisticrepeater": "repetidor balístico",
        "energycannon": "cañón de energía", "mining_laser": "láser minero",
        "fuel_nozzle": "boquilla de combustible", "utility": "herramienta",
    }
    parts = item_id.lower().split("_")
    manufacturer = manufacturers.get(parts[0], parts[0].upper())
    compact = "_".join(parts[1:])
    description = next((label for key, label in types.items() if key in compact), None)
    if description:
        size = re.search(r"(?:^|_)s(\d+)(?:_|$)", compact)
        return f"{description.capitalize()} {manufacturer}" + (f" S{size.group(1)}" if size else "")
    component_types = {
        "cool": "Enfriador", "powr": "Planta de energía", "shld": "Generador de escudo",
        "radr": "Radar", "qdrv": "Motor cuántico", "fuel": "Componente de combustible",
        "mining": "Equipo de minería", "salvage": "Equipo de salvamento", "cargo": "Contenedor",
    }
    if parts[0] in component_types:
        brand = parts[1].upper() if len(parts) > 1 else ""
        model_parts = [part for part in parts[2:] if part != "scitem"]
        tokens = {
            "armor": "armadura", "heavy": "pesada", "medium": "mediana", "light": "ligera",
            "arms": "brazales", "legs": "perneras", "core": "torso", "helmet": "casco",
            "backpack": "mochila", "suit": "traje", "mag": "cargador", "pod": "cápsula",
            "shipmining": "minera", "nozzle": "boquilla", "tank": "depósito",
        }
        model = []
        size = None
        for part in model_parts:
            if re.fullmatch(r"s\d+", part):
                size = part.upper()
            else:
                model.append(tokens.get(part, part.capitalize()))
        label = " ".join([component_types[parts[0]], brand, *model]).strip()
        return label + (f" {size}" if size else "")
    generic = {
        "heavy": "pesado", "medium": "mediano", "light": "ligero", "core": "torso",
        "arms": "brazales", "legs": "perneras", "helmet": "casco", "backpack": "mochila",
        "flight": "vuelo", "suit": "traje", "armor": "armadura", "armour": "armadura",
    }
    words = [generic.get(part, part) for part in parts[1:]]
    return manufacturer + (" " + " ".join(words) if words else "")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    catalog_path = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "datos" / "misiones_reputacion_planos.json"
    ini_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "global.ini"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    contracts = catalog["contratos"]

    groups: dict[str, list[dict]] = defaultdict(list)
    for contract in contracts:
        title = contract.get("titulo_loc_id")
        if title and title != "@LOC_UNINITIALIZED":
            groups[title.lstrip("@").strip()].append(contract)

    original_bytes = ini_path.read_bytes()
    has_bom = original_bytes.startswith(b"\xef\xbb\xbf")
    original = original_bytes.decode("utf-8-sig")
    newline = "\r\n" if "\r\n" in original else "\n"
    lines = original.splitlines(keepends=True)
    values: dict[str, str] = {}
    key_pattern = re.compile(r"^([^=,]+)(,P)?=(.*)$")
    for line in lines:
        match = key_pattern.match(line.rstrip("\r\n"))
        if match:
            values[match.group(1).strip()] = match.group(3)

    updates: dict[str, str] = {}
    skipped_ambiguous = 0
    for title_key, variants in groups.items():
        signatures = {reward_signature(c) for c in variants}
        if len(signatures) != 1:
            skipped_ambiguous += 1
            continue
        for description_key in candidate_description_keys(title_key):
            if description_key in values:
                updates[description_key] = reward_text(variants[0], values)
                break

    written = 0
    result = []
    for line in lines:
        ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
        body = line[:-len(ending)] if ending else line
        match = key_pattern.match(body)
        if match and match.group(1).strip() in updates:
            key, suffix, value = match.group(1), match.group(2) or "", match.group(3)
            value = value.split(MARKER, 1)[0].rstrip()
            result.append(key + suffix + "=" + value + MARKER + r"\n" + updates[match.group(1).strip()] + ending)
            written += 1
        else:
            result.append(line)

    output_bytes = "".join(result).encode("utf-8")
    # global.ini in this repository is distributed as UTF-8 with a BOM.
    ini_path.write_bytes((b"\xef\xbb\xbf" if has_bom or ini_path.name.lower() == "global.ini" else b"") + output_bytes)
    print(f"Descripciones actualizadas: {written}")
    print(f"Claves de misión ambiguas omitidas: {skipped_ambiguous}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
