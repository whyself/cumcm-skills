"""Create or update a private configuration without putting secrets in CLI arguments."""

import argparse
import getpass
import json
import os
import tempfile
from pathlib import Path

from runtime import DEFAULT_CONFIG, FIELDS, load_config


def save_config(target, data):
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=target.parent, prefix=".config-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=True)
            handle.write("\n")
        os.chmod(temporary, 0o600)
        os.replace(temporary, target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--init", action="store_true")
    modes.add_argument("--set", choices=FIELDS)
    modes.add_argument("--show", action="store_true")
    args = parser.parse_args()
    try:
        if args.show:
            cfg = load_config(args.config)
            print(json.dumps({"path": str(args.config), "configured": {FIELDS[k]: bool(v) for k, v in cfg.items()}}, indent=2))
            return 0
        if args.init:
            if not args.config.exists():
                save_config(args.config, {k: "" for k in FIELDS})
            print("Configuration file ready: " + str(args.config))
            return 0
        data = json.loads(args.config.read_text(encoding="utf-8-sig")) if args.config.exists() else {k: "" for k in FIELDS}
        if not isinstance(data, dict) or set(data) - set(FIELDS) or any(not isinstance(v, str) for v in data.values()):
            raise ValueError("Invalid config")
        value = getpass.getpass("Value for " + FIELDS[args.set] + " (hidden; blank cancels): ").strip()
        if not value:
            print("No change")
            return 0
        if args.set == "email" and ("@" not in value or any(c.isspace() for c in value)):
            raise ValueError("Invalid email")
        data[args.set] = value
        save_config(args.config, data)
        print("Saved " + FIELDS[args.set] + " to " + str(args.config) + "; value hidden")
        if os.environ.get(FIELDS[args.set]):
            print("An existing environment variable overrides this saved value")
        return 0
    except (ValueError, OSError, EOFError):
        print("Configuration failed. Check the file format, field names, path, and interactive input.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
