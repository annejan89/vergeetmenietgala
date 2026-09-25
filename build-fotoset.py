"""Zet de aangeleverde kavelfoto's klaar voor de site.

Per kavel: een hoofdfoto in 4:5 voor de kaart en vierkante beelden voor het
raster in de detailweergave. Het bijsnijden gebeurt op het onderwerp
(gezichtsherkenning, anders het zwaartepunt van de beeldenergie) via
build-kavelfotos.py.

Draaien: python3 build-fotoset.py   (vereist _orig/zip met het aangeleverde materiaal)
"""
import importlib.util
import json
import os

import cv2
import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None

spec = importlib.util.spec_from_file_location("bk", "build-kavelfotos.py")
bk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bk)

ZIP = "_orig/zip/Veilingkavels input (extern)"

# hoofdfoto (4:5) en rasterbeelden per kavel; het eerste bestand is de hoofdfoto
BRON = {
    "k17": ["Kavel - Krug/_01A2287.jpg", "Kavel - Krug/_01A1953.jpg",
            "Kavel - Krug/_01A2004.jpg", "Kavel - Krug/_01A2028.jpg",
            "Kavel - Krug/_01A2300.jpg"],
    "k07": ["Kavel - Da Vinci/Margo Reuten & Petro Kools 2.jpg",
            "Kavel - Da Vinci/Da Vinci tarbot kreeft 3.jpg",
            "Kavel - Da Vinci/Da Vinci asperges gepocheerd ei.jpg",
            "Kavel - Da Vinci/Ivo van der Bijl HR.JPG"],
    "k02": ["Kavel - koetsentocht Cor van Zadelhoff/Koetstocht langs de Vecht 2.jpg"],
    "k03a": ["Kavel - KLM/KLM Huisje Special - Rijksmuseum (1).jpeg",
             "Kavel - KLM/KLM Huisje Special - Rijksmuseum (2).jpeg",
             "Kavel - KLM/KLM Huisje Special - Rijksmuseum (3).jpeg",
             "Kavel - KLM/KLM Specials - overzicht FD.jpeg"],
    "k03b": ["Kavel - KLM/Vrij om te gebruiken/IMG_1872.jpeg",
             "Kavel - KLM/Vrij om te gebruiken/IMG_1873.jpeg",
             "Kavel - KLM/Vrij om te gebruiken/IMG_1874.jpeg",
             "Kavel - KLM/Vrij om te gebruiken/IMG_1875.jpeg"],
    "k04": ["Kavel - de Burgemeester x MC /8X0A1398.jpg",
            "Kavel - de Burgemeester x MC /8X0A1429.jpg",
            "Kavel - de Burgemeester x MC /8X0A6150.jpg",
            "Kavel - de Burgemeester x MC /8X0A6412.jpg"],
    "k12": ["Kavel -  Legends Lounge/W photography - www.willemijnbeekman.com-115.jpg",
            "Kavel -  Legends Lounge/W photography - www.willemijnbeekman.com-003.jpg",
            "Kavel -  Legends Lounge/W photography - www.willemijnbeekman.com-007.jpg",
            "Kavel -  Legends Lounge/W photography - www.willemijnbeekman.com-117.jpg"],
    "k13": ["Kavel -  Legends Lounge/W photography - www.willemijnbeekman.com-117.jpg",
            "Kavel -  Legends Lounge/W photography - www.willemijnbeekman.com-115.jpg",
            "Kavel -  Legends Lounge/W photography - www.willemijnbeekman.com-003.jpg"],
    "k15": ["Kavel - Champions Lounge/ChampionsLounge_07_08_2023_2.jpg"],
    "k06": ["Kavel - Racen Circuit Zandvoort/2026-09-02AB26191GPElite-ExclusiveTrackdayAssen-22.jpeg",
            "Kavel - Racen Circuit Zandvoort/LDDK-20250430-0097.jpg",
            "Kavel - Racen Circuit Zandvoort/2026-09-02AB26191GPElite-ExclusiveTrackdayAssen-78.jpeg",
            "Kavel - Racen Circuit Zandvoort/2026-09-02AB26191GPElite-ExclusiveTrackdayAssen-198.jpeg"],
    "k11": ["Kavel - Merlet x Werner Loens/Merlet.restaurant-20.jpg",
            "Kavel - Merlet x Werner Loens/LDDK-20260402-0159 - kopie.jpg",
            "Kavel - Merlet x Werner Loens/image003.jpg",
            "Kavel - Merlet x Werner Loens/image002.jpg"],
    "k01": ["Kavel - Jochem Myjer/Jochem_netalsof_LiggendSite_3417x1500_titel.jpg",
            "Kavel - Jochem Myjer/Jochem_netalsof_FB_Inst_post_1080x1080_3.jpg"],
    "k05": ["Kavel - Artis/Huize Welgelegen 1.PNG",
            "Kavel - Artis/Huize Welgelegen 5.jpg",
            "Kavel - Artis/_t Amsterdammetje(1).jpg"],
    "k10": ["Kavel - Bloemebeek x Inter Scaldes /AX0I5809.JPG",
            "Kavel - Bloemebeek x Inter Scaldes /INTER SCALDES 8-9-07-2027-01677.jpg",
            "Kavel - Bloemebeek x Inter Scaldes /INTER SCALDES 8-9-07-2027-01773.jpg",
            "Kavel - Bloemebeek x Inter Scaldes /INTER SCALDES 8-9-07-2027-02049.jpg"],
    "k08": ["Kavel - Diner VIP avond Masters/BEELD TE GEBRUIKEN MASTERS EXPO YVESKE_S KITCHEN/MASTERS EXPO 1.jpg",
            "Kavel - Diner VIP avond Masters/BEELD TE GEBRUIKEN MASTERS EXPO YVESKE_S KITCHEN/MASTERS EXPO 2.jpg",
            "Kavel - Diner VIP avond Masters/BEELD TE GEBRUIKEN MASTERS EXPO YVESKE_S KITCHEN/MASTERS EXPO 3.jpg",
            "Kavel - Diner VIP avond Masters/BEELD TE GEBRUIKEN MASTERS EXPO YVESKE_S KITCHEN/MASTERS EXPO 4.jpg",
            "Kavel - Diner VIP avond Masters/BEELD TE GEBRUIKEN MASTERS EXPO YVESKE_S KITCHEN/MASTERS EXPO 5.jpg"],
    "k16": ["Kavel 16 - Ramses Shaffy/Ramses Shaffy - Didi _ Special edition/Ramses Shaffy - Didi - plat.jpg",
            "Kavel 16 - Ramses Shaffy/Ramses Shaffy - Didi _ Special edition/Ramses Shaffy - Didi - spread 4.jpg",
            "Kavel 16 - Ramses Shaffy/Ramses Shaffy - Didi _ Special edition/Ramses Shaffy - Didi - spread 8.jpg",
            "Kavel 16 - Ramses Shaffy/Ramses Shaffy - Didi _ Special edition/Ramses Shaffy - Didi - spread 14.jpg"],
    "k09": ["Kavel -  Aan de Poel/8B3A9507.jpeg"],
}

