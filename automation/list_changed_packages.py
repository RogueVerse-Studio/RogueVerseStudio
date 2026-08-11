from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--package")
    parser.add_argument("--output", type=Path, default=Path("automation/build/changed-packages.txt"))
    args = parser.parse_args()
    if args.package:
        manual = Path(args.package).as_posix()
        if not manual.startswith("content-packages/approved/") or not manual.endswith(".json"):
            raise SystemExit("Manual package must be a JSON file under content-packages/approved")
        if not Path(manual).is_file():
            raise SystemExit(f"Approved package does not exist: {manual}")
        packages = [manual]
    else:
        before = args.before if args.before and set(args.before) != {"0"} else f"{args.after}^"
        result = subprocess.run(
            ["git", "diff", "--name-only", before, args.after],
            check=True,
            capture_output=True,
            text=True,
        )
        packages = [
            line for line in result.stdout.splitlines()
            if line.startswith("content-packages/approved/") and line.endswith(".json")
        ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(packages) + ("\n" if packages else ""), encoding="utf-8")
    print("\n".join(packages))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
