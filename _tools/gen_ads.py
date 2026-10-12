# -*- coding: utf-8 -*-
"""Generate photoreal Google Ads creatives for Neta Sagi with gpt-image-1, then cut Google Ads sizes."""
import sys, json, base64, pathlib, re, time, urllib.request, urllib.error
from PIL import Image

ENV = pathlib.Path(r"C:/Users/bzik2/.claude/skills/content-engine/.env")
KEY = re.search(r"^OPENAI_API_KEY=(\S+)", ENV.read_text(encoding="utf-8"), re.M).group(1)

OUT = pathlib.Path(r"C:/Users/bzik2/Desktop/Neta-Sagi-Logo/google-ads"); OUT.mkdir(exist_ok=True)
RAW = pathlib.Path(__file__).parent / "ads-raw"; RAW.mkdir(exist_ok=True)

STYLE = ("Photorealistic editorial photograph, natural light, shot on a 35mm full-frame camera, "
         "shallow depth of field, realistic skin and fabric, Israeli / Tel Aviv setting with Mediterranean light. "
         "No text, no captions, no logos, no watermarks, no readable writing anywhere in the frame.")

SCENES = {
 "surveillance-couple": (
  "Over-the-shoulder view from a distant vantage point: in the foreground, a woman private investigator in her late 30s, "
  "dark hair tied back, plain dark blazer, stands partly hidden behind a concrete pillar on a rooftop terrace and holds a DSLR "
  "camera with a long telephoto lens up to her eye, discreetly photographing. Far below across the street, clearly visible, "
  "a man and a woman in their 40s sit close together at a small table on a sunny cafe terrace, smiling and leaning toward each "
  "other over coffee, suggesting a secret romantic meeting. Both the investigator and the couple are legible in the frame. "
  "Warm late-afternoon light, cinematic but realistic."),
 "two-women-talk": (
  "Two women in their 40s sit at an outdoor cafe table in Tel Aviv having a warm, pleasant conversation over coffee. "
  "The woman on the left is a private investigator in smart-casual clothes: calm, attentive, leaning slightly forward, listening "
  "with a gentle knowing smile and open body language. The woman on the right is relaxed and talkative, mid-sentence, hands "
  "gesturing. Candid, natural feel, soft daylight through trees, pleasant and trustworthy mood."),
 "business-partner": (
  "Corporate investigation scene: seen from inside a parked car, over the shoulder of a woman private investigator holding a "
  "camera with a long lens and photographing through the windshield. Across the street, through the glass facade of a modern "
  "office building, two businessmen in suits shake hands at a conference table while a third person slides a folder across the "
  "table, suggesting a secret deal between a business partner and a competitor. Daylight, Tel Aviv business district with glass "
  "towers, cool professional tones, both the investigator and the meeting are legible."),
 "financial-desk": (
  "Financial investigation close-up: a woman investigator's hands at a dark wooden desk, one hand holding a magnifying glass over "
  "printed financial statements with bar charts and highlighted rows, the other pointing at a figure. A laptop beside shows abstract "
  "line graphs, next to a smartphone, a pen and a cup of coffee. Moody professional atmosphere, cool blue-grey tones with a warm "
  "desk lamp, top-down angled view. All documents and screens are abstract and unreadable."),
}

SIZES = {"landscape": "1536x1024", "square": "1024x1024", "portrait": "1024x1536"}

def generate(prompt, size, quality):
    payload = {"model": "gpt-image-1", "prompt": prompt + " " + STYLE, "size": size, "quality": quality, "n": 1}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations",
                                 data=json.dumps(payload).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {e.code}: {body[:600]}")
    return base64.b64decode(data["data"][0]["b64_json"])

def crop_to(im, w, h):
    """Center-crop to aspect w:h then resize to exactly w x h."""
    W, H = im.size; target = w / h
    if W / H > target:
        nw = round(H * target); box = ((W - nw) // 2, 0, (W - nw) // 2 + nw, H)
    else:
        nh = round(W / target); box = (0, (H - nh) // 2, W, (H - nh) // 2 + nh)
    return im.crop(box).resize((w, h), Image.LANCZOS)

def finish(name, kind, png_bytes):
    raw = RAW / f"{name}-{kind}.png"; raw.write_bytes(png_bytes)
    im = Image.open(raw).convert("RGB")
    if kind == "landscape":
        outs = [("1200x628", crop_to(im, 1200, 628))]
    elif kind == "square":
        outs = [("1200x1200", crop_to(im, 1200, 1200))]
    else:
        outs = [("960x1200", crop_to(im, 960, 1200))]
    for tag, o in outs:
        p = OUT / f"{name}-{tag}.jpg"; o.save(p, quality=92, subsampling=0, optimize=True)
        print(f"  -> {p.name} ({p.stat().st_size//1024} KB)")

if __name__ == "__main__":
    # usage: gen_ads.py <quality> <scene>:<kind> [<scene>:<kind> ...]
    quality = sys.argv[1]
    for job in sys.argv[2:]:
        scene, kind = job.split(":")
        t = time.time(); print(f"{scene} {kind} ({SIZES[kind]}, {quality}) ...", flush=True)
        finish(scene, kind, generate(SCENES[scene], SIZES[kind], quality))
        print(f"  done in {time.time()-t:.0f}s", flush=True)
