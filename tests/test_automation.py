from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "automation"))

from build_package import AUTOMATION_END, AUTOMATION_START, build  # noqa: E402
from package_tools import load_package, validate_package  # noqa: E402


class PackageAutomationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.example_path = ROOT / "content-packages" / "examples" / "faceless-package.example.json"
        self.example = load_package(self.example_path)

    def test_example_package_is_valid(self) -> None:
        self.assertEqual(validate_package(self.example, ROOT), [])

    def test_unsafe_article_markup_is_rejected(self) -> None:
        package = json.loads(json.dumps(self.example))
        package["article"]["blocks"][0]["html"] = '<script>alert("no")</script>'
        errors = validate_package(package, ROOT)
        self.assertTrue(any("unsafe markup" in error for error in errors))

    def test_build_writes_approval_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary) / "site"
            output = Path(temporary) / "output"
            for section in ("old-man-otaku", "news/movies", "future"):
                section_dir = site / section
                section_dir.mkdir(parents=True, exist_ok=True)
                (section_dir / "index.html").write_text(
                    f'<div class="section-cards">\n{AUTOMATION_START}\n{AUTOMATION_END}\n</div>\n',
                    encoding="utf-8",
                )
            hero = site / "assets" / "optimized" / "animanga-updates-1440.webp"
            hero.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / self.example["hero"]["src"], hero)
            (site / "index.html").write_text("<html></html>\n", encoding="utf-8")
            (site / "feed.xml").write_text(
                '<?xml version="1.0"?><rss xmlns:dc="x" xmlns:media="y" xmlns:content="z"><channel><lastBuildDate>old</lastBuildDate>\n  </channel></rss>\n',
                encoding="utf-8",
            )
            package_path = site / "content-packages" / "drafts" / "example.json"
            package_path.parent.mkdir(parents=True, exist_ok=True)
            package_path.write_text(json.dumps(self.example), encoding="utf-8")

            manifest = build(package_path, site, output)

            self.assertEqual(manifest["slug"], self.example["slug"])
            self.assertTrue((site / "old-man-otaku" / self.example["slug"] / "index.html").is_file())
            self.assertTrue((site / "content-packages" / "approved" / f"{self.example['slug']}.json").is_file())
            self.assertTrue((site / "sitemap.xml").is_file())
            self.assertTrue((site / "robots.txt").is_file())
            self.assertTrue((output / "video-props.json").is_file())
            self.assertIn(self.example["slug"], (site / "feed.xml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
