#!/usr/bin/env python3
"""QA Render: Convert PPTX to PDF to PNG for visual validation."""

import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any
from PIL import Image
import shutil


class QARenderer:
    def __init__(self, pptx_path: Path, output_dir: Path):
        self.pptx_path = pptx_path
        self.output_dir = output_dir
        self.pdf_path = output_dir / f"{pptx_path.stem}.pdf"
        self.images_dir = output_dir / "slides"
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def pptx_to_pdf(self) -> bool:
        """Convert PPTX to PDF using LibreOffice."""
        try:
            result = subprocess.run([
                "soffice", "--headless", "--convert-to", "pdf",
                "--outdir", str(self.output_dir),
                str(self.pptx_path)
            ], capture_output=True, text=True, timeout=120)
            return result.returncode == 0 and self.pdf_path.exists()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def pdf_to_png(self) -> List[Path]:
        """Convert PDF to PNG images using Poppler."""
        images = []
        try:
            result = subprocess.run([
                "pdftoppm", "-png", "-r", "144",
                str(self.pdf_path),
                str(self.images_dir / "slide")
            ], capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                images = sorted(self.images_dir.glob("slide-*.png"))
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return images

    def analyze_slide(self, image_path: Path) -> Dict[str, Any]:
        """Basic visual analysis of a slide image."""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                gray = img.convert("L")
                return {
                    "slide": image_path.name,
                    "dimensions": f"{width}x{height}",
                    "mode": img.mode,
                    "has_content": width > 100 and height > 100,
                }
        except Exception as e:
            return {"slide": image_path.name, "error": str(e)}

    def run(self) -> Dict[str, Any]:
        """Run full QA render pipeline."""
        report = {
            "pptx": str(self.pptx_path),
            "pdf_generated": False,
            "slides_rendered": 0,
            "slides": [],
            "issues": [],
        }

        if self.pptx_to_pdf():
            report["pdf_generated"] = True
        else:
            report["issues"].append("PDF generation failed (LibreOffice not available or error)")
            return report

        images = self.pdf_to_png()
        report["slides_rendered"] = len(images)

        for img_path in images:
            analysis = self.analyze_slide(img_path)
            report["slides"].append(analysis)

        return report


def main():
    if len(sys.argv) < 2:
        print("Usage: qa_render.py <pptx_file> [output_dir]")
        return 1

    pptx_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else pptx_path.parent / "qa"

    if not pptx_path.exists():
        print(f"PPTX not found: {pptx_path}")
        return 1

    renderer = QARenderer(pptx_path, output_dir)
    report = renderer.run()

    report_path = output_dir / "qa-report.json"
    with open(report_path, "w") as f:
        json.dump(report, indent=2)

    print(f"QA Report: {report_path}")
    print(f"Slides rendered: {report['slides_rendered']}")
    if report["issues"]:
        print(f"Issues: {report['issues']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())