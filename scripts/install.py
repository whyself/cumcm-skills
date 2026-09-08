"""Copy bundled skills to a skill directory without overwriting existing skills."""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil


SKILLS = (
    "literature-search",
    "cumcm-modeling",
    "cumcm-result-verification",
    "cumcm-paper-planning",
    "cumcm-plotting",
    "cumcm-language-polish",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dest", type=Path, default=Path.home() / ".agents" / "skills",
        help="Destination skill directory (default: ~/.agents/skills)",
    )
    parser.add_argument("--only", nargs="+", choices=SKILLS, help="Install selected skills")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "skills"
    destination = args.dest.expanduser().resolve()
    selected = tuple(dict.fromkeys(args.only or SKILLS))

    # Reject recursive copies, including destinations reached through symlinks.
    if destination == source or source in destination.parents:
        parser.error("Destination must be outside this repository's skills directory.")
    if destination.exists() and not destination.is_dir():
        parser.error(f"Destination is not a directory: {destination}")
    for name in selected:
        if not (source / name / "SKILL.md").is_file():
            parser.error(f"Missing skill entry point: {source / name / 'SKILL.md'}")

    skipped = []
    for name in selected:
        target = destination / name
        if target.exists() or target.is_symlink():
            print(f"SKIP {name}: destination already exists: {target}")
            skipped.append(name)
            continue
        if args.dry_run:
            print(f"COPY {source / name} -> {target}")
            continue
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copytree(
            source / name, target,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".mplconfig"),
        )
        print(f"INSTALLED {name}: {target}")

    if skipped:
        print("Existing skills were kept. Back up and move them before reinstalling.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
