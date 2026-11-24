"""NoBorderAI: legg krok-tekst øverst og @noborderai-merke nederst på en Higgsfield-video.
Kjøres i Higgsfield-sandkassen (sandbox_exec), som har ffmpeg, Pillow og Montserrat.
Bruk: python3 finish.py inn.mp4 ut.mp4 "Krok-tekst"   (ingen emojier i teksten)"""
import sys, subprocess, os
from PIL import Image, ImageDraw, ImageFont
src, out, hook = sys.argv[1], sys.argv[2], sys.argv[3]
W, H = 1080, 1920
FB = "/usr/share/fonts/truetype/higgsfield/Montserrat-ExtraBold.ttf"
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
size = 74
while True:
    f = ImageFont.truetype(FB, size)
    words, lines, cur = hook.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= 940: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    if len(lines) <= 3 or size <= 50: break
    size -= 4
y = 230
for ln in lines:
    tw = d.textlength(ln, font=f)
    d.text(((W - tw) / 2, y), ln, font=f, fill=(255, 255, 255, 255), stroke_width=9, stroke_fill=(0, 0, 0, 255))
    y += int(size * 1.18)
fs = ImageFont.truetype(FB, 38)
tag = "@noborderai"
tw = d.textlength(tag, font=fs)
x0, y0 = (W - tw) / 2 - 26, 1700
d.rounded_rectangle([x0, y0, x0 + tw + 52, y0 + 64], radius=32, fill=(11, 11, 20, 170))
d.text((x0 + 26, y0 + 10), tag, font=fs, fill=(198, 255, 61, 255))
im.save("/tmp/ov.png")
cmd = ["ffmpeg", "-v", "error", "-y", "-i", src, "-i", "/tmp/ov.png",
       "-filter_complex", "[0:v]scale=1080:1920,setsar=1[v];[v][1:v]overlay=0:0,format=yuv420p[o]",
       "-map", "[o]", "-map", "0:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "30",
       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out + ".part.mp4"]
subprocess.run(cmd, check=True)
os.replace(out + ".part.mp4", out)
print("ok", out)
