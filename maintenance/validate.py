from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator
from PIL import Image
from evals.isolation import safe_temp_parent

from maintenance.catalog import rendered_files
from maintenance.catalog_data import SKILLS
from maintenance.official_validate import main as official_validate


ROOT = Path(__file__).resolve().parents[1]


def _run(command: list[str], *, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(command, cwd=ROOT, env=env, check=False)
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}")


def _expect_failure(command: list[str]) -> None:
    if subprocess.run(command, cwd=ROOT, check=False, capture_output=True).returncode == 0:
        raise RuntimeError(f"command unexpectedly succeeded: {' '.join(command)}")


def _syntax_checks() -> None:
    for path in sorted((ROOT / "skills").rglob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    for path in sorted((ROOT / "maintenance").glob("*.py")) + sorted((ROOT / "evals").rglob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    for path in sorted((ROOT / "skills").rglob("*.sh")):
        _run(["bash", "-n", str(path)])


def _script_smokes() -> None:
    art = ROOT / "skills" / "game-dev-2d-art" / "scripts"
    bibliography = ROOT / "skills" / "research-paper-authoring" / "scripts" / "validate-bib.py"
    with tempfile.TemporaryDirectory(prefix="storehouse-script-smoke-", dir=safe_temp_parent()) as raw:
        work = Path(raw).resolve()
        first = work / "first.png"
        second = work / "second.png"
        first_image = Image.new("RGBA", (8, 8), (255, 0, 0, 0))
        first_image.putpixel((3, 3), (255, 0, 0, 255))
        first_image.save(first)
        Image.new("RGBA", (8, 8), (0, 255, 0, 255)).save(second)

        _run([sys.executable, str(art / "asset_qa.py"), str(first), "--expect-width", "8", "--expect-height", "8", "--require-alpha", "--json"])
        processed = work / "processed.png"
        _run([sys.executable, str(art / "pixel_art_process.py"), str(second), str(processed), "--width", "8", "--height", "8"])
        with Image.open(processed) as generated:
            if generated.size != (8, 8):
                raise RuntimeError("pixel-art processor produced the wrong dimensions")
        _expect_failure([sys.executable, str(art / "pixel_art_process.py"), str(second), str(processed), "--width", "8", "--height", "8"])
        dangling = work / "dangling.png"
        dangling.symlink_to(work / "missing-target.png")
        _expect_failure([sys.executable, str(art / "pixel_art_process.py"), str(second), str(dangling), "--width", "8", "--height", "8"])

        sheet = work / "sheet.png"
        manifest = work / "sheet.json"
        _run([sys.executable, str(art / "pack_spritesheet.py"), str(first), str(second), "--output", str(sheet), "--cell-width", "8", "--cell-height", "8", "--columns", "2", "--manifest", str(manifest)])
        frames = work / "frames"
        sliced_manifest = work / "frames.json"
        _run([sys.executable, str(art / "slice_spritesheet.py"), str(sheet), str(frames), "--frame-width", "8", "--frame-height", "8", "--count", "2", "--manifest", str(sliced_manifest)])
        if len(list(frames.glob("*.png"))) != 2:
            raise RuntimeError("spritesheet slicer did not produce two frames")
        external_frames = work / "external-frames"
        external_frames.mkdir()
        linked_frames = work / "linked-frames"
        linked_frames.symlink_to(external_frames, target_is_directory=True)
        _expect_failure([sys.executable, str(art / "slice_spritesheet.py"), str(sheet), str(linked_frames), "--frame-width", "8", "--frame-height", "8", "--count", "1"])
        collision = work / "collision"
        _expect_failure([sys.executable, str(art / "slice_spritesheet.py"), str(sheet), str(collision), "--frame-width", "8", "--frame-height", "8", "--count", "1", "--manifest", str(collision)])
        ancestor_manifest = work / "ancestor"
        _expect_failure([sys.executable, str(art / "slice_spritesheet.py"), str(sheet), str(ancestor_manifest / "frames"), "--frame-width", "8", "--frame-height", "8", "--count", "1", "--manifest", str(ancestor_manifest)])
        external_nested = work / "external-nested"
        (external_nested / "subdir").mkdir(parents=True)
        linked_parent = work / "linked-parent"
        linked_parent.symlink_to(external_nested, target_is_directory=True)
        _expect_failure([sys.executable, str(art / "pixel_art_process.py"), str(second), str(linked_parent / "subdir/out.png"), "--width", "8", "--height", "8"])
        duplicate_output = work / "duplicate.png"
        _expect_failure([sys.executable, str(art / "pixel_art_process.py"), str(second), str(duplicate_output), "--width", "8", "--height", "8", "--preview", str(duplicate_output)])

        contact = work / "contact.png"
        _run([sys.executable, str(art / "make_contact_sheet.py"), str(first), str(second), "--output", str(contact), "--columns", "2", "--no-labels"])
        if not contact.is_file():
            raise RuntimeError("contact sheet was not created")

        tex = work / "paper.tex"
        bib = work / "sources.bib"
        tex.write_text("Evidence \\cite{fixture}.\n", encoding="utf-8")
        bib.write_text("@article{fixture,\n  author={A. Author},\n  title={Fixture},\n  journal={Synthetic},\n  year={2026}\n}\n", encoding="utf-8")
        _run([sys.executable, str(bibliography), "--tex", str(tex), "--bib", str(bib), "--strict"])
        outside = work.parent / f"{work.name}-outside.tex"
        outside.write_text("outside\n", encoding="utf-8")
        escaping = work / "escaping.tex"
        escaping.write_text(f"\\input{{{outside}}}\n", encoding="utf-8")
        _expect_failure([sys.executable, str(bibliography), "--tex", str(escaping), "--bib", str(bib), "--strict"])
        outside.unlink()


def _catalog_check(source: Path) -> None:
    for path, expected in rendered_files(source).items():
        if not path.is_file() or path.read_text(encoding="utf-8") != expected:
            raise RuntimeError(f"catalog drift: {path.relative_to(ROOT)}")


def _schema_checks() -> None:
    for stem in ("collections", "skills"):
        schema = json.loads((ROOT / "catalog" / f"{stem}.schema.json").read_text(encoding="utf-8"))
        document = json.loads((ROOT / "catalog" / f"{stem}.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(document)


def main() -> int:
    safe_temp_parent()
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-sources", action="store_true")
    args = parser.parse_args()
    env = os.environ.copy()
    if args.live_sources:
        for name in ("STOREHOUSE_GEREMMYAS_SOURCE", "STOREHOUSE_BASELINE_SOURCE"):
            raw = env.get(name)
            if not raw or not Path(raw).is_absolute():
                raise SystemExit(f"{name} must be an absolute path for live source validation")
        _catalog_check(Path(env["STOREHOUSE_GEREMMYAS_SOURCE"]).resolve())
        env["STOREHOUSE_RUN_EXTERNAL"] = "1"
    else:
        env.pop("STOREHOUSE_GEREMMYAS_SOURCE", None)
        env.pop("STOREHOUSE_BASELINE_SOURCE", None)
    _run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], env=env)
    _syntax_checks()
    _script_smokes()
    _schema_checks()
    official_validate()
    if set(SKILLS) != {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}:
        raise RuntimeError("destination inventory changed after validation")
    print("Deterministic repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
