#!/usr/bin/env python3
"""Build a single-file demo of the site, with every asset inlined.

The production page in site/index.html loads its video and images as separate
files. That is right for a real host and wrong for a shareable preview link, so
this script folds them into one HTML file as data URIs and strips the document
wrapper, which the artifact host supplies itself.

    python3 make-demo.py review/demo.html

It also stamps a small notice, because the hero clip in a demo build is a
procedural stand-in rather than Sky Worth's real footage.
"""
import base64, mimetypes, pathlib, re, sys

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / "site"
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "review" / "demo.html")
OUT.parent.mkdir(parents=True, exist_ok=True)

html = (SITE / "index.html").read_text(encoding="utf-8")


def data_uri(rel):
    p = SITE / rel
    if not p.exists():
        return None
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode("ascii"), p.stat().st_size


inlined, missing = [], []
for rel in ("assets/hero-scrub.mp4", "assets/hero-scrub.webm",
            "assets/hero-poster.jpg", "assets/hero-ending.jpg",
            "assets/fuel-corridor.jpg", "assets/fitting-bay.jpg"):
    got = data_uri(rel)
    if not got:
        missing.append(rel)
        continue
    uri, size = got
    if rel.endswith("hero-scrub.mp4"):
        # index.html already picks between mp4 and webm at runtime, so the demo
        # only has to swap each path for its inlined copy.
        html = html.replace("var VIDEO_MP4='" + rel + "';", "var VIDEO_MP4='" + uri + "';")
        html = re.sub(r"var VIDEO_BYTES=\d+;", f"var VIDEO_BYTES={size};", html)
    elif rel.endswith("hero-scrub.webm"):
        html = html.replace("var VIDEO_WEBM='" + rel + "';", "var VIDEO_WEBM='" + uri + "';")
    elif rel.endswith("hero-poster.jpg"):
        html = html.replace(f"var POSTER_URL='{rel}';", f"var POSTER_URL='{uri}';")
    else:
        html = html.replace(f'src="{rel}"', f'src="{uri}"')
    inlined.append(f"{rel} ({size/1024:.0f} KB)")

# the artifact host supplies the document wrapper, so strip ours
html = re.sub(r"(?is)^.*?<head[^>]*>", "", html)
html = re.sub(r"(?is)</head>\s*<body[^>]*>", "", html)
html = re.sub(r"(?is)</body>\s*</html>\s*$", "", html)
# meta tags that only mean something on a real host
html = re.sub(r'(?im)^\s*<meta\s+(?:charset|name="viewport")[^>]*>\s*$\n?', "", html)
html = re.sub(r'(?is)<!--\s*DEPLOY STEP.*?-->\s*', "", html)
html = re.sub(r'(?im)^\s*<meta\s+(?:property="og:|name="twitter:)[^>]*>\s*$\n?', "", html)
# a name, not a name plus a tagline
html = re.sub(r"<title>.*?</title>", "<title>Sky Worth Tracking</title>", html, flags=re.S)

notice = """
<style>
.demo-note{position:fixed;left:50%;bottom:14px;translate:-50% 0;z-index:90;
  display:flex;align-items:center;gap:10px;max-width:min(92vw,560px);
  font-family:var(--mono);font-size:.68rem;line-height:1.45;letter-spacing:.02em;
  color:var(--text-secondary);background:rgba(8,12,24,.82);backdrop-filter:blur(12px);
  border:1px solid var(--line-strong);border-radius:999px;padding:9px 14px 9px 16px}
.demo-note b{color:var(--accent);font-weight:500}
.demo-note button{flex:none;background:none;border:0;color:var(--text-secondary);
  cursor:pointer;font:inherit;padding:2px 4px;border-radius:6px}
.demo-note button:hover{color:var(--text-primary)}
@media (max-width:640px){.demo-note{font-size:.62rem;bottom:10px}}
</style>
<div class="demo-note" id="demoNote">
  <span><b>Demo build.</b> The hero clip is a stand-in, not Sky Worth's real footage.
  Two section photographs are absent and show a placeholder.</span>
  <button type="button" aria-label="Dismiss" onclick="document.getElementById('demoNote').remove()">&times;</button>
</div>
"""
html = html.replace("</main>", "</main>\n" + notice)

OUT.write_text(html.strip() + "\n", encoding="utf-8")
kb = OUT.stat().st_size / 1024
print("inlined : " + (", ".join(inlined) or "nothing"))
print("missing : " + (", ".join(missing) or "nothing"))
print(f"wrote   : {OUT}  ({kb:.0f} KB)")
