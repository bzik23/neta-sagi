# -*- coding: utf-8 -*-
"""Surveillance-themed Google Ads composites built on the bus-stop frame (text-free)."""
import sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

SCR = pathlib.Path(__file__).parent
OUT = pathlib.Path(r"C:/Users/bzik2/Desktop/Neta-Sagi-Logo/google-ads"); OUT.mkdir(exist_ok=True)
HTML_DIR = SCR / "html-sv"; HTML_DIR.mkdir(exist_ok=True)
PNG_DIR = SCR / "png-sv"; PNG_DIR.mkdir(exist_ok=True)
FR = lambda n: (SCR / "frames" / n).as_uri()
WOMAN = FR("p1-2.jpg")      # woman standing at the bus stop (1024x832)
WOMAN2 = FR("p1-0.5.jpg")   # woman walking toward the bench
WATCH = FR("p1-6.5.jpg")    # investigator at the monitors

SIZES = {"1200x628": (1200, 628), "1200x1200": (1200, 1200), "960x1200": (960, 1200)}

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:{W}px;height:{H}px;overflow:hidden;background:#000}
.card{position:relative;width:{W}px;height:{H}px;overflow:hidden}
.bg{position:absolute;inset:0}
.bg img{width:100%;height:100%;object-fit:cover;display:block}
"""

# Woman stands at ~x 52% / y 45% of the frame; keep her in view in every ratio.
POS = "object-position:55% 40%"

# --- silhouette of a woman holding a camera (foreground watcher), drawn as a simple path ---
# Photographer seen from the side/back, facing right, camera with a long lens raised to the eye.
SIL = """<svg viewBox="0 0 460 520" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMax meet">
 <g fill="#06141c">
  <ellipse cx="200" cy="118" rx="56" ry="66"/>
  <circle cx="152" cy="92" r="30"/>
  <path d="M140 100 C110 130 112 190 125 235 L158 232 C146 190 150 150 168 118 Z"/>
  <rect x="178" y="168" width="48" height="40"/>
  <path d="M110 215 C150 190 260 190 300 215 C330 240 340 330 338 520 L92 520 C86 330 88 240 110 215 Z"/>
  <path d="M118 245 L158 212 L232 132 L262 156 L196 238 L150 275 Z"/>
  <path d="M292 250 L312 206 L352 150 L382 172 L336 236 L312 272 Z"/>
  <rect x="208" y="92" width="112" height="62" rx="9"/>
  <rect x="232" y="78" width="40" height="18" rx="4"/>
  <rect x="318" y="100" width="142" height="48" rx="12"/>
  <circle cx="322" cy="124" r="33"/>
 </g>
