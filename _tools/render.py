import os, subprocess, sys, shutil

FFMPEG_PATHS = [
    r"C:\Program Files\Shutter Encoder\Library",
    r"C:\ffmpeg\bin",
    r"C:\Program Files\ffmpeg\bin",
    os.path.join(os.path.dirname(sys.executable)),
    os.path.join(os.path.dirname(sys.executable), "Scripts"),
    r"C:\Users\LITE\AppData\Local\Programs\Python\Python313",
]
for p in FFMPEG_PATHS:
    if os.path.isdir(p) and p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")

TIMELINE_FILE = os.path.join(os.getcwd(), "timeline.txt")
AUDIO_FILE = os.path.join(os.getcwd(), "audio.mp3")
OUTPUT_FILE = os.path.join(os.getcwd(), "output.mp4")
IMG_FOLDER = os.path.join(os.getcwd(), "img")
TEMP_FOLDER = os.path.join(os.getcwd(), "_temp_segments")
RESOLUTION = "1920:1080"
FPS = 24


def load_timeline(filepath):
    segments = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
    header = True
    for line in lines:
        if header and line.startswith("sentence_id"):
            header = False
            continue
        parts = line.strip().split("\t")
        if len(parts) == 5:
            sid, text, start, end, img = parts
            duration = float(end) - float(start)
            if duration < 0.1:
                duration = 0.5
            segments.append({
                "id": sid, "text": text,
                "start": float(start), "end": float(end),
                "duration": duration, "image": img
            })
    return segments


def find_image_path(fname):
    path = os.path.join(IMG_FOLDER, fname)
    if os.path.exists(path):
        return path
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        base = os.path.splitext(fname)[0]
        p2 = os.path.join(IMG_FOLDER, base + ext)
        if os.path.exists(p2):
            return p2
    return None


def pad_first_segment(segments):
    if not segments or segments[0]["start"] <= 0:
        return segments
    pad = {"id": "PAD", "text": "", "start": 0.0,
           "end": segments[0]["start"],
           "duration": segments[0]["start"], "image": segments[0]["image"]}
    return [pad] + segments


def make_segment_videos(segments):
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    seg_files = []
    for i, seg in enumerate(segments):
        img_path = find_image_path(seg["image"])
        if not img_path:
            print(f"  WARNING: Image missing: {seg['image']}, using placeholder")
            img_path = os.path.join(TEMP_FOLDER, "_blank.png")
            if not os.path.exists(img_path):
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=black:s={RESOLUTION}:d=1",
                     "-frames:v", "1", img_path],
                    capture_output=True
                )

        out_file = os.path.join(TEMP_FOLDER, f"seg{i:04d}.ts")
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_path,
            "-c:v", "libx264",
            "-t", f"{seg['duration']:.3f}",
            "-pix_fmt", "yuv420p",
            "-vf", f"scale={RESOLUTION}:force_original_aspect_ratio=decrease,pad={RESOLUTION}:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-r", str(FPS),
            "-preset", "medium", "-crf", "23",
            "-an", out_file
        ]
        print(f"  Seg {i+1}/{len(segments)}: {seg['id']} ({seg['duration']:.2f}s)")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  FFmpeg error: {r.stderr[:200]}")
            return None
        seg_files.append(out_file)
    return seg_files


def concat_videos(seg_files, audio_file, output_file):
    concat_txt = os.path.join(TEMP_FOLDER, "concat_list.txt")
    with open(concat_txt, "w") as f:
        for sf in seg_files:
            f.write(f"file '{os.path.basename(sf)}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", audio_file,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-map", "0:v:0", "-map", "1:a:0",
        "-shortest", output_file
    ]
    print("Concatenating with audio...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FFmpeg error: {r.stderr[:300]}")
        return False
    return True


def get_video_duration(filepath):
    r = subprocess.run(
        ["ffmpeg", "-i", filepath],
        capture_output=True, text=True
    )
    import re
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", r.stderr)
    if m:
        h, m_, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
        return h * 3600 + m_ * 60 + s
    return 0.0


def cleanup():
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)


def main():
    print("=" * 50)
    print(" RENDERING FINAL VIDEO")
    print("=" * 50)

    if not os.path.exists(TIMELINE_FILE):
        print(f"ERROR: '{TIMELINE_FILE}' not found.")
        sys.exit(1)

    audio_path = AUDIO_FILE
    if not os.path.exists(audio_path):
        alt = os.path.join(os.getcwd(), "output.mp3")
        if os.path.exists(alt):
            audio_path = alt
        else:
            print("ERROR: No audio file found.")
            sys.exit(1)

    segments = load_timeline(TIMELINE_FILE)
    print(f"Loaded {len(segments)} segments")
    print(f"Total duration: {sum(s['duration'] for s in segments):.2f}s")

    missing = sum(1 for s in segments if not find_image_path(s["image"]))
    if missing:
        print(f"WARNING: {missing} images missing, placeholders used")
    else:
        print("All images found!")

    segments = pad_first_segment(segments)
    print(f"After padding: {len(segments)} segments (start at {segments[0]['start']}s)")

    print("\nRendering segments...")
    seg_files = make_segment_videos(segments)
    if not seg_files:
        cleanup()
        sys.exit(1)

    if concat_videos(seg_files, audio_path, OUTPUT_FILE):
        d = get_video_duration(OUTPUT_FILE)
        print(f"\n{'='*50}")
        print(f" SUCCESS! output.mp4 created")
        print(f" Duration: {d:.2f}s | Resolution: {RESOLUTION}")
        print(f"{'='*50}")
    else:
        print("ERROR: Render failed")
        cleanup()
        sys.exit(1)

    cleanup()


if __name__ == "__main__":
    main()