# beelden die al eerder klaargezet zijn en in het raster mee mogen
EXTRA = {
    "k05": ["_orig/k05s2.jpg", "_orig/k05s3.jpg"],
    "k10": ["_orig/k10s3.jpg"],
    "k14": ["_orig/k14.jpg"],
    "k16": ["_orig/k16.jpg"],
}

UIT = "kavels"
HOOFD_BREED, VIERKANT = 900, 760


def laad(pad):
    im = Image.open(pad)
    im = ImageOps.exif_transpose(im).convert("RGB")
    im.thumbnail((2600, 2600), Image.LANCZOS)
    return im


def brandpunt(im):
    """Gezichten, anders het zwaartepunt van de beeldenergie."""
    arr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    h, w = arr.shape[:2]
    g = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
    faces = []
    for naam in ("haarcascade_frontalface_default.xml", "haarcascade_profileface.xml"):
        c = cv2.CascadeClassifier(cv2.data.haarcascades + naam)
        faces += [list(map(int, f)) for f in
                  c.detectMultiScale(g, 1.1, 7, minSize=(int(min(w, h) * 0.07),) * 2)]
    if faces:
        x0 = min(f[0] for f in faces); x1 = max(f[0] + f[2] for f in faces)
        y0 = min(f[1] for f in faces); y1 = max(f[1] + f[3] for f in faces)
        return (x0 + x1) / 2 / w, max(0.0, (y0 + y1) / 2 / h - 0.10)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, 3); gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, 3)
    e = cv2.GaussianBlur(np.abs(gx) + np.abs(gy), (0, 0), max(w, h) / 60)
    e = e / (e.sum() + 1e-9)
    return (float((e.sum(0) * np.arange(w)).sum()) / w,
            float((e.sum(1) * np.arange(h)).sum()) / h)


def snij(im, ar, breed, pad_uit):
    w, h = im.size
    fx, fy = brandpunt(im)
    if w / h > ar:
        cw, ch = int(round(h * ar)), h
    else:
        cw, ch = w, min(h, int(round(w / ar)))
    left = max(0, min(w - cw, int(round(fx * w - cw / 2))))
    top = max(0, min(h - ch, int(round(fy * h - ch / 2))))
    uit = im.crop((left, top, left + cw, top + ch))
    if uit.width > breed:
        uit = uit.resize((breed, int(round(breed / ar))), Image.LANCZOS)
    uit.save(pad_uit, "JPEG", quality=82, optimize=True, progressive=True)
    return uit.size


def pad_van(bron):
    return bron if bron.startswith("_orig/") else os.path.join(ZIP, bron)


if __name__ == "__main__":
    os.makedirs(UIT, exist_ok=True)
    overzicht = {}
    for kid in sorted(set(list(BRON) + list(EXTRA))):
        bronnen = [pad_van(b) for b in BRON.get(kid, [])]
        bronnen += [pad_van(b) for b in EXTRA.get(kid, [])]
        bronnen = [b for b in bronnen if os.path.exists(b)]
        if not bronnen:
            print(f"{kid}: geen bronbestanden"); continue
        beelden = []
        for i, bron in enumerate(bronnen):
            im = laad(bron)
            if i == 0:
                hoofd = f"{UIT}/{kid}.jpg"
                snij(im, 0.8, HOOFD_BREED, hoofd)      # 4:5 voor de kaart
                beelden.append(hoofd)
            vk = f"{UIT}/{kid}-v{i+1}.jpg"
            snij(im, 1.0, VIERKANT, vk)                 # vierkant voor het raster
            beelden.append(vk)
        overzicht[kid] = beelden
        print(f"{kid}: {len(bronnen)} bronnen -> hoofdfoto + {len(bronnen)} vierkant")
    json.dump(overzicht, open("_orig/_fotoset.json", "w"), indent=1)
