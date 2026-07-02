import os, re, sys, subprocess

IMG_FOLDER = os.path.join(os.getcwd(), "img")
TRANSCRIPT_FILE = os.path.join(os.getcwd(), "transcript_words.txt")
SCRIPT_FILE = os.path.join(os.getcwd(), "script.txt")
OUTPUT_FILE = os.path.join(os.getcwd(), "timeline.txt")
DEBUG_FILE = os.path.join(os.getcwd(), "debug_log.txt")


def n(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def load_transcript(filepath):
    words = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
    header = True
    for line in lines:
        if header and line.startswith("word"):
            header = False
            continue
        parts = line.strip().split("\t")
        if len(parts) == 3:
            w, s, e = parts
            words.append({"word": w.strip().lower(), "start": float(s), "end": float(e)})
    return words


def load_images(folder):
    images = []
    if not os.path.isdir(folder):
        print(f"ERROR: img folder not found: {folder}")
        return images
    for fname in sorted(os.listdir(folder)):
        if fname.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            images.append(fname)
    return images


def parse_image_name(fname):
    name = os.path.splitext(fname)[0]
    m = re.match(r"^(\d+)[.\-_\s]*(.*)", name)
    if m:
        return int(m.group(1)), m.group(2).strip().lower(), fname
    return 999, name.lower(), fname


def get_audio_duration():
    FFMPEG_PATHS = [
        r"C:\Program Files\Shutter Encoder\Library",
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        os.path.join(os.path.dirname(sys.executable)),
        os.path.join(os.path.dirname(sys.executable), "Scripts"),
    ]
    for p in FFMPEG_PATHS:
        if os.path.isdir(p) and p not in os.environ.get("PATH", ""):
            os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
    try:
        for fname in ["audio.mp3", "output.mp3"]:
            path = os.path.join(os.getcwd(), fname)
            if os.path.exists(path):
                r = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=noprint_wrappers=1:nokey=1", path],
                    capture_output=True, text=True, timeout=10
                )
                if r.returncode == 0 and r.stdout.strip():
                    return float(r.stdout.strip())
    except:
        pass
    try:
        for fname in ["audio.mp3", "output.mp3"]:
            path = os.path.join(os.getcwd(), fname)
            if os.path.exists(path):
                r = subprocess.run(
                    ["ffmpeg", "-i", path, "-f", "null", "-",
                     "-loglevel", "error", "-stats"],
                    capture_output=True, text=True, timeout=10
                )
                for line in r.stderr.split("\n"):
                    if "time=" in line:
                        m = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                        if m:
                            h, m_, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
                            return h * 3600 + m_ * 60 + s
    except:
        pass
    for fname in ["audio.mp3", "output.mp3"]:
        path = os.path.join(os.getcwd(), fname)
        if os.path.exists(path):
            return os.path.getsize(path) / 20000
    return 60.0


SHORT_WORDS = set(n(w) for w in ["a", "an", "in", "on", "at", "to", "of", "is", "it",
                                 "or", "as", "by", "up", "if", "be", "no", "so", "do",
                                 "he", "we", "my", "me", "us", "go", "your", "you",
                                 "its", "his", "her", "our", "the", "and", "not",
                                 "was", "had", "but", "for", "are", "can", "all",
                                 "had", "has", "now", "than", "did", "get", "out",
                                 "way", "say", "who", "why", "how", "any", "own",
                                 "see", "new", "two", "may", "too", "very", "just",
                                 "that", "this", "what", "which", "with", "from",
                                 "they", "them", "been", "some", "each", "when",
                                 "more", "also", "into", "over", "such", "only",
                                 "like", "even", "than", "then", "well", "here",
                                 "there", "after", "still", "about", "because",
                                 "people", "something", "between", "without"])


def words_match(sw, tw):
    if sw == tw:
        return True
    if sw in SHORT_WORDS or tw in SHORT_WORDS:
        return False
    if len(sw) >= 3 and len(tw) >= 3 and (sw.startswith(tw) or tw.startswith(sw)):
        return True
    return False


