from __future__ import annotations

import argparse
from pathlib import Path

from build_package import prepare_video_inputs
from package_tools import PackageError, load_package, require_valid_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare Remotion inputs from an approved package")
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--site-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=Path("automation/build"))
    args = parser.parse_args()
    site_root = args.site_root.resolve()
    package = load_package(args.package)
    require_valid_package(package, site_root)
    props = prepare_video_inputs(package, site_root, args.output_dir.resolve())
    print(props)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PackageError as exc:
        print(exc)
        raise SystemExit(2)
