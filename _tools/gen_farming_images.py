from PIL import Image, ImageDraw, ImageFont
import os

IMG_DIR = os.path.join(os.getcwd(), "img")
W, H = 1920, 1080
GROUND = (139, 94, 60)

os.makedirs(IMG_DIR, exist_ok=True)

images = []

def stick_figure(d, x, y, scale=1.0, color=(0,0,0), width=4, arm_angle=0, leg_angle=0):
    s = scale
    head_r = int(40 * s)
    body_len = int(120 * s)
    arm_len = int(60 * s)
    leg_len = int(70 * s)
    d.ellipse([x-head_r, y, x+head_r, y+head_r*2], outline=color, width=width)
    d.ellipse([x-3, y+int(25*s), x+3, y+int(31*s)], fill=color)
    d.line([x, y+head_r*2, x, y+head_r*2+body_len], fill=color, width=width)
    d.line([x, y+head_r*2+int(40*s), x-arm_len, y+head_r*2+int(40*s)+arm_angle], fill=color, width=width)
    d.line([x, y+head_r*2+int(40*s), x+arm_len, y+head_r*2+int(40*s)-arm_angle], fill=color, width=width)
    d.line([x, y+head_r*2+body_len, x-leg_len, y+head_r*2+body_len+leg_len+leg_angle], fill=color, width=width)
    d.line([x, y+head_r*2+body_len, x+leg_len, y+head_r*2+body_len+leg_len-leg_angle], fill=color, width=width)
    return (x, y+head_r*2+body_len+leg_len)

def draw_text_centered(d, text, y, size=60, color=(0,0,0)):
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except:
        font = ImageFont.load_default()
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, y), text, fill=color, font=font)

def draw_text(d, text, x, y, size=40, color=(0,0,0)):
    try:
        font = ImageFont.truetype("arial.ttf", size)
    except:
        font = ImageFont.load_default()
    d.text((x, y), text, fill=color, font=font)