</svg>"""

def viewfinder(W, H):
    cw, ch = int(W * .34), int(H * .50)
    L = f"""
    <div class="card">
      <div class="bg"><img src="{WOMAN}" style="{POS}"></div>
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse at 55% 42%,transparent 40%,rgba(0,0,0,.55) 100%)"></div>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),transparent 18%,transparent 82%,rgba(0,0,0,.35))"></div>
      <div style="position:absolute;left:33.3%;top:0;bottom:0;width:1px;background:rgba(255,255,255,.18)"></div>
      <div style="position:absolute;left:66.6%;top:0;bottom:0;width:1px;background:rgba(255,255,255,.18)"></div>
      <div style="position:absolute;top:33.3%;left:0;right:0;height:1px;background:rgba(255,255,255,.18)"></div>
      <div style="position:absolute;top:66.6%;left:0;right:0;height:1px;background:rgba(255,255,255,.18)"></div>
      <div style="position:absolute;left:calc(55% - {cw//2}px);top:calc(40% - {ch//2}px);width:{cw}px;height:{ch}px">
        <i style="position:absolute;left:0;top:0;width:34px;height:34px;border-left:4px solid #fff;border-top:4px solid #fff"></i>
        <i style="position:absolute;right:0;top:0;width:34px;height:34px;border-right:4px solid #fff;border-top:4px solid #fff"></i>
        <i style="position:absolute;left:0;bottom:0;width:34px;height:34px;border-left:4px solid #fff;border-bottom:4px solid #fff"></i>
        <i style="position:absolute;right:0;bottom:0;width:34px;height:34px;border-right:4px solid #fff;border-bottom:4px solid #fff"></i>
        <i style="position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px;border:3px solid #7CFF6B;box-shadow:0 0 12px rgba(124,255,107,.7)"></i>
      </div>
      <div style="position:absolute;left:40px;top:34px;display:flex;align-items:center;gap:12px">
        <i style="width:22px;height:22px;border-radius:50%;background:#FF3B30;box-shadow:0 0 14px #FF3B30"></i>
      </div>
      <div style="position:absolute;right:40px;top:36px;width:54px;height:24px;border:3px solid #fff;border-radius:5px;padding:3px"><i style="display:block;width:70%;height:100%;background:#fff"></i></div>
      <div style="position:absolute;right:30px;bottom:34px;display:flex;gap:8px">{''.join('<i style="width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.7)"></i>' for _ in range(4))}</div>
    </div>"""
    return L

def binoculars(W, H):
    r = int(H * .47) if W > H else int(min(W, H) * .42)
    cx1, cx2 = f"calc(50% - {int(r*.62)}px)", f"calc(50% + {int(r*.62)}px)"
    mask = f"radial-gradient(circle {r}px at {cx1} 50%,#000 97%,transparent 100%),radial-gradient(circle {r}px at {cx2} 50%,#000 97%,transparent 100%)"
    return f"""
    <div class="card" style="background:#000">
      <div class="bg" style="-webkit-mask-image:{mask};mask-image:{mask};-webkit-mask-composite:source-over;mask-composite:add">
        <img src="{WOMAN}" style="{POS}">
        <div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,transparent 55%,rgba(0,0,0,.35) 100%)"></div>
      </div>
    </div>"""

def watcher(W, H):
    # object-position moves the picture, not the subject: 0% shows the left part of the frame and
    # pushes the woman (at ~55% of the frame) toward the right edge of the crop.
    if W > H:   f, pos, blur, rot, bot = .92, 64, 5, 0, -.04      # landscape: tall figure at the left
    elif W == H: f, pos, blur, rot, bot = .62, 0, 7, -22, -.10    # square: lens tilted up toward her face
    else:        f, pos, blur, rot, bot = .55, 0, 7, -25, -.10    # portrait
    sh = int(H * f); sw = int(sh * 460 / 520)
    return f"""
    <div class="card">
      <div class="bg"><img src="{WOMAN}" style="object-position:{pos}% 40%"></div>
      <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,20,28,.55),transparent 42%)"></div>
      <div style="position:absolute;left:-{int(sw*.10)}px;bottom:{int(H*bot)}px;width:{sw}px;height:{sh}px;filter:blur({blur}px);opacity:.93;transform:rotate({rot}deg);transform-origin:0% 100%">{SIL}</div>
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse at {pos}% 40%,transparent 45%,rgba(0,0,0,.35) 100%)"></div>
    </div>"""

def lens(W, H):
    r = int(max(W, H) * .62)
    return f"""
    <div class="card" style="background:#000">
      <div class="bg"><img src="{WOMAN}" style="{POS};filter:blur(9px) brightness(.8);transform:scale(1.05)"></div>
      <div class="bg" style="-webkit-mask-image:radial-gradient(ellipse 30% 42% at 55% 42%,#000 60%,transparent 100%);mask-image:radial-gradient(ellipse 30% 42% at 55% 42%,#000 60%,transparent 100%)"><img src="{WOMAN}" style="{POS}"></div>
      <div style="position:absolute;inset:0;background:radial-gradient(circle {r}px at 50% 50%,transparent 62%,rgba(0,0,0,.75) 86%,#000 100%)"></div>
      <div style="position:absolute;inset:0;background:radial-gradient(circle at 55% 42%,transparent 50%,rgba(0,0,0,.25) 100%)"></div>
    </div>"""

def phone(W, H):
    ph = int(H * .78); pw = int(ph * .48)
    return f"""
    <div class="card">
      <div class="bg"><img src="{WOMAN}" style="{POS};filter:blur(7px) brightness(.62) saturate(.8);transform:scale(1.04)"></div>
      <div style="position:absolute;left:{int(W*.07)}px;bottom:-{int(ph*.06)}px;width:{pw}px;height:{ph}px;transform:rotate(-7deg);transform-origin:50% 100%;border-radius:{int(pw*.13)}px;background:#0b0f14;padding:{int(pw*.035)}px;box-shadow:0 30px 60px rgba(0,0,0,.55),0 0 0 2px #2a2f36">
        <div style="position:relative;width:100%;height:100%;border-radius:{int(pw*.10)}px;overflow:hidden;background:#000">
          <img src="{WOMAN}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:55% 32%;transform:scale(1.25);transform-origin:55% 32%">
          <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45),transparent 20%,transparent 78%,rgba(0,0,0,.55))"></div>
          <i style="position:absolute;left:50%;top:38%;width:{int(pw*.28)}px;height:{int(pw*.28)}px;margin-left:-{int(pw*.14)}px;border:2px solid #FFD60A;border-radius:4px"></i>
          <i style="position:absolute;left:50%;bottom:{int(pw*.06)}px;width:{int(pw*.19)}px;height:{int(pw*.19)}px;margin-left:-{int(pw*.095)}px;border-radius:50%;background:#fff;box-shadow:0 0 0 5px #000,0 0 0 8px #fff"></i>
          <i style="position:absolute;left:{int(pw*.08)}px;bottom:{int(pw*.09)}px;width:{int(pw*.13)}px;height:{int(pw*.13)}px;border-radius:6px;background:#333;border:2px solid #777"></i>
          <i style="position:absolute;right:{int(pw*.08)}px;bottom:{int(pw*.09)}px;width:{int(pw*.13)}px;height:{int(pw*.13)}px;border-radius:50%;background:rgba(255,255,255,.25);border:2px solid #fff"></i>
          <i style="position:absolute;left:50%;top:{int(pw*.05)}px;width:{int(pw*.26)}px;height:{int(pw*.075)}px;margin-left:-{int(pw*.13)}px;border-radius:999px;background:#000"></i>
        </div>
      </div>
    </div>"""

def cctv(W, H):
    g = 6
    cell = f"position:relative;overflow:hidden;background:#000"
    def tile(src, pos, zoom=1.0):
        return f"""<div style="{cell}"><img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};transform:scale({zoom});transform-origin:{pos};filter:saturate(.75) contrast(1.05)">
          <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.14) 0 2px,transparent 2px 5px)"></div>
          <i style="position:absolute;left:16px;top:16px;width:14px;height:14px;border-radius:50%;background:#FF3B30;box-shadow:0 0 10px #FF3B30"></i>
          <i style="position:absolute;right:14px;top:14px;width:26px;height:26px;border-right:3px solid rgba(255,255,255,.8);border-top:3px solid rgba(255,255,255,.8)"></i>
          <i style="position:absolute;left:14px;bottom:14px;width:26px;height:26px;border-left:3px solid rgba(255,255,255,.8);border-bottom:3px solid rgba(255,255,255,.8)"></i>
        </div>"""
    return f"""
    <div class="card" style="background:#000;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:{g}px;padding:{g}px">
      {tile(WOMAN2, "50% 40%")}
      {tile(WOMAN, "60% 35%", 1.35)}
      {tile(WATCH, "30% 50%")}
      {tile(WOMAN, "55% 42%")}
    </div>"""

CONCEPTS = {"viewfinder": viewfinder, "binoculars": binoculars, "watcher": watcher, "phone": phone, "cctv": cctv, "lens": lens}

def main():
    only = set(sys.argv[1:])
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for name, fn in CONCEPTS.items():
            if only and name not in only: continue
            for tag, (W, H) in SIZES.items():
                html = f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE.replace("{W}", str(W)).replace("{H}", str(H))}</style></head><body>{fn(W, H)}</body></html>'
                hp = HTML_DIR / f"{name}-{tag}.html"; hp.write_text(html, encoding="utf-8")
                page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
                page.goto(hp.as_uri()); page.wait_for_load_state("networkidle"); page.wait_for_timeout(250)
                png = PNG_DIR / f"{name}-{tag}.png"; page.screenshot(path=str(png)); page.close()
                out = OUT / f"surveillance-{name}-{tag}.jpg"
                Image.open(png).convert("RGB").save(out, quality=92, subsampling=0, optimize=True)
                print(f"{out.name} {out.stat().st_size//1024} KB")
        browser.close()

if __name__ == "__main__":
    main()
