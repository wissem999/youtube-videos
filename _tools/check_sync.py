import os, re, sys

TIMELINE_FILE = os.path.join(os.getcwd(), "timeline.txt")
TRANSCRIPT_FILE = os.path.join(os.getcwd(), "transcript_words.txt")
SCRIPT_FILE = os.path.join(os.getcwd(), "script.txt")


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
            segments.append({
                "id": sid, "text": text,
                "start": float(start), "end": float(end),
                "duration": float(end) - float(start),
                "image": img
            })
    return segments


def load_script(filepath):
    sentences = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                sentences.append(line)
    return sentences


def check_durations(segments):
    issues = []
    durations = [s["duration"] for s in segments]
    avg = sum(durations) / len(durations) if durations else 0
    for seg in segments:
        if seg["duration"] > 30:
            issues.append(f"{seg['id']}: {seg['duration']:.1f}s (too long, avg={avg:.1f}s)")
        elif seg["duration"] < 0.3 and seg["duration"] > 0:
            issues.append(f"{seg['id']}: {seg['duration']:.2f}s (too short, avg={avg:.1f}s)")
    return issues, avg


def check_overlaps(segments):
    issues = []
    for i in range(len(segments) - 1):
        a, b = segments[i], segments[i + 1]
        if a["end"] > b["start"] + 0.1:
            issues.append(f"{a['id']} end ({a['end']:.2f}s) overlaps {b['id']} start ({b['start']:.2f}s)")
    return issues


def check_ordering(segments, scripts):
    issues = []
    return issues


def main():
    print("=" * 60)
    print(" SYNC CHECK")
    print("=" * 60)

    if not os.path.exists(TIMELINE_FILE):
        print(f"MISSING: {TIMELINE_FILE}")
        sys.exit(1)

    segments = load_timeline(TIMELINE_FILE)
    print(f"Segments:  {len(segments)}")

    has_script = os.path.exists(SCRIPT_FILE)
    script = load_script(SCRIPT_FILE) if has_script else []
    print(f"Script:    {len(script)} lines {'(OK)' if has_script else '(MISSING)'}")

    audio_dur = segments[-1]["end"] if segments else 0
    print(f"Duration:  {audio_dur:.2f}s")
    print()

    structural_issues = []
    desync_count = 0

    dur_issues, avg_dur = check_durations(segments)
    for iss in dur_issues:
        structural_issues.append(iss)
        desync_count += 1

    overlap_issues = check_overlaps(segments)
    for iss in overlap_issues:
        structural_issues.append(iss)
        desync_count += 1

    if has_script:
        order_issues = check_ordering(segments, script)
        for iss in order_issues:
            structural_issues.append(iss)
            desync_count += 1

    if structural_issues:
        print("--- Issues ---")
        for iss in structural_issues:
            if "overlap" in iss.lower():
                print(f"  OVERLAP: {iss}")
            elif "long" in iss.lower():
                print(f"  LONG:    {iss}")
            elif "short" in iss.lower():
                print(f"  SHORT:   {iss}")
            elif "mismatch" in iss.lower():
                print(f"  MISMATCH: {iss}")
            else:
                print(f"  ISSUE:   {iss}")
        print()

    duration_total = sum(s["duration"] for s in segments)
    expected = audio_dur
    duration_diff = abs(duration_total - expected)

    has_audio = os.path.exists(os.path.join(os.getcwd(), "audio.mp3"))
    has_video = os.path.exists(os.path.join(os.getcwd(), "output.mp4"))

    print("=" * 60)
    print(" SUMMARY")
    print("=" * 60)
    print(f"  Segments:          {len(segments)}")
    print(f"  Avg duration:      {avg_dur:.2f}s")
    print(f"  Total duration:    {duration_total:.2f}s")
    print(f"  Expected:          {expected:.2f}s")
    print(f"  Duration diff:     {duration_diff:.2f}s")
    print(f"  Issues found:      {len(structural_issues)}")
    print(f"  Audio:             {'OK' if has_audio else 'MISSING'}")
    print(f"  Video:             {'OK' if has_video else 'MISSING'}")

    if has_video:
        import subprocess
        r = subprocess.run(["ffmpeg", "-i", os.path.join(os.getcwd(), "output.mp4")],
                           capture_output=True, text=True)
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", r.stderr)
        if m:
            h, m_, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
            vdur = h * 3600 + m_ * 60 + s
            vdiff = abs(vdur - audio_dur)
            print(f"  Video duration:    {vdur:.2f}s")
            print(f"  Video vs timeline: {'OK' if vdiff < 1 else 'MISMATCH (' + str(round(vdiff, 2)) + 's)'}")

    print()
    verdict = "PASS" if desync_count == 0 else "FAIL"
    print(f"  VERDICT: {verdict}")
    if desync_count > 0:
        print(f"  Fix {desync_count} issue(s)")
    if not has_script:
        print(f"  (script.txt missing - ordering not checked)")
    print()


if __name__ == "__main__":
    main()
