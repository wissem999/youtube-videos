import os, re, sys

IMG_FOLDER = os.path.join(os.getcwd(), "img")
TRANSCRIPT_FILE = os.path.join(os.getcwd(), "transcript_words.txt")
SCRIPT_FILE = os.path.join(os.getcwd(), "script.txt")
OUTPUT_FILE = os.path.join(os.getcwd(), "timeline.txt")
DEBUG_FILE = os.path.join(os.getcwd(), "debug_log.txt")
PAUSE_THRESHOLD = 0.4


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


def load_script_sentences(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


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


def normalize(t):
    return re.sub(r"[^\w\s]", "", t).strip()


def group_words_by_pause(transcript_words):
    groups = []
    current = []
    for w in transcript_words:
        if not current:
            current.append(w)
        else:
            gap = w["start"] - current[-1]["end"]
            if gap > PAUSE_THRESHOLD:
                groups.append(current)
                current = [w]
            else:
                current.append(w)
    if current:
        groups.append(current)
    return groups


def assign_images_to_groups(groups, parsed_images):
    timeline = []
    n_groups = len(groups)
    n_images = len(parsed_images)
    for i, group in enumerate(groups):
        if i < n_images:
            num, text, fname = parsed_images[i]
        else:
            _, _, fname = parsed_images[-1]
            num = i + 1
            text = " ".join(w["word"] for w in group)
        start_time = group[0]["start"]
        if i + 1 < n_groups:
            end_time = groups[i + 1][0]["start"]
        else:
            end_time = group[-1]["end"]
        timeline.append({
            "sentence_id": f"S{num:03d}",
            "text": text,
            "start_time": start_time,
            "end_time": end_time,
            "image_file": fname
        })
    for i in range(n_groups, n_images):
        num, text, fname = parsed_images[i]
        start = timeline[-1]["end_time"] if timeline else 0
        timeline.append({
            "sentence_id": f"S{num:03d}",
            "text": text,
            "start_time": start,
            "end_time": start + 2.0,
            "image_file": fname
        })
    return timeline


def distribute_evenly(parsed_images, audio_duration):
    if not parsed_images or audio_duration <= 0:
        return []
    chunk = audio_duration / len(parsed_images)
    return [{
        "sentence_id": f"S{num:03d}",
        "text": text,
        "start_time": i * chunk,
        "end_time": (i + 1) * chunk,
        "image_file": fname
    } for i, (num, text, fname) in enumerate(parsed_images)]


def get_audio_duration():
    FFMPEG_PATHS = [
        r"C:\Program Files\Shutter Encoder\Library",
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin",
        os.path.join(os.path.dirname(sys.executable)),
        os.path.join(os.path.dirname(sys.executable), "Scripts"),
    ]
    import subprocess
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
                        import re
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


def write_timeline(timeline, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("sentence_id\ttext\tstart_time\tend_time\timage_file\n")
        for e in timeline:
            f.write(f"{e['sentence_id']}\t{e['text']}\t{e['start_time']:.2f}\t{e['end_time']:.2f}\t{e['image_file']}\n")


def write_debug_log(timeline, transcript_words, groups):
    with open(DEBUG_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n DEBUG LOG\n" + "=" * 60 + "\n\n")
        f.write("PAUSES:\n")
        for i in range(len(transcript_words) - 1):
            gap = transcript_words[i + 1]["start"] - transcript_words[i]["end"]
            if gap > PAUSE_THRESHOLD:
                f.write(f"  {transcript_words[i]['end']:.2f}s -> {transcript_words[i+1]['start']:.2f}s ({gap:.2f}s)\n")
        f.write("\nGROUPS:\n")
        for i, g in enumerate(groups):
            txt = " ".join(w["word"] for w in g)
            f.write(f"  {i+1}: {g[0]['start']:.2f}s - {g[-1]['end']:.2f}s => {txt}\n")
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
        print(f"ERROR: '{TRANSCRIPT_FILE}' not found. Run transcribe.bat first.")
        sys.exit(1)

    transcript = load_transcript(TRANSCRIPT_FILE)
    print(f"Transcript: {len(transcript)} words")

    images = load_images(IMG_FOLDER)
    print(f"Images:     {len(images)} found")

    parsed = [parse_image_name(img) for img in images]
    parsed.sort(key=lambda x: x[0])

    script_sentences = load_script_sentences(SCRIPT_FILE)
    if script_sentences:
        print(f"Script:     {len(script_sentences)} lines")

    print(f"\nDetecting sentences by pause (>={PAUSE_THRESHOLD}s)...")
    groups = group_words_by_pause(transcript)
    print(f"Found {len(groups)} sentence groups")

    timeline = []
    if groups and parsed:
        print(f"Assigning {len(parsed)} images to {len(groups)} groups...")
        timeline = assign_images_to_groups(groups, parsed)
    else:
        print("FALLBACK: even distribution")
        timeline = distribute_evenly(parsed, get_audio_duration())

    if not timeline:
        print("ERROR: No timeline segments!")
        sys.exit(1)

    write_timeline(timeline, OUTPUT_FILE)
    write_debug_log(timeline, transcript, groups)

    print(f"\n{'='*50}")
    print(" FINAL TIMELINE")
    print(f"{'='*50}")
    for e in timeline:
        d = e["end_time"] - e["start_time"]
        print(f"  {e['sentence_id']} | {e['start_time']:6.2f}s -> {e['end_time']:6.2f}s ({d:.2f}s) | {e['image_file']}")

    print(f"\nSegments: {len(timeline)}")
    if timeline:
        print(f"Duration: {timeline[-1]['end_time']:.2f}s")
    print(f"Output:   {OUTPUT_FILE}")
    print()


if __name__ == "__main__":
    main()
