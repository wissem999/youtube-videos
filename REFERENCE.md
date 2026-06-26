# YouTube Video Pipeline — Full Reference

## Overview

Script + numbered images → pause-aware sentence-level MP4 video with zero black frames. Two image paths: auto-draw (Pillow stick figures) or real downloaded images.

## Directory Structure

```
Desktop\youtube videos\
├── new_video.bat          # Create fresh project folder
├── setup.bat              # pip install whisperx, torch, edge-tts, Pillow
├── .gitignore             # Ignores __pycache__, *.mp3, *.mp4, *.wav
├── REFERENCE.md           # This file
│
├── _tools\                # Shared scripts (delegated by project folder .bat files)
│   ├── generate_audio.bat   # Step 1: edge-tts script.txt → audio.mp3
│   ├── transcribe.bat       # Step 2: audio.mp3 → transcript_words.txt
│   ├── transcribe.py         # WhisperX word-level transcription
│   ├── ensure_images.bat    # Step 2b: decision engine (images vs prompts)
│   ├── draw_images.py       # Pillow stick-figure generator from prompt blocks
│   ├── match_images.bat     # Step 3: timeline.txt generation
│   ├── match_images.py      # Pause-based sentence grouping + image assignment
│   ├── render.bat           # Step 4: output.mp4 rendering
│   ├── render.py            # FFmpeg segment rendering + concat
│   ├── download_real_images.py  # Download real photos from Flickr/Picsum
│   ├── generate_test_images.py  # Legacy — 6 hand-drawn test images
│   ├── gen_farming_images.py    # Legacy — farming-themed test images
│   ├── imagesprompts_generator.txt  # Claude prompt to generate imagesprompts.txt
│   ├── img_prompt_template.txt  # Short format reference
│   └── requirements.txt        # whisperx, torch, torchaudio, edge-tts
│
├── YYYY-MM-DD_HH-MM-SS-XXX\  # One per `new_video.bat` run
│   ├── script.txt           # Voiceover script (one sentence per line)
│   ├── imagesprompts.txt    # `1. text` → blank line → IMAGE PROMPT → blank line → repeat
│   ├── img\                 # Image files: `1. exact text.png` or `.jpg`
│   ├── generate_audio.bat   # Delegates to _tools\
│   ├── transcribe.bat
│   ├── ensure_images.bat
│   ├── match_images.bat
│   ├── render.bat
│   ├── run_all.bat          # Full pipeline in one click
│   ├── audio.mp3            # Generated (gitignored)
│   ├── transcript_words.txt  # Word: start_time, end_time (tab-separated)
│   ├── timeline.txt         # sentence_id, text, start, end, image_file (tab-separated)
│   ├── debug_log.txt        # Pause boundaries + group details
│   └── output.mp4           # Final video (gitignored)
│
├── TEST-*/                 # Test outputs (may contain stale data)
└── 2026-06-26_03-44-59-683/ # Latest test run
```

## Key Constraints

- **Windows filenames forbid `:`** → image files use `1. text.png` (dot + space), NOT `1: text.png`
- `imagesprompts.txt` can use `1. text` or `1: text` or `1 - text` etc — the code strips any leading `^\d+[.\-_\s:]*` prefix
- FFmpeg path: `C:\Program Files\Shutter Encoder\Library\ffmpeg.exe` (injected into PATH by Python scripts)
- Python 3.11.9, WhisperX CPU-only (no GPU), torchcodec warning is harmless
- Voice: edge-tts `en-US-ChristopherNeural`

## Pipeline (run_all.bat)

### Step 1: Generate Audio
- `generate_audio.bat` reads `script.txt`, runs edge-tts → `audio.mp3`
- Falls back to `C:\Users\bayou\Desktop\voice_over\generate.bat` if edge-tts not in PATH

### Step 2: Transcribe
- `transcribe.bat` → `transcribe.py`: loads WhisperX base model (CPU), transcribes audio, aligns word-level timestamps
- Output: `transcript_words.txt` tab-separated `word\tstart_time\tend_time`

### Step 2b: Ensure Images (decision engine)
`ensure_images.bat` logic:

| img/ has files? | imagesprompts.txt exists? | Action |
|---|---|---|
| Yes | — | Use real images (best quality) |
| No | Yes | Call `draw_images.py` to auto-generate |
| No | No | Show error message, stop |

### Step 3: Match Images
`match_images.py`:
1. Load transcript words
2. Group words by pause threshold (>= 0.4s gap) → sentence groups
3. List images in `img/`, parse number prefix from filename for sorting
4. Assign images to groups in order (1 image per group)
5. **end_time per image = next sentence start_time** (image covers pauses, hard cut at next start)
6. Write `timeline.txt` tab-separated

