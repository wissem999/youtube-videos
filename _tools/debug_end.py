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
        transcript.append({"word": w.strip().lower(), "start": float(s), "end": float(e)})

print("Last 20 transcript words:")
for i in range(len(transcript) - 20, len(transcript)):
    w = transcript[i]
    print(f"  {i}: {w['word']:25s} start={w['start']:.2f} end={w['end']:.2f}")

# Also show where 542.35 is
print("\nWords around 542.35s:")
for i, w in enumerate(transcript):
    if 540 <= w["start"] <= 545:
        print(f"  {i}: {w['word']:25s} start={w['start']:.2f} end={w['end']:.2f}")

# Find the last word before 542.35
last_before = 0
for i, w in enumerate(transcript):
    if w["start"] < 542.35:
        last_before = i
print(f"\nLast word index before 542.35: {last_before}")
print(f"  {transcript[last_before]['word']:25s} start={transcript[last_before]['start']:.2f}")
