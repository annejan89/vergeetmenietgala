# Vergeet Mij Niet Gala 2026 — digitaal boekje

Het digitale programma- en kavelboekje voor het gala van 6 oktober 2026
(Grand Ballroom, Hotel Okura Amsterdam).

| Bestand | Wat het is |
| --- | --- |
| `index.html` | de site: het programma van de avond, de spelregels van de veiling en alle 18 kavels |
| `kavels.json` | de kavelgegevens: volgorde, nummer, tekst, aanbieder en minimale opbrengst |
| `build-kavelkaarten.py` | zet de kavelkaarten in `index.html` op basis van `kavels.json` |
| `build-kavelfotos.py` | snijdt de foto's uit de PowerPoint bij tot 4:5, met het onderwerp in beeld |

Statische HTML, geen build-stap nodig om te bekijken:

```bash
python3 -m http.server 8000
```

## Mappen

- `assets/` — logo, bloempatroon, markeerstreep en golf-divider uit het design system
- `fonts/` — PP Frama Extralight (Playfair en Source Sans 3 komen van Google Fonts)
- `kavels/` — de kavelfoto's, bijgesneden naar 4:5

De bronpresentatie (`.pptx`, 96 MB), het Word-document met de kavellijst en de
onbewerkte foto's (`_orig/`) staan niet in de repo.

## Inhoud bijwerken

De volgorde en de teksten komen uit `kavels.json`. Pas die aan en draai
`python3 build-kavelkaarten.py`; dat schrijft de kaarten opnieuw in `index.html`.

## Let op

- De contactgegevens van de inbrengers uit het Word-document staan bewust niet op de
  site. De minimale opbrengst per kavel staat er wel op.
- PP Frama is een betaalde letter van Pangram Pangram; de licentie hoort bij de stichting.
- De foto's komen uit materiaal van de stichting en haar partners. Controleer de
  gebruiksrechten voordat deze repo of de pagina's publiek gedeeld worden.
