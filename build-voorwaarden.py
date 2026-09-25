"""Zet de veilingvoorwaarden uit het Word-document in index.html.

Leest 'Veilingvoorwaarden compleet.docx' en schrijft de inhoud tussen de
markeringen <!-- voorwaarden --> en <!-- /voorwaarden --> in index.html.
Draaien: python3 build-voorwaarden.py
"""
import html
import re

import docx

BRON = "Veilingvoorwaarden compleet.docx"
PAGINA = "index.html"

e = lambda s: html.escape(s, quote=True)


def blokken():
    d = docx.Document(BRON)
    uit, lijst = [], []

    def sluit_lijst():
        if lijst:
            uit.append("<ul>" + "".join(f"<li>{e(x)}</li>" for x in lijst) + "</ul>")
            lijst.clear()

    for p in d.paragraphs:
        tekst = p.text.strip()
        if not tekst:
            continue
        stijl = p.style.name
        if stijl == "Heading 1":
            continue                                  # de titel staat al in de kop
        if stijl == "Heading 2":
            sluit_lijst()
            uit.append(f"<h3>{e(tekst)}</h3>")
        elif stijl.startswith("List"):
            lijst.append(tekst)
        else:
            sluit_lijst()
            regels = "<br>".join(e(r) for r in tekst.split("\n"))
            uit.append(f"<p>{regels}</p>")
    sluit_lijst()
    return "\n      ".join(uit)


def bouw():
    s = open(PAGINA).read()
    nieuw = f"<!-- voorwaarden -->\n      {blokken()}\n      <!-- /voorwaarden -->"
    s, n = re.subn(r"<!-- voorwaarden -->.*?<!-- /voorwaarden -->", nieuw, s, flags=re.S)
    if not n:
        raise SystemExit("markeringen <!-- voorwaarden --> niet gevonden in index.html")
    open(PAGINA, "w").write(s)
    return n


if __name__ == "__main__":
    bouw()
    print("veilingvoorwaarden geschreven")
