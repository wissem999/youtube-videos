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

test_sentences = [
    "Right now, you are alone in a room.",
    "The phone in your hand is glowing.",
    "Outside, millions of people move through their own evenings, behind their own doors, in their own quiet.",
    "It looks nothing like the one you are living in right now.",
    "In 1992, Oxford anthropologist Robin Dunbar compared the brain sizes of primates to the size of their social groups.",
    "This is normal.",
    "Not once.",
    "He found a pattern.",
    "In 2011, anthropologist Kim Hill and his colleagues published a study in the journal Science, analyzing the social networks of the Ache and the Hadza, two hunter-gatherer popula",
    "It happened because nearly every modern convenience was optimized for efficiency, privacy, and independence \u2014 three values your ancestors\u2019 biology never had to negotiate, becau",
    "And somewhere underneath your glowing phone, in the quiet of an ordinary Tuesday, that ancient alarm is still doing the only job it has ever known how to do_ trying, in the dar",
]

for idx, text in enumerate(test_sentences):
    s_words = [n(w) for w in text.split() if n(w)]
    total = len(transcript)
    n_img = 125
    est = round(idx * total / n_img)
    margin = 300
    search_start = max(0, est - margin)
    search_end = min(total, est + margin + 1)

    best_score = -1
    best_pos = search_start
    for pos in range(search_start, search_end):
        if n(transcript[pos]["word"]) != s_words[0]:
            continue
        check_len = min(30, len(s_words), len(transcript) - pos)
        score = 0
        for i in range(check_len):
            sw = s_words[i]
            tw = n(transcript[pos + i]["word"])
            if sw == tw:
                score += 1
            elif i == len(s_words) - 1 and (tw.startswith(sw) or sw.startswith(tw)):
                score += 0.8
        if score > best_score:
            best_score = score
            best_pos = pos

    actual_word = transcript[best_pos]["word"] if best_pos < len(transcript) else "???"
    print(f"S{idx+1:3d}: est={est:4d} best_pos={best_pos:4d} score={best_score:5.1f} first_word={actual_word:20s} text={text[:50]}")
