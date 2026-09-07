#!/usr/bin/env python3
"""Build orchestrator for deck-builder skill."""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any


class DeckBuilder:
    def __init__(self, mode: str, project_dir: Path):
        self.mode = mode
        self.project_dir = project_dir
        self.mode_dir = Path(__file__).parent.parent / "modes" / mode

    def run(self, **kwargs) -> Dict[str, Any]:
        """Run the build for the specified mode."""
        if self.mode == "markdown":
            return self._build_markdown(**kwargs)
        elif self.mode == "native":
            return self._build_native(**kwargs)
        elif self.mode == "illustrated":
            return self._build_illustrated(**kwargs)
        elif self.mode == "reconstruct":
            return self._build_reconstruct(**kwargs)
        elif self.mode == "studio":
            return self._build_studio(**kwargs)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def _build_markdown(self, content: str, style: str, **kwargs) -> Dict[str, Any]:
        """Build markdown-mode deck."""
        return {
            "mode": "markdown",
            "style": style,
            "content_file": "content.md",
            "outputs": ["deck.pptx", "deck.pdf", "deck.html", "slides/"],
            "status": "planned"
        }

    def _build_native(self, references: list, content: str, **kwargs) -> Dict[str, Any]:
        """Build native PPTX deck."""
        return {
            "mode": "native",
            "references": references,
            "dna_output": "dna-sheet.json",
            "plan_output": "plan.json",
            "draft_output": "draft.pptx",
            "final_output": "final.pptx",
            "qa_report": "qa-report.json",
            "status": "planned"
        }

    def _build_illustrated(self, style: str, content: str, **kwargs) -> Dict[str, Any]:
        """Build illustrated deck."""
        return {
            "mode": "illustrated",
            "style": style,
            "content_file": "content.md",
            "outputs": ["deck.html", "deck.pptx"],
            "status": "planned"
        }

    def _build_reconstruct(self, input_files: list, pipeline: str, **kwargs) -> Dict[str, Any]:
        """Build reconstructed deck."""
        return {
            "mode": "reconstruct",
            "pipeline": pipeline,
            "inputs": input_files,
            "outputs": ["reconstructed.pptx", "fidelity-report.json"],
            "status": "planned"
        }

    def _build_studio(self, project: str, **kwargs) -> Dict[str, Any]:
        """Build studio project."""
        return {
            "mode": "studio",
            "project": project,
            "outputs": ["deck.pptx", "deck.pdf", "deck.html", "slides/"],
            "deploy": "vercel/presenton",
            "status": "planned"
        }


def main():
    parser = argparse.ArgumentParser(description="Deck Builder")
    parser.add_argument("--mode", required=True, choices=["markdown", "native", "illustrated", "reconstruct", "studio"])
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--content", help="Content file or text")
    parser.add_argument("--style", help="Style name")
    parser.add_argument("--references", nargs="+", help="Reference PPTX files")
    parser.add_argument("--pipeline", help="Reconstruction pipeline")
    parser.add_argument("--inputs", nargs="+", help="Input files for reconstruction")
    parser.add_argument("--project", help="Studio project name")
    parser.add_argument("--input-file", help="JSON input file with all parameters")
    args = parser.parse_args()

    # If input file provided, load from there
    if args.input_file:
        with open(args.input_file) as f:
            input_data = json.load(f)
        project_dir = Path(args.project_dir).resolve()
        builder = DeckBuilder(input_data.get("mode", args.mode), project_dir)
        result = builder.run(**input_data)
    else:
        project_dir = Path(args.project_dir).resolve()
        builder = DeckBuilder(args.mode, project_dir)
        result = builder.run(
            content=args.content,
            style=args.style,
            references=args.references,
            pipeline=args.pipeline,
            inputs=args.inputs,
            project=args.project,
        )

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())