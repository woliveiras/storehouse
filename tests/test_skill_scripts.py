from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from evals.isolation import safe_temp_parent


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=ROOT, check=True)


def expect_failure(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
    if completed.returncode == 0:
        raise AssertionError(f"command unexpectedly succeeded: {' '.join(command)}")


class SkillScriptTests(unittest.TestCase):
    def test_art_helpers_and_bibliography_validator(self) -> None:
        art = ROOT / "skills" / "game-dev-2d-art" / "scripts"
        bibliography = (
            ROOT
            / "skills"
            / "research-paper-authoring"
            / "scripts"
            / "validate-bib.py"
        )
        with tempfile.TemporaryDirectory(
            prefix="storehouse-script-test-", dir=safe_temp_parent()
        ) as raw:
            work = Path(raw).resolve()
            first = work / "first.png"
            second = work / "second.png"
            first_image = Image.new("RGBA", (8, 8), (255, 0, 0, 0))
            first_image.putpixel((3, 3), (255, 0, 0, 255))
            first_image.save(first)
            Image.new("RGBA", (8, 8), (0, 255, 0, 255)).save(second)

            run(
                [
                    sys.executable,
                    str(art / "asset_qa.py"),
                    str(first),
                    "--expect-width",
                    "8",
                    "--expect-height",
                    "8",
                    "--require-alpha",
                    "--json",
                ]
            )
            processed = work / "processed.png"
            process = [
                sys.executable,
                str(art / "pixel_art_process.py"),
                str(second),
                str(processed),
                "--width",
                "8",
                "--height",
                "8",
            ]
            run(process)
            with Image.open(processed) as generated:
                self.assertEqual((8, 8), generated.size)
            expect_failure(process)
            dangling = work / "dangling.png"
            dangling.symlink_to(work / "missing-target.png")
            expect_failure(
                [
                    sys.executable,
                    str(art / "pixel_art_process.py"),
                    str(second),
                    str(dangling),
                    "--width",
                    "8",
                    "--height",
                    "8",
                ]
            )

            sheet = work / "sheet.png"
            run(
                [
                    sys.executable,
                    str(art / "pack_spritesheet.py"),
                    str(first),
                    str(second),
                    "--output",
                    str(sheet),
                    "--cell-width",
                    "8",
                    "--cell-height",
                    "8",
                    "--columns",
                    "2",
                ]
            )
            frames = work / "frames"
            run(
                [
                    sys.executable,
                    str(art / "slice_spritesheet.py"),
                    str(sheet),
                    str(frames),
                    "--frame-width",
                    "8",
                    "--frame-height",
                    "8",
                    "--count",
                    "2",
                ]
            )
            self.assertEqual(2, len(list(frames.glob("*.png"))))
            external_frames = work / "external-frames"
            external_frames.mkdir()
            linked_frames = work / "linked-frames"
            linked_frames.symlink_to(external_frames, target_is_directory=True)
            expect_failure(
                [
                    sys.executable,
                    str(art / "slice_spritesheet.py"),
                    str(sheet),
                    str(linked_frames),
                    "--frame-width",
                    "8",
                    "--frame-height",
                    "8",
                    "--count",
                    "1",
                ]
            )

            duplicate_output = work / "duplicate.png"
            expect_failure(
                [
                    sys.executable,
                    str(art / "pixel_art_process.py"),
                    str(second),
                    str(duplicate_output),
                    "--width",
                    "8",
                    "--height",
                    "8",
                    "--preview",
                    str(duplicate_output),
                ]
            )

            contact = work / "contact.png"
            run(
                [
                    sys.executable,
                    str(art / "make_contact_sheet.py"),
                    str(first),
                    str(second),
                    "--output",
                    str(contact),
                    "--columns",
                    "2",
                    "--no-labels",
                ]
            )

            self.assertTrue(contact.is_file())

            tex = work / "paper.tex"
            bib = work / "sources.bib"
            tex.write_text("Evidence \\cite{fixture}.\n", encoding="utf-8")
            bib.write_text(
                "@article{fixture,\n"
                "  author={A. Author},\n"
                "  title={Fixture},\n"
                "  journal={Synthetic},\n"
                "  year={2026}\n"
                "}\n",
                encoding="utf-8",
            )
            run(
                [
                    sys.executable,
                    str(bibliography),
                    "--tex",
                    str(tex),
                    "--bib",
                    str(bib),
                    "--strict",
                ]
            )

            outside = work.parent / f"{work.name}-outside.tex"
            outside.write_text("outside\n", encoding="utf-8")
            escaping = work / "escaping.tex"
            escaping.write_text(f"\\input{{{outside}}}\n", encoding="utf-8")
            expect_failure(
                [
                    sys.executable,
                    str(bibliography),
                    "--tex",
                    str(escaping),
                    "--bib",
                    str(bib),
                    "--strict",
                ]
            )
            outside.unlink()


if __name__ == "__main__":
    unittest.main()
