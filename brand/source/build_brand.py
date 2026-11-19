"""
Builds the Foxcrest Property Media brand kit into ../ (the brand/ folder).

    pip install fonttools brotli
    python3 brand/source/build_brand.py        # from the repo root

Writes logo SVGs, then renders PNGs and PDFs with Playwright (render.js).
Edit CONTACT below, then re-run, to update the business card.
"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from mark import mark
from textpath import load, text_path, width

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(OUT, ".."))

C = {
    "navy": "#0b2545", "blue": "#1f5fbf", "bright": "#2f7de1", "sky": "#bcd5f5",
    "tint": "#eef4fc", "white": "#ffffff", "slate": "#56627a",
}
CONTACT = {
    "name": "[OWNER NAME]",
    "title": "Owner & Videographer",
    "phone": "(555) 555-5555",
    "email": "hello@foxcrestpropertymedia.com",
    "web": "foxcrestpropertymedia.com",
}

SERIF = load("fraunces-latin-wght-normal.woff2", wght=700)
SANS = load("inter-latin-600-normal.woff2")

def svg(inner, w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}">{inner}</svg>\n'

# ---- marks -------------------------------------------------------------
MARKS = {
    "foxcrest-mark": mark(),  # primary: navy tile
    "foxcrest-mark-blue": mark(bg=C["blue"], face=C["white"], muzzle=C["blue"], detail=C["white"], inner=C["blue"], eye=C["blue"]),
    "foxcrest-mark-transparent": mark(bgshape=False, face=C["blue"], muzzle=C["white"], detail=C["navy"], inner=C["sky"]),
    "foxcrest-mark-white": mark(bgshape=False, face=C["white"], muzzle=C["navy"], detail=C["white"], inner=C["sky"], eye=C["navy"]),
}

# ---- lockups -----------------------------------------------------------
def horizontal(text1, text2, mark_inner, pad=0):
    s1, s2 = 34, 12.2
    w1 = width(SERIF, "Foxcrest", s1)
    w2 = width(SANS, "PROPERTY MEDIA", s2, tracking=0.2)
    x = 64 + 16
    d1, _ = text_path(SERIF, "Foxcrest", s1, x, 35)
    d2, _ = text_path(SANS, "PROPERTY MEDIA", s2, x + 1, 55, tracking=0.2)
    W = x + max(w1, w2) + 2 + pad
    inner = (f'<g>{mark_inner}</g><path d="{d1}" fill="{text1}"/><path d="{d2}" fill="{text2}"/>')
    return svg(inner, W, 64)

def stacked(text1, text2, mark_inner):
    s1, s2 = 34, 12.2
    w1 = width(SERIF, "Foxcrest", s1); w2 = width(SANS, "PROPERTY MEDIA", s2, tracking=0.2)
    W = max(w1, w2) + 4
    mx = (W - 64) / 2
    d1, _ = text_path(SERIF, "Foxcrest", s1, (W - w1) / 2, 64 + 40)
    d2, _ = text_path(SANS, "PROPERTY MEDIA", s2, (W - w2) / 2, 64 + 62, tracking=0.2)
    inner = f'<g transform="translate({mx:.1f} 0)">{mark_inner}</g><path d="{d1}" fill="{text1}"/><path d="{d2}" fill="{text2}"/>'
    return svg(inner, W, 132)

LOGOS = dict((k, svg(v, 64, 64)) for k, v in MARKS.items())
LOGOS["foxcrest-logo-horizontal"] = horizontal(C["navy"], C["blue"], MARKS["foxcrest-mark"])
LOGOS["foxcrest-logo-horizontal-white"] = horizontal(C["white"], C["sky"], MARKS["foxcrest-mark-blue"])
LOGOS["foxcrest-logo-stacked"] = stacked(C["navy"], C["blue"], MARKS["foxcrest-mark"])
LOGOS["foxcrest-logo-stacked-white"] = stacked(C["white"], C["sky"], MARKS["foxcrest-mark-blue"])

os.makedirs(f"{OUT}/logo/svg", exist_ok=True)
for name, s in LOGOS.items():
    open(f"{OUT}/logo/svg/{name}.svg", "w").write(s)

# website logo + favicon use the primary mark
open(f"{ROOT}/assets/logo.svg", "w").write(LOGOS["foxcrest-mark"])
open(f"{ROOT}/assets/favicon.svg", "w").write(LOGOS["foxcrest-mark"])
open(f"{ROOT}/assets/logo-on-dark.svg", "w").write(LOGOS["foxcrest-mark-blue"])

# ---- render jobs (PNG / PDF via Playwright) -----------------------------
import base64
def _font(fname):
    data = base64.b64encode(open(f"{ROOT}/assets/fonts/{fname}", "rb").read()).decode()
    return f"url(data:font/woff2;base64,{data}) format('woff2')"
FONTCSS = f"""
@font-face {{ font-family: Inter; font-weight: 400; src: {_font('inter-latin-400-normal.woff2')}; }}
@font-face {{ font-family: Inter; font-weight: 500; src: {_font('inter-latin-500-normal.woff2')}; }}
@font-face {{ font-family: Inter; font-weight: 600; src: {_font('inter-latin-600-normal.woff2')}; }}
@font-face {{ font-family: Fraunces; font-weight: 100 900; src: {_font('fraunces-latin-wght-normal.woff2')}; }}
* {{ box-sizing: border-box; }} html, body {{ margin: 0; }}
body {{ font-family: Inter, sans-serif; -webkit-font-smoothing: antialiased; }}
"""
def page(body, css=""):
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{FONTCSS}{css}</style></head><body>{body}</body></html>"

def logo_img(name, h=None, w=None):
    s = LOGOS[name]
    style = (f"height:{h}px;" if h else "") + (f"width:{w}px;" if w else "")
    return s.replace("<svg ", f'<svg style="display:block;{style}" ', 1)

house_lines = """<svg viewBox="0 0 400 300" style="position:absolute;right:-40px;bottom:-30px;width:62%;opacity:.13" fill="none" stroke="#fff" stroke-width="3">
<path d="M40 280V140L200 30l160 110v140z"/><path d="M160 280v-80h80v80"/><rect x="80" y="160" width="50" height="40"/><rect x="270" y="160" width="50" height="40"/><path d="M290 70V30h30v62"/></svg>"""

jobs = []
os.makedirs(f"{OUT}/logo/png", exist_ok=True)
for name in LOGOS:
    if name.endswith("white"):
        bg = C["navy"]
    else:
        bg = "transparent"
    for size in (512, 1024) if "mark" in name else (1000, 2000):
        key = "h" if "mark" in name else "w"
        body = f'<div id="x" style="display:inline-block;background:{bg}">{logo_img(name, **{key: size})}</div>'
        jobs.append({"type": "png", "html": page(body), "out": f"{OUT}/logo/png/{name}-{size}.png", "selector": "#x",
                     "transparent": bg == "transparent"})

# social
os.makedirs(f"{OUT}/social", exist_ok=True)
jobs.append({"type": "png", "w": 1080, "h": 1080, "out": f"{OUT}/social/profile-picture-1080.png", "html": page(
    f'<div style="width:1080px;height:1080px;background:{C["navy"]};display:grid;place-items:center">'
    f'{logo_img("foxcrest-mark-white", h=680)}</div>')})
cover_css = f"""
.c {{ position:relative; overflow:hidden; background:linear-gradient(120deg,{C['navy']} 0%,#123a6e 60%,{C['blue']} 100%); color:#fff; }}
.c h1 {{ font-family:Fraunces; font-weight:700; margin:0; line-height:1.05; letter-spacing:-.01em; }}
.c p {{ color:{C['sky']}; margin:0; }}
.pill {{ display:inline-block; background:#fff; color:{C['navy']}; font-weight:600; border-radius:999px; }}
"""
jobs.append({"type": "png", "w": 1640, "h": 624, "out": f"{OUT}/social/facebook-cover-1640x624.png", "html": page(
    f'<div class="c" style="width:1640px;height:624px;padding:0 120px;display:flex;flex-direction:column;justify-content:center;gap:26px">'
    f'{house_lines}{logo_img("foxcrest-logo-horizontal-white", h=96)}'
    f'<h1 style="font-size:76px;max-width:1000px">Tour the home before you drive over.</h1>'
    f'<p style="font-size:32px">Property video walkthroughs &nbsp;·&nbsp; from $300</p></div>', cover_css)})
jobs.append({"type": "png", "w": 1200, "h": 630, "out": f"{OUT}/social/link-preview-1200x630.png", "html": page(
    f'<div class="c" style="width:1200px;height:630px;padding:0 90px;display:flex;flex-direction:column;justify-content:center;gap:30px">'
    f'{house_lines}{logo_img("foxcrest-logo-horizontal-white", h=78)}'
    f'<h1 style="font-size:66px;max-width:860px">Let buyers walk through the house first.</h1>'
    f'<p style="font-size:28px">Video walkthroughs for homes for sale</p></div>', cover_css)})
jobs.append({"type": "png", "w": 1080, "h": 1350, "out": f"{OUT}/social/instagram-post-template-1080x1350.png", "html": page(
    f'<div class="c" style="width:1080px;height:1350px;padding:100px;display:flex;flex-direction:column;justify-content:space-between">'
    f'{house_lines}{logo_img("foxcrest-logo-horizontal-white", h=110)}'
    f'<div><p style="font-size:30px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;margin-bottom:28px">New walkthrough</p>'
    f'<h1 style="font-size:104px">Your listing<br>headline here</h1>'
    f'<p style="font-size:38px;margin-top:30px;color:#fff">3 bed · 2 bath · Your Town</p></div>'
    f'<div><span class="pill" style="font-size:32px;padding:18px 38px">▶ Watch the full tour · link in bio</span></div></div>', cover_css)})

# business card: 3.5 x 2 in, with 0.125in bleed on each side
os.makedirs(f"{OUT}/print", exist_ok=True)
card_css = f"""
@page {{ size: 3.75in 2.25in; margin: 0; }}
.card {{ width:3.75in; height:2.25in; position:relative; overflow:hidden; page-break-after:always; }}
.safe {{ position:absolute; inset:0.25in; }}
.front {{ background:{C['navy']}; }}
.back {{ background:#fff; color:{C['navy']}; }}
.back h2 {{ font-family:Fraunces; font-weight:700; font-size:13pt; margin:0; }}
.back .t {{ color:{C['blue']}; font-size:7pt; font-weight:600; letter-spacing:.12em; text-transform:uppercase; margin:2pt 0 9pt; }}
.back p {{ margin:0 0 2.5pt; font-size:7.6pt; color:{C['slate']}; }}
.back p b {{ color:{C['navy']}; font-weight:600; display:inline-block; width:34pt; }}
.stripe {{ position:absolute; left:0; right:0; bottom:0; height:0.32in; background:{C['blue']}; color:#fff; font-size:7pt; font-weight:600; letter-spacing:.06em; display:flex; align-items:center; padding-left:0.25in; padding-top:0; }}
"""
card = page(
    f'<div class="card front"><svg viewBox="0 0 400 300" style="position:absolute;right:-.3in;bottom:-.35in;width:2.4in;opacity:.12" fill="none" stroke="#fff" stroke-width="5">'
    f'<path d="M40 280V140L200 30l160 110v140z"/><path d="M160 280v-80h80v80"/></svg>'
    f'<div class="safe" style="display:flex;align-items:center;justify-content:center">{logo_img("foxcrest-logo-stacked-white", h=118)}</div></div>'
    f'<div class="card back"><div class="safe" style="display:flex;gap:14pt;align-items:center;bottom:0.42in">'
    f'<div style="flex:none">{logo_img("foxcrest-mark", h=46)}</div>'
    f'<div><h2>{CONTACT["name"]}</h2><div class="t">{CONTACT["title"]}</div>'
    f'<p><b>Phone</b>{CONTACT["phone"]}</p><p><b>Email</b>{CONTACT["email"]}</p><p><b>Web</b>{CONTACT["web"]}</p></div></div>'
    f'<div class="stripe">PROPERTY VIDEO WALKTHROUGHS &nbsp;·&nbsp; MARKETING CAMPAIGNS</div></div>', card_css)
jobs.append({"type": "pdf", "out": f"{OUT}/print/business-card-3.5x2in-with-bleed.pdf", "html": card})

# brand guide (one page, letter)
sw = lambda name, hexv, use, dark=False: (
    f'<div class="sw"><div class="chip" style="background:{hexv};{"border:1px solid #dbe5f1;" if hexv in ("#ffffff", C["tint"]) else ""}"></div>'
    f'<b>{name}</b><code>{hexv.upper()}</code><span>RGB {int(hexv[1:3],16)}, {int(hexv[3:5],16)}, {int(hexv[5:7],16)}</span><em>{use}</em></div>')
guide_css = f"""
@page {{ size: Letter; margin: 0.4in 0.5in; }}
body {{ color:{C["navy"]}; font-size:9pt; line-height:1.4; }}
h1 {{ font-family:Fraunces; font-size:26pt; margin:0; }}
h2 {{ break-after:avoid; font-family:Fraunces; font-size:13pt; margin:12pt 0 7pt; padding-bottom:4pt; border-bottom:1.5px solid {C['navy']}; }}
.k {{ color:{C['blue']}; font-weight:600; letter-spacing:.14em; text-transform:uppercase; font-size:8pt; margin:0 0 4pt; }}
.row {{ display:flex; gap:12pt; align-items:stretch; }}
.tile {{ border:1px solid #dbe5f1; border-radius:8pt; padding:12pt 8pt; display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1; min-width:0; }}
.cap {{ font-size:7.5pt; color:{C['slate']}; text-align:center; margin-top:4pt; }}
.sw {{ flex:1; }} .sw .chip {{ height:34pt; border-radius:6pt; margin-bottom:5pt; }}
.sw b, .sw code, .sw span, .sw em {{ display:block; }} .sw code {{ font-family:Inter; font-weight:600; color:{C['blue']}; }}
.sw span {{ font-size:7.5pt; color:{C['slate']}; }} .sw em {{ font-style:normal; font-size:7.5pt; margin-top:2pt; }}
.type {{ display:flex; gap:20pt; }} .type > div {{ flex:1; }}
ul {{ margin:0; padding-left:14pt; }} li {{ margin-bottom:3pt; }}
.dont {{ display:flex; gap:10pt; }} .dont div {{ flex:1; border:1px solid #f0c9c9; background:#fff7f7; border-radius:6pt; padding:6pt; text-align:center; font-size:7.5pt; }}
"""
guide = page(f"""
<p class="k">Brand guide</p><h1>Foxcrest Property Media</h1>
<p style="color:{C['slate']};margin:4pt 0 0">Blue and white: trustworthy, clean and calm, like a well-lit open house.</p>
<h2>Logo</h2>
<div class="row">
 <div class="tile">{logo_img("foxcrest-logo-horizontal", h=36)}<div class="cap">Primary: horizontal</div></div>
 <div class="tile" style="background:{C['navy']};border-color:{C['navy']}">{logo_img("foxcrest-logo-horizontal-white", h=36)}<div class="cap" style="color:{C['sky']}">On dark backgrounds</div></div>
 <div class="tile" style="flex:.6">{logo_img("foxcrest-logo-stacked", h=66)}<div class="cap">Stacked</div></div>
 <div class="tile" style="flex:.45">{logo_img("foxcrest-mark", h=48)}<div class="cap">Icon / favicon</div></div>
</div>
<p style="margin:8pt 0 0">The fox's ears form a <b>crest</b> like a roofline, and its white muzzle is a house gable with a doorway nose. Keep clear space around the logo at least the height of the fox's ear, and don't use it smaller than 24px / 0.25in tall.</p>
<div class="dont" style="margin-top:8pt"><div>✕ Don't stretch or squash</div><div>✕ Don't recolor (e.g. orange, green)</div><div>✕ Don't add shadows or outlines</div><div>✕ Don't place on busy photos without a navy panel</div></div>
<h2>Colors</h2>
<div class="row">
 {sw("Navy", C['navy'], "Text, dark sections")}
 {sw("Foxcrest Blue", C['blue'], "Buttons, links, highlights")}
 {sw("Bright Blue", C['bright'], "Logo face, illustrations")}
 {sw("Sky", C['sky'], "Accents on navy")}
 {sw("Mist", C['tint'], "Section backgrounds")}
 {sw("White", C['white'], "Main background")}
</div>
<p style="margin:8pt 0 0;color:{C['slate']}">White text on Foxcrest Blue, and Foxcrest Blue or Navy text on white/Mist, all meet WCAG AA contrast. Don't use Bright Blue or Sky for small text on white.</p>
<h2>Typography</h2>
<div class="type">
 <div><div style="font-family:Fraunces;font-weight:700;font-size:20pt;line-height:1.1">Fraunces Bold</div>
  <p style="color:{C['slate']}">Headlines and the wordmark. Short, confident lines.</p></div>
 <div><div style="font-weight:600;font-size:15pt;line-height:1.2">Inter <span style="font-weight:400">Regular</span> / <span style="font-weight:500">Medium</span> / SemiBold</div>
  <p style="color:{C['slate']}">Body text, buttons, labels. Small caps-style labels use SemiBold, uppercase, wide letter spacing.</p></div>
</div>
<p style="color:{C['slate']};margin:0">Both fonts are free (SIL Open Font License) from Google Fonts and are included in <code>assets/fonts/</code>.</p>
<h2>Voice</h2>
<ul>
 <li><b>Plain and friendly.</b> "Let buyers walk through the house before they drive over," not "Leverage immersive media solutions."</li>
 <li><b>Benefit first.</b> Lead with what the agent or seller gets: attention, fewer wasted showings, faster interest.</li>
 <li><b>Honest.</b> Prices upfront, and no promises of a sale.</li>
</ul>
<h2>Files in this kit</h2>
<p style="margin:0">Logo SVG and PNG (<code>brand/logo/</code>) · Profile picture, Facebook cover, link preview and Instagram template (<code>brand/social/</code>) · Print-ready business card with bleed (<code>brand/print/</code>).</p>
""", guide_css)
jobs.append({"type": "pdf", "out": f"{OUT}/foxcrest-brand-guide.pdf", "html": guide, "letter": True})

tmp = os.path.join(HERE, ".jobs.json")
json.dump(jobs, open(tmp, "w"))
subprocess.run(["node", os.path.join(HERE, "render.js"), tmp], check=True)
os.remove(tmp)
print("Brand kit written to", OUT)
