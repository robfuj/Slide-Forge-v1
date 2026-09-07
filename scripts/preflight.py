#!/usr/bin/env python3
"""Preflight checks for deck-builder skill."""

import sys
import subprocess
import shutil
from pathlib import Path


def check_python():
    """Check Python version >= 3.11."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (need 3.11+)"


def check_node():
    """Check Node.js version >= 20."""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        version_str = result.stdout.strip().lstrip("v")
        major = int(version_str.split(".")[0])
        if major >= 20:
            return True, f"Node.js {version_str}"
        return False, f"Node.js {version_str} (need 20+)"
    except FileNotFoundError:
        return False, "Node.js not found"


def check_python_packages():
    """Check required Python packages."""
    required = ["pptx", "PIL", "numpy"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if not missing:
        return True, "All packages installed"
    return False, f"Missing: {', '.join(missing)}"


def check_libreoffice():
    """Check LibreOffice availability."""
    for cmd in ["soffice", "libreoffice"]:
        if shutil.which(cmd):
            return True, f"LibreOffice found ({cmd})"
    return False, "LibreOffice not found (optional, for QA render)"


def check_poppler():
    """Check Poppler (pdftoppm) availability."""
    if shutil.which("pdftoppm"):
        return True, "Poppler found (pdftoppm)"
    return False, "Poppler not found (optional, for QA render)"


def check_fonts():
    """Check for common fonts."""
    # This is a placeholder - real implementation would check fontconfig
    return True, "Font check skipped (manual verification needed)"


def main():
    checks = [
        ("Python", check_python),
        ("Node.js", check_node),
        ("Python packages", check_python_packages),
        ("LibreOffice", check_libreoffice),
        ("Poppler", check_poppler),
        ("Fonts", check_fonts),
    ]

    print("=" * 50)
    print("DECK-BUILDER PREFLIGHT CHECKS")
    print("=" * 50)

    all_pass = True
    for name, check_fn in checks:
        passed, msg = check_fn()
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}: {msg}")
        if not passed and name in ("Python", "Python packages"):
            all_pass = False

    print("=" * 50)
    if all_pass:
        print("[OK] All critical checks passed")
        return 0
    else:
        print("[FAIL] Critical checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())