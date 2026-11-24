"""NoBorderAI – profilbilde og YouTube-banner. Alt tegnes prosedyrisk."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

INK   = (11, 11, 20)
INK2  = (22, 22, 36)
LIME  = (198, 255, 61)
PINK  = (255, 46, 136)
CYAN  = (41, 227, 255)
WHITE = (255, 255, 255)
BLACK_F = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
XB_F    = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
SB_F    = "/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf"

def F(path, size): return ImageFont.truetype(path, size)

def mascot(s):
    """Tegner en tullete robot ('doh-bot') på eget RGBA-lag, størrelse ca. 1.6s x 1.8s."""
    W, H = int(s * 1.9), int(s * 2.1)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = W // 2
    lw = max(4, int(s * 0.055))
    hw, hh = s * 0.78, s * 0.62          # halv bredde/høyde på hodet
    top = H * 0.36
    # antenne
    ax, ay = cx + s * 0.18, top - s * 0.42
    d.line([(cx + s * 0.05, top + 4), (ax, ay)], fill=INK, width=lw + 2)
    d.line([(cx + s * 0.05, top + 4), (ax, ay)], fill=WHITE, width=max(2, lw - 4))
    r = s * 0.13
    d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=PINK, outline=INK, width=lw)
    for k in range(6):                   # gnister
        a = -math.pi / 2 + (k - 2.5) * 0.45
        x1, y1 = ax + math.cos(a) * r * 1.5, ay + math.sin(a) * r * 1.5
        x2, y2 = ax + math.cos(a) * r * 2.3, ay + math.sin(a) * r * 2.3
        d.line([(x1, y1), (x2, y2)], fill=LIME if k % 2 else CYAN, width=max(3, lw - 2))
    # hode
    box = [cx - hw, top, cx + hw, top + hh * 2]
    d.rounded_rectangle([box[0] + lw * 1.2, box[1] + lw * 1.6, box[2] + lw * 1.2, box[3] + lw * 1.6],
                        radius=s * 0.32, fill=(0, 0, 0, 120))          # skygge
    d.rounded_rectangle(box, radius=s * 0.32, fill=LIME, outline=INK, width=lw)
    # ører/bolter
    for sx in (-1, 1):
        ex = cx + sx * (hw + s * 0.06)
        d.rounded_rectangle([ex - s * 0.09, top + hh * 0.7, ex + s * 0.09, top + hh * 1.3],
                            radius=s * 0.05, fill=CYAN, outline=INK, width=lw)
    # skjerm-ansikt
    m = s * 0.14
    face = [box[0] + m, box[1] + m, box[2] - m, box[3] - m * 1.1]
    d.rounded_rectangle(face, radius=s * 0.22, fill=INK2, outline=INK, width=lw)
    # øyne – ett stort, ett lite, pupiller som ser hver sin vei (doh)
    ey = top + hh * 0.78
    def eye(x, rr, px, py):
        d.ellipse([x - rr, ey - rr, x + rr, ey + rr], fill=WHITE, outline=INK, width=max(3, lw // 2))
        pr = rr * 0.48
        d.ellipse([x + px * rr - pr, ey + py * rr - pr, x + px * rr + pr, ey + py * rr + pr], fill=INK)
        d.ellipse([x + px * rr - pr * 0.35 + pr * 0.25, ey + py * rr - pr * 0.6,
                   x + px * rr + pr * 0.15 + pr * 0.25, ey + py * rr - pr * 0.1], fill=WHITE)
    eye(cx - s * 0.30, s * 0.22, -0.32, 0.25)
    eye(cx + s * 0.30, s * 0.15, 0.30, -0.30)
    # munn – stort glis med tunge
    my = top + hh * 1.30
    mw = s * 0.42
    d.chord([cx - mw, my - s * 0.22, cx + mw, my + s * 0.26], 0, 180, fill=WHITE, outline=INK, width=max(3, lw // 2))
    tx = cx + s * 0.12
    d.ellipse([tx - s * 0.13, my + s * 0.02, tx + s * 0.13, my + s * 0.34], fill=PINK, outline=INK, width=max(3, lw // 2))
    d.rectangle([tx - s * 0.13 + 3, my - 2, tx + s * 0.13 - 3, my + s * 0.12], fill=PINK)
    d.line([(cx - mw + 6, my + 1), (cx + mw - 6, my + 1)], fill=INK, width=max(3, lw // 2))
    d.line([(tx, my + s * 0.08), (tx, my + s * 0.22)], fill=(200, 20, 100), width=max(2, lw // 3))
    return im

def broken_frame(d, box, gap, col=WHITE, w=12, dash=None, rad=40):
    """Rektangulær ramme med et brudd (gap = (start, slutt) som andel av omkretsen)."""
    x0, y0, x1, y1 = box
    pts = []
    per = 2 * (x1 - x0) + 2 * (y1 - y0)
    N = 600
    for i in range(N + 1):
        t = i / N
        L = t * per
        if L < x1 - x0: p = (x0 + L, y0)
        elif L < (x1 - x0) + (y1 - y0): p = (x1, y0 + L - (x1 - x0))
        elif L < 2 * (x1 - x0) + (y1 - y0): p = (x1 - (L - (x1 - x0) - (y1 - y0)), y1)
        else: p = (x0, y1 - (L - 2 * (x1 - x0) - (y1 - y0)))
        pts.append((t, p))
    seg = []
    for t, p in pts:
        inside_gap = gap[0] <= t <= gap[1]
        on = not inside_gap
        if dash: on = on and (int(t * per / dash) % 2 == 0)
        if on: seg.append(p)
        else:
            if len(seg) > 1: d.line(seg, fill=col, width=w, joint="curve")
            seg = []
    if len(seg) > 1: d.line(seg, fill=col, width=w, joint="curve")

def shards(d, cx, cy, n, spread, size, rnd, cols=(WHITE, LIME, PINK, CYAN), ang=(-1.2, 0.4)):
    for _ in range(n):
        a = rnd.uniform(*ang); r = rnd.uniform(spread * 0.4, spread)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r
        sz = rnd.uniform(size * 0.4, size)
        rot = rnd.uniform(0, math.pi)
        poly = [(x + math.cos(rot + k * 2.2) * sz * (0.6 + 0.4 * (k % 2)),
                 y + math.sin(rot + k * 2.2) * sz * (0.6 + 0.4 * (k % 2))) for k in range(3)]
        d.polygon(poly, fill=rnd.choice(cols))

def bg(W, H, rnd):
    im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im)
    # myk glød
    glow = Image.new("RGB", (W, H), INK); g = ImageDraw.Draw(glow)
    g.ellipse([W * 0.15, H * 0.05, W * 0.85, H * 0.95], fill=(40, 20, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(W * 0.12))
    im = Image.blend(im, glow, 0.9)
    d = ImageDraw.Draw(im)
    # halvtone-prikker
    step = max(18, W // 70)
    for y in range(0, H, step):
        for x in range(0, W, step):
            dist = math.hypot((x - W / 2) / W, (y - H / 2) / H)
            r = max(0, 2.6 - dist * 5)
            if r > 0.4: d.ellipse([x - r, y - r, x + r, y + r], fill=(60, 50, 95))
    return im

# ---------------- profilbilde ----------------
def profile(out, S=2160):
    rnd = random.Random(7)
    im = bg(S, S, rnd); d = ImageDraw.Draw(im)
    # ramme (border) inne i sirkelen – brutt i øvre høyre hjørne der roboten bryter ut
    box = (S * 0.21, S * 0.27, S * 0.79, S * 0.81)
    broken_frame(d, box, gap=(0.14, 0.33), col=WHITE, w=int(S * 0.020), dash=S * 0.05)
    shards(d, S * 0.72, S * 0.27, 18, S * 0.11, S * 0.026, rnd, ang=(-1.3, 0.1))
    bot = mascot(S * 0.33).rotate(-10, resample=Image.BICUBIC, expand=True)
    im.paste(bot, (int(S / 2 - bot.width / 2 + S * 0.03), int(S / 2 - bot.height / 2 - S * 0.03)), bot)
    im = im.resize((S // 2, S // 2), Image.LANCZOS)
    im.save(out)
    return im

# ---------------- YouTube-banner ----------------
def banner(out, W=5120, H=2880):
    rnd = random.Random(3)
    im = bg(W, H, rnd); d = ImageDraw.Draw(im)
    sx0, sy0, sx1, sy1 = 1014, 1016, 4106, 1862          # trygg sone (x2)
    # maskot til venstre i trygg sone
    bot = mascot(340).rotate(-10, resample=Image.BICUBIC, expand=True)
    bx = sx0 + 30
    im.paste(bot, (int(bx), int((sy0 + sy1) / 2 - bot.height / 2 + 10)), bot)
    tx0 = bx + bot.width + 20
    # ordmerke tilpasset plassen som er igjen
    avail = sx1 - tx0 - 40
    size = 400
    while True:
        f = F(BLACK_F, size)
        w1 = d.textlength("NOBORDER", font=f); w2 = d.textlength("AI", font=f)
        if w1 + w2 * 1.05 + 40 <= avail: break
        size -= 6
    bb = d.textbbox((0, 0), "NOBORDER", font=f)
    capH = bb[3] - bb[1]
    tag_f = F(XB_F, int(size * 0.27)); sub_f = F(SB_F, int(size * 0.17))
    block_h = capH + 70 + int(size * 0.27)
    ty = (sy0 + sy1) / 2 - block_h / 2 - bb[1] + 20
    x = tx0 + 40
    fb = (x - 45, ty + bb[1] - 45, x + w1 + 30, ty + bb[3] + 45)
    broken_frame(d, fb, gap=(0.20, 0.41), col=WHITE, w=16, dash=56)
    d.text((x + 9, ty + 12), "NOBORDER", font=f, fill=(0, 0, 0))
    d.text((x, ty), "NOBORDER", font=f, fill=WHITE)
    ai = Image.new("RGBA", (int(w2 + 160), int(size * 1.5)), (0, 0, 0, 0)); da = ImageDraw.Draw(ai)
    da.text((52, 40), "AI", font=f, fill=(0, 0, 0, 255)); da.text((40, 28), "AI", font=f, fill=LIME)
    ai = ai.rotate(9, resample=Image.BICUBIC, expand=True)
    im.paste(ai, (int(x + w1 - 30), int(ty - size * 0.30)), ai)
    shards(d, x + w1 + 10, ty + bb[1] - 10, 20, 170, 30, rnd, ang=(-1.8, -0.2))
    tag = "AI, BUT WAY TOO FAR."
    yy = ty + bb[3] + 75
    d.text((x - 45, yy), tag, font=tag_f, fill=PINK)
    tw = d.textlength(tag, font=tag_f)
    d.text((x - 45 + tw + 40, yy + int(size * 0.27) - int(size * 0.17) - 4), "New videos every day", font=sub_f, fill=(200, 200, 225))
    # dekor utenfor trygg sone
    for _ in range(70):
        xx, yy2 = rnd.uniform(0, W), rnd.uniform(0, H)
        if sx0 - 80 < xx < sx1 + 80 and sy0 - 80 < yy2 < sy1 + 80: continue
        r = rnd.uniform(6, 22)
        d.ellipse([xx - r, yy2 - r, xx + r, yy2 + r], fill=rnd.choice([LIME, PINK, CYAN, (80, 70, 130)]))
    im = im.resize((W // 2, H // 2), Image.LANCZOS)
    im.save(out)
    return im

if __name__ == "__main__":
    import os
    os.makedirs("/home/claude/noborder/out", exist_ok=True)
    profile("/home/claude/noborder/out/noborderai-profilbilde.png")
    b = banner("/home/claude/noborder/out/noborderai-youtube-banner.png")
    # forhåndsvisning med trygg sone og sirkelutsnitt
    p = Image.open("/home/claude/noborder/out/noborderai-profilbilde.png").convert("RGB")
    mask = Image.new("L", p.size, 0); ImageDraw.Draw(mask).ellipse([0, 0, p.width, p.height], fill=255)
    circ = Image.new("RGB", p.size, (240, 240, 240)); circ.paste(p, (0, 0), mask)
    prev = b.copy(); dp = ImageDraw.Draw(prev)
    dp.rectangle([507, 508, 2053, 931], outline=(255, 0, 0), width=4)
    sheet = Image.new("RGB", (2560 + 1080 + 40, 1440), (240, 240, 240))
    sheet.paste(prev, (0, 0)); sheet.paste(circ, (2600, 0))
    small = circ.resize((110, 110), Image.LANCZOS); sheet.paste(small, (2600, 1120))
    sheet.resize((sheet.width // 2, sheet.height // 2)).save("/home/claude/noborder/out/preview.jpg", quality=88)
    print("ok")
