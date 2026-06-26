import os, sys

FFMPEG_PATHS = [
    r"C:\Program Files\Shutter Encoder\Library",
    r"C:\ffmpeg\bin",
    r"C:\Program Files\ffmpeg\bin",
]
for p in FFMPEG_PATHS:
    if os.path.isdir(p) and p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")

try:
    import whisperx
except ImportError:
    print("ERROR: whisperx not installed. Run setup.bat first.")
    sys.exit(1)

AUDIO_FILE = os.path.join(os.getcwd(), "audio.mp3")
OUTPUT_FILE = os.path.join(os.getcwd(), "transcript_words.txt")

device = "cpu"
batch_size = 16
compute_type = "float32"

print("=" * 50)
print(" WHISPERX WORD-LEVEL TRANSCRIPTION")
print("=" * 50)

if not os.path.exists(AUDIO_FILE):
    print(f"ERROR: '{AUDIO_FILE}' not found. Run generate_audio.bat first.")
    sys.exit(1)

print(f"Loading WhisperX model (base)...")
model = whisperx.load_model("base", device, compute_type=compute_type)

print(f"Transcribing {os.path.basename(AUDIO_FILE)}...")
audio = whisperx.load_audio(AUDIO_FILE)
result = model.transcribe(audio, batch_size=batch_size)

print(f"Aligning word-level timestamps...")
try:
    align_model, metadata = whisperx.load_align_model(language_code="en", device=device)
    result = whisperx.align(
        result["segments"], align_model, metadata,
        audio, device, return_char_alignments=False
    )
except Exception as e:
    print(f"Alignment skipped: {e}")

print(f"Saving word-level timestamps...")
word_count = 0
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("word\tstart_time\tend_time\n")
    for segment in result["segments"]:
        words = segment.get("words", [])
        if not words:
            start = segment.get("start", 0)
            end = segment.get("end", 0)
            text = segment.get("text", "").strip().lower()
            if text:
                for w in text.split():
                    f.write(f"{w}\t{start:.2f}\t{end:.2f}\n")
                    word_count += 1
        else:
            for word in words:
                word_text = word.get("word", "").strip().lower()
                if word_text:
                    f.write(f"{word_text}\t{word.get('start',0):.2f}\t{word.get('end',0):.2f}\n")
                    word_count += 1

total_duration = 0
if result["segments"]:
    total_duration = result["segments"][-1]["end"] - result["segments"][0]["start"]

print(f"\nDone! {word_count} words transcribed")
print(f"Output: {OUTPUT_FILE}")
print(f"Audio duration: {total_duration:.2f}s")
print()
