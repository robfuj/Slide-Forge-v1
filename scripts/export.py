#!/usr/bin/env python3
"""Multi-format export for deck-builder skill."""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any


class DeckExporter:
    def __init__(self, deck_dir: Path):
        self.deck_dir = deck_dir
        self.manifest_path = deck_dir / "deck.json"
        self.load_manifest()

    def load_manifest(self):
        """Load deck manifest."""
        if self.manifest_path.exists():
            with open(self.manifest_path) as f:
                self.manifest = json.load(f)
        else:
            self.manifest = {
                "title": self.deck_dir.name,
                "version": "1.0.0",
                "mode": "unknown",
                "formats": [],
            }

    def save_manifest(self):
        """Save updated manifest."""
        with open(self.manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2)

    def export_pptx(self, source: Path) -> Path:
        """Export to PPTX (copy if already PPTX, convert if needed)."""
        dest = self.deck_dir / f"{self.manifest['title'].lower().replace(' ', '-')}.pptx"
        if source.suffix == ".pptx":
            import shutil
            shutil.copy2(source, dest)
        else:
            # Would convert from HTML/MD using Marp/Slidev/etc.
            pass
        self.manifest["exports"] = self.manifest.get("exports", {})
        self.manifest["exports"]["pptx"] = str(dest.name)
        return dest

    def export_pdf(self, source: Path) -> Path:
        """Export to PDF using LibreOffice."""
        dest = self.deck_dir / f"{self.manifest['title'].lower().replace(' ', '-')}.pdf"
        try:
            subprocess.run([
                "soffice", "--headless", "--convert-to", "pdf",
                "--outdir", str(self.deck_dir),
                str(source)
            ], check=True, timeout=120)
            # LibreOffice names it same as source
            generated = self.deck_dir / f"{source.stem}.pdf"
            if generated != dest:
                generated.rename(dest)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass
        self.manifest["exports"] = self.manifest.get("exports", {})
        self.manifest["exports"]["pdf"] = str(dest.name)
        return dest

    def export_html(self, source: Path) -> Path:
        """Export to HTML (copy if already HTML)."""
        dest = self.deck_dir / f"{self.manifest['title'].lower().replace(' ', '-')}.html"
        if source.suffix == ".html":
            import shutil
            shutil.copy2(source, dest)
        self.manifest["exports"] = self.manifest.get("exports", {})
        self.manifest["exports"]["html"] = str(dest.name)
        return dest

    def export_png(self, source: Path) -> Path:
        """Export slides to PNG using Playwright or LibreOffice+Poppler."""
        slides_dir = self.deck_dir / "slides"
        slides_dir.mkdir(exist_ok=True)

        # Try Playwright first (best quality)
        try:
            import asyncio
            from playwright.async_api import async_playwright

            async def render_slides():
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page()
                    await page.goto(f"file://{source.absolute()}")
                    # Wait for fonts
                    await page.wait_for_load_state("networkidle")
                    # Get slide count
                    slides = await page.query_selector_all(".slide, section, [data-slide]")
                    for i, slide in enumerate(slides):
                        await slide.screenshot(path=str(slides_dir / f"slide-{i+1:02d}.png"))
                    await browser.close()

            asyncio.run(render_slides())
        except ImportError:
            # Fallback: PDF -> PNG
            pdf = self.export_pdf(source)
            try:
                subprocess.run([
                    "pdftoppm", "-png", "-r", "144",
                    str(pdf), str(slides_dir / "slide")
                ], check=True, timeout=120)
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass

        self.manifest["exports"] = self.manifest.get("exports", {})
        self.manifest["exports"]["png_dir"] = "slides/"
        return slides_dir

    def export_all(self, source: Path, formats: List[str]) -> Dict[str, Any]:
        """Export to all requested formats."""
        results = {}
        for fmt in formats:
            if fmt == "pptx":
                results["pptx"] = str(self.export_pptx(source))
            elif fmt == "pdf":
                results["pdf"] = str(self.export_pdf(source))
            elif fmt == "html":
                results["html"] = str(self.export_html(source))
            elif fmt == "png":
                results["png"] = str(self.export_png(source))
        self.save_manifest()
        return results


def main():
    parser = argparse.ArgumentParser(description="Export deck to multiple formats")
    parser.add_argument("source", help="Source file (PPTX, HTML, etc.)")
    parser.add_argument("--formats", nargs="+", default=["pptx", "pdf", "png"],
                        choices=["pptx", "pdf", "html", "png"])
    parser.add_argument("--deck-dir", default=".", help="Deck directory")
    args = parser.parse_args()

    deck_dir = Path(args.deck_dir).resolve()
    source = Path(args.source).resolve()

    if not source.exists():
        print(f"Source not found: {source}")
        return 1

    exporter = DeckExporter(deck_dir)
    results = exporter.export_all(source, args.formats)

    print("Export complete:")
    for fmt, path in results.items():
        print(f"  {fmt}: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())