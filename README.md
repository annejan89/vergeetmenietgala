# Vergeet Mij Niet Gala 2026 — digitaal boekje

Twee varianten van het digitale boekje voor het gala van 6 oktober 2026
(Grand Ballroom, Hotel Okura Amsterdam).

| Bestand | Wat het is |
| --- | --- |
| `index.html` | keuzepagina tussen de twee varianten |
| `site.html` | **programmaboekje**: een pagina met het programma en alle kavels in een raster |
| `boekje.html` | **veilingboekje**: een spread per kavel, groot beeld en grote tekst, bladerbaar met een vaste inhoudsopgave |

Statische HTML, geen build-stap nodig. Lokaal bekijken:

```bash
python3 -m http.server 8000
```

## Mappen

- `assets/` — logo, bloempatroon, markeerstreep en golf-divider uit het design system
- `fonts/` — PP Frama Extralight (Playfair en Source Sans 3 komen van Google Fonts)
- `kavels/` — de kavelfoto's, bijgesneden naar 4:5
- `kavels.json` / `kavels.md` — de kavelgegevens
- `build-kavelfotos.py` — snijdt de foto's uit de PowerPoint bij tot 4:5, met het onderwerp in beeld
- `build-boekje.py` — genereert `boekje.html` uit `kavels.json`

De bronpresentatie (`.pptx`, 96 MB) en de onbewerkte foto's (`_orig/`) staan niet in
de repo. Zonder die bestanden draaien de twee build-scripts niet; de gegenereerde
HTML en de bijgesneden foto's staan er wel in.

## Let op

- PP Frama is een betaalde letter van Pangram Pangram; de licentie hoort bij de stichting.
- De foto's komen uit materiaal van de stichting en haar partners. Controleer de
  gebruiksrechten voordat deze repo of de pagina's publiek gedeeld worden.
