# Foto til Jorda Rundt (pilot: 10 byer)

Spillet bruker tegninger som standard. Når `photos/photos.json` finnes, vises ekte foto over tegningen, med fotografens navn og lisens. Mangler et bilde, eller det ikke laster, vises tegningen.

Pilotbyene er Oslo, Paris, London, Roma, Kairo, Tokyo, New York, Rio, Sydney og Kappstaden. Hver by har ett byfoto og tre stedsfoto (samme rekkefølge som sightseeing i spillet).

## Slik gjør du det

1. Installer Pillow: `pip install pillow`
2. Finn forslag. Skriptet trenger kontaktinfo (nettadresse eller e-post), som Wikimedia krever:

   ```
   python3 tools/fetch_photos.py search --contact "https://github.com/BRUKERNAVN/jorda-rundt"
   ```

   Det søker på Wikimedia Commons, fjerner bilder med feil lisens og lager `tools/contact_sheet.html`. Det tar noen minutter fordi skriptet venter mellom hver forespørsel.
3. Åpne `tools/contact_sheet.html` i nettleseren. Trykk på ett bilde per rute (trykk igjen for å fjerne). Trykk **Last ned valg**, og flytt `photo_selection.json` til `tools/`.
4. Last ned og klargjør valgene:

   ```
   python3 tools/fetch_photos.py fetch --contact "https://github.com/BRUKERNAVN/jorda-rundt"
   ```

   Skriptet sjekker lisensen på nytt, lager små WebP-bilder i `photos/`, og skriver `photos/photos.json` og `photos/CREDITS.md`.
5. Sjekk resultatet lokalt (`python3 -m http.server 8000`), øk versjonen i `sw.js`, og commit og push.

Test at skriptet fungerer uten nett: `python3 tools/fetch_photos.py selftest`.

## Sjekkliste for den voksne

- Bildet viser riktig sted og landemerke.
- Dagslys. Ikke velg nattbilder, særlig ikke av Eiffeltårnet: lysshowet er vernet av opphavsrett.
- Ingen gjenkjennelige personer eller barn, og ingenting upassende.
- Åpne «Filside» ved tvil og les lisensen og beskrivelsen.
- Moderne bygg i land uten fri fotografering av bygninger (blant annet Frankrike, Belgia og Italia) kan være vernet. Velg heller gamle monumenter eller bilder Commons har akseptert, og sjekk filsiden.

## Lisenser

- Godkjent automatisk: CC0, offentlig eie, CC BY og CC BY-SA. Slå av BY-SA med `--no-sa`.
- Avvist automatisk: NC, ND, bare GFDL, og filer merket personality, insignia eller currency.
- Fotografiene har sine egne lisenser, uavhengig av spillets kode. Krediteringen vises på bildet og under Meny → Bildekreditter.

## Legge til flere byer

Legg til byen i `tools/photo_slots.json` med samme `id` som i spillet (se `CITIES` i `index.html`). Rutene `s0`–`s2` svarer til de tre severdighetene i `SIGHTS`, i samme rekkefølge. Kjør så `search` og `fetch` på nytt (bruk `--only id1,id2` for å begrense).

## Egenlagde illustrasjoner i stedet for foto
Hvis dere vil bruke tegneserie-bilder laget i ChatGPT i stedet for foto, se `tools/image_prompts/chatgpt_arbeidsflyt.md` og importer med `python3 tools/import_images.py --src generated`. Bildene får ingen fotokreditt. Foto og egenlagde bilder kan blandes. Det som importeres sist, erstatter bare de rutene det gjelder.
