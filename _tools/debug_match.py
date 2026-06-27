import os, re

def n(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())

transcript = []
with open(os.path.join(os.getcwd(), "transcript_words.txt"), "r", encoding="utf-8") as f:
    lines = f.read().strip().split("\n")
header = True
for line in lines:
    if header and line.startswith("word"):
        header = False
        continue
    parts = line.strip().split("\t")
    if len(parts) == 3:
        w, s, e = parts
        transcript.append({"word": w.strip(), "start": float(s), "end": float(e)})

# Test S037
img37_text = "It looks nothing like the one you are living in right now."
sw37 = [n(w) for w in img37_text.split() if n(w)]
print("S037 words:", sw37)
print()

# Transcript words 358-377
print("Transcript words 358-377:")
for i in range(358, min(378, len(transcript))):
    tw = transcript[i]["word"]
    print(f"  {i}: {tw:25s} n={n(tw):20s} start={transcript[i]['start']}")

# Check match at pos 358
print("\nMatching S037 at pos 358:")
for i, sw in enumerate(sw37):
    if 358 + i < len(transcript):
        tw = n(transcript[358 + i]["word"])
        status = "OK" if sw == tw else "MISMATCH"
        print(f"  {i}: sw={sw:15s} tw={tw:15s} {status}")

# Test S045
img45_text = "In 2011, anthropologist Kim Hill and his colleagues published a study in the journal Science, analyzing the social networks of the Ache and the Hadza, two hunter-gatherer popula"
sw45 = [n(w) for w in img45_text.split() if n(w)]
print(f"\nS045 words ({len(sw45)}): {sw45[:10]}...{sw45[-5:]}")

# Test S001
img1_text = "Right now, you are alone in a room."
sw1 = [n(w) for w in img1_text.split() if n(w)]
print(f"\nS001 words: {sw1}")
print(f"Transcript words 0-15:")
for i in range(0, min(16, len(transcript))):
    tw = transcript[i]["word"]
    print(f"  {i}: {tw:25s} n={n(tw):20s}")