# ─── IMAGE 1 ─────────────────────────────────────
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([0, H-80, W, H], fill=GROUND)
stick_figure(d, W//2, H-80-280, 1.2, (0,0,0), 5)
draw_text_centered(d, '"A MISTAKE"', 120, 80, (0,0,0))
d.line([W//2-200, 240, W//2+200, 240], fill=(0,0,0), width=2)
img.save(os.path.join(IMG_DIR, "1. Farming wasnt an invention it was a mistake.png"))
print("1 done")

# ─── IMAGE 2 ─────────────────────────────────────
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([0, H-80, W, H], fill=GROUND)
# Sun
d.ellipse([W-200, 50, W-50, 200], outline=(255, 200, 0), width=4)
for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
    import math
    rad = angle * 3.14159 / 180
    d.line([W-125+int(50*math.cos(rad)), 125+int(50*math.sin(rad)),
            W-125+int(85*math.cos(rad)), 125+int(85*math.sin(rad))],
           fill=(255, 200, 0), width=3)
# Wheat stalks
for wx in [300, 500, 700, 900]:
    d.line([wx, H-80, wx, H-300], fill=(0, 100, 0), width=3)
    d.ellipse([wx-15, H-340, wx+15, H-300], fill=(200, 150, 0), outline=(0,0,0), width=2)
    d.line([wx-10, H-320, wx+10, H-310], fill=(0, 0, 0), width=1)
# Figure walking away
fig_x = 1200
stick_figure(d, fig_x, H-80-280, 1.1, (0,0,0), 4, arm_angle=-20, leg_angle=15)
draw_text(d, "300,000 years...", 100, 80, 50, (150, 0, 0))
img.save(os.path.join(IMG_DIR, "2. For 300000 years ancestors walked past wild wheat.png"))
print("2 done")

# ─── IMAGE 3 ─────────────────────────────────────
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([0, H-80, W, H], fill=GROUND)
# Figure relaxing (lying down)
d.ellipse([700, 300, 780, 380], outline=(0,0,0), width=4)
d.line([740, 380, 740, 450], fill=(0,0,0), width=4)
d.line([740, 400, 670, 430], fill=(0,0,0), width=4)
d.line([740, 400, 810, 430], fill=(0,0,0), width=4)
d.line([740, 450, 700, 520], fill=(0,0,0), width=4)
d.line([740, 450, 780, 520], fill=(0,0,0), width=4)
# Speech bubble
d.ellipse([900, 200, 1200, 320], outline=(0,0,0), width=3)
d.text((950, 240), "15 hrs/week", fill=(0, 100, 0), font_size=36)
draw_text_centered(d, "HUNTER-GATHERER", 120, 55, (0,0,0))
draw_text_centered(d, "Worked less. Ate better.", 800, 45, (0, 100, 0))
img.save(os.path.join(IMG_DIR, "3. Hunter gatherers worked 15 hours a week.png"))
print("3 done")

# ─── IMAGE 4 ─────────────────────────────────────
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([0, H-80, W, H], fill=GROUND)
# Three wheat stalks
for wx in [400, 600, 800]:
    d.line([wx, H-80, wx, H-350], fill=(0, 100, 0), width=3)
    d.ellipse([wx-12, H-380, wx+12, H-350], fill=(200, 150, 0), outline=(0,0,0), width=2)
# Figure carrying bundle
stick_figure(d, 1100, H-80-280, 1.1, (0,0,0), 4, arm_angle=-30, leg_angle=10)
d.line([1100-60, H-80-240, 1100, H-80-250], fill=(200, 150, 0), width=4)
d.line([1100-60, H-80-210, 1100, H-80-220], fill=(200, 150, 0), width=4)
draw_text_centered(d, "Harvest. Grind. Eat. Move on.", 120, 50, (0,0,0))
img.save(os.path.join(IMG_DIR, "4. They harvested it ground it ate it and moved on.png"))
print("4 done")

# ─── IMAGE 5 ─────────────────────────────────────
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([0, H-80, W, H], fill=GROUND)
# Left plant: shattered (seeds falling)
d.line([400, H-80, 400, H-350], fill=(0, 100, 0), width=3)
d.ellipse([388, H-380, 412, H-350], fill=(200, 150, 0), outline=(0,0,0), width=2)
for fx in [370, 390, 410, 430, 360, 440]:
    d.ellipse([fx, H-320, fx+10, H-310], fill=(200, 150, 0), width=2)
# Right plant: mutation (seeds cling)
d.line([900, H-80, 900, H-350], fill=(0, 100, 0), width=5)
d.ellipse([888, H-380, 912, H-350], fill=(200, 150, 0), outline=(0,0,255), width=3)
d.ellipse([880, H-320, 920, H-300], fill=(200, 150, 0), outline=(0,0,255), width=2)
# Labels
draw_text_centered(d, "SHATTERS", 600, 40, (200, 0, 0))
draw_text_centered(d, "CLINGS", 1100, 40, (0, 0, 200))
draw_text(d, "MUTATION", 800, 100, 50, (0, 0, 200))
draw_text(d, "X", 350, 400, 60, (200, 0, 0))
img.save(os.path.join(IMG_DIR, "5. Wild grain shatters to scatter but some plants had a mutation.png"))
print("5 done")

# ─── IMAGE 6 ─────────────────────────────────────
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
d.rectangle([0, H-80, W, H], fill=GROUND)
# Figure shrugging
stick_figure(d, 600, H-80-280, 1.2, (0,0,0), 5, arm_angle=30, leg_angle=0)
# Spilled seeds on ground
for sx in range(700, 1300, 60):
    for sy in range(H-160, H-90, 30):
        d.ellipse([sx, sy, sx+12, sy+12], fill=(200, 150, 0), outline=(0,0,0), width=1)
# Scattered stalks
for wx in [800, 950, 1100]:
    d.line([wx, H-80, wx, H-250], fill=(0, 100, 0), width=2,)
    d.ellipse([wx-8, H-270, wx+8, H-250], fill=(200, 150, 0), outline=(0,0,0), width=1)
draw_text_centered(d, "ACCIDENTAL SPILL", 120, 70, (200, 0, 0))
draw_text_centered(d, "10,000 years later...", 800, 45, (100, 100, 100))
img.save(os.path.join(IMG_DIR, "6. Your entire world was built on a single accidental spill.png"))
print("6 done")

print(f"\nAll 6 images saved to {IMG_DIR}")
