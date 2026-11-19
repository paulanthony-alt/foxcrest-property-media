"""Turn text into SVG path data using the site's own font files (so logos render identically everywhere)."""
import io, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONTS = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "fonts")
_cache = {}

def load(name, wght=None):
    key = (name, wght)
    if key in _cache: return _cache[key]
    f = TTFont(os.path.join(FONTS, name))
    if wght is not None and "fvar" in f:
        from fontTools.varLib.instancer import instantiateVariableFont
        f = instantiateVariableFont(f, {"wght": wght})
    _cache[key] = f
    return f

def text_path(font, text, size, x=0, y=0, tracking=0.0):
    """Return (path_d, width). y is the baseline. tracking in em."""
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font["head"].unitsPerEm
    s = size / upm
    kern = {}
    pen = SVGPathPen(gs)
    cx = 0.0
    names = [cmap.get(ord(ch)) for ch in text]
    for i, gname in enumerate(names):
        if gname is None: continue
        tp = TransformPen(pen, (s, 0, 0, -s, x + cx, y))
        gs[gname].draw(tp)
        cx += gs[gname].width * s + tracking * size
    return pen.getCommands(), cx - tracking * size

def width(font, text, size, tracking=0.0):
    return text_path(font, text, size, tracking=tracking)[1]
