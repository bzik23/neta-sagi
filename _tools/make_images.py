# -*- coding: utf-8 -*-
"""Render branded social images for Neta Sagi (square + wide) from HTML templates."""
import sys, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = pathlib.Path(r"C:/Users/bzik2/Desktop/Neta-Sagi-Logo")
SCR = pathlib.Path(__file__).parent
HTML_DIR = SCR / "html"; HTML_DIR.mkdir(exist_ok=True)
PNG_DIR = SCR / "png"; PNG_DIR.mkdir(exist_ok=True)

LOGO_W = (OUT / "neta-sagi-logo-white-transparent.png").as_uri()
LOGO_B = (OUT / "neta-sagi-logo-blue-transparent.png").as_uri()
FR = lambda n: (SCR / "frames" / n).as_uri()

PHONE = "050-602-3000"

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wdth,wght@75..100,300..800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:{W}px;height:{H}px;overflow:hidden}
body{font-family:"Open Sans",Arial,sans-serif;direction:rtl;color:#2E3A48;background:#EAF3F8;-webkit-font-smoothing:antialiased}
.card{position:relative;width:{W}px;height:{H}px;overflow:hidden}
h1,h2,.cond{font-stretch:75%;font-weight:800;letter-spacing:-.012em;line-height:1.04;text-wrap:balance}
.overline{display:flex;align-items:center;gap:14px;font-weight:700;color:#437D98}
.overline::before{content:"";flex:none;width:44px;height:5px;background:#F37A20;border-radius:3px}
.dark .overline{color:#97C8DD}
.pill{display:inline-flex;align-items:center;gap:12px;background:#F37A20;color:#fff;font-weight:800;border-radius:999px;white-space:nowrap}
.phone{font-weight:800;color:#2B5A72;direction:ltr;unicode-bidi:isolate;white-space:nowrap;letter-spacing:.02em}
.dark .phone{color:#fff}
.steel{background:linear-gradient(135deg,#437D98 0%,#2B5A72 100%)}
.glow{position:absolute;border-radius:50%;filter:blur(70px);pointer-events:none}
.photo{position:absolute;overflow:hidden}
.photo img{width:100%;height:100%;object-fit:cover;display:block}
.line{width:64px;height:6px;background:#F37A20;border-radius:3px}
.muted{color:#5E6B7A}
.dark .muted{color:rgba(255,255,255,.78)}
.row{display:flex;align-items:center;gap:28px}
.svc{background:#197EB4;color:#fff;border-radius:22px;display:flex;flex-direction:column;gap:10px}
.svc svg{width:52px;height:52px;stroke:#fff;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.svc b{font-stretch:75%;font-weight:800;line-height:1.1}
.svc span{opacity:.9;line-height:1.35}
.stat{display:flex;flex-direction:column;align-items:center;gap:6px}
.stat b{color:#F37A20;font-stretch:75%;font-weight:800;line-height:1;direction:ltr;unicode-bidi:isolate}
.badge{position:absolute;top:44px;right:52px;padding:14px 20px 12px;border-radius:16px;background:rgba(255,255,255,.88);backdrop-filter:blur(8px);box-shadow:0 4px 18px rgba(14,60,90,.14)}
.badge img{display:block;width:230px}
.badge.dk{background:rgba(30,68,88,.72);box-shadow:none}
.stat span{color:#fff;font-weight:600}
"""

ICONS = {
 "eye": '<svg viewBox="0 0 24 24"><path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
 "chart": '<svg viewBox="0 0 24 24"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
 "brief": '<svg viewBox="0 0 24 24"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 12h18"/></svg>',
 "talk": '<svg viewBox="0 0 24 24"><path d="M4 5h16v10H9l-5 4V5z"/><path d="M8 9h8M8 12h5"/></svg>',
}

SERVICES = [
 ("eye",   "מעקבים ובגידות",   "חשיפת האמת בדיסקרטיות מלאה, עם ראיות ברורות"),
 ("chart", "חקירות כלכליות",   "איתור נכסים, הונאות והברחת כספים"),
 ("brief", "מעקבים עסקיים",    "ריגול עסקי, גניבות ומעילות בארגון"),
 ("talk",  "דיבוב מקצועי",     "חשיפת מידע והגעה לחקר האמת, במסגרת החוק"),
]

def svc_cards(w, h, title, sub):
    return "".join(
        f'<div class="svc" style="width:{w}px;height:{h}px;padding:30px 28px">{ICONS[k]}'
        f'<b style="font-size:{title}px">{t}</b><span style="font-size:{sub}px">{s}</span></div>'
        for k, t, s in SERVICES)

def stats(num, label, gap):
    items = [("30+", "שנות ניסיון"), ("4,300+", "חקירות"), ("97%", "הצלחה")]
    return f'<div class="row" style="justify-content:center;gap:{gap}px">' + "".join(
        f'<div class="stat"><b style="font-size:{num}px">{n}</b><span style="font-size:{label}px">{l}</span></div>'
        for n, l in items) + "</div>"

TRUST = "משרד חקירות מורשה ממשרד המשפטים · חוקרים יוצאי שב״כ ומשטרה"
LICENSE = "רישיון משרד המשפטים 1221423 · חברים בלשכת החוקרים הפרטיים בישראל"

IMAGES = []
def add(name, W, H, body, cls=""):
    IMAGES.append((name, W, H, body, cls))

# ---------- SQUARE 1080x1080 ----------
add("square-01-logo", 1080, 1080, f"""
<div class="card steel dark">
  <div class="glow" style="width:620px;height:620px;background:#97C8DD;opacity:.35;right:-180px;top:-200px"></div>
  <div class="glow" style="width:560px;height:560px;background:#197EB4;opacity:.55;left:-200px;bottom:-220px"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;padding:0 90px">
    <img src="{LOGO_W}" style="width:760px">
    <div class="line"></div>
    <p style="color:rgba(255,255,255,.82);font-size:28px;font-weight:600;text-align:center;line-height:1.45">{TRUST}</p>
  </div>
  <div style="position:absolute;left:0;right:0;bottom:70px;display:flex;align-items:center;justify-content:center;gap:34px">
    <span class="pill" style="font-size:28px;padding:16px 34px">ייעוץ ראשוני ללא תשלום</span>
    <span class="phone" style="font-size:44px">{PHONE}</span>
  </div>
</div>""")

add("square-02-suspicion", 1080, 1080, f"""
<div class="card">
  <div class="photo" style="inset:0 0 auto 0;height:640px;-webkit-mask-image:linear-gradient(to bottom,#000 55%,transparent 100%);mask-image:linear-gradient(to bottom,#000 55%,transparent 100%)">
    <img src="{FR('p1-2.jpg')}" style="transform:scale(1.18);transform-origin:50% 40%">
  </div>
  <div class="badge"><img src="{LOGO_B}"></div>
  <div style="position:absolute;left:72px;right:72px;bottom:70px;display:flex;flex-direction:column;gap:22px">
    <div class="overline" style="font-size:24px">חקירות בגידות · מעקבים דיסקרטיים</div>
    <h1 style="font-size:86px;color:#2B5A72">מרגישים שמישהו<br>מסתיר מכם משהו?</h1>
    <p class="muted" style="font-size:30px;line-height:1.4;font-weight:500">מעקב דיסקרטי, דיבוב מקצועי והשגת ראיות חותכות.<br>סודיות וחשאיות מוחלטת.</p>
    <div class="row" style="margin-top:10px">
      <span class="pill" style="font-size:28px;padding:16px 34px">ייעוץ ראשוני ללא תשלום</span>
      <span class="phone" style="font-size:42px">{PHONE}</span>
    </div>
  </div>
</div>""")

add("square-03-stats", 1080, 1080, f"""
<div class="card steel dark">
  <div class="glow" style="width:700px;height:700px;background:#197EB4;opacity:.5;left:-260px;top:-260px"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:80px 80px 72px">
    <img src="{LOGO_W}" style="width:460px">
    <div style="display:flex;flex-direction:column;align-items:center;gap:56px">
      <h1 style="color:#fff;font-size:66px;text-align:center">המספרים מדברים בעד עצמם</h1>
      {stats(124, 30, 64)}
    </div>
    <p style="color:rgba(255,255,255,.75);font-size:24px;font-weight:600;text-align:center">{LICENSE}</p>
  </div>
</div>""")

add("square-04-services", 1080, 1080, f"""
<div class="card" style="background:#fff">
  <div style="position:absolute;inset:0 0 auto 0;height:380px;background:linear-gradient(180deg,#EAF3F8,#fff)"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:72px 72px 60px;gap:40px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start">
      <div style="display:flex;flex-direction:column;gap:16px">
        <div class="overline" style="font-size:24px">מה אנחנו עושים</div>
        <h1 style="font-size:78px;color:#2B5A72">ארבעה תחומי התמחות</h1>
      </div>
      <img src="{LOGO_B}" style="width:230px;margin-top:6px">
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:26px">{svc_cards(455, 290, 40, 24)}</div>
    <div class="row" style="justify-content:space-between;margin-top:auto">
      <span class="muted" style="font-size:21px;font-weight:600;max-width:640px;line-height:1.35">{TRUST}</span>
      <span class="phone" style="font-size:40px">{PHONE}</span>
    </div>
  </div>
</div>""")

add("square-05-court", 1080, 1080, f"""
<div class="card dark" style="background:#1E4458">
  <div class="photo" style="inset:0 0 auto 0;height:660px;-webkit-mask-image:linear-gradient(to bottom,#000 50%,transparent 100%);mask-image:linear-gradient(to bottom,#000 50%,transparent 100%)">
    <img src="{FR('p2-5.jpg')}" style="transform:scale(1.2);transform-origin:50% 45%">
    <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,68,88,.25),rgba(30,68,88,.55))"></div>
  </div>
  <div class="badge dk"><img src="{LOGO_W}"></div>
  <div style="position:absolute;left:72px;right:72px;bottom:70px;display:flex;flex-direction:column;gap:22px">
    <div class="overline" style="font-size:24px">ראיות שעומדות בבית משפט</div>
    <h1 style="font-size:96px;color:#fff">לא תחושות.<br>הוכחות.</h1>
    <p class="muted" style="font-size:29px;line-height:1.4;font-weight:500">חוקרים יוצאי שב״כ ומשטרה, רישיון משרד המשפטים,<br>דוח חקירה מסודר וראיות חותכות.</p>
    <div class="row" style="margin-top:10px">
      <span class="pill" style="font-size:28px;padding:16px 34px">ייעוץ ראשוני ללא תשלום</span>
      <span class="phone" style="font-size:42px">{PHONE}</span>
    </div>
  </div>
</div>""")

add("square-06-investigator", 1080, 1080, f"""
<div class="card">
  <div class="photo" style="inset:0 0 auto 0;height:620px;-webkit-mask-image:linear-gradient(to bottom,#000 55%,transparent 100%);mask-image:linear-gradient(to bottom,#000 55%,transparent 100%)">
    <img src="{FR('p1-6.5.jpg')}" style="transform:scale(1.16);transform-origin:50% 45%">
  </div>
  <div class="badge"><img src="{LOGO_B}"></div>
  <div style="position:absolute;left:72px;right:72px;bottom:70px;display:flex;flex-direction:column;gap:22px">
    <div class="overline" style="font-size:24px">מעקב מקצועי · <span dir="ltr">30+</span> שנות ניסיון</div>
    <h1 style="font-size:86px;color:#2B5A72">הספק מכרסם?<br>אנחנו נביא תשובות.</h1>
    <p class="muted" style="font-size:30px;line-height:1.4;font-weight:500">צוות חוקרות וחוקרים יוצאי שב״כ ומשטרה.<br>מעקב, תיעוד וראיות, בשקט ובדיסקרטיות.</p>
    <div class="row" style="margin-top:10px">
      <span class="pill" style="font-size:28px;padding:16px 34px">ייעוץ ראשוני ללא תשלום</span>
      <span class="phone" style="font-size:42px">{PHONE}</span>
    </div>
  </div>
</div>""")

# ---------- WIDE 1200x630 ----------
add("wide-01-logo-1200x630", 1200, 630, f"""
<div class="card steel dark">
  <div class="glow" style="width:520px;height:520px;background:#97C8DD;opacity:.35;right:-160px;top:-200px"></div>
  <div class="glow" style="width:480px;height:480px;background:#197EB4;opacity:.55;left:-180px;bottom:-200px"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;padding-bottom:40px">
    <img src="{LOGO_W}" style="width:600px">
    <div class="line"></div>
    <p style="color:rgba(255,255,255,.82);font-size:24px;font-weight:600;text-align:center">{TRUST}</p>
  </div>
  <div style="position:absolute;left:0;right:0;bottom:44px;display:flex;align-items:center;justify-content:center;gap:30px">
    <span class="pill" style="font-size:22px;padding:12px 28px">ייעוץ ראשוני ללא תשלום</span>
    <span class="phone" style="font-size:36px">{PHONE}</span>
  </div>
</div>""")

add("wide-02-investigator-1200x630", 1200, 630, f"""
<div class="card">
  <div class="photo" style="inset:0 auto 0 0;width:640px;-webkit-mask-image:linear-gradient(to right,#000 55%,transparent 100%);mask-image:linear-gradient(to right,#000 55%,transparent 100%)">
    <img src="{FR('p1-6.5.jpg')}" style="transform:scale(1.2);transform-origin:40% 50%">
  </div>
  <div style="position:absolute;top:56px;right:64px;bottom:56px;width:560px;display:flex;flex-direction:column;justify-content:center;gap:18px">
    <img src="{LOGO_B}" style="width:230px;margin-bottom:6px">
    <div class="overline" style="font-size:20px">חקירות בגידות · מעקבים דיסקרטיים</div>
    <h1 style="font-size:62px;color:#2B5A72">מרגישים שמישהו מסתיר מכם משהו?</h1>
    <p class="muted" style="font-size:23px;line-height:1.4;font-weight:500">מעקב דיסקרטי, דיבוב מקצועי והשגת ראיות חותכות. סודיות מוחלטת.</p>
    <div class="row" style="gap:22px;margin-top:6px">
      <span class="pill" style="font-size:21px;padding:12px 26px">ייעוץ ראשוני ללא תשלום</span>
      <span class="phone" style="font-size:32px">{PHONE}</span>
    </div>
  </div>
</div>""")

add("wide-03-services-1200x630", 1200, 630, f"""
<div class="card" style="background:#fff">
  <div style="position:absolute;inset:0 0 auto 0;height:260px;background:linear-gradient(180deg,#EAF3F8,#fff)"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;padding:48px 56px 40px;gap:30px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start">
      <div style="display:flex;flex-direction:column;gap:12px">
        <div class="overline" style="font-size:20px">מה אנחנו עושים</div>
        <h1 style="font-size:58px;color:#2B5A72">ארבעה תחומי התמחות</h1>
      </div>
      <img src="{LOGO_B}" style="width:210px">
    </div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:18px">{svc_cards(258, 250, 30, 19)}</div>
    <div class="row" style="justify-content:space-between;margin-top:auto">
      <span class="muted" style="font-size:19px;font-weight:600">{TRUST}</span>
      <span class="phone" style="font-size:32px">{PHONE}</span>
    </div>
  </div>
</div>""")

# ---------- WIDE 1920x1080 ----------
add("wide-04-court-1920x1080", 1920, 1080, f"""
<div class="card dark" style="background:#1E4458">
  <div class="photo" style="inset:0 auto 0 0;width:1150px;-webkit-mask-image:linear-gradient(to right,#000 50%,transparent 100%);mask-image:linear-gradient(to right,#000 50%,transparent 100%)">
    <img src="{FR('p2-5.jpg')}" style="transform:scale(1.2);transform-origin:45% 50%">
    <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(30,68,88,.2),rgba(30,68,88,.5))"></div>
  </div>
  <div style="position:absolute;top:90px;right:110px;bottom:90px;width:800px;display:flex;flex-direction:column;justify-content:center;gap:30px">
    <img src="{LOGO_W}" style="width:360px;margin-bottom:10px">
    <div class="overline" style="font-size:28px">ראיות שעומדות בבית משפט</div>
    <h1 style="font-size:118px;color:#fff">לא תחושות.<br>הוכחות.</h1>
    <p class="muted" style="font-size:34px;line-height:1.4;font-weight:500">חוקרים יוצאי שב״כ ומשטרה, רישיון משרד המשפטים, דוח חקירה מסודר וראיות חותכות.</p>
    <div class="row" style="gap:34px;margin-top:10px">
      <span class="pill" style="font-size:32px;padding:18px 40px">ייעוץ ראשוני ללא תשלום</span>
      <span class="phone" style="font-size:50px">{PHONE}</span>
    </div>
  </div>
</div>""")

add("wide-05-stats-1920x1080", 1920, 1080, f"""
<div class="card steel dark">
  <div class="glow" style="width:900px;height:900px;background:#197EB4;opacity:.5;left:-300px;top:-300px"></div>
  <div class="glow" style="width:700px;height:700px;background:#97C8DD;opacity:.3;right:-250px;bottom:-300px"></div>
  <div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:90px 120px 80px">
    <img src="{LOGO_W}" style="width:560px">
    <div style="display:flex;flex-direction:column;align-items:center;gap:60px">
      <h1 style="color:#fff;font-size:84px;text-align:center">המספרים מדברים בעד עצמם</h1>
      {stats(190, 36, 170)}
    </div>
    <p style="color:rgba(255,255,255,.75);font-size:28px;font-weight:600;text-align:center">{LICENSE}</p>
  </div>
</div>""")

add("wide-06-suspicion-1920x1080", 1920, 1080, f"""
<div class="card">
  <div class="photo" style="inset:0 auto 0 0;width:1100px;-webkit-mask-image:linear-gradient(to right,#000 50%,transparent 100%);mask-image:linear-gradient(to right,#000 50%,transparent 100%)">
    <img src="{FR('p1-2.jpg')}" style="transform:scale(1.18);transform-origin:45% 45%">
  </div>
  <div style="position:absolute;top:90px;right:110px;bottom:90px;width:860px;display:flex;flex-direction:column;justify-content:center;gap:30px">
    <img src="{LOGO_B}" style="width:360px;margin-bottom:10px">
    <div class="overline" style="font-size:28px">חקירות בגידות · מעקבים דיסקרטיים</div>
    <h1 style="font-size:104px;color:#2B5A72">מרגישים שמישהו מסתיר מכם משהו?</h1>
    <p class="muted" style="font-size:34px;line-height:1.4;font-weight:500">מעקב דיסקרטי, דיבוב מקצועי והשגת ראיות חותכות. סודיות וחשאיות מוחלטת.</p>
    <div class="row" style="gap:34px;margin-top:10px">
      <span class="pill" style="font-size:32px;padding:18px 40px">ייעוץ ראשוני ללא תשלום</span>
      <span class="phone" style="font-size:50px">{PHONE}</span>
    </div>
  </div>
</div>""")

def main():
    only = set(sys.argv[1:])
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome")
        for name, W, H, body, cls in IMAGES:
            if only and name not in only:
                continue
            html = f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{BASE_CSS.replace("{W}", str(W)).replace("{H}", str(H))}</style></head><body class="{cls}">{body}</body></html>'
            hp = HTML_DIR / f"{name}.html"
            hp.write_text(html, encoding="utf-8")
            page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
            page.goto(hp.as_uri())
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(400)
            png = PNG_DIR / f"{name}.png"
            page.screenshot(path=str(png))
            page.close()
            im = Image.open(png).convert("RGB")
            out = OUT / f"{name}.jpg"
            im.save(out, quality=92, subsampling=0, optimize=True)
            print(f"{name}: {im.size} -> {out.stat().st_size//1024} KB")
        browser.close()

if __name__ == "__main__":
    main()
