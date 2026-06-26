from PIL import Image, ImageDraw, ImageFont
import os, re, sys

IMG_DIR = os.path.join(os.getcwd(), "img")
SCRIPT_FILE = os.path.join(os.getcwd(), "script.txt")
PROMPT_FILE = os.path.join(os.getcwd(), "imagesprompts.txt")
W, H = 1920, 1080
GROUND = (139, 94, 60)


def sf(d, x, y, s=1.0, c=(0,0,0), w=4, aa=0, la=0, arm_up=0):
    hr = int(40 * s)
    bl = int(120 * s)
    al = int(60 * s)
    ll = int(70 * s)
    d.ellipse([x-hr, y, x+hr, y+hr*2], outline=c, width=w)
    d.ellipse([x-3, y+int(25*s), x+3, y+int(31*s)], fill=c)
    d.line([x, y+hr*2, x, y+hr*2+bl], fill=c, width=w)
    if arm_up:
        d.line([x, y+hr*2+int(40*s), x-al, y+hr*2+int(40*s)+aa-arm_up], fill=c, width=w)
        d.line([x, y+hr*2+int(40*s), x+al, y+hr*2+int(40*s)-aa-arm_up], fill=c, width=w)
    else:
        d.line([x, y+hr*2+int(40*s), x-al, y+hr*2+int(40*s)+aa], fill=c, width=w)
        d.line([x, y+hr*2+int(40*s), x+al, y+hr*2+int(40*s)-aa], fill=c, width=w)
    d.line([x, y+hr*2+bl, x-ll, y+hr*2+bl+ll+la], fill=c, width=w)
    d.line([x, y+hr*2+bl, x+ll, y+hr*2+bl+ll-la], fill=c, width=w)
    return (x, y+hr*2+bl+ll)


def tc(d, text, y, size=60, color=(0,0,0)):
    try: font = ImageFont.truetype("arial.ttf", size)
    except: font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), text, font=font)
    d.text(((W - (bbox[2]-bbox[0])) // 2, y), text, fill=color, font=font)


def tx(d, text, x, y, size=40, color=(0,0,0)):
    try: font = ImageFont.truetype("arial.ttf", size)
    except: font = ImageFont.load_default()
    d.text((x, y), text, fill=color, font=font)


def new_canvas():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, H-80, W, H], fill=GROUND)
    return img, d


def draw_wheat(d, cx, by, count=3):
    off = (count-1)*100
    for i in range(count):
        wx = cx - off + i*200
        d.line([wx, by, wx, by-270], fill=(0, 100, 0), width=3)
        d.ellipse([wx-12, by-290, wx+12, by-260], fill=(200, 150, 0), outline=(0,0,0), width=2)


# ── TEMPLATES ──────────────────────────────────────────

