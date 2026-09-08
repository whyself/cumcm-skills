"""Inspect image decoding and blank-image risk; visual judgment is still required."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def inspect(path: Path) -> dict:
    try:
        with Image.open(path) as image:
            image.load()
            size, dpi = image.size, image.info.get("dpi")
            rgba = image.convert("RGBA")
            alpha = np.asarray(rgba.getchannel("A"))
            # Inspect visible pixels; transparent RGB payload must not hide a blank canvas.
            background = Image.new("RGBA", size, "white")
            rgb = np.asarray(Image.alpha_composite(background, rgba).convert("RGB"), dtype=float)
        spatial_variance = float(np.var(rgb, axis=(0, 1)).mean())
        white_ratio = float(np.mean(np.all(rgb > 245, axis=2)))
        blank = spatial_variance < 1e-8 or not np.any(alpha)
        risk = blank or spatial_variance < 5 or white_ratio > .98
        return {"path": str(path), "readable": True, "size_px": size, "dpi": dpi,
                "file_bytes": path.stat().st_size, "spatial_variance": spatial_variance,
                "white_ratio": white_ratio, "blank": bool(blank), "possible_blank": bool(risk),
                "status": "fail" if blank else "review" if risk else "readable"}
    except (OSError, ValueError) as exc:
        return {"path": str(path), "readable": False, "status": "fail", "error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    result = inspect(args.image)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
