# utils.py (create this file if needed)
from PIL import Image
import numpy as np
import re
from app.models import Color

def detect_skin_tone_from_image(image_file):
    img = Image.open(image_file).convert("RGB")
    img_np = np.array(img)
    h, w, _ = img_np.shape

    # Crop center to approximate hand area
    crop = img_np[h//3:h*2//3, w//3:w*2//3]

    avg_color = crop.reshape(-1, 3).mean(axis=0)
    r, g, b = [int(c) for c in avg_color]
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_closest_skin_tone(hex_color, skin_tones):
    def color_distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2))

    detected_rgb = hex_to_rgb(hex_color)
    return min(skin_tones, key=lambda tone: color_distance(detected_rgb, hex_to_rgb(tone.color_hex)))

UNDERTONE_COLOR_MAP = {
    "neutral": [
        "Ivory", "Charcoal", "Teal", "Soft Pink", "Burgundy", "Forest Green"
        # "Mauve", "Soft Navy", "Cocoa", "Slate", "Wine", "Alabaster", "Sand", "Steel Blue", "Heather Gray"
    ],
    "warm olive": [
        "Emerald", "Terracotta", "Mustard", "Berry", "Coral", "Plum", "Olive Green"
        # "Warm Taupe", "Crimson", "Deep Red", "Caramel", "Golden Beige"
    ],
    "warm golden": [
        "Sunflower", "Deep Sea Blue" ,"Turquoise", "Olive Green", "Fuchsia", "Chocolate", "Amber",
        "Coral", "Scarlet", "Red", "Crimson", "Cherry", "Cream", "Sandy Brown"
    ],
    "warm peach": [
        # "Peach", "Golden Yellow", "Mint", "Mocha", "Soft Blue", "Apricot",
        "Cinnamon", "Coral", "Brick Red", "Beige", "Warm White", "Soft Pink"
    ],
    "warm yellow": [
        "Honey", "Rust", "Emerald", "Lavender", "Burnt Orange", "Cobalt Blue",
        "Chartreuse", "Caramel", "Strawberry Red", "Goldenrod", "Soft Pink", "Soft Peach"
    ],
    "cool pink": [
        "Lilac", "Sky Blue", "Rose", "Soft Pink", "Dusty Lavender", "Steel Gray",
        # "Periwinkle", "Blush", "Cool White", "Magenta", "Mauve", "Orchid", "Indigo", "Light Gray"
    ],
    "warm bronze": [
        "Copper", "Wine", "Sage", "Mustard", "Brick Red", "Midnight Blue"
        # "Espresso", "Warm Beige", "Chocolate", "Mahogany", "Cherry", "Camel"
    ],
    "warm neutral": [
        # "Camel", "Olive", "Cream", "Rust", "Beige", "Deep Red", "Bronze", "Tan",
        "Chestnut", "Sand", "Maroon", "Warm Ivory", "Charcoal"
    ],
    "cool peach": [
        "Mauve", "Iris", "Dusty Pink", "Powder Blue",
        "Rosewood", "Heather Gray",
        # "Cool Mint", "Orchid", "Violet", "Cool White", "Plum", "Lavender Gray"
    ],
    "neutral olive": [
        "Moss Green", "Navy", "Burgundy", "Warm Beige"
        # "Olive", "Blush", "Slate Blue", "Taupe", "Slate Gray"
    ],
}

# Optional: add shortcut aliases
UNDERTONE_COLOR_MAP["olive"] = UNDERTONE_COLOR_MAP["neutral olive"]
UNDERTONE_COLOR_MAP["golden"] = UNDERTONE_COLOR_MAP["warm golden"]
UNDERTONE_COLOR_MAP["bronze"] = UNDERTONE_COLOR_MAP["warm bronze"]
UNDERTONE_COLOR_MAP["peach"] = UNDERTONE_COLOR_MAP["warm peach"]
UNDERTONE_COLOR_MAP["yellow"] = UNDERTONE_COLOR_MAP["warm yellow"]


def extract_undertone(name):
    match = re.search(r'with (.+?) undertones', name.lower())
    if match:
        return match.group(1)
    return None

def get_colors_for_skin_tone(skin_tone_name):
    print("SKIN TONE NAME:", skin_tone_name)  # ✅ Debug
    undertone = extract_undertone(skin_tone_name)
    print("EXTRACTED UNDERTONE:", undertone)  # ✅ Debug
    if not undertone:
        return Color.objects.none()

    base_colors = UNDERTONE_COLOR_MAP.get(undertone.lower().strip(), [])
    print("COLORS FROM MAP:", base_colors)  # ✅ Debug
    return Color.objects.filter(name__in=base_colors)