def get_meaningful(sentence_words):
    meaningful = [w for w in sentence_words if len(w) >= 3 and w not in SHORT_WORDS]
    if not meaningful:
        meaningful = sentence_words
    return meaningful


def find_nearest_word(transcript_words, target_time, min_pos):
    for pos in range(min_pos, len(transcript_words)):
        if transcript_words[pos]["start"] >= target_time:
            return pos
    return len(transcript_words) - 1


def find_first_match(sentence_words, transcript_words, start_pos, end_pos):
    if not sentence_words or start_pos >= len(transcript_words):
        return -1, -1
    end_pos = min(end_pos, len(transcript_words))
    meaningful = get_meaningful(sentence_words)
    if not meaningful:
        return -1, -1
    for pos in range(start_pos, end_pos):
        tw = n(transcript_words[pos]["word"])
        for sw in meaningful:
            if sw == tw or words_match(sw, tw):
                window = max(len(meaningful) * 3, 10)
                end = min(pos + window, len(transcript_words))
                score = 0
                for j in range(pos, end):
                    tw2 = n(transcript_words[j]["word"])
                    for sw2 in meaningful:
                        if sw2 == tw2 or words_match(sw2, tw2):
                            score += 1
                            break
                return pos, score
    return -1, -1


def match_sentences(parsed_images, transcript_words, audio_dur):
    n_images = len(parsed_images)
    n_words = len(transcript_words)
    positions = [0] * n_images
    scores = [0] * n_images
    ti = 0

    for i in range(n_images):
        s_words = [n(w) for w in parsed_images[i][1].split() if n(w)]
        if not s_words:
            positions[i] = ti
            scores[i] = 0
            continue

        meaningful = get_meaningful(s_words)
        if not meaningful:
            meaningful = s_words

        found = -1
        score = 0
        while ti < n_words:
            tw = n(transcript_words[ti]["word"])
            for sw in meaningful:
                if sw == tw or words_match(sw, tw):
                    found = ti
                    score = 1
                    remaining = [w for w in meaningful if w != sw]
                    for j in range(ti + 1, min(ti + max(len(meaningful) * 3, 15), n_words)):
                        tw2 = n(transcript_words[j]["word"])
                        for rw in remaining[:]:
                            if rw == tw2 or words_match(rw, tw2):
                                score += 1
                                remaining.remove(rw)
                    break
            if found >= 0:
                break
            ti += 1

        if found >= 0:
            positions[i] = found
            scores[i] = score
            ti = found + 1
        else:
            positions[i] = min(ti, n_words - 1)
            scores[i] = 0
            ti += 1

    return positions, scores


