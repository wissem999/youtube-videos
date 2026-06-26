from PIL import Image, ImageDraw, ImageFont
import os, re, sys

IMG_DIR = os.path.join(os.getcwd(), "img")
PROMPT_FILE = os.path.join(os.getcwd(), "imagesprompts.txt")
W, H = 1920, 1080
GROUND = (139, 94, 60)

def sf(d, x, y, s=1.0, c=(0,0,0), w=4, aa=0, la=0, arm_up=0):
    hr = int(40 * s); bl = int(120 * s); al = int(60 * s); ll = int(70 * s)
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

def tc(d, text, y, size=60, color=(0,0,0)):
    try: font = ImageFont.truetype("arial.ttf", size)
    except: font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), text, font=font)
    d.text(((W - (bbox[2]-bbox[0])) // 2, y), text, fill=color, font=font)

def tx(d, text, x, y, size=40, color=(0,0,0)):
    try: font = ImageFont.truetype("arial.ttf", size)
    except: font = ImageFont.load_default()
    d.text((x, y), text, fill=color, font=font)

def draw_wheat(d, cx, by, count=3):
    off = (count-1)*100
    for i in range(count):
        wx = cx - off + i*200
        d.line([wx, by, wx, by-270], fill=(0, 100, 0), width=3)
        d.ellipse([wx-12, by-290, wx+12, by-260], fill=(200, 150, 0), outline=(0,0,0), width=2)

# ── TEMPLATES ──

def t_shock(d, p, s):
    sf(d, W//2, H-80-280, 1.3, (0,0,0), 5, aa=20, arm_up=40)
    tc(d, "\"A MISTAKE\"", 100, 80)

def t_walk(d, p, s):
    draw_wheat(d, 600, H-80, 3)
    sf(d, 1200, H-80-280, 1.1, (0,0,0), 4, aa=-20, la=15)
    import math
    d.ellipse([W-200, 50, W-50, 200], outline=(255, 200, 0), width=4)
    for a in [0,45,90,135,180,225,270,315]:
        r = a*3.14159/180
        d.line([W-125+int(50*math.cos(r)),125+int(50*math.sin(r)),W-125+int(85*math.cos(r)),125+int(85*math.sin(r))],fill=(255,200,0),width=3)
    tx(d, "Walking...", 100, 80, 50, (150,0,0))

def t_relax(d, p, s):
    d.ellipse([700,300,780,380], outline=(0,0,0), width=4)
    d.line([740,380,740,450], fill=(0,0,0), width=4)
    d.line([740,400,670,430], fill=(0,0,0), width=4)
    d.line([740,400,810,430], fill=(0,0,0), width=4)
    d.line([740,450,700,520], fill=(0,0,0), width=4)
    d.line([740,450,780,520], fill=(0,0,0), width=4)
    d.ellipse([900,200,1200,320], outline=(0,0,0), width=3)
    tx(d, "15 hrs/week", 950, 240, 36, (0,100,0))

def t_harvest(d, p, s):
    draw_wheat(d, 600, H-80, 3)
    sf(d, 1100, H-80-280, 1.1, (0,0,0), 4, aa=-30, la=10)
    d.line([1100-60, H-80-240, 1100, H-80-250], fill=(200,150,0), width=4)
    d.line([1100-60, H-80-210, 1100, H-80-220], fill=(200,150,0), width=4)

def t_vs(d, p, s):
    d.line([W//2,0,W//2,H], fill=(200,200,200), width=2)
    for bad, cx in [(True, W//4), (False, 3*W//4)]:
        x, y = cx-60, H-80-280; c = (255,0,0) if bad else (0,150,0)
        d.ellipse([x, y, x+120, y+80], outline=c, width=4)
        d.line([x+60, y+80, x+60, y+200], fill=c, width=4)
        d.line([x+60, y+130, x, y+180], fill=c, width=4)
        d.line([x+60, y+130, x+120, y+180], fill=c, width=4)
        d.line([x+60, y+200, x+30, y+260], fill=c, width=4)
        d.line([x+60, y+200, x+90, y+260], fill=c, width=4)
        if bad:
            d.line([x-20, y+40, x+140, y+120], fill=(255,0,0), width=6)
            d.line([x-20, y+120, x+140, y+40], fill=(255,0,0), width=6)
        else:
            d.ellipse([x+140, y-10, x+180, y+30], fill=(255,200,0), outline=(0,0,0), width=2)
        tc(d, "BAD" if bad else "GOOD", cx-70, 750, 50, c)
    tc(d, "VS", 100, 350, 50, (100,100,100))

def t_spill(d, p, s):
    sf(d, 600, H-80-280, 1.2, (0,0,0), 5, aa=30)
    for sx in range(700,1300,60):
        for sy in range(H-160,H-90,30):
            d.ellipse([sx,sy,sx+12,sy+12], fill=(200,150,0), outline=(0,0,0), width=1)
    for wx in [800,950,1100]:
        d.line([wx,H-80,wx,H-250], fill=(0,100,0), width=2)
        d.ellipse([wx-8,H-270,wx+8,H-250], fill=(200,150,0), outline=(0,0,0), width=1)
    tc(d, "ACCIDENT", 120, 70, (200,0,0))

def t_crowd(d, p, s):
    for row in range(3):
        for col in range(5):
            x, y = 200+col*320, 200+row*180
            d.ellipse([x, y, x+50, y+50], outline=(0,0,0), width=3)
            d.line([x+25, y+50, x+25, y+130], fill=(0,0,0), width=3)
            d.line([x+25, y+85, x+5, y+120], fill=(0,0,0), width=3)
            d.line([x+25, y+85, x+45, y+120], fill=(0,0,0), width=3)
            d.line([x+25, y+130, x+12, y+165], fill=(0,0,0), width=3)
            d.line([x+25, y+130, x+38, y+165], fill=(0,0,0), width=3)

def t_think(d, p, s):
    sf(d, 600, H-80-280, 1.2, (0,0,0), 5, aa=20, arm_up=40)
    d.ellipse([800,150,1100,350], outline=(255,200,0), width=4)
    d.ellipse([870,170,1030,330], outline=(0,0,0), width=2)
    tx(d, "?", 940, 220, 60, (200,0,0))
    d.ellipse([400,80,500,180], fill=(255,200,0), outline=(0,0,0), width=3)
    d.line([450,180,450,200], fill=(255,200,0), width=3)

def t_gen(d, p, s):
    sf(d, W//2, H-80-280, 1.2, (0,0,0), 5)
    w = s.split()[:6]; lbl = " ".join(w) + ("..." if len(w)<len(s.split()) else "")
    tc(d, lbl, 100, 60)

TEMPLATES = [
    (["shock","mistake","surprise","wrong","error"], t_shock),
    (["walk","wheat","path","journey","ancestor","past","field"], t_walk),
    (["relax","rest","sleep","15 hour","speech","bubble","free time","play"], t_relax),
    (["harvest","work","hunt","plant","cook","build","grind","collect"], t_harvest),
    (["vs","comparison","versus","mutation","change","evolution","different"], t_vs),
    (["spill","scatter","shrug","accident","drop","fall","seed"], t_spill),
    (["crowd","row","group","army","mass","identical","many","village"], t_crowd),
    (["think","thought","brain","mind","idea","question","philosophy"], t_think),
]

def match_template(text):
    tl = text.lower()
    for keywords, func in TEMPLATES:
        if any(k in tl for k in keywords):
            return func
    return t_gen

def parse_blocks(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    blocks = re.split(r'\n\s*\n', raw.strip())
    blocks = [b.strip() for b in blocks if b.strip()]
    entries = []
    for i in range(0, len(blocks), 2):
        sentence = blocks[i]
        prompt = blocks[i+1] if i+1 < len(blocks) else sentence
        entries.append((sentence, prompt))
    return entries

def main():
    if not os.path.exists(PROMPT_FILE):
        print("ERROR: imagesprompts.txt not found")
        sys.exit(1)

    entries = parse_blocks(PROMPT_FILE)
    if not entries:
        print("ERROR: imagesprompts.txt is empty or badly formatted.")
        print("Format: EXACT SCRIPT TEXT on first line, then prompt lines, then blank line between images.")
        sys.exit(1)

    os.makedirs(IMG_DIR, exist_ok=True)
    print(f"Generating {len(entries)} images from prompts...\n")

    for i, (sentence, prompt) in enumerate(entries):
        safe = re.sub(r'[<>:"/\\|?*]', '', sentence).strip()[:120] or f"image{i+1}"
        safe = safe.rstrip('. ')
        fname = f"{i+1}. {safe}.png"

        img = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.rectangle([0, H-80, W, H], fill=GROUND)

        tmpl = match_template(prompt + ' ' + sentence)
        tmpl(d, prompt, sentence)

        path = os.path.join(IMG_DIR, fname)
        img.save(path, "PNG")
        print(f"  [{i+1}/{len(entries)}] {fname} ({os.path.getsize(path)} bytes)")

    print(f"\nDone! {len(entries)} images saved to {IMG_DIR}")

if __name__ == "__main__":
    main()
