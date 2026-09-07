#!/usr/bin/env python3
"""Schema validation for deck-builder skill."""

import sys
import json
import argparse
from pathlib import Path
from jsonschema import validate, ValidationError


def load_schema(schema_path: Path) -> dict:
    """Load JSON schema from file."""
    with open(schema_path) as f:
        return json.load(f)


def validate_deck(deck_path: Path, schema_path: Path) -> tuple[bool, list[str]]:
    """Validate deck.json against schema."""
    with open(deck_path) as f:
        deck = json.load(f)

    schema = load_schema(schema_path)

    try:
        validate(instance=deck, schema=schema)
        return True, []
    except ValidationError as e:
        return False, [str(e)]


def main():
    parser = argparse.ArgumentParser(description="Validate deck against schema")
    parser.add_argument("deck", help="Path to deck.json")
    parser.add_argument("--schema", default="schemas/deck.json", help="Path to schema")
    args = parser.parse_args()

    deck_path = Path(args.deck)
    schema_path = Path(args.schema)

    if not deck_path.exists():
        print(f"Deck not found: {deck_path}")
        return 1

    if not schema_path.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent
        schema_path = script_dir / args.schema

    if not schema_path.exists():
        print(f"Schema not found: {schema_path}")
        return 1

    valid, errors = validate_deck(deck_path, schema_path)

    if valid:
        print("SCHEMA VALIDATION PASSED")
        return 0
    else:
        print("SCHEMA VALIDATION FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1


if __name__ == "__main__":
    sys.exit(main())