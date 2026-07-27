import requests
from PIL import Image, ImageDraw, ImageFont
import random
import io
import os

def create_animation():
    url = "https://github.com/ganeshbirajdar286.png"
    print(f"Fetching GitHub profile image from {url}...")
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception as e:
        print(f"Error fetching avatar: {e}, creating placeholder canvas")
        img = Image.new("RGB", (200, 200), (0, 255, 135))

    char_width = 10
    char_height = 12
    cols = 48
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
    num_transition_frames = 20
    print("Generating binary matrix animation frames...")
    
    cx_px = (cols * char_width) / 2
    cy_px = (rows * char_height) / 2
    radius_px = min(cx_px, cy_px) - 6

    # 1. Matrix Digital Rain / Random 0/1 frames (5 frames)
    for _ in range(5):
        frame = Image.new("RGB", (cols * char_width, rows * char_height), (13, 17, 23))
        draw = ImageDraw.Draw(frame)
        for y in range(rows):
            for x in range(cols):
                px = x * char_width + char_width / 2
                py = y * char_height + char_height / 2
                if ((px - cx_px)**2 + (py - cy_px)**2)**0.5 <= radius_px:
                    char = str(random.randint(0, 1))
                    color = (0, 255, 135) # Matrix Neon green
                    draw.text((x * char_width, y * char_height), char, font=font, fill=color)
        draw.ellipse([cx_px - radius_px, cy_px - radius_px, cx_px + radius_px, cy_px + radius_px], outline=(0, 255, 135), width=4)
        frames.append(frame)
        
    # 2. Transition frames (Matrix numbers morphing into actual profile picture colors)
    for i in range(num_transition_frames):
        frame = Image.new("RGB", (cols * char_width, rows * char_height), (13, 17, 23))
        draw = ImageDraw.Draw(frame)
        progress = i / (num_transition_frames - 1)
        
        for y in range(rows):
            for x in range(cols):
                px = x * char_width + char_width / 2
                py = y * char_height + char_height / 2
                if ((px - cx_px)**2 + (py - cy_px)**2)**0.5 <= radius_px:
                    if random.random() < progress:
                        char = target_chars[y][x]
                        color = target_colors[y][x]
                    else:
                        char = str(random.randint(0, 1))
                        color = (0, 255, 135)
                    draw.text((x * char_width, y * char_height), char, font=font, fill=color)
        draw.ellipse([cx_px - radius_px, cy_px - radius_px, cx_px + radius_px, cy_px + radius_px], outline=(0, 255, 135), width=4)
        frames.append(frame)
        
    # 3. Final profile image frames (hold for 15 frames)
    final_frame = frames[-1]
    for _ in range(15):
        frames.append(final_frame)

    # 4. Fade back to Matrix rain for continuous smooth looping (10 frames)
    for i in range(10):
        frame = Image.new("RGB", (cols * char_width, rows * char_height), (13, 17, 23))
        draw = ImageDraw.Draw(frame)
        progress = (9 - i) / 9.0
        
        for y in range(rows):
            for x in range(cols):
                px = x * char_width + char_width / 2
                py = y * char_height + char_height / 2
                if ((px - cx_px)**2 + (py - cy_px)**2)**0.5 <= radius_px:
                    if random.random() < progress:
                        char = target_chars[y][x]
                        color = target_colors[y][x]
                    else:
                        char = str(random.randint(0, 1))
                        color = (0, 255, 135)
                    draw.text((x * char_width, y * char_height), char, font=font, fill=color)
        draw.ellipse([cx_px - radius_px, cy_px - radius_px, cx_px + radius_px, cy_px + radius_px], outline=(0, 255, 135), width=4)
        frames.append(frame)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "binary_avatar.gif")
    print(f"Saving animated GIF to {out_path}...")
    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=120, loop=0)
    print(f"Successfully generated {len(frames)} frames into {out_path}!")

if __name__ == "__main__":
    create_animation()
