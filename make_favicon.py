#!/usr/bin/env python3
"""Draw favicon.ico — the same mark as the inline SVG icon in index.html.

The app's icon is an inline SVG data URI, which every current browser prefers.
favicon.ico is the fallback: it's what a browser fetches from the site root on
its own, what older ones use, and what a bookmark or a search result shows. The
two have to be the same picture, so this draws the SVG's geometry with Pillow
rather than hand-editing a binary nobody can review in a diff.

    python3 make_favicon.py

It also writes the INSTALL icons — the PNGs manifest.webmanifest and the
apple-touch-icon link name. Three rules, and they are the whole reason there
are four files rather than one:

- **favicon.ico and the manifest's `any` icons are ROUNDED.** Nothing masks
  them, so the corners have to be in the file.
- **The maskable icon is full bleed with square corners.** A launcher crops it
  to whatever outline it likes — a circle on a lot of Android ones — so anything
  in the corners is thrown away and rounding it would round a picture that is
  about to be rounded again. Nothing has to move for that crop: the safe zone is
  the centre disc of 80% of the width, radius 25.6 in this 64 viewport, and the
  furthest point of the mark — the round cap at (18,46), and its mirror at
  (46,46) — is 23.8 from the centre. Widen a bar or drop its base and re-check
  that number.
- **apple-touch-icon.png is SQUARE and opaque**, for the same reason in reverse:
  Apple applies its own corner radius, and a rounded source under that mask
  leaves a pale seam inside the curve.

The mark is what the app measures: three weeks of flow, side by side, one of
them a good week. It's the family shape — the midnight page as a rounded tile,
the soft disc in the bottom-left corner, one gradient stroke in the accent —
worn by Money Map, PAPTrack and Sprint Predictability too. Sprint
Predictability is its sibling and carries the same tile under a cycle; if the
family's shared parts change, change them in both.

Everything is drawn at 8x and reduced with Lanczos, which is what gives the
16px version clean edges. Keep the shapes here in step with the SVG in
index.html if that ever changes.
"""

from PIL import Image, ImageDraw

# The mark, in the SVG's own 64x64 coordinates.
BG = (10, 14, 26, 255)          # #0a0e1a — midnight, the default theme's page
GLOW = (20, 28, 51, 255)        # #141c33 — the darker disc in the corner
GRAD_FROM = (129, 140, 248)     # #818cf8 — midnight's accent
GRAD_TO = (165, 180, 252)       # #a5b4fc
GRAD_AXIS = ((10, 52), (54, 12))                  # where the gradient runs

BAR_BASE = 46                   # every bar stands on this line
BAR_WIDTH = 8
BARS = [(18, 30), (32, 18), (46, 25)]   # (x, top) — three weeks, one of them good

SCALE = 8                       # supersample, then reduce
SIZES = [16, 32, 48, 64, 128, 256]

# The INSTALL icons, named by manifest.webmanifest and by index.html's
# apple-touch-icon link, and cached by sw.js. Renaming one means editing all
# three of those as well as this line. 192 and 512 are the two sizes Chrome asks
# for when it offers "Install app"; 180 is Apple's.
PWA_ICONS = [(192, 'icon-192.png'), (512, 'icon-512.png')]
MASKABLE = (512, 'icon-512-maskable.png')
APPLE = (180, 'apple-touch-icon.png')


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient_at(point):
    """Colour for a point, projected onto the gradient's axis."""
    (x0, y0), (x1, y1) = GRAD_AXIS
    dx, dy = x1 - x0, y1 - y0
    span = dx * dx + dy * dy
    t = ((point[0] - x0) * dx + (point[1] - y0) * dy) / span
    return lerp(GRAD_FROM, GRAD_TO, min(1.0, max(0.0, t)))


def stamp(d, pts, width):
    """A gradient stroke, drawn by stamping a circle at every step.

    Round caps come free that way: a bar drawn as a coloured rectangle would
    have to be capped separately, and a stroke drawn in pieces would show a
    seam wherever two pieces meet.
    """
    r = width / 2
    for x, y in pts:
        d.ellipse([(x - r) * SCALE, (y - r) * SCALE,
                   (x + r) * SCALE, (y + r) * SCALE],
                  fill=gradient_at((x, y)) + (255,))


def bar_points(x, top, base, steps=400):
    return [(x, top + (base - top) * s / steps) for s in range(steps + 1)]


def build(rounded=True):
    n = 64 * SCALE
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, n, n], fill=BG)
    # the soft disc bottom-left, the way the SVG has it
    d.ellipse([(14 - 20) * SCALE, (52 - 20) * SCALE,
               (14 + 20) * SCALE, (52 + 20) * SCALE], fill=GLOW)

    for x, top in BARS:
        stamp(d, bar_points(x, top, BAR_BASE), BAR_WIDTH)

    if not rounded:
        # Full bleed, for the maskable icon and for Apple's — see the docstring.
        # The glow is drawn to overflow the tile, so without the mask below it
        # needs cutting back to it, which dropping the alpha channel does.
        return img.convert('RGB')
    # Round the corners with an alpha mask. The SVG leaves the disc square at
    # the edges; an icon reads better rounded, and this is the file that ends
    # up on a bookmarks bar.
    mask = Image.new('L', (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1],
                                           radius=14 * SCALE, fill=255)
    img.putalpha(mask)
    return img


def main():
    art = build()
    frames = [art.resize((s, s), Image.LANCZOS) for s in SIZES]
    frames[-1].save('favicon.ico', format='ICO',
                    sizes=[(s, s) for s in SIZES])
    print('favicon.ico written at ' + ', '.join(f'{s}px' for s in SIZES))

    square = build(rounded=False)
    for size, name in PWA_ICONS:
        art.resize((size, size), Image.LANCZOS).save(name, format='PNG', optimize=True)
        print(f'{name} written (rounded — nothing masks a `purpose: any` icon)')
    size, name = APPLE
    # No alpha channel: Apple asks for an opaque icon, and every pixel of this
    # one is opaque already — carrying the channel would only invite a renderer
    # to composite it against something.
    square.resize((size, size), Image.LANCZOS).save(name, format='PNG', optimize=True)
    print(f'{name} written (square, opaque — Apple masks it)')
    size, name = MASKABLE
    square.resize((size, size), Image.LANCZOS).save(name, format='PNG', optimize=True)
    print(f'{name} written (full bleed — the launcher supplies the shape)')

    print('Now bump the ?v= on both favicon.ico references in index.html — '
          'browsers cache an icon for a long time and will keep showing the old '
          'one otherwise. The install icons are versioned by sw.js\'s CACHE '
          'constant instead; bump that too.')


if __name__ == '__main__':
    main()
