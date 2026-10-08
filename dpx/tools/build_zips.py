#!/usr/bin/env python3
"""Build the ZIP packages in assets/packages from variants.json (reproducible: fixed timestamps).

    python3 tools/build_zips.py          # rewrite the zips
    python3 tools/build_zips.py --check  # fail if a zip does not match the files on disk
"""
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

ROOT = build.ROOT
FIXED_TIME = (2026, 1, 1, 0, 0, 0)
# (folder on disk, file suffix)
FORMATS = [("svg", ".svg"), ("png", ".png"), ("png", "@2x.png"), ("docs", ".pdf"), ("source", ".ai")]


def specs():
    """{zip name: [(path inside zip, file on disk)]}; each zip has one top-level folder named after it."""
    data = json.loads((ROOT / "variants.json").read_text())
    return {name: [(f"{name[:-4]}/{s}{ext}", ROOT / "assets" / disk / f"{s}{ext}") for s in stems for disk, ext in FORMATS]
            for name, stems in build.variant_stems(data).items()}


def write(path, entries):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for arcname, source in sorted(entries):
            info = zipfile.ZipInfo(arcname, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, source.read_bytes())


def problems():
    out = []
    for name, entries in specs().items():
        path = ROOT / "assets" / "packages" / name
        if not path.exists():
            out.append(f"{name}: missing")
            continue
        with zipfile.ZipFile(path) as zf:
            have = {i.filename: zf.read(i) for i in zf.infolist() if not i.filename.endswith("/")}
        missing = [arc for arc, src in entries if not src.exists()]
        out += [f"{name}: source file missing for {a}" for a in missing]
        want = {arc: src.read_bytes() for arc, src in entries if src.exists()}
        out += [f"{name}: missing entry {a}" for a in sorted(want.keys() - have.keys())]
        out += [f"{name}: unexpected entry {a}" for a in sorted(have.keys() - want.keys())]
        out += [f"{name}: {a} differs from assets file" for a in sorted(want.keys() & have.keys()) if want[a] != have[a]]
    return out


if __name__ == "__main__":
    if "--check" in sys.argv:
        found = problems()
        sys.exit("\n".join(found) if found else 0)
    (ROOT / "assets" / "packages").mkdir(exist_ok=True)
    for name, entries in specs().items():
        write(ROOT / "assets" / "packages" / name, entries)
        print(f"wrote {name} ({len(entries)} files)")
