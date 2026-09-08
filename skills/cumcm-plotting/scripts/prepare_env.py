"""Check imports, install missing plotting packages, then verify in this Python."""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = ("numpy", "pandas", "matplotlib", "seaborn", "PIL")
PACKAGES = {
    **{name: name for name in ("numpy", "pandas", "matplotlib", "seaborn", "scipy",
       "openpyxl", "xlrd", "plotly", "kaleido", "networkx", "shap", "xgboost",
       "lightgbm", "catboost", "rasterio", "pingouin", "pygam", "pycirclize",
       "statsmodels", "geopandas", "geoshapley", "scienceplots", "adjustText",
       "joypy", "squarify", "upsetplot", "factor_analyzer", "pypdf", "joblib")},
    "PIL": "Pillow", "yaml": "PyYAML", "sklearn": "scikit-learn",
    "cv2": "opencv-python", "skimage": "scikit-image", "dateutil": "python-dateutil",
    "mpl_toolkits": "matplotlib", "ternary": "python-ternary", "fitz": "PyMuPDF",
}


def script_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return {name for name in names if name not in sys.stdlib_module_names
            and not (path.parent / (name + ".py")).exists()
            and not (path.parent / name / "__init__.py").exists()}


def probe(name: str) -> dict:
    # A subprocess also catches binary/version failures that find_spec cannot detect.
    code = "import importlib,sys; m=importlib.import_module(sys.argv[1]); print(getattr(m,'__version__','unknown'))"
    result = subprocess.run([sys.executable, "-c", code, name], capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=60)
    return {"available": result.returncode == 0, "version": result.stdout.strip(),
            "error": result.stderr.strip() if result.returncode else ""}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", type=Path)
    parser.add_argument("--extra", action="append", default=[], help="Additional import name")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    requested = set(BASE) | set(args.extra)
    if args.script:
        requested |= script_imports(args.script.resolve())
    for name in requested:
        if not re.fullmatch(r"[A-Za-z_]\w*", name):
            parser.error(f"Invalid import name: {name}")
    unknown = sorted(name for name in requested if name not in PACKAGES)
    if unknown:
        parser.error("Verify package or local-module mapping before installation: " + ", ".join(unknown))
    before = {name: probe(name) for name in sorted(requested)}
    missing = [name for name, info in before.items() if not info["available"]]
    absent = [name for name in missing if importlib.util.find_spec(name) is None]
    installed = []
    install_error = ""
    if absent and not args.check_only:
        packages = sorted({PACKAGES[name] for name in absent})
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", *packages],
                                    capture_output=True, text=True, encoding="utf-8",
                                    errors="replace", timeout=600)
            print(result.stdout, file=sys.stderr)
            if result.returncode:
                install_error = result.stderr.strip()
            else:
                installed = packages
        except subprocess.TimeoutExpired:
            install_error = "Package installation timed out after 600 seconds."
    after = {name: probe(name) for name in sorted(requested)} if absent and not args.check_only else before
    report = {"python": sys.executable, "before": before, "installed": installed,
              "after": after, "install_error": install_error,
              "success": all(info["available"] for info in after.values()) and not install_error}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
