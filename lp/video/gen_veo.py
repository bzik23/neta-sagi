"""Generate the Neta Sagi story shots with Google Veo 3.1 (Gemini API).

The OpenAI Sora API was shut down on 2026-09-24, so gen.py no longer works.
This script uses the same prompts with Veo. It needs a Gemini API key on a
paid-tier project (Veo is not available on the free tier):

  set GEMINI_API_KEY=...        (or put GEMINI_API_KEY=... in this folder's .env)
  pip install google-genai
  python gen_veo.py 1           # shot 1, 16:9
  python gen_veo.py all         # all six shots
  python gen_veo.py 1 2 3 --mobile   # 9:16 recut for the mobile hero

Output: raw/s<N>.mp4 (landscape) or raw/m<N>.mp4 (mobile).
Veo 3.1 clips are 8 seconds with native audio. Each clip is billed per second
(see ai.google.dev/pricing); expect roughly 3-6 USD for the six landscape shots.
"""
import sys, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen import CHARACTERS, SHOTS  # same prompt pack

def api_key():
    k = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if k:
        return k
    env = os.path.join(HERE, ".env")
    if os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            if line.startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                return line.split("=", 1)[1].strip()
    raise SystemExit("no GEMINI_API_KEY (paid tier required for Veo)")

def main():
    from google import genai
    from google.genai import types
    args = sys.argv[1:]
    mobile = "--mobile" in args
    model = "veo-3.1-generate-preview"
    if "--model" in args:
        model = args[args.index("--model") + 1]
    nums = [int(a) for a in args if a.isdigit()]
    if "all" in args:
        nums = sorted(SHOTS)
    if not nums:
        raise SystemExit(__doc__)
    client = genai.Client(api_key=api_key())
    outdir = os.path.join(HERE, "raw"); os.makedirs(outdir, exist_ok=True)
    ops = {}
    for n in nums:
        prompt = CHARACTERS + "\nSHOT:\n" + SHOTS[n]
        if mobile:
            prompt += "\nVERTICAL 9:16 framing: the bench and the people centered, headroom above, street in the lower third."
        cfg = types.GenerateVideosConfig(aspect_ratio="9:16" if mobile else "16:9", resolution="1080p", number_of_videos=1)
        ops[n] = client.models.generate_videos(model=model, prompt=prompt, config=cfg)
        print(f"shot {n}: submitted", flush=True)
    done = {}
    while len(done) < len(ops):
        time.sleep(15)
        for n, op in ops.items():
            if n in done:
                continue
            op = client.operations.get(op); ops[n] = op
            if not op.done:
                print(f"  shot {n}: running", flush=True); continue
            if op.error:
                done[n] = None; print(f"  shot {n}: FAILED {op.error}", flush=True); continue
            vid = op.response.generated_videos[0]
            name = ("m" if mobile else "s") + f"{n}.mp4"
            path = os.path.join(outdir, name)
            client.files.download(file=vid.video)
            vid.video.save(path)
            done[n] = path
            print(f"  shot {n}: saved {path}", flush=True)
    print("done:", done)

if __name__ == "__main__":
    main()
