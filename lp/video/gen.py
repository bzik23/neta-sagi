"""Generate the Neta Sagi story shots with OpenAI Sora 2.

Usage:
  python gen.py 1            # shot 1, landscape (1280x720), sora-2
  python gen.py 1 2 3        # several shots, submitted together
  python gen.py all          # all six shots
  python gen.py 1 2 3 --mobile   # 720x1280 recut for the mobile hero
  python gen.py 4 --model sora-2-pro --seconds 12

Output: raw/s<N>.mp4 (landscape) or raw/m<N>.mp4 (mobile).
The API key is read from OPENAI_API_KEY or the content-engine .env file.
"""
import sys, os, time, json, urllib.request, urllib.error, re, io

HERE = os.path.dirname(os.path.abspath(__file__))
ENV = r"C:\Users\bzik2\.claude\skills\content-engine\.env"

def api_key():
    k = os.environ.get("OPENAI_API_KEY")
    if k:
        return k
    for line in open(ENV, encoding="utf-8"):
        if line.startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("no OPENAI_API_KEY")

CHARACTERS = """CHARACTERS (keep identical across shots):
- SUSPECT: Israeli woman, late 30s, shoulder-length dark wavy hair, light-blue linen shirt, black jeans, white sneakers, black leather tote bag on her lap, phone in hand, slightly tense posture.
- INVESTIGATOR: Israeli woman, early 50s, confident and warm, short dark-blonde hair, beige lightweight blazer over a white t-shirt, dark trousers, small crossbody bag, no visible badge or equipment, relaxed body language, calm steady eye contact.
- POLICE: two Israeli police officers (one woman, one man) in light-blue Israel Police uniforms with dark vests, arriving on foot from a white police car with blue-and-white markings parked at the curb.
LOCATION: a real-looking central Tel Aviv bus stop on a wide boulevard: modern glass-and-steel shelter with a bench, Bauhaus-style white buildings, ficus trees, scooters, a cafe across the street, Hebrew street signage, bright hazy midday light.
STYLE: cinematic documentary realism, 35mm lens, shallow depth of field, natural color, slight handheld feel, no text overlays, no captions, no logos. Keep the bench and the people in the LEFT two thirds of the frame with calmer negative space on the right.
"""

SHOTS = {
    1: """Wide establishing shot of the bus stop at midday. SUSPECT sits alone on the bench, scrolling her phone, glancing up the street. Pedestrians pass, a scooter goes by, a bus pulls away in the background. Slow push-in from across the street. Ambient audio only: city traffic, distant horns, a bus hiss, footsteps, Hebrew chatter from passersby, birds in the ficus trees. No music, no dialogue.""",
    2: """Medium shot from the side of the bench. INVESTIGATOR walks into frame casually, checks the bus timetable on the shelter pole, then sits on the bench leaving a polite gap next to SUSPECT. She exhales, looks up the street like any commuter, then glances at SUSPECT with a small friendly smile and says in Hebrew: "גם את מחכה לחמש? היום הוא פשוט לא מגיע." SUSPECT half-smiles and nods. Natural street ambience continues. No music.""",
    3: """Two-shot, slightly low angle, both women on the bench. INVESTIGATOR speaks softly with open body language and relaxed hands. SUSPECT gradually turns toward her, shoulders dropping. Quiet natural dialogue in Hebrew. INVESTIGATOR: "נראה שעבר עלייך בוקר לא פשוט." SUSPECT: "את לא יודעת כמה." INVESTIGATOR: "לפעמים עוזר להגיד את זה בקול למישהי זרה." SUSPECT pauses and looks down at her bag. Background: bus brakes, a dog barking, cafe chatter. No music.""",
    4: """Slow push-in on SUSPECT's face, INVESTIGATOR soft in the foreground edge of frame. SUSPECT speaks quietly in Hebrew, voice breaking slightly: "לקחתי את הכסף מהחשבון של החברה. חשבתי שאף אחד לא ישים לב." INVESTIGATOR nods slowly without judgment and says: "תודה שסיפרת לי." A short beat. SUSPECT suddenly realizes and looks at her: "רגע... מי את?" Street ambience continues; a faint police siren begins to rise in the distance.""",
    5: """Wide shot. A white Israel Police car with blue markings pulls up to the curb with a short siren chirp. The two POLICE officers step out and walk calmly to the bench. INVESTIGATOR stands and steps aside, giving the female officer a small nod. The officers speak briefly to SUSPECT, who stands up slowly with slumped shoulders and is escorted toward the car by the arm, calmly and without force. Passersby glance and keep walking. Ambient: siren chirp, car doors, radio chatter, city noise. No music.""",
    6: """Medium shot of INVESTIGATOR alone at the bus stop as the police car pulls away softly in the background. She takes out her phone, types a short message, puts it away, straightens her blazer and walks out of frame into the Tel Aviv street, blending into the crowd. Camera holds on the empty bench. Ambient city sound only. No music.""",
}

def req(method, path, key, body=None, raw=False):
    url = "https://api.openai.com/v1" + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", "Bearer " + key)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            return resp.read() if raw else json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} {method} {path}: {e.read().decode()[:600]}")

def main():
    args = sys.argv[1:]
    mobile = "--mobile" in args
    model = "sora-2"
    seconds = "8"
    if "--model" in args:
        model = args[args.index("--model") + 1]
    if "--seconds" in args:
        seconds = args[args.index("--seconds") + 1]
    nums = [int(a) for a in args if a.isdigit()]
    if "all" in args:
        nums = sorted(SHOTS)
    if not nums:
        raise SystemExit(__doc__)
    size = "720x1280" if mobile else "1280x720"
    key = api_key()
    outdir = os.path.join(HERE, "raw"); os.makedirs(outdir, exist_ok=True)
    jobs = {}
    for n in nums:
        prompt = CHARACTERS + "\nSHOT:\n" + SHOTS[n]
        if mobile:
            prompt += "\nVERTICAL 9:16 framing: the bench and the people centered in the frame, headroom above, street in the lower third."
        v = req("POST", "/videos", key, {"model": model, "prompt": prompt, "seconds": seconds, "size": size})
        jobs[n] = v["id"]
        print(f"shot {n}: submitted {v['id']} status={v.get('status')}", flush=True)
    done = {}
    while len(done) < len(jobs):
        time.sleep(15)
        for n, vid in jobs.items():
            if n in done:
                continue
            v = req("GET", f"/videos/{vid}", key)
            st = v.get("status"); prog = v.get("progress")
            print(f"  shot {n}: {st} {prog if prog is not None else ''}", flush=True)
            if st == "completed":
                data = req("GET", f"/videos/{vid}/content", key, raw=True)
                name = ("m" if mobile else "s") + f"{n}.mp4"
                path = os.path.join(outdir, name)
                open(path, "wb").write(data)
                done[n] = path
                print(f"  shot {n}: saved {path} ({len(data)//1024} KB)", flush=True)
            elif st in ("failed", "cancelled"):
                done[n] = None
                print(f"  shot {n}: FAILED {json.dumps(v.get('error'))[:400]}", flush=True)
    print("done:", json.dumps(done, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
