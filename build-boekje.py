"""Bouwt boekje.html: de veilingboekje-variant van de site.

Leest kavels.json (uit de PowerPoint) en zet er een bladerbaar boekje van:
een spread per kavel, groot beeld, grote tekst, en een inhoudsopgave die
meescrollt. Draaien: python3 build-boekje.py
"""
import html
import json
import os

KAVELS = json.load(open("kavels.json"))

# extra beelden per kavel; zonder regel hieronder is het kavels/<id>.jpg
FOTOS = {
    "k05": ["kavels/k05s1.jpg", "kavels/k05s2.jpg", "kavels/k05s3.jpg"],
    "k10": ["kavels/k10.jpg", "kavels/k10s3.jpg", "kavels/k10s2.jpg", "kavels/k10s4.jpg"],
}
BIJSCHRIFT = {
    "kavels/k05s1.jpg": "Huize Welgelegen in ARTIS",
    "kavels/k05s2.jpg": "Een luipaard in ARTIS",
    "kavels/k05s3.jpg": "Zebra en giraffes in ARTIS",
    "kavels/k10.jpg": "Landhuishotel De Bloemenbeek",
    "kavels/k10s3.jpg": "Het landgoed met feesttent vanuit de lucht",
    "kavels/k10s2.jpg": "De helikopter waarmee u naar Zeeland vliegt",
    "kavels/k10s4.jpg": "Inter Scaldes vanuit de lucht",
}

PROGRAMMA = [
    ("17:30", "Ontvangst",
     "Aanvang van de avond in de foyer van de Grand Ballroom met champagne en amuses."),
    ("18:00", "Deuren Grand Ballroom geopend",
     "Vanaf dat moment nodigen wij u uit om plaats te nemen aan uw tafel."),
    ("18:15", "Offici&euml;le start",
     "U geniet van een 5-gangendiner, bereid door de top Michelinsterrenchefs van Nederland. "
     "Tussen de gangen door wordt u meegenomen in prachtige verhalen en verrast met "
     "spectaculaire optredens."),
    ("23:30", "Afsluiting",
     "Een stijlvolle afsluiting van een prachtige en waardevolle avond."),
]

SPELREGELS = [
    "Bordje omhoog tot de veilingmeester u ziet",
    "Samen bieden met de tafel mag",
    "Bij de hamerslag is het kavel van u",
    "De factuur volgt na de avond",
]

HART = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 '
        '5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.29 '
        '1.49 4.04 3 5.5l7 7Z"/></svg>')

e = lambda s: html.escape(s, quote=True)


def fotos_van(k):
    lijst = FOTOS.get(k["id"], [f"kavels/{k['id']}.jpg"])
    return [p for p in lijst if os.path.exists(p)]


def beeld_blok(k):
    fotos = fotos_van(k)
    if not fotos:
        return ('<figure class="spread-beeld">'
                '<div class="beeld beeld--leeg"></div>'
                '<figcaption>Beeld volgt</figcaption></figure>')
    if len(fotos) == 1:
        bij = BIJSCHRIFT.get(fotos[0], k["titel"])
        return (f'<figure class="spread-beeld"><div class="beeld">'
                f'<img src="{fotos[0]}" alt="{e(k["titel"])}" loading="lazy"></div>'
                f'<figcaption>{e(bij)}</figcaption></figure>')
    imgs = "".join(
        f'<img src="{p}" alt="{e(BIJSCHRIFT.get(p, k["titel"]))}"'
        f'{" class=\"is-on\"" if i == 0 else ""} loading="lazy">'
        for i, p in enumerate(fotos))
    return (f'<figure class="spread-beeld"><div class="beeld beeld--slider" data-slider>{imgs}'
            f'<div class="beeld-dots" role="tablist" aria-label="Beelden bij dit kavel"></div>'
            f'</div><figcaption data-bijschrift>{e(BIJSCHRIFT.get(fotos[0], k["titel"]))}</figcaption>'
            f'</figure>')


