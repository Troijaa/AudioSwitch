#!/usr/bin/env python3
from PIL import Image, ImageDraw

def draw_icon(size=64):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    W = (255, 255, 255, 255)

    # --- Lautsprecher-Körper ---
    # Rechteck (linker Teil)
    d.rectangle([int(s*0.12), int(s*0.35), int(s*0.32), int(s*0.65)], fill=W)
    # Dreieck (Trichter)
    d.polygon([
        (int(s*0.32), int(s*0.35)),
        (int(s*0.32), int(s*0.65)),
        (int(s*0.52), int(s*0.80)),
        (int(s*0.52), int(s*0.20)),
    ], fill=W)

    # --- Schallwelle (kurz) ---
    d.arc([int(s*0.54), int(s*0.32), int(s*0.66), int(s*0.68)],
          start=-70, end=70, fill=W, width=max(2, int(s*0.05)))

    # --- Pfeil links ---
    ax = int(s * 0.05)
    ay = int(s * 0.50)
    d.polygon([
        (ax,            ay),
        (ax + int(s*0.10), ay - int(s*0.12)),
        (ax + int(s*0.10), ay + int(s*0.12)),
    ], fill=W)

    # --- Pfeil rechts ---
    bx = int(s * 0.95)
    by = int(s * 0.50)
    d.polygon([
        (bx,            by),
        (bx - int(s*0.10), by - int(s*0.12)),
        (bx - int(s*0.10), by + int(s*0.12)),
    ], fill=W)

    return img

if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__), "audio_switch_icon.png")
    img = draw_icon(64)
    img.save(out)
    print(f"Icon saved: {out}")
