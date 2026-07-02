import os, sys, asyncio, subprocess

SCRIPT_FILE = os.path.join(os.getcwd(), "script.txt")
AUDIO_FILE = os.path.join(os.getcwd(), "audio.mp3")
TRANSCRIPT_FILE = os.path.join(os.getcwd(), "transcript_words.txt")


async def generate():
    if not os.path.exists(SCRIPT_FILE):
        print(f"ERROR: {SCRIPT_FILE} not found")
        sys.exit(1)

    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("ERROR: script.txt is empty")
        sys.exit(1)

    print(f"Generating audio from script.txt ({len(text)} chars)...")
    import edge_tts

    communicate = edge_tts.Communicate(
        text,
        "en-US-ChristopherNeural",
        rate="+10%",
        boundary="WordBoundary"
    )

    audio_data = bytearray()
    words = []

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            offset = chunk["offset"] / 10_000_000
            duration = chunk["duration"] / 10_000_000
            words.append({
                "word": chunk["text"].strip(),
                "start": offset,
                "end": offset + duration
            })

    with open(AUDIO_FILE, "wb") as f:
        f.write(audio_data)

    with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as f:
        f.write("word\tstart_time\tend_time\n")
        for w in words:
            f.write(f"{w['word']}\t{w['start']:.2f}\t{w['end']:.2f}\n")

    audio_size = os.path.getsize(AUDIO_FILE)
    audio_dur = words[-1]["end"] if words else 0
    print(f"Audio:  {AUDIO_FILE} ({audio_size} bytes, {audio_dur:.2f}s)")
    print(f"Words:  {len(words)} timestamped")
    print(f"Output: {TRANSCRIPT_FILE}")


if __name__ == "__main__":
    asyncio.run(generate())