def spread(k, i):
    incl = ""
    if k["bullets"]:
        lis = "".join(f"<li>{e(b)}</li>" for b in k["bullets"])
        incl = f'<div class="incl"><p class="incl-t">Inclusief</p><ul>{lis}</ul></div>'
    meta = f'<p class="spread-meta">{e(k["meta"])}</p>' if k["meta"] else ""
    kant = "spread--rechts" if i % 2 else "spread--links"
    return f'''<section class="spread {kant}" id="kavel-{k['id']}" data-kavel="{k['id']}" data-num="{e(k['num'])}" data-titel="{e(k['titel'])}">
  <div class="spread-in">
    {beeld_blok(k)}
    <div class="spread-tekst">
      <p class="spread-num"><span>Kavel</span> {e(k['num'])}</p>
      <h2>{e(k['titel'])}</h2>
      <p class="lead">{e(k['intro'])}</p>
      {incl}
      {meta}
      <p class="spread-door"><span>Aangeboden door</span>{e(k['aanbieder'])}</p>
      <button class="hart" data-fav="{k['id']}" aria-label="Zet kavel {e(k['num'])} op mijn lijst">{HART}<span>Op mijn lijst</span></button>
    </div>
  </div>
</section>'''


def toc_regel(k):
    return (f'<li><a href="#kavel-{k["id"]}" data-toc="{k["id"]}">'
            f'<span class="toc-num">{e(k["num"])}</span>'
            f'<span class="toc-titel">{e(k["titel"])}</span>'
            f'<span class="toc-hart" aria-hidden="true">{HART}</span></a></li>')


def bouw():
    spreads = "\n\n".join(spread(k, i) for i, k in enumerate(KAVELS))
    toc = "\n".join(toc_regel(k) for k in KAVELS)
    programma = "\n".join(
        f'      <li><span class="pg-t">{t}</span><div><h3>{kop}</h3><p>{tekst}</p></div></li>'
        for t, kop, tekst in PROGRAMMA)
    regels = "\n".join(
        f'      <li><b>{n}</b>{e(r)}</li>' for n, r in enumerate(SPELREGELS, 1))

    return TEMPLATE.format(spreads=spreads, toc=toc, programma=programma,
                           regels=regels, aantal=len(KAVELS))


