# YouTube Video Pipeline — Full Reference

## Overview

Script + numbered images → pause-aware sentence-level MP4 video with auto-appended outro card.

## Directory Structure

```
Desktop\youtube-videos-main\
├── new_video.bat          # Create fresh project folder with all batch files
├── setup.bat              # pip install whisperx, torch, edge-tts, Pillow
├── build_outro.bat        # Rebuild the outro MP4 (image + voiceover)
├── add_outro.bat          # Append outro to any video manually
├── REFERENCE.md           # This file
├── .gitignore
│
├── _tools\                # Shared scripts (delegated by project folder .bat files)
│   ├── generate_audio.bat   # edge-tts script.txt → audio.mp3
│   ├── transcribe.bat       # audio.mp3 → transcript_words.txt
│   ├── transcribe.py         # WhisperX word-level transcription
│   ├── ensure_images.bat    # Decision engine: real images or auto-draw
│   ├── draw_images.py       # Pillow stick-figure generator
│   ├── match_images.bat     # timeline.txt generation
│   ├── match_images.py      # Pause-based sentence grouping + image assignment
│   ├── render.bat           # output.mp4 rendering
│   ├── render.py            # FFmpeg segment rendering + concat
│   ├── add_outro.bat        # Append outro card to rendered video
│   ├── download_real_images.py
│   ├── generate_test_images.py
│   ├── gen_farming_images.py
│   ├── imagesprompts_generator.txt
│   ├── img_prompt_template.txt
│   ├── requirements.txt
│   └── watermark_mask.png
│
├── outro\                 # Outro card (voiceover + image)
│   ├── script.txt           # Text for the outro voiceover
│   ├── audio.mp3            # Generated voiceover
│   ├── 1. if you enjoyed...png  # Outro background image
│   └── outro.mp4            # Final rendered outro video
│
└── YYYY-MM-DD_HH-MM-SS-XXX\  # One project per `new_video.bat` run
    ├── script.txt
    ├── imagesprompts.txt
    ├── img\                 # Numbered images (1. sentence.png)
    ├── generate_audio.bat
    ├── transcribe.bat
    ├── ensure_images.bat
    ├── match_images.bat
    ├── render.bat
    ├── add_outro.bat        # Step 5: append outro to output.mp4
    ├── run_all.bat          # Full pipeline in one click
    ├── audio.mp3
    ├── transcript_words.txt
    ├── timeline.txt
    ├── debug_log.txt
    ├── output.mp4            # Final video with outro
    └── output_main.mp4       # Backup of video before outro was appended
```

## Full Pipeline (run_all.bat — 7 steps)

### Step 1 — Generate Audio
Reads `script.txt`, runs edge-tts voice `en-US-ChristopherNeural` at +10% speed → `audio.mp3`

### Step 2 — Transcribe
WhisperX (base model, CPU) transcribes the audio and aligns word-level timestamps → `transcript_words.txt`

### Step 3 — Remove Watermarks
IOPaint AI removes watermarks from images in `img-with-watermark\` → cleaned `img\`

### Step 4 — Ensure Images
- If `img\` has files → use them
- If `img\` is empty but `imagesprompts.txt` exists → auto-draw stick figure images
- If neither → error

### Step 5 — Match Images
Groups words by pauses (>= 0.4s gap), assigns one image per sentence group → `timeline.txt`

### Step 6 — Render
FFmpeg renders each image as a video segment, concatenates them, muxes with audio → `output.mp4`

### Step 7 — Add Outro
Appends `outro\outro.mp4` to the rendered video. Old `output.mp4` saved as `output_main.mp4`.

## Usage

```
new_video.bat           → creates a dated project folder
  ├── write script.txt  → one sentence per line
  ├── paste images into img\ or create imagesprompts.txt
  └── run_all.bat       → full pipeline: audio → render → outro
```

Rebuild the outro anytime: `build_outro.bat`
Append outro to any existing video: `add_outro.bat path\to\video.mp4`
