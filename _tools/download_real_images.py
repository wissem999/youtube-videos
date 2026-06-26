from PIL import Image, ImageDraw
import requests, io, os, sys

IMG_DIR = os.path.join(os.getcwd(), "img")
os.makedirs(IMG_DIR, exist_ok=True)

QUERIES = [
    "wheat field",
    "golden wheat field landscape",
    "ancient hunter gatherer",
    "campfire night",
    "spilled grain seeds",
    "silhouette walking away sunset",
]

W, H = 1920, 1080
HEADERS = {"User-Agent": "Mozilla/5.0"}


def download_flickr(query, index):
    clean = query.replace(" ", ",")
    urls = [
        f"https://loremflickr.com/1920/1080/{clean}?lock={index}",
        f"https://loremflickr.com/1920/1080/{clean}",
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 10000:
                return Image.open(io.BytesIO(r.content))
        except:
            pass
    return None


def download_fallback(query, index):
    urls = [
        f"https://picsum.photos/seed/{index}/1920/1080",
        "https://picsum.photos/1920/1080",
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200 and len(r.content) > 5000:
                return Image.open(io.BytesIO(r.content))
        except:
            pass
    return None


def crop_center(img):
    iw, ih = img.size
    target_ratio = W / H
    img_ratio = iw / ih
    if img_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    elif img_ratio < target_ratio:
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    return img.resize((W, H), Image.LANCZOS)


print("Downloading real images...\n")

for i, query in enumerate(QUERIES):
    idx = i + 1
    fname = f"{idx}. {query}.jpg"
    path = os.path.join(IMG_DIR, fname)
    img = None

    print(f"  [{idx}/6] Downloading '{query}'...")
    img = download_flickr(query, idx)
    if not img:
        print(f"  [{idx}/6] Flickr failed, trying fallback...")
        img = download_fallback(query, idx)

    if img:
        img = crop_center(img)
        img.save(path, "JPEG", quality=92)
        print(f"  [{idx}/6] Saved: {fname} ({os.path.getsize(path)} bytes)")
    else:
        print(f"  [{idx}/6] FAILED: could not download image for '{query}'")
        # Create a colored placeholder
        colors = [(200,50,50), (50,150,50), (50,50,200), (200,200,50), (200,50,200), (50,200,200)]
        img = Image.new("RGB", (W, H), colors[i % len(colors)])
        from PIL import ImageFont
        draw = ImageDraw.Draw(img)
        try: font = ImageFont.truetype("arial.ttf", 60)
        except: font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), f"Image {idx}", font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, H // 2), f"Image {idx}", fill=(255,255,255), font=font)
        img.save(path, "JPEG", quality=85)
        print(f"  [{idx}/6] Created placeholder instead")

print(f"\nDone! Check {IMG_DIR}")
