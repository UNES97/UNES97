"""
Shared toolkit for the profile README scenes (assets/src/scene_*.py).

Each scene builds an SVG string per theme and calls `write(name, {"light": svg, "dark": svg})`.
Fonts are subset to the characters a scene uses and embedded, so every SVG renders the same everywhere
(GitHub shows SVGs as <img>: no external fonts/scripts, but CSS animations inside the SVG work).

Needs: fonttools, pillow  (pip install fonttools pillow)
"""
from __future__ import annotations

import base64
import io
import subprocess
import urllib.request
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
CACHE = Path(__file__).resolve().parent / ".cache"

W = 840  # every scene is 840 px wide (GitHub README content width)

# ───────────────────────── palette (same identity as the website) ─────────────────────────
THEMES = {
    "light": dict(
        bg="#f2efe7", panel="#fbfaf6", ink="#0f1013", ink2="#44454d", ink3="#66676f", line="#ddd9cf",
        grid="rgba(15,16,19,0.07)", cobalt="#2a3bff", cobalt_soft="#e4e6ff", on_cobalt="#f2efe7",
        lilac="#b9c0ff", peach="#ff9b71", mint="#c7f0d8", green="#17b26a", impact="#ffd23f", danger="#ff5a4e",
    ),
    "dark": dict(
        bg="#0f1013", panel="#17181c", ink="#f2efe7", ink2="#c9c7c0", ink3="#9a9aa2", line="#2a2b31",
        grid="rgba(242,239,231,0.06)", cobalt="#5263ff", cobalt_soft="#1c2150", on_cobalt="#ffffff",
        lilac="#b9c0ff", peach="#ff9b71", mint="#7fe0a8", green="#22c87a", impact="#ffd23f", danger="#ff6b5f",
    ),
}

# ───────────────────────── fonts ─────────────────────────
# JX = Plus Jakarta Sans ExtraBold (800), JS = SemiBold (600), JP = Noto Sans JP Black (900, for katakana).
_WEBSITE_FONTS = {"JX": "src/app/fonts/PlusJakartaSans-ExtraBold.ttf", "JS": "src/app/fonts/PlusJakartaSans-SemiBold.ttf"}
_JP_URL = "https://github.com/google/fonts/raw/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf"
_raw: dict[str, bytes] = {}


def _git_show(path: str) -> bytes:
    return subprocess.run(["git", "show", f"website:{path}"], cwd=ROOT, capture_output=True, check=True).stdout


def font_bytes(key: str) -> bytes:
    if key in _raw:
        return _raw[key]
    if key in _WEBSITE_FONTS:
        _raw[key] = _git_show(_WEBSITE_FONTS[key])
    elif key == "JP":
        CACHE.mkdir(exist_ok=True)
        static = CACHE / "NotoSansJP-Black.ttf"
        if not static.exists():
            var = CACHE / "NotoSansJP-var.ttf"
            if not var.exists():
                urllib.request.urlretrieve(_JP_URL, var)
            font = instancer.instantiateVariableFont(TTFont(var), {"wght": 900})
            font.save(static)
        _raw[key] = static.read_bytes()
    else:
        raise KeyError(key)
    return _raw[key]


def _subset_b64(raw: bytes, text: str) -> str:
    font = TTFont(io.BytesIO(raw))
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["kern", "liga"]
    sub = subset.Subsetter(opts)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def font_css(text: str, keys=("JX", "JS")) -> str:
    """@font-face rules for the given font keys, subset to `text` (pass ALL text the SVG shows)."""
    chars = "".join(sorted(set(text + " 0123456789")))
    rules = []
    for k in keys:
        rules.append(f"@font-face{{font-family:{k};src:url(data:font/woff;base64,{_subset_b64(font_bytes(k), chars)}) format('woff');}}")
    rules.append(".jx{font-family:JX,sans-serif;font-weight:800}.js{font-family:JS,sans-serif;font-weight:600}.jp{font-family:JP,sans-serif;font-weight:900}")
    return "".join(rules)


class Metrics:
    """Measure text width with the real font metrics (for precise layout)."""

    def __init__(self, key="JX"):
        f = TTFont(io.BytesIO(font_bytes(key)))
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]

    def width(self, text: str, size: float, tracking: float = 0.0) -> float:
        units = sum(self.hmtx[self.cmap[ord(c)]][0] for c in text if ord(c) in self.cmap)
        return units / self.upm * size + tracking * max(len(text) - 1, 0)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ───────────────────────── photo ─────────────────────────
def photo_duotone(theme: str, size: int = 520) -> str:
    """Younes's portrait as a two-tone image (ink shadows → cobalt/lilac highlights), base64 JPEG data URI."""
    from PIL import Image, ImageOps

    raw = _git_show("src/assets/photo.jpg")
    im = Image.open(io.BytesIO(raw)).convert("L").resize((size, size), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=1)
    t = THEMES[theme]
    dark, light = (t["ink"], t["cobalt"]) if theme == "light" else ("#0b0c1f", t["lilac"])
    duo = ImageOps.colorize(im, black=dark, white=light, mid=None)
    buf = io.BytesIO()
    duo.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


# ───────────────────────── output ─────────────────────────
def write(name: str, svgs: dict[str, str]) -> None:
    OUT.mkdir(exist_ok=True)
    for theme, svg in svgs.items():
        p = OUT / f"{name}-{theme}.svg"
        p.write_text(svg, encoding="utf-8")
        print(f"{p.name:28} {p.stat().st_size / 1024:6.1f} KB")
