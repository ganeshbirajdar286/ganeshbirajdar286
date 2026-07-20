import requests
from PIL import Image, ImageDraw, ImageFont
import random
import io
import os

def create_animation():
    url = "https://github.com/ganeshbirajdar286.png"
    print("Fetching image...")
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content)).convert("RGB")

    char_width = 10
    char_height = 12
    cols = 40
    rows = 40

    img_resized = img.resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = img_resized.load()

    # Try to load a nice monospace font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
    except:
        font = ImageFont.load_default()

    target_chars = []
    target_colors = []
    for y in range(rows):
        char_row = []
        color_row = []
        for x in range(cols):
            r, g, b = pixels[x, y]
            brightness = (r + g + b) / 3
            char_row.append('1' if brightness > 127 else '0')
            color_row.append((r, g, b))
        target_chars.append(char_row)
        target_colors.append(color_row)

    frames = []
    num_frames = 20
    print("Generating frames...")
    
    # 5 frames of pure matrix
    for _ in range(5):
        frame = Image.new("RGB", (cols * char_width, rows * char_height), (13, 17, 23))
        draw = ImageDraw.Draw(frame)
        for y in range(rows):
            for x in range(cols):
                char = str(random.randint(0, 1))
                color = (0, 255, 0) # Neon green
                draw.text((x * char_width, y * char_height), char, font=font, fill=color)
        frames.append(frame)
        
    # Transition frames
    for i in range(num_frames):
        frame = Image.new("RGB", (cols * char_width, rows * char_height), (13, 17, 23))
        draw = ImageDraw.Draw(frame)
        progress = i / (num_frames - 1)
        
        for y in range(rows):
            for x in range(cols):
                if random.random() < progress:
                    char = target_chars[y][x]
                    color = target_colors[y][x]
                else:
                    char = str(random.randint(0, 1))
                    color = (0, 255, 0)
                draw.text((x * char_width, y * char_height), char, font=font, fill=color)
        frames.append(frame)
        
    # Final frames (hold the actual image)
    for _ in range(10):
        frames.append(frames[-1])

    out_path = "/home/ganesh/.gemini/antigravity/scratch/github-profile/binary_avatar.gif"
    print(f"Saving GIF to {out_path}...")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=150, loop=0)
    print("Done!")

if __name__ == "__main__":
    create_animation()
