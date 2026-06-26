from PIL import Image, ImageDraw
import os, re

IMG_DIR = os.path.join(os.getcwd(), "img")
W, H = 1920, 1080

SCENES = [
    {
        "file": "1. School teaches you to follow orders.png",
        "draw": lambda d: (
            d.rectangle([0, 0, W, H], fill=(255, 255, 255)),
            d.rectangle([0, H-80, W, H], fill=(139, 94, 60)),
            # Teacher stick figure (left)
            d.ellipse([200, 200, 280, 280], outline=(0, 0, 0), width=4),
            d.line([240, 280, 240, 500], fill=(0, 0, 0), width=4),
            d.line([240, 340, 180, 420], fill=(0, 0, 0), width=4),
            d.line([240, 340, 300, 420], fill=(0, 0, 0), width=4),
            d.line([240, 500, 200, 620], fill=(0, 0, 0), width=4),
            d.line([240, 500, 280, 620], fill=(0, 0, 0), width=4),
            # Pointer stick
            d.line([300, 300, 500, 200], fill=(0, 0, 0), width=3),
            # Board
            d.rectangle([600, 150, 1100, 550], outline=(0, 0, 0), width=4),
            d.rectangle([610, 160, 1090, 540], fill=(50, 50, 150)),
            d.text((700, 300), "2 + 2 = 4", fill=(255, 255, 255), font_size=40),
            # Student stick figure (right)
            d.ellipse([1400, 350, 1480, 430], outline=(0, 0, 0), width=4),
            d.line([1440, 430, 1440, 650], fill=(0, 0, 0), width=4),
            d.line([1440, 490, 1380, 570], fill=(0, 0, 0), width=4),
            d.line([1440, 490, 1500, 570], fill=(0, 0, 0), width=4),
            d.line([1440, 650, 1400, 770], fill=(0, 0, 0), width=4),
            d.line([1440, 650, 1480, 770], fill=(0, 0, 0), width=4),
            # Desk
            d.rectangle([1350, 650, 1530, 670], fill=(101, 67, 33)),
            d.rectangle([1370, 670, 1390, 730], fill=(101, 67, 33)),
            d.rectangle([1490, 670, 1510, 730], fill=(101, 67, 33)),
            d.text((100, 100), "School", fill=(200, 0, 0), font_size=60),
        )
    },
    {
        "file": "2. You sit in rows and raise your hand.png",
        "draw": lambda d: (
            d.rectangle([0, 0, W, H], fill=(255, 255, 255)),
            d.rectangle([0, H-80, W, H], fill=(139, 94, 60)),
            # Row of student desks
            *[(
                d.rectangle([x, 600, x+120, 615], fill=(101, 67, 33)),
                d.rectangle([x+10, 615, x+25, 650], fill=(101, 67, 33)),
                d.rectangle([x+95, 615, x+110, 650], fill=(101, 67, 33)),
                d.ellipse([x+30, 350, x+90, 410], outline=(0, 0, 0), width=3),
                d.line([x+60, 410, x+60, 560], fill=(0, 0, 0), width=3),
                d.line([x+60, 460, x+20, 520], fill=(0, 0, 0), width=3),
                d.line([x+60, 460, x+100, 520], fill=(0, 0, 0), width=3),
                d.line([x+60, 560, x+40, 600], fill=(0, 0, 0), width=3),
                d.line([x+60, 560, x+80, 600], fill=(0, 0, 0), width=3),
            ) for x in [200, 500, 800, 1100, 1400]],
            # One student raising hand (middle)
            d.ellipse([530, 350, 590, 410], outline=(255, 0, 0), width=4),
            d.line([560, 410, 560, 560], fill=(255, 0, 0), width=4),
            d.line([560, 410, 560, 300], fill=(255, 0, 0), width=4),
            d.line([560, 460, 520, 520], fill=(255, 0, 0), width=4),
            d.line([560, 460, 600, 520], fill=(255, 0, 0), width=4),
            d.line([560, 560, 540, 600], fill=(255, 0, 0), width=4),
            d.line([560, 560, 580, 600], fill=(255, 0, 0), width=4),
            d.text((100, 100), "Raise your hand", fill=(200, 0, 0), font_size=60),
        )
    },
    {
        "file": "3. They tell you what to think not how to think.png",
        "draw": lambda d: (
            d.rectangle([0, 0, W, H], fill=(255, 255, 255)),
            d.rectangle([0, H-80, W, H], fill=(139, 94, 60)),
            # Brain outline left
            d.ellipse([200, 200, 600, 500], outline=(0, 0, 0), width=4),
            d.line([250, 300, 350, 250, 450, 300, 500, 250, 550, 300], fill=(0, 0, 0), width=3),
            d.line([250, 400, 350, 450, 450, 400, 500, 450, 550, 400], fill=(0, 0, 0), width=3),
            # Funnel pouring into brain
            d.polygon([700, 150, 750, 400, 650, 400], outline=(0, 0, 0), width=4),
            d.line([700, 50, 700, 150], fill=(0, 0, 0), width=4),
            d.text((680, 40), "FACTS", fill=(0, 0, 150), font_size=30),
            # Brain right
            d.ellipse([1300, 200, 1700, 500], outline=(0, 0, 0), width=4),
            d.line([1350, 300, 1450, 250, 1550, 300, 1600, 250, 1650, 300], fill=(0, 0, 0), width=3),
            # X mark on right brain
            d.line([1400, 350, 1600, 450], fill=(255, 0, 0), width=5),
            d.line([1600, 350, 1400, 450], fill=(255, 0, 0), width=5),
            d.text((1350, 140), "No questions", fill=(200, 0, 0), font_size=40),
            d.text((100, 100), "What to think", fill=(200, 0, 0), font_size=60),
        )
    },
    {
        "file": "4. The bell controls your day like a prison.png",
        "draw": lambda d: (
            d.rectangle([0, 0, W, H], fill=(255, 255, 255)),
            d.rectangle([0, H-80, W, H], fill=(139, 94, 60)),
            # Bell
            d.arc([800, 80, 1120, 400], 180, 0, fill=(0, 0, 0), width=6),
            d.ellipse([890, 380, 1030, 420], fill=(200, 150, 0), outline=(0, 0, 0), width=3),
            d.line([960, 420, 960, 520], fill=(0, 0, 0), width=4),
            d.line([960, 520, 880, 540], fill=(0, 0, 0), width=4),
            d.line([960, 520, 1040, 540], fill=(0, 0, 0), width=4),
            d.text((880, 440), "DING!", fill=(200, 0, 0), font_size=40),
            # Stick figure running
            d.ellipse([200, 200, 280, 280], outline=(0, 0, 0), width=4),
            d.line([240, 280, 240, 450], fill=(0, 0, 0), width=4),
            d.line([240, 340, 150, 400], fill=(0, 0, 0), width=4),
            d.line([240, 340, 330, 400], fill=(0, 0, 0), width=4),
            d.line([240, 450, 180, 550], fill=(0, 0, 0), width=4),
            d.line([240, 450, 300, 550], fill=(0, 0, 0), width=4),
            # Clock
            d.ellipse([1500, 180, 1700, 380], outline=(0, 0, 0), width=4),
            d.ellipse([1500, 180, 1700, 380], fill=(255, 255, 200)),
            d.line([1600, 280, 1600, 240], fill=(0, 0, 0), width=3),
            d.line([1600, 280, 1630, 280], fill=(0, 0, 0), width=3),
            d.text((100, 100), "Bell controls your day", fill=(200, 0, 0), font_size=60),
        )
    },
    {
        "file": "5. Creativity is punished conformity is rewarded.png",
        "draw": lambda d: (
            d.rectangle([0, 0, W, H], fill=(255, 255, 255)),
            d.rectangle([0, H-80, W, H], fill=(139, 94, 60)),
            # Left side: Creativity punished
            d.ellipse([120, 200, 280, 360], outline=(0, 0, 0), width=4),
            d.line([200, 360, 200, 550], fill=(0, 0, 0), width=4),
            d.line([200, 420, 130, 500], fill=(0, 0, 0), width=4),
            d.line([200, 420, 270, 500], fill=(0, 0, 0), width=4),
            d.line([200, 550, 160, 650], fill=(0, 0, 0), width=4),
            d.line([200, 550, 240, 650], fill=(0, 0, 0), width=4),
            # Lightbulb above (creativity)
            d.ellipse([130, 80, 270, 200], outline=(255, 200, 0), width=4),
            d.line([200, 200, 200, 220], fill=(255, 200, 0), width=4),
            d.text((70, 20), "IDEA", fill=(255, 200, 0), font_size=30),
            # X mark
            d.line([100, 300, 300, 400], fill=(255, 0, 0), width=6),
            d.line([100, 400, 300, 300], fill=(255, 0, 0), width=6),
            d.text((100, 480), "BAD", fill=(200, 0, 0), font_size=40),
            # Right side: Conformity rewarded
            d.ellipse([1500, 200, 1680, 380], outline=(0, 0, 0), width=4),
            d.ellipse([1500, 200, 1680, 380], fill=(200, 255, 200)),
            d.line([1590, 380, 1590, 570], fill=(0, 0, 0), width=4),
            d.line([1590, 440, 1520, 520], fill=(0, 0, 0), width=4),
            d.line([1590, 440, 1660, 520], fill=(0, 0, 0), width=4),
            d.line([1590, 570, 1550, 670], fill=(0, 0, 0), width=4),
            d.line([1590, 570, 1630, 670], fill=(0, 0, 0), width=4),
            # Trophy
            d.ellipse([1540, 100, 1640, 150], outline=(255, 200, 0), width=3),
            d.rectangle([1560, 150, 1620, 180], fill=(255, 200, 0), outline=(0, 0, 0)),
            d.text((1530, 50), "GOOD", fill=(0, 150, 0), font_size=40),
            d.text((1500, 700), "Conform!", fill=(0, 150, 0), font_size=40),
            d.text((100, 100), "Creativity vs Conformity", fill=(200, 0, 0), font_size=50),
        )
    },
    {
        "file": "6. By the end you are trained to obey.png",
        "draw": lambda d: (
            d.rectangle([0, 0, W, H], fill=(255, 255, 255)),
            d.rectangle([0, H-80, W, H], fill=(139, 94, 60)),
            # Rows of identical stick figures
            *[(
                d.ellipse([x, 200+y, x+60, 260+y], outline=(0, 0, 0), width=3),
                d.line([x+30, 260+y, x+30, 380+y], fill=(0, 0, 0), width=3),
                d.line([x+30, 310+y, x+5, 360+y], fill=(0, 0, 0), width=3),
                d.line([x+30, 310+y, x+55, 360+y], fill=(0, 0, 0), width=3),
                d.line([x+30, 380+y, x+15, 420+y], fill=(0, 0, 0), width=3),
                d.line([x+30, 380+y, x+45, 420+y], fill=(0, 0, 0), width=3),
            ) for y, row in [(0, 0), (120, 1), (240, 2)] for x in [100, 350, 600, 850, 1100, 1350, 1600]],
            # Checkmark
            d.line([800, 500, 920, 620], fill=(0, 200, 0), width=8),
            d.line([920, 620, 1200, 350], fill=(0, 200, 0), width=8),
            d.text((880, 650), "TRAINED", fill=(0, 150, 0), font_size=60),
            d.text((100, 100), "By the end you obey", fill=(200, 0, 0), font_size=60),
        )
    }
]

os.makedirs(IMG_DIR, exist_ok=True)

for scene in SCENES:
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    scene["draw"](draw)
    path = os.path.join(IMG_DIR, scene["file"])
    img.save(path, "PNG")
    print(f"  Created: {scene['file']} ({os.path.getsize(path)} bytes)")

print(f"\nDone! {len(SCENES)} images generated in {IMG_DIR}")