def tmpl_shock(d, prompt, sentence):
    sf(d, W//2, H-80-280, 1.3, (0,0,0), 5, aa=20, arm_up=40)
    tc(d, '"A MISTAKE"', 100, 80, (0,0,0))
    d.line([W//2-200, 220, W//2+200, 220], fill=(0,0,0), width=2)

def tmpl_walking(d, prompt, sentence):
    draw_wheat(d, 600, H-80, 3)
    sf(d, 1200, H-80-280, 1.1, (0,0,0), 4, aa=-20, la=15)
    d.ellipse([W-200, 50, W-50, 200], outline=(255, 200, 0), width=4)
    import math
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = angle * 3.14159 / 180
        d.line([W-125+int(50*math.cos(rad)), 125+int(50*math.sin(rad)),
                W-125+int(85*math.cos(rad)), 125+int(85*math.sin(rad))],
               fill=(255, 200, 0), width=3)
    tx(d, "Walking...", 100, 80, 50, (150, 0, 0))

def tmpl_relax(d, prompt, sentence):
    d.ellipse([700, 300, 780, 380], outline=(0,0,0), width=4)
    d.line([740, 380, 740, 450], fill=(0,0,0), width=4)
    d.line([740, 400, 670, 430], fill=(0,0,0), width=4)
    d.line([740, 400, 810, 430], fill=(0,0,0), width=4)
    d.line([740, 450, 700, 520], fill=(0,0,0), width=4)
    d.line([740, 450, 780, 520], fill=(0,0,0), width=4)
    d.ellipse([900, 200, 1200, 320], outline=(0,0,0), width=3)
    tx(d, "Relaxed", 960, 240, 36, (0, 100, 0))
    tc(d, "EASY LIFE", 800, 45, (0, 100, 0))

def tmpl_harvest(d, prompt, sentence):
    draw_wheat(d, 600, H-80, 3)
    sf(d, 1100, H-80-280, 1.1, (0,0,0), 4, aa=-30, la=10)
    d.line([1100-60, H-80-240, 1100, H-80-250], fill=(200, 150, 0), width=4)
    d.line([1100-60, H-80-210, 1100, H-80-220], fill=(200, 150, 0), width=4)
    tc(d, "Work", 100, 50, (0,0,0))

def tmpl_comparison(d, prompt, sentence):
    d.line([W//2, 0, W//2, H], fill=(200,200,200), width=2)
    for side, label, cx, bad in [("LEFT", "BAD", W//4, True), ("RIGHT", "GOOD", 3*W//4, False)]:
        x = cx - 60
        y = H-80-280
        d.ellipse([x, y, x+120, y+80], outline=(255,0,0) if bad else (0,150,0), width=4)
        d.line([x+60, y+80, x+60, y+200], fill=(255,0,0) if bad else (0,150,0), width=4)
        d.line([x+60, y+130, x, y+180], fill=(255,0,0) if bad else (0,150,0), width=4)
        d.line([x+60, y+130, x+120, y+180], fill=(255,0,0) if bad else (0,150,0), width=4)
        d.line([x+60, y+200, x+30, y+260], fill=(255,0,0) if bad else (0,150,0), width=4)
        d.line([x+60, y+200, x+90, y+260], fill=(255,0,0) if bad else (0,150,0), width=4)
        if bad: d.line([x-20, y+40, x+140, y+120], fill=(255,0,0), width=6); d.line([x-20, y+120, x+140, y+40], fill=(255,0,0), width=6)
        else: d.ellipse([x+140, y-10, x+180, y+30], fill=(255,200,0), outline=(0,0,0), width=2)
        tc(d, label, cx-90, 750, 50, (255,0,0) if bad else (0,150,0))
    tc(d, "VS", 100, 350, 50, (100,100,100))

def tmpl_spill(d, prompt, sentence):
    sf(d, 600, H-80-280, 1.2, (0,0,0), 5, aa=30, la=0)
    for sx in range(700, 1300, 60):
        for sy in range(H-160, H-90, 30):
            d.ellipse([sx, sy, sx+12, sy+12], fill=(200, 150, 0), outline=(0,0,0), width=1)
    for wx in [800, 950, 1100]:
        d.line([wx, H-80, wx, H-250], fill=(0, 100, 0), width=2)
        d.ellipse([wx-8, H-270, wx+8, H-250], fill=(200, 150, 0), outline=(0,0,0), width=1)
    tc(d, "SPILL", 120, 70, (200, 0, 0))

def tmpl_crowd(d, prompt, sentence):
    positions = []
    for row in range(3):
        for col in range(5):
            x = 200 + col * 320
            y = 200 + row * 180
            c = (0,0,0)
            w = 3
            d.ellipse([x, y, x+50, y+50], outline=c, width=w)
            d.line([x+25, y+50, x+25, y+130], fill=c, width=w)
            d.line([x+25, y+85, x+5, y+120], fill=c, width=w)
            d.line([x+25, y+85, x+45, y+120], fill=c, width=w)
            d.line([x+25, y+130, x+12, y+165], fill=c, width=w)
            d.line([x+25, y+130, x+38, y+165], fill=c, width=w)
    tc(d, "CROWD", 750, 60, (0,0,0))
    d.line([800, 500, 900, 600], fill=(0,200,0), width=6)
    d.line([900, 600, 1100, 400], fill=(0,200,0), width=6)
    tx(d, "CHECK", 1020, 380, 40, (0,150,0))

def tmpl_thinking(d, prompt, sentence):
    sf(d, 600, H-80-280, 1.2, (0,0,0), 5, aa=20, arm_up=40)
    d.ellipse([800, 150, 1100, 350], outline=(255,200,0), width=4)
    d.ellipse([870, 170, 1030, 330], outline=(0,0,0), width=2)
    for i, q in enumerate(["?"]):
        tx(d, "?", 940, 220, 60, (200,0,0))
    d.ellipse([400, 80, 500, 180], fill=(255,200,0), outline=(0,0,0), width=3)
    d.line([450, 180, 450, 200], fill=(255,200,0), width=3)
    tc(d, "THINK", 100, 50, (0,0,150))

def tmpl_school(d, prompt, sentence):
    d.ellipse([200, 200, 280, 280], outline=(0,0,0), width=4)
    d.line([240, 280, 240, 500], fill=(0,0,0), width=4)
    d.line([240, 340, 180, 420], fill=(0,0,0), width=4)
    d.line([240, 340, 300, 420], fill=(0,0,0), width=4)
    d.line([240, 500, 200, 620], fill=(0,0,0), width=4)
    d.line([240, 500, 280, 620], fill=(0,0,0), width=4)
    d.line([300, 300, 500, 200], fill=(0,0,0), width=3)
    d.rectangle([600, 150, 1100, 550], outline=(0,0,0), width=4)
    d.rectangle([610, 160, 1090, 540], fill=(50, 50, 150))
    tx(d, "LESSON", 730, 300, 50, (255,255,255))
    sf(d, 1400, 350, 0.8, (0,0,0), 3, arm_up=20)
    d.rectangle([1320, 550, 1480, 570], fill=(101, 67, 33))
    tc(d, "CLASS", 100, 60, (0,0,150))

def tmpl_generic(d, prompt, sentence):
    sf(d, W//2, H-80-280, 1.2, (0,0,0), 5)
    words = sentence.split()[:5]
    label = " ".join(words) + ("..." if len(words) < len(sentence.split()) else "")
    tc(d, label, 100, 60, (0,0,0))


TEMPLATES = [
    (["shock", "mistake", "surprise", "wrong", "error"], tmpl_shock),
    (["walk", "wheat", "path", "journey", "ancestor", "past"], tmpl_walking),
    (["relax", "rest", "sleep", "15 hour", "speech", "bubble", "easy"], tmpl_relax),
    (["harvest", "work", "hunt", "plant", "cook", "build", "grind"], tmpl_harvest),
    (["vs", "comparison", "versus", "mutation", "change", "evolution"], tmpl_comparison),
    (["spill", "scatter", "shrug", "accident", "fall"], tmpl_spill),
    (["crowd", "row", "group", "army", "mass", "identical", "many"], tmpl_crowd),
    (["think", "thought", "brain", "mind", "idea", "question", "philosophy"], tmpl_thinking),
    (["school", "teacher", "student", "class", "lesson", "learn", "teach"], tmpl_school),
]


def match_template(prompt):
    pl = prompt.lower()
    for keywords, func in TEMPLATES:
        if any(k in pl for k in keywords):
            return func
    return tmpl_generic


def main():
    if not os.path.exists(SCRIPT_FILE):
        print("ERROR: script.txt not found")
        sys.exit(1)

    if not os.path.exists(PROMPT_FILE):
        print("ERROR: imagesprompts.txt not found")
        sys.exit(1)

    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompts = [l.strip() for l in f if l.strip()]

    if not prompts:
        print("ERROR: imagesprompts.txt is empty. Write one prompt per line.")
        sys.exit(1)

    n = len(prompts)
    os.makedirs(IMG_DIR, exist_ok=True)

    print(f"Generating {n} images from prompts...\n")

    for i in range(n):
        sentence = lines[i] if i < len(lines) else f"Scene {i+1}"
        prompt = prompts[i]
        safe = re.sub(r'[<>:"/\\|?*]', '', sentence)[:100].strip() or f"image{i+1}"
        fname = f"{i+1}. {safe}.png"

        img = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.rectangle([0, H-80, W, H], fill=GROUND)

        tmpl = match_template(prompt)
        tmpl(d, prompt, sentence)

        path = os.path.join(IMG_DIR, fname)
        img.save(path, "PNG")
        sz = os.path.getsize(path)
        print(f"  [{i+1}/{n}] {fname} ({sz} bytes)")

    print(f"\nDone! {n} images saved to {IMG_DIR}")


if __name__ == "__main__":
    main()
