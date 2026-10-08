# Neta Sagi LP - hero video prompt pack

Scene: an ordinary weekday in central Tel Aviv. A woman waits at a bus stop. Our investigator (plain clothes) sits next to her, starts a casual conversation, and through skilled elicitation ("dibuv") gets her to admit what she did. Police arrive and detain the woman.

Two deliverables are cut from the same shots:

1. `assets/video/hero.mp4` - silent loop for the hero background, 12-16 s, 1920x1080, shots 1-3 only (ambient, investigator sits, conversation). No arrest in the loop: the hero must feel calm and discreet.
2. `assets/video/story.mp4` - the full story with sound, 40-50 s, shown in the "watch" section with a play button.
3. Optional `assets/video/hero-mobile.mp4` - 1080x1920 vertical recut of shots 1-3 (the page picks it automatically under 720 px).

Generate 8-second clips (Veo 3 / Sora 2 / Kling 2.x), keep character consistency with the same character block in every prompt, then concatenate with ffmpeg (see bottom).

---

## Character block (paste at the top of every prompt)

```
CHARACTERS (keep identical across shots):
- SUSPECT: Israeli woman, late 30s, shoulder-length dark wavy hair, light-blue linen shirt, black jeans, white sneakers, black leather tote bag on her lap, phone in hand, slightly tense posture.
- INVESTIGATOR: Israeli woman, early 50s, confident and warm, short dark-blonde hair, beige lightweight blazer over a white t-shirt, dark trousers, small crossbody bag, no visible badge or equipment, relaxed body language, calm steady eye contact.
- POLICE: two Israeli police officers (one woman, one man) in light-blue Israel Police uniforms with dark vests, arriving on foot from a white police car with blue-and-white markings parked at the curb.
LOCATION: a real-looking central Tel Aviv bus stop on a wide boulevard (Ibn Gabirol / Dizengoff feel): modern glass-and-steel shelter with a bench, Bauhaus-style white buildings, ficus trees, scooters, a cafe across the street, Hebrew street signage, bright hazy midday light.
STYLE: cinematic documentary realism, shot on a 35mm lens, shallow depth of field, natural color, slight handheld feel, no text overlays, no captions, no logos.
```

## Shot list

### Shot 1 - Establishing (8 s)
```
[CHARACTER BLOCK]
Wide establishing shot of the bus stop at midday. SUSPECT sits alone on the bench, scrolling her phone, glancing up the street. Pedestrians pass, a scooter goes by, a bus pulls away in the background. Slow push-in from across the street. Ambient audio only: city traffic, distant horns, a bus hiss, footsteps, Hebrew chatter from passersby, birds in the ficus trees. No music.
```

### Shot 2 - The investigator arrives (8 s)
```
[CHARACTER BLOCK]
Medium shot from the side of the bench. INVESTIGATOR walks into frame casually, checks the bus timetable on the shelter pole, then sits on the bench leaving a polite gap next to SUSPECT. She exhales, looks up the street like any commuter, then glances at SUSPECT with a small friendly smile and says in Hebrew: "גם את מחכה לחמש? היום הוא פשוט לא מגיע." SUSPECT half-smiles, nods. Natural street ambience continues. No music.
```

### Shot 3 - The conversation (8 s)
```
[CHARACTER BLOCK]
Two-shot, slightly low angle, both women on the bench. INVESTIGATOR speaks softly, open body language, hands relaxed. SUSPECT gradually turns toward her, shoulders dropping. Dialogue in Hebrew, quiet and natural:
INVESTIGATOR: "נראה שעבר עלייך בוקר לא פשוט."
SUSPECT: "את לא יודעת כמה."
INVESTIGATOR: "לפעמים עוזר להגיד את זה בקול למישהי זרה."
SUSPECT pauses, looks at her bag. Background: bus brakes, a dog barking, cafe chatter. No music.
```

### Shot 4 - The confession (8 s)
```
[CHARACTER BLOCK]
Slow push-in on SUSPECT's face, INVESTIGATOR soft in the foreground edge of frame. SUSPECT speaks quietly in Hebrew, voice breaking slightly: "לקחתי את הכסף מהחשבון של החברה. חשבתי שאף אחד לא ישים לב." INVESTIGATOR nods slowly, no judgment, and says: "תודה שסיפרת לי." A short beat. SUSPECT suddenly realizes and looks at her: "רגע... מי את?" Street ambience continues; a faint police siren begins to rise in the distance.
```

### Shot 5 - Police arrive (8 s)
```
[CHARACTER BLOCK]
Wide shot. A white Israel Police car with blue markings pulls up to the curb with a short siren chirp. The two POLICE officers step out and walk calmly to the bench. INVESTIGATOR stands and steps aside, giving the female officer a small nod. The officers address SUSPECT, who stands up slowly, shoulders slumped, and is escorted toward the car by the arm, without force. Passersby glance and keep walking. Ambient: siren chirp, car doors, radio chatter, city noise.
```

### Shot 6 - Closing (8 s)
```
[CHARACTER BLOCK]
Medium shot of INVESTIGATOR alone at the bus stop as the police car pulls away in the soft background. She takes out her phone, types a short message, puts it away, straightens her blazer and walks out of frame into the Tel Aviv street, blending into the crowd. Camera holds on the empty bench. Ambient city sound only. No music.
```

---

## Notes for the generator

- Ask for **1920x1080, 24 fps**, highest quality. For the mobile hero, regenerate shots 1-3 as **9:16** with the bench centered.
- Keep the camera on the **left two thirds** of the frame in shots 1-3: the landing page places the headline on the right, so the bench and the women should sit left of center with calmer negative space on the right.
- Hebrew dialogue: if the model's Hebrew speech is weak, generate the clips with ambience only and record the lines separately (any Hebrew TTS or a voice actor), then mix in ffmpeg.
- Avoid: visible logos, readable license plates, real brand names, blood, weapons, handcuffs in close-up.

## ffmpeg assembly

```
# hero loop (silent, shots 1-3)
ffmpeg -i s1.mp4 -i s2.mp4 -i s3.mp4 -filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]" -map "[v]" -an -movflags +faststart -pix_fmt yuv420p -crf 23 -preset slow hero.mp4

# full story (with sound, shots 1-6)
ffmpeg -i s1.mp4 -i s2.mp4 -i s3.mp4 -i s4.mp4 -i s5.mp4 -i s6.mp4 -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a][3:v][3:a][4:v][4:a][5:v][5:a]concat=n=6:v=1:a=1[v][a]" -map "[v]" -map "[a]" -movflags +faststart -pix_fmt yuv420p -crf 22 -preset slow story.mp4

# poster frames
ffmpeg -ss 2 -i hero.mp4 -frames:v 1 -q:v 3 ../hero-poster.jpg
ffmpeg -ss 2 -i hero-mobile.mp4 -frames:v 1 -q:v 3 ../hero-poster-mobile.jpg
```

Target sizes: hero.mp4 under 4 MB, hero-mobile.mp4 under 3 MB, story.mp4 under 12 MB.

---

## A softer alternative ending (optional)

If the arrest feels too harsh for an infidelity audience, replace shots 5-6 with: INVESTIGATOR thanks her, stands, walks away, and in the final shot a client (a woman at home) receives a WhatsApp message "יש לנו תשובה. מתי נוח לדבר?" and closes her eyes in relief. Same shots 1-4.