Edge cases:
- **More images than groups**: extra images get 2.0s default duration, appended after last group
- **Fewer images than groups**: only first N groups get images, video shorter than audio
- **No groups**: even distribution across audio duration

### Step 4: Render
`render.py`:
1. Read `timeline.txt` segments
2. For each segment: FFmpeg `-loop 1 -i image -t duration` → `.ts` segment (1920×1080, yuv420p, 24fps)
3. Concat segments with FFmpeg concat demuxer
4. Mux with audio (`-shortest`)
5. Output: `output.mp4`

## Image Naming Convention

**Filename format**: `N. EXACT SENTENCE TEXT.png` (or `.jpg`)

Where `N` starts at 1, dot + space after number, then the EXACT sentence text (verbatim).

The `parse_image_name` function in `match_images.py:47` uses regex `r"^(\d+)[.\-_\s]*(.*)"` to extract the number and text from any filename.

**Accepted separator variants**: `.` (dot), `-` (dash), `_` (underscore), `:` (colon — for input format only, Windows can't save `:` in filenames), whitespace

## `imagesprompts.txt` Format

Paired blocks separated by a blank line:

```
1. EXACT SCRIPT TEXT (verbatim from script)

IMAGE PROMPT (description for auto-draw)

2. NEXT SCRIPT TEXT

IMAGE PROMPT

...
```

`draw_images.py:170` strips `^\d+[.\-_\s:]*` prefix before constructing filename as `{i+1}. {clean_text}.png`.

## Auto-Draw Templates (`draw_images.py`)

Keyword-based template matching (`match_template` function):

| Keywords | Template Function | Visual |
|---|---|---|
| shock, mistake, surprise, wrong, error | `t_shock` | Shocked figure, "A MISTAKE" text |
| walk, wheat, path, journey, ancestor, past, field | `t_walk` | Figure walking past wheat, sun rays |
| relax, rest, sleep, 15 hour, speech, bubble, free time, play | `t_relax` | Relaxed figure, speech bubble |
| harvest, work, hunt, plant, cook, build, grind, collect | `t_harvest` | Figure with wheat, harvesting |
| vs, comparison, versus, mutation, change, evolution, different | `t_vs` | Split screen BAD vs GOOD |
| spill, scatter, shrug, accident, drop, fall, seed | `t_spill` | Figure with scattered seeds, "ACCIDENT" |
| crowd, row, group, army, mass, identical, many, village | `t_crowd` | Grid of small figures |
| think, thought, brain, mind, idea, question, philosophy | `t_think` | Figure with thought bubble "?" |
| (no match) | `t_gen` | Generic stick figure + first 6 words as text |

All templates draw on 1920×1080 white background with brown ground strip at bottom.

## Download Real Images (`download_real_images.py`)

Downloads from Flickr (`loremflickr.com`) with Picsum fallback. Crops to 1920×1080 center. 6 hardcoded queries. Falls back to colored placeholder if download fails.

## Claude Prompt (`imagesprompts_generator.txt`)

Located at `_tools\imagesprompts_generator.txt` and `Desktop\imagesprompts_generator.txt`.

Gives Claude strict instructions to output `1. EXACT SCRIPT TEXT` then blank line then IMAGE PROMPT. Enforces stick-figure style, flat colors, no gradients, simple composition.

## Test Results Summary

| Test | Scenario | Result |
|---|---|---|
| 1 | Empty `img/` + `imagesprompts.txt` | Auto-draw 4 images → 13.08s video |
| 2 | 4 real JPGs in `img/`, no prompts | Uses real images → 13.08s video (1.2MB) |
| 3 | Both images + prompts | "Using your images" — ignores prompts |
| 4 | Neither images nor prompts | Error message, pipeline stops |
| 5 | 2 images for 4 sentences | First 2 sentences only, video 7.88s < audio 13s |

## New PC Setup

1. Install Git, Python 3.11, FFmpeg (Shutter Encoder or manual)
2. `cd Desktop && git clone https://github.com/wissem999/youtube-videos.git`
3. `setup.bat` (pip installs dependencies)
4. Update FFmpeg path in `_tools\render.py` and `_tools\match_images.py` if different
5. `new_video.bat` → write `script.txt` → paste Claude output into `imagesprompts.txt` → `run_all.bat`

## GitHub

- Remote: `https://github.com/wissem999/youtube-videos` (private)
- Auth: GitHub CLI (`gh.exe`) installed via winget, authenticated as wissem999
