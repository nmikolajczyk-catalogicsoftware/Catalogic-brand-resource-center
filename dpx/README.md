# Catalogic / DPX / vStor / GuardMode Brand Resource Center

Static brand site. Open `dpx/index.html` in a browser; there is no runtime dependency.

## Editing the download rows

`dpx/index.html` is **generated**. Do not edit the download sections by hand.

- `dpx/variants.json` lists every download row (section, file, name, description).
- `dpx/index.template.html` holds the rest of the page.
- Build from `dpx/`: `python3 tools/build.py` (add `--check` to verify `index.html` is up to date).

Each row `<file>` expects: `assets/svg/<file>.svg`, `assets/png/<file>.png`, `assets/png/<file>@2x.png`,
`assets/docs/<file>.pdf`, `assets/source/<file>.ai`.
