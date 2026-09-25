"""Zet de kavelkaarten in index.html op basis van kavels.json.

De volgorde, de nummers en de minimale opbrengst komen uit kavels.json
(bijgewerkt naar de Word-update van 23-09). Draaien: python3 build-kavelkaarten.py
"""
import html
import json
import os
import re

KAVELS = json.load(open("kavels.json"))

# meerdere beelden bij een kavel: dan wordt het een slider met langzame zoom
FOTOS = {
    "k05": ["kavels/k05s1.jpg", "kavels/k05s2.jpg", "kavels/k05s3.jpg"],
    "k10": ["kavels/k10.jpg", "kavels/k10s3.jpg", "kavels/k10s2.jpg", "kavels/k10s4.jpg"],
}
ALT = {
    "kavels/k05s1.jpg": "Huize Welgelegen in ARTIS",
    "kavels/k05s2.jpg": "Een luipaard in ARTIS",
    "kavels/k05s3.jpg": "Zebra en giraffes in ARTIS",
    "kavels/k10.jpg": "Landhuishotel De Bloemenbeek",
    "kavels/k10s3.jpg": "Het landgoed met feesttent vanuit de lucht",
    "kavels/k10s2.jpg": "De helikopter waarmee u naar Zeeland vliegt",
    "kavels/k10s4.jpg": "Inter Scaldes vanuit de lucht",
}

HART = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 '
        '5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 '
        '1.49 4.04 3 5.5l7 7Z"/></svg>')

e = lambda s: html.escape(s, quote=True)


def bedrag(n):
    return f"&euro;&nbsp;{n:,}".replace(",", ".")


def foto(k):
    lijst = [p for p in FOTOS.get(k["id"], [f"kavels/{k['id']}.jpg"]) if os.path.exists(p)]
    if not lijst:
        return '<div class="kv-foto kv-foto--leeg"></div>'
    if len(lijst) == 1:
        return (f'<div class="kv-foto"><img src="{lijst[0]}" alt="{e(k["titel"])}" '
                f'loading="lazy"></div>')
    imgs = "".join(
        f'<img src="{p}" alt="{e(ALT.get(p, k["titel"]))}"'
        f'{" class=\"is-on\"" if i == 0 else ""} loading="lazy">'
        for i, p in enumerate(lijst))
    return (f'<div class="kv-foto kv-slider" data-slider>{imgs}'
            f'<div class="kv-dots" role="tablist" aria-label="Beelden bij dit kavel"></div></div>')


def kaart(k):
    incl = ""
    if k["bullets"]:
        lis = "".join(f"<li>{e(b)}</li>" for b in k["bullets"])
        incl = f'<div class="kv-incl"><p class="kv-incl-t">Inclusief</p><ul>{lis}</ul></div>'
    meta = f'<p class="kv-meta">{e(k["meta"])}</p>' if k.get("meta") else ""
    minimum = (f'<p class="kv-min"><span>Minimale opbrengst</span>{bedrag(k["minimum"])}</p>'
               if k.get("minimum") else "")
    return f'''      <article class="kv" data-id="{k['id']}">
        {foto(k)}
        <span class="kv-num">{e(k['num'])}</span>
        <button class="kv-open" data-open="{k['id']}" aria-label="Bekijk kavel {e(k['num'])}: {e(k['titel'])}"></button>
        <button class="kv-fav" aria-label="Zet kavel {e(k['num'])} op mijn lijst" data-fav="{k['id']}">{HART}</button>
        <div class="kv-body">
          <span class="kv-ronde">Kavel {e(k['num'])}</span>
          <h3>{e(k['titel'])}</h3>
          <p>{e(k['intro'])}</p>
          {incl}
          {meta}
          {minimum}
          <p class="kv-door"><span>Aangeboden door</span>{e(k['aanbieder'])}</p>
        </div>
      </article>'''


def bouw(pad="index.html"):
    grid = ('    <div class="kv-grid">\n'
            + "\n\n".join(kaart(k) for k in KAVELS)
            + '\n\n      <p class="kv-leeg" hidden>Nog niets op uw lijst. '
              'Tik op een hartje bij een kavel.</p>\n    </div>')
    s = open(pad).read()
    start = s.index('    <div class="kv-grid">')
    eind = s.index('\n  </div>\n</section>', start)
    s = s[:start] + grid + s[eind:]

    # het aantal kavels in de inleiding meelopen laten
    s = re.sub(r'<p>[A-Za-z]+ kavels, in een ronde\.',
               f'<p>{len(KAVELS)} kavels, in een ronde.', s)
    open(pad, "w").write(s)
    return len(KAVELS)


if __name__ == "__main__":
    print("kaarten geschreven:", bouw())
