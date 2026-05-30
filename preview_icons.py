#!/usr/bin/env python3
"""Generiert Icon-Varianten zur Vorschau."""
from PIL import Image, ImageDraw
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def variant_a(color=(255,255,255,255), bg=(0,0,0,0), size=64):
    """Nur Lautsprecher-Outline, kein Hintergrundkreis."""
    img = Image.new("RGBA", (size, size), bg)
    d = ImageDraw.Draw(img)
    s = size
    W = color
    # Lautsprecher-Körper
    d.rectangle([int(s*.18), int(s*.38), int(s*.34), int(s*.62)], fill=W)
    d.polygon([
        (int(s*.34), int(s*.38)),
        (int(s*.34), int(s*.62)),
        (int(s*.54), int(s*.76)),
        (int(s*.54), int(s*.24)),
    ], fill=W)
    # Schallwelle
    lw = max(2, int(s*.05))
    d.arc([int(s*.56), int(s*.30), int(s*.72), int(s*.70)], -65, 65, fill=W, width=lw)
    d.arc([int(s*.62), int(s*.22), int(s*.82), int(s*.78)], -65, 65, fill=W, width=lw)
    return img

def variant_b(color=(255,255,255,255), bg=(30,30,30,255), size=64):
    """Dunkler Kreis + weißer Lautsprecher."""
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)
    s = size
    d.ellipse([1,1,s-1,s-1], fill=bg)
    inner = variant_a(color=color, bg=(0,0,0,0), size=size)
    img.paste(inner, mask=inner)
    return img

def variant_c(color=(255,255,255,255), bg=(0,0,0,0), size=64):
    """Nur Lautsprecher, einfacher/größer, keine Schallwellen."""
    img = Image.new("RGBA", (size, size), bg)
    d = ImageDraw.Draw(img)
    s = size
    W = color
    d.rectangle([int(s*.14), int(s*.36), int(s*.32), int(s*.64)], fill=W)
    d.polygon([
        (int(s*.32), int(s*.36)),
        (int(s*.32), int(s*.64)),
        (int(s*.58), int(s*.80)),
        (int(s*.58), int(s*.20)),
    ], fill=W)
    lw = max(2, int(s*.06))
    d.arc([int(s*.60), int(s*.28), int(s*.80), int(s*.72)], -65, 65, fill=W, width=lw)
    return img

def make_preview(variants, filename):
    """Legt alle Varianten nebeneinander auf dunklem Hintergrund."""
    size = 64
    pad  = 16
    n    = len(variants)
    w    = n * size + (n+1) * pad
    h    = size + 2 * pad
    bg   = Image.new("RGBA", (w, h), (50,50,50,255))
    for i, v in enumerate(variants):
        x = pad + i * (size + pad)
        bg.paste(v, (x, pad), mask=v)
    # 3x vergrößern zur Vorschau
    bg.resize((w*3, h*3), Image.NEAREST).save(filename)

if __name__ == "__main__":
    variants = [
        variant_a(),                        # A: nur Speaker weiß
        variant_b(),                        # B: dunkler Kreis + Speaker
        variant_c(),                        # C: großer Speaker kein Kreis
    ]
    out = "/tmp/icon_variants.png"
    make_preview(variants, out)
    print(f"Vorschau: {out}")
    print("Varianten: A=links, B=mitte, C=rechts")