TEMPLATE = '''<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Veilingboekje Vergeet Mij Niet Gala</title>
<meta name="description" content="Het veilingboekje van het Vergeet Mij Niet Gala op 6 oktober 2026: het programma en alle kavels van de veiling.">
<link rel="icon" href="assets/logo-geel.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair:ital,wght@0,400;0,500;1,400&family=Source+Sans+3:ital,wght@0,200..700;1,300&display=swap" rel="stylesheet">
<style>
@font-face{{font-family:'PP Frama';src:url('fonts/PPFrama-Extralight.otf') format('opentype');font-weight:200;font-style:normal;font-display:swap}}

:root{{
  --geel:#fbd242; --geel-licht:#fce180; --ink:#27251c;
  --beige:#f6f4eb; --beige-donker:#efede4;
  --blauw:#d2edff; --wit:#fff;
  --ink-60:#27251c99; --ink-40:#27251c66; --lijn:#0000001a; --lijn-2:#27251c33;
  --op-donker:rgba(246,244,235,.7);
  --toc:320px; --balk:64px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
body{{background:var(--beige);color:var(--ink);font-family:'Source Sans 3',system-ui,sans-serif;
  font-weight:300;font-size:19px;line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
img{{display:block;max-width:100%}}
a{{color:inherit}}
h1,h2,h3{{font-family:Playfair,Georgia,serif;font-weight:500;line-height:1.05;text-wrap:balance}}
p{{text-wrap:pretty}}
:focus-visible{{outline:2px solid var(--ink);outline-offset:3px}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}

/* inhoudsopgave, vast in beeld op desktop */
.toc{{position:fixed;left:0;top:0;bottom:0;width:var(--toc);z-index:40;display:flex;flex-direction:column;
  background:var(--ink);color:var(--beige);padding:28px 0 20px}}
.toc-kop{{display:flex;align-items:center;gap:12px;padding:0 28px 20px;border-bottom:1px solid rgba(246,244,235,.18)}}
.toc-kop img{{width:44px;height:44px;object-fit:contain}}
.toc-kop b{{display:block;font-family:Playfair,serif;font-weight:500;font-size:19px}}
.toc-kop span{{display:block;font-size:14px;color:var(--op-donker);text-transform:uppercase;letter-spacing:.1em}}
.toc-lijst{{list-style:none;overflow-y:auto;padding:12px 0 8px;flex:1;scrollbar-width:thin}}
.toc-lijst a{{display:grid;grid-template-columns:38px 1fr 18px;align-items:baseline;gap:10px;
  padding:9px 28px;text-decoration:none;font-size:16px;color:var(--op-donker);transition:color .2s,background .2s}}
.toc-lijst a:hover{{color:var(--beige);background:rgba(246,244,235,.06)}}
.toc-num{{font-family:'PP Frama','Source Sans 3',sans-serif;font-weight:200;font-size:20px;color:var(--geel)}}
.toc-titel{{line-height:1.3}}
.toc-hart{{width:13px;opacity:0;align-self:center}}
.toc-hart svg{{width:13px;height:13px;fill:var(--geel);stroke:var(--geel)}}
.toc-lijst a.is-fav .toc-hart{{opacity:1}}
.toc-lijst a.is-nu{{color:var(--beige);background:rgba(251,210,66,.14);box-shadow:inset 3px 0 0 var(--geel)}}
.toc-voet{{padding:14px 28px 0;border-top:1px solid rgba(246,244,235,.18);font-size:14px;color:var(--op-donker)}}
.toc-voet a{{color:var(--geel)}}

/* bladwijzer: de balk onderaan */
.balk{{position:fixed;left:var(--toc);right:0;bottom:0;height:var(--balk);z-index:45;display:flex;align-items:center;
  justify-content:center;gap:20px;background:rgba(246,244,235,.94);backdrop-filter:blur(8px);border-top:1px solid var(--lijn)}}
.balk button{{width:44px;height:44px;display:grid;place-items:center;background:transparent;border:1px solid var(--lijn-2);
  cursor:pointer;color:var(--ink);transition:background .2s,border-color .2s}}
.balk button:hover{{background:var(--lijn)}}
.balk button[disabled]{{opacity:.3;cursor:default}}
.balk button svg{{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6}}
.balk-tel{{min-width:15ch;text-align:center;font-size:16px;color:var(--ink-60);font-variant-numeric:tabular-nums}}
#toc-knop{{display:none}}

.blad{{margin-left:var(--toc);padding-bottom:var(--balk)}}
.in{{max-width:1120px;margin:0 auto;padding:0 clamp(20px,4vw,56px)}}

/* omslag */
.omslag{{background:var(--blauw);color:var(--ink);padding:clamp(72px,14vh,140px) 0 clamp(64px,12vh,120px);position:relative;overflow:hidden}}
.omslag .in{{position:relative}}
.omslag-bloem{{position:absolute;right:-60px;top:-60px;width:min(420px,45vw);opacity:.2;pointer-events:none}}
.omslag-logo{{width:clamp(96px,11vw,148px);height:auto;margin-bottom:clamp(28px,4vh,48px)}}
.omslag-lbl{{color:var(--ink-60);font-size:16px;text-transform:uppercase;letter-spacing:.12em}}
.omslag h1{{margin:20px 0 28px;font-size:clamp(44px,7vw,92px);color:var(--ink);max-width:14ch}}
.omslag .datum{{font-family:'PP Frama','Source Sans 3',sans-serif;font-weight:200;
  font-size:clamp(56px,13vw,180px);line-height:1;color:var(--ink);letter-spacing:.01em}}
.omslag p.plaats{{margin-top:20px;font-size:clamp(19px,2vw,26px);max-width:34ch}}
.golf{{display:block;width:100%;height:clamp(28px,4vw,52px)}}

/* pagina's */
.pagina{{padding:clamp(64px,11vh,132px) 0}}
.pagina--wit{{background:var(--wit)}}
.pagina--beige2{{background:var(--beige-donker)}}
.kop-lbl{{font-size:16px;text-transform:uppercase;letter-spacing:.12em;color:var(--ink-60)}}
.pagina h2{{font-size:clamp(34px,5vw,64px);margin-top:14px}}
.streep{{display:block;height:12px;width:min(340px,60%);margin-top:16px;
  background:url('assets/markeerstreep-blauw.svg') left center/100% 100% no-repeat}}

.pg{{list-style:none;margin-top:clamp(36px,6vh,64px)}}
.pg li{{display:grid;grid-template-columns:1fr;gap:6px;padding:clamp(22px,3vh,34px) 0;border-top:1px solid var(--lijn)}}
.pg li:last-child{{border-bottom:1px solid var(--lijn)}}
.pg-t{{font-family:'PP Frama','Source Sans 3',sans-serif;font-weight:200;
  font-size:clamp(30px,4vw,46px);line-height:1;color:var(--ink-60)}}
.pg h3{{font-size:clamp(24px,2.8vw,34px);margin:6px 0 8px}}
.pg p{{max-width:62ch;font-size:clamp(18px,1.6vw,21px)}}
@media(min-width:900px){{.pg li{{grid-template-columns:200px 1fr;gap:40px;align-items:baseline}}}}

.regels{{list-style:none;display:grid;gap:18px 40px;margin-top:clamp(32px,5vh,56px)}}
.regels li{{display:flex;gap:16px;align-items:baseline;font-size:clamp(18px,1.7vw,22px)}}
.regels b{{font-family:'PP Frama','Source Sans 3',sans-serif;font-weight:200;font-size:34px;color:var(--geel);
  line-height:1;min-width:1.2em}}
@media(min-width:900px){{.regels{{grid-template-columns:1fr 1fr}}}}

/* een kavel per spread */
.spread{{padding:clamp(56px,10vh,120px) 0;border-top:1px solid var(--lijn);scroll-margin-top:0}}
.spread:nth-child(even){{background:var(--wit)}}
.spread-in{{max-width:1240px;margin:0 auto;padding:0 clamp(20px,4vw,56px);display:grid;gap:clamp(28px,4vw,56px)}}
@media(min-width:960px){{
  .spread-in{{grid-template-columns:minmax(0,5fr) minmax(0,6fr);align-items:center}}
  .spread--rechts .spread-beeld{{order:2}}
}}
.spread-beeld figcaption{{margin-top:12px;font-size:15px;color:var(--ink-60)}}
.beeld{{position:relative;aspect-ratio:4/5;background:var(--beige-donker);overflow:hidden}}
.beeld img{{width:100%;height:100%;object-fit:cover}}
.beeld--leeg::after{{content:'';position:absolute;inset:0;background:url('assets/bloem-monogram.svg') center/96px no-repeat;opacity:.18}}
.beeld--slider img{{position:absolute;inset:0;opacity:0;transition:opacity 1.2s ease}}
.beeld--slider img.is-on{{opacity:1;animation:kenburns 7s linear both}}
.beeld--slider img.is-on:nth-child(2){{animation-name:kenburns-2}}
.beeld--slider img.is-on:nth-child(3){{animation-name:kenburns-3}}
.beeld--slider img.is-on:nth-child(4){{animation-name:kenburns-2}}
@keyframes kenburns{{from{{transform:scale(1) translate(0,0)}}to{{transform:scale(1.08) translate(-1.5%,-1%)}}}}
@keyframes kenburns-2{{from{{transform:scale(1.08) translate(1.5%,1%)}}to{{transform:scale(1) translate(0,0)}}}}
@keyframes kenburns-3{{from{{transform:scale(1) translate(1%,-1%)}}to{{transform:scale(1.08) translate(-1%,1%)}}}}
.beeld-dots{{position:absolute;left:14px;bottom:14px;z-index:2;display:flex;gap:6px}}
.beeld-dots button{{width:26px;height:4px;padding:0;border:0;cursor:pointer;background:rgba(255,255,255,.55)}}
.beeld-dots button.is-on{{background:var(--geel)}}

/* subtiele parallax: het beeld loopt iets trager dan de pagina.
   Scroll-driven animaties; browsers zonder view() tonen alles gewoon stil. */
@supports (animation-timeline: view()){{
  @media (prefers-reduced-motion:no-preference){{
    .spread-beeld{{animation:parallax-beeld linear both;animation-timeline:view();animation-range:entry 0% exit 100%}}
    .spread-tekst{{animation:parallax-tekst linear both;animation-timeline:view();animation-range:entry 10% exit 90%}}
    .omslag-bloem{{animation:parallax-bloem linear both;animation-timeline:view();animation-range:entry 0% exit 100%}}
    @keyframes parallax-beeld{{from{{transform:translateY(18px)}}to{{transform:translateY(-18px)}}}}
    @keyframes parallax-tekst{{from{{transform:translateY(8px)}}to{{transform:translateY(-8px)}}}}
    @keyframes parallax-bloem{{from{{transform:translateY(-24px)}}to{{transform:translateY(40px)}}}}

    /* naast elkaar op desktop: het beeld loopt voor, de tekst blijft iets achter.
       Het verschil tussen de twee is wat je ziet, niet de beweging zelf. */
    @media(min-width:960px){{
      .spread-beeld{{animation-name:parallax-beeld-groot}}
      .spread-tekst{{animation-name:parallax-tekst-groot;animation-range:entry 0% exit 100%}}
      @keyframes parallax-beeld-groot{{from{{transform:translateY(30px)}}to{{transform:translateY(-30px)}}}}
      @keyframes parallax-tekst-groot{{from{{transform:translateY(10px)}}to{{transform:translateY(-10px)}}}}
    }}
  }}
}}

.spread-num{{display:flex;align-items:baseline;gap:12px;font-family:'PP Frama','Source Sans 3',sans-serif;
  font-weight:200;font-size:clamp(40px,5vw,72px);line-height:1;color:var(--geel)}}
.spread-num span{{font-family:'Source Sans 3',sans-serif;font-weight:400;font-size:16px;
  text-transform:uppercase;letter-spacing:.12em;color:var(--ink-60)}}
.spread-tekst h2{{margin:18px 0 20px;font-size:clamp(32px,4.4vw,60px)}}
.lead{{font-size:clamp(20px,2.1vw,28px);line-height:1.45;max-width:36ch}}
.incl{{margin-top:clamp(24px,3vh,36px)}}
.incl-t{{font-size:15px;text-transform:uppercase;letter-spacing:.12em;color:var(--ink-60);margin-bottom:12px}}
.incl ul{{list-style:none;display:flex;flex-direction:column;gap:10px}}
.incl li{{position:relative;padding-left:26px;font-size:clamp(17px,1.6vw,20px);line-height:1.45;max-width:46ch}}
.incl li::before{{content:'';position:absolute;left:0;top:.62em;width:10px;height:10px;background:var(--geel)}}
.spread-meta{{margin-top:clamp(24px,3vh,34px);padding-top:16px;border-top:1px solid var(--lijn);
  font-size:15px;text-transform:uppercase;letter-spacing:.12em}}
.spread-door{{margin-top:14px;font-family:Playfair,serif;font-size:clamp(21px,2vw,28px);line-height:1.25}}
.spread-door span{{display:block;font-family:'Source Sans 3',sans-serif;font-size:14px;font-weight:400;
  text-transform:uppercase;letter-spacing:.12em;color:var(--ink-60);margin-bottom:4px}}
.hart{{margin-top:clamp(24px,3vh,34px);display:inline-flex;align-items:center;gap:10px;background:transparent;
  border:1px solid var(--lijn-2);padding:11px 20px;font-family:'Source Sans 3',sans-serif;font-size:16px;
  color:var(--ink);cursor:pointer;transition:background .2s,border-color .2s}}
.hart svg{{width:18px;height:18px;fill:none;stroke:var(--ink);stroke-width:1.7}}
.hart:hover{{background:var(--lijn)}}
.hart.is-fav{{background:var(--geel);border-color:var(--geel)}}
.hart.is-fav svg{{fill:var(--ink)}}

/* slot */
.slot{{background:var(--ink);color:var(--beige);padding:clamp(64px,12vh,128px) 0 clamp(48px,8vh,88px)}}
.slot h2{{color:var(--beige);font-size:clamp(32px,4.4vw,60px);max-width:18ch}}
.slot p{{margin-top:20px;max-width:52ch;font-size:clamp(18px,1.7vw,22px)}}
.slot-voet{{margin-top:clamp(40px,6vh,72px);padding-top:20px;border-top:1px solid rgba(246,244,235,.2);
  font-size:15px;color:var(--op-donker)}}

@media(max-width:959px){{
  :root{{--toc:0px;--balk:56px}}
  .toc{{position:fixed;left:0;right:0;top:auto;bottom:var(--balk);width:auto;max-height:70vh;padding:20px 0 12px;
    transform:translateY(102%);transition:transform .3s ease;box-shadow:0 -16px 40px rgba(0,0,0,.25)}}
  .toc.is-open{{transform:translateY(0)}}
  .toc-kop{{padding:0 20px 14px}}
  .toc-lijst a{{padding:11px 20px}}
  .toc-voet{{padding:12px 20px 0}}
  .balk{{left:0;justify-content:space-between;padding:0 12px;gap:10px}}
  #toc-knop{{display:inline-flex;align-items:center;gap:8px;width:auto;padding:0 16px;height:40px;font-family:'Source Sans 3',sans-serif;font-size:15px}}
  .balk button{{width:40px;height:40px}}
  .balk-tel{{min-width:0;font-size:14px}}
  .blad{{margin-left:0}}
}}
@media print{{
  .toc,.balk{{display:none}}
  .blad{{margin-left:0;padding:0}}
  .spread{{break-inside:avoid;page-break-after:always}}
}}
</style>
</head>
<body>

<nav class="toc" id="toc" aria-label="Inhoudsopgave">
  <div class="toc-kop">
    <img src="assets/logo-geel.png" alt="">
    <div><b>Veilingboekje</b><span>6 oktober 2026</span></div>
  </div>
  <ul class="toc-lijst">
    <li><a href="#programma" data-toc="programma"><span class="toc-num">&middot;</span><span class="toc-titel">Het programma</span><span class="toc-hart"></span></a></li>
    <li><a href="#veiling" data-toc="veiling"><span class="toc-num">&middot;</span><span class="toc-titel">Zo werkt de veiling</span><span class="toc-hart"></span></a></li>
{toc}
  </ul>
  <p class="toc-voet">Uw lijst telt <b id="fav-n">0</b> kavels. <a href="#top">Naar het begin</a></p>
</nav>

<main class="blad" id="top">

<section class="omslag" id="omslag" data-titel="Omslag">
  <div class="in">
    <img class="omslag-bloem" src="assets/bloem-patroon.svg" alt="">
    <img class="omslag-logo" src="assets/logo-geel.png" alt="Vergeet Mij Niet Gala">
    <p class="omslag-lbl">Het eerste culinaire gala voor Alzheimer Nederland</p>
    <h1>Het veilingboekje</h1>
    <p class="datum">06.10.2026</p>
    <p class="plaats">Grand Ballroom, Hotel Okura Amsterdam. {aantal} kavels, in een ronde, geveild door Mark Grol.</p>
  </div>
</section>
<svg class="golf" viewBox="0 0 1440 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0H1440V0Q1080 40 720 40Q360 40 0 0Z" fill="#D2EDFF"></path></svg>

<section class="pagina" id="programma" data-titel="Het programma">
  <div class="in">
    <p class="kop-lbl">Het programma</p>
    <h2>Van ontvangst tot afsluiting<span class="streep"></span></h2>
    <ol class="pg">
{programma}
    </ol>
  </div>
</section>

<section class="pagina pagina--beige2" id="veiling" data-titel="Zo werkt de veiling">
  <div class="in">
    <p class="kop-lbl">Zo werkt de veiling</p>
    <h2>Vier dingen en u kunt bieden<span class="streep"></span></h2>
    <ol class="regels">
{regels}
    </ol>
  </div>
</section>

{spreads}

<section class="slot" id="slot" data-titel="Tot slot">
  <div class="in">
    <h2>Dank dat u meebiedt</h2>
    <p>De volledige opbrengst van de veiling gaat naar Alzheimer Nederland, met bijzondere aandacht voor dementie op jonge leeftijd. Samen zorgen we ervoor dat niemand wordt vergeten.</p>
    <p class="slot-voet">Stichting Vergeet Mij Niet Gala &middot; Wittevrouwensingel 1, 3581 GA Utrecht &middot; vergeetmijnietgala.nl</p>
  </div>
</section>

</main>

<div class="balk">
  <button id="toc-knop" type="button" aria-expanded="false" aria-controls="toc">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>Kavels
  </button>
  <button id="vorige" type="button" aria-label="Vorige pagina">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>
  </button>
  <p class="balk-tel" id="teller">Omslag</p>
  <button id="volgende" type="button" aria-label="Volgende pagina">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>
  </button>
</div>

<script>
const paginas=[...document.querySelectorAll('.omslag, .pagina, .spread, .slot')];
const kavels=paginas.filter(p=>p.dataset.kavel);
const tocLinks=[...document.querySelectorAll('[data-toc]')];
const teller=document.getElementById('teller');
const vorige=document.getElementById('vorige');
const volgende=document.getElementById('volgende');
const tocKnop=document.getElementById('toc-knop');
const toc=document.getElementById('toc');
const favN=document.getElementById('fav-n');
const KEY='vmn-gala-shortlist';
let fav=new Set(JSON.parse(localStorage.getItem(KEY)||'[]').map(String));
let nu=0;

// bladeren
function naar(i){{
  nu=Math.max(0,Math.min(paginas.length-1,i));
  paginas[nu].scrollIntoView({{behavior:'smooth',block:'start'}});
}}
vorige.addEventListener('click',()=>naar(nu-1));
volgende.addEventListener('click',()=>naar(nu+1));
addEventListener('keydown',ev=>{{
  if(ev.target.matches('input,textarea')) return;
  if(ev.key==='ArrowRight'||ev.key==='PageDown'){{ev.preventDefault();naar(nu+1);}}
  if(ev.key==='ArrowLeft'||ev.key==='PageUp'){{ev.preventDefault();naar(nu-1);}}
}});

// waar ben ik: inhoudsopgave en teller volgen de pagina in beeld
function zetActief(el){{
  nu=paginas.indexOf(el);
  const k=el.dataset.kavel;
  const n=kavels.indexOf(el);
  teller.textContent = k ? 'Kavel '+el.dataset.num+' van {aantal}' : (el.dataset.titel||'');
  vorige.disabled = nu===0;
  volgende.disabled = nu===paginas.length-1;
  tocLinks.forEach(a=>a.classList.toggle('is-nu', a.dataset.toc===(k||el.id)));
  const actief=toc.querySelector('.is-nu');
  if(actief && innerWidth>=960){{
    const r=actief.getBoundingClientRect(), c=actief.closest('.toc-lijst').getBoundingClientRect();
    if(r.top<c.top+40||r.bottom>c.bottom-40) actief.scrollIntoView({{block:'center'}});
  }}
}}
const spion=new IntersectionObserver(es=>{{
  const zichtbaar=es.filter(e=>e.isIntersecting)
                    .sort((a,b)=>b.intersectionRatio-a.intersectionRatio)[0];
  if(zichtbaar) zetActief(zichtbaar.target);
}},{{threshold:[0,.2,.4,.6,.8],rootMargin:'-15% 0px -35% 0px'}});
paginas.forEach(p=>spion.observe(p));

// inhoudsopgave op mobiel
tocKnop.addEventListener('click',()=>{{
  const open=toc.classList.toggle('is-open');
  tocKnop.setAttribute('aria-expanded',open);
}});
toc.addEventListener('click',ev=>{{ if(ev.target.closest('a')) toc.classList.remove('is-open'); }});

// mijn lijst, gedeeld met de site
function sync(){{
  document.querySelectorAll('[data-fav]').forEach(b=>{{
    const aan=fav.has(b.dataset.fav);
    b.classList.toggle('is-fav',aan);
    b.setAttribute('aria-pressed',aan);
    b.querySelector('span').textContent = aan ? 'Op mijn lijst' : 'Zet op mijn lijst';
  }});
  tocLinks.forEach(a=>a.classList.toggle('is-fav',fav.has(a.dataset.toc)));
  favN.textContent=fav.size;
  try{{localStorage.setItem(KEY,JSON.stringify([...fav]));}}catch(e){{}}
}}
document.querySelectorAll('[data-fav]').forEach(b=>b.addEventListener('click',()=>{{
  const id=b.dataset.fav;
  fav.has(id)?fav.delete(id):fav.add(id);
  sync();
}}));
sync();

// beeldsliders met langzame zoom
const stil=matchMedia('(prefers-reduced-motion:reduce)');
document.querySelectorAll('[data-slider]').forEach(sl=>{{
  const beelden=[...sl.querySelectorAll('img')];
  if(beelden.length<2) return;
  const dots=sl.querySelector('.beeld-dots');
  const bij=sl.closest('figure').querySelector('[data-bijschrift]');
  let i=0,timer=null;
  beelden.forEach((b,n)=>{{
    const d=document.createElement('button');
    d.type='button'; d.setAttribute('aria-label','Beeld '+(n+1));
    d.className=n===0?'is-on':'';
    d.addEventListener('click',()=>{{toon(n);start();}});
    dots.appendChild(d);
  }});
  function toon(n){{
    i=n;
    beelden.forEach((b,k)=>{{ b.classList.remove('is-on'); if(k===n){{ void b.offsetWidth; b.classList.add('is-on'); }} }});
    [...dots.children].forEach((d,k)=>d.classList.toggle('is-on',k===n));
    if(bij) bij.textContent=beelden[n].alt;
  }}
  function start(){{
    stop();
    if(stil.matches) return;
    toon(i);                                  // zoom opnieuw starten bij het beeld dat nu in beeld komt
    timer=setInterval(()=>toon((i+1)%beelden.length),6000);
  }}
  function stop(){{ if(timer){{clearInterval(timer);timer=null;}} }}
  new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting?start():stop()),{{threshold:.25}}).observe(sl);
}});
</script>
</body>
</html>
'''

if __name__ == "__main__":
    open("boekje.html", "w").write(bouw())
    print("boekje.html geschreven:", len(KAVELS), "kavels")
