"""Snijdt de kavelfoto's uit de PowerPoint bij tot 4:5, met het onderwerp in beeld.

MODE per kavel:
  ("crop", fx, fy)  snijd bij naar 4:5, met (fx, fy) als brandpunt (0..1)
  ("pad",)          schaal de hele foto in een 4:5 vlak, niets valt weg
Zonder regel hieronder: brandpunt uit gezichtsherkenning, anders het
zwaartepunt van de beeldenergie (zie detect()).
"""
import json, os
import cv2, numpy as np
from PIL import Image

AR = 0.8                      # 4:5
OUT_W = 900
PAD_BG = (239, 237, 228)      # donker-beige, gelijk aan de kaartachtergrond

MODE = {
    "k03a": ("pad",),         # rij miniatuurhuisjes loopt van rand tot rand
    "k15":  ("pad",),         # drie personen naast de beker
    "k06":  ("crop", 0.33, 0.62),   # auto zit links van het midden
    "k10s2": ("crop", 0.50, 0.50),  # helikopter: romp en cabine in beeld, staartboom valt weg
    "k10s3": ("crop", 0.50, 0.50),  # luchtfoto: landhuis boven, tent in het midden
    "k10s4": ("crop", 0.50, 0.50),  # Inter Scaldes: hele landhuis met terras in beeld
}

def detect(path):
    img = cv2.imread(path); h, w = img.shape[:2]
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = []
    for name in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"):
        c = cv2.CascadeClassifier(cv2.data.haarcascades + name)
        faces += [list(map(int, f)) for f in
                  c.detectMultiScale(g, 1.1, 7, minSize=(int(min(w, h) * 0.07),) * 2)]
    if faces:
        x0 = min(f[0] for f in faces); x1 = max(f[0] + f[2] for f in faces)
        y0 = min(f[1] for f in faces); y1 = max(f[1] + f[3] for f in faces)
        return (x0 + x1) / 2 / w, max(0.0, (y0 + y1) / 2 / h - 0.12)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3); gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    e = cv2.GaussianBlur(np.abs(gx) + np.abs(gy), (0, 0), max(w, h) / 60)
    e = e / (e.sum() + 1e-9)
    return float((e.sum(0) * np.arange(w)).sum()) / w, float((e.sum(1) * np.arange(h)).sum()) / h

def to_45(k):
    src = f"_orig/{k}.jpg"
    im = Image.open(src); w, h = im.size
    mode = MODE.get(k, ("crop",))
    if mode[0] == "pad":
        out_w = min(OUT_W, max(w, int(round(h * AR))))
        out_h = int(round(out_w / AR))
        canvas = Image.new("RGB", (out_w, out_h), PAD_BG)
        fit = im.copy(); fit.thumbnail((out_w, out_h), Image.LANCZOS)
        canvas.paste(fit, ((out_w - fit.width) // 2, (out_h - fit.height) // 2))
        crop, focus = canvas, None
    else:
        fx, fy = (mode[1], mode[2]) if len(mode) == 3 else detect(src)
        if w / h > AR:
            cw, ch = int(round(h * AR)), h
        else:
            cw, ch = w, min(h, int(round(w / AR)))
        left = max(0, min(w - cw, int(round(fx * w - cw / 2))))
        top = max(0, min(h - ch, int(round(fy * h - ch / 2))))
        crop = im.crop((left, top, left + cw, top + ch))
        if crop.width > OUT_W:
            crop = crop.resize((OUT_W, int(round(OUT_W / AR))), Image.LANCZOS)
        focus = [round(fx, 3), round(fy, 3)]
    crop.save(f"kavels/{k}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    return dict(mode=mode[0], focus=focus, out=list(crop.size), src=[w, h])

if __name__ == "__main__":
    os.makedirs("kavels", exist_ok=True)
    rep = {k[:-4]: to_45(k[:-4]) for k in sorted(os.listdir("_orig")) if k.endswith(".jpg")}
    json.dump(rep, open("_orig/_crops.json", "w"), indent=1)
    for k, v in rep.items(): print(k, v)