def write_timeline(timeline, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("sentence_id\ttext\tstart_time\tend_time\timage_file\n")
        for e in timeline:
            f.write(f"{e['sentence_id']}\t{e['text']}\t{e['start_time']:.2f}\t{e['end_time']:.2f}\t{e['image_file']}\n")


def write_debug_log(timeline, transcript_words, positions, scores):
    with open(DEBUG_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n DEBUG LOG\n" + "=" * 60 + "\n\n")
        f.write("MATCH POSITIONS:\n")
        for e in timeline:
            pass
        f.write("\nPER-IMAGE MATCH:\n")
        for i, e in enumerate(timeline):
            num = int(e["sentence_id"][1:])
            pos = positions[i] if i < len(positions) else 0
            sc = scores[i] if i < len(scores) else 0
            f.write(f"  S{num:03d}: pos={pos:4d} score={sc:5.1f} start={e['start_time']:.2f}s | {e['image_file'][:40]}\n")

        f.write("\nTIMELINE:\n")
        for e in timeline:
            d = e["end_time"] - e["start_time"]
            f.write(f"  {e['sentence_id']}: {e['start_time']:.2f}s - {e['end_time']:.2f}s ({d:.2f}s) | {e['image_file'][:40]}\n")

        f.write(f"\nSegments: {len(timeline)}\n")
        if timeline:
            f.write(f"Duration: {timeline[-1]['end_time']:.2f}s\n")


def main():
    print("=" * 50)
    print(" MATCHING IMAGES TO TRANSCRIPT")
    print("=" * 50 + "\n")

    if not os.path.exists(TRANSCRIPT_FILE):
        print(f"ERROR: '{TRANSCRIPT_FILE}' not found.")
        sys.exit(1)

    transcript = load_transcript(TRANSCRIPT_FILE)
    print(f"Transcript: {len(transcript)} words")

    images = load_images(IMG_FOLDER)
    print(f"Images:     {len(images)} found")

    parsed = [parse_image_name(img) for img in images]
    parsed.sort(key=lambda x: x[0])
    print(f"Parsed {len(parsed)} images (sorted)")

    audio_dur = get_audio_duration()

    print(f"\nMatching sentences to transcript positions...")
    positions, scores = match_sentences(parsed, transcript, audio_dur)

    nz = sum(1 for s in scores if s > 0)
    print(f"Match scores: min={min(scores):.1f}, max={max(scores):.1f}, avg={sum(scores)/len(scores):.1f}, nonzero={nz}/{len(scores)}")

    timeline = []
    for i, (num, text, fname) in enumerate(parsed):
        start_time = transcript[positions[i]]["start"]
        if i + 1 < len(parsed):
            np = positions[i + 1]
            if np <= positions[i]:
                np = positions[i] + 1
            end_time = transcript[min(np, len(transcript) - 1)]["start"]
        else:
            end_time = audio_dur

        if start_time >= audio_dur:
            start_time = audio_dur
            end_time = audio_dur
        else:
            if end_time > audio_dur:
                end_time = audio_dur
            if end_time <= start_time:
                end_time = min(start_time + 1.5, audio_dur)

        timeline.append({
            "sentence_id": f"S{num:03d}",
            "text": text[0].upper() + text[1:] if text else text,
            "start_time": start_time,
            "end_time": end_time,
            "image_file": fname
        })

    if timeline:
        timeline[0]["start_time"] = 0.0

    for i in range(1, len(timeline)):
        prev = timeline[i - 1]
        curr = timeline[i]
        if curr["start_time"] <= prev["start_time"]:
            curr["start_time"] = prev["end_time"]
        if curr["end_time"] <= curr["start_time"]:
            curr["end_time"] = min(curr["start_time"] + 0.5, audio_dur)
        if prev["end_time"] > curr["start_time"]:
            prev["end_time"] = curr["start_time"]

    MIN_DUR = 1.0
    for i in range(len(timeline)):
        dur = timeline[i]["end_time"] - timeline[i]["start_time"]
        if dur < MIN_DUR:
            shortage = MIN_DUR - dur
            new_end = min(timeline[i]["end_time"] + shortage, audio_dur)
            timeline[i]["end_time"] = new_end
            if i + 1 < len(timeline) and timeline[i + 1]["start_time"] < new_end:
                timeline[i + 1]["start_time"] = new_end

    write_timeline(timeline, OUTPUT_FILE)
    write_debug_log(timeline, transcript, positions, scores)

    print(f"\n{'='*50}")
    print(" FINAL TIMELINE")
    print(f"{'='*50}")
    for e in timeline[:10]:
        d = e["end_time"] - e["start_time"]
        print(f"  {e['sentence_id']} | {e['start_time']:6.2f}s -> {e['end_time']:6.2f}s ({d:.2f}s) | {e['image_file']}")
    if len(timeline) > 10:
        print(f"  ... ({len(timeline) - 10} more)")
        for e in timeline[-3:]:
            d = e["end_time"] - e["start_time"]
            print(f"  {e['sentence_id']} | {e['start_time']:6.2f}s -> {e['end_time']:6.2f}s ({d:.2f}s) | {e['image_file']}")

    print(f"\nSegments: {len(timeline)}")
    if timeline:
        print(f"Duration: {timeline[-1]['end_time']:.2f}s")
    print(f"Output:   {OUTPUT_FILE}")
    print()


if __name__ == "__main__":
    main()
