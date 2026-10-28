# Jorda Rundt 🧭

Et reisespill for barn (ca. 1.–4. klasse). Reis til 70 byer på alle verdensdeler, ta småjobber for å tjene til neste billett, og lær om land, flagg og landemerker underveis.

**Mål:** besøk alle seks verdensdeler og kom hjem til Oslo på kortest mulig tid. Det finnes også stempeljakt og sertifikatjakt.

- 70 byer med egen illustrasjon, tre spørsmål med bilder og en fakta-setning
- Landkart med landegrenser, landnavn og flagg
- 22 minispill: regning, treffsikkerhet, par, rekkefølge, timing, sortering, fang, finn på kartet, flagg, pakk kofferten, postkort, og de nye yrkesspillene koffertminne (hotellportier), kaffebestillinger (barista), lederfugl (fuglekikker), plantelogikk (gartner), rytme (trommeslager) ansikter og navn (resepsjonist) og trikkestyring med sporvekslere (trikkefører), kortest vei (pizzabud), finn stien (fjellguide), halv oppskrift (bakerlærling og kokk) og beste kjøp (basarselger og tepphandler)
- To nivåer: Turist og Globetrotter
- Alle 55 postkort er tegnet i samme tegneserie-stil (kontur, smilende sol, skyer). Stilen styres sentralt av hjelpefunksjonene `A.r`, `A.p`, `A.c`, `A.e`, `A.d` og `A.t` i `index.html`
- Yrkesquiz: alle 78 yrker har en kort quiz om yrket (3 spørsmål med emoji-svar og forklaring). Når en jobb startes, trekkes det tilfeldig (50/50) om spilleren får quizen eller yrkets minispill. Spørsmålene ligger i konstanten `PQ` i `index.html`
- 15 nye byer (Asia, Sør-Amerika og Afrika): Hanoi, Petra, Colombo, Samarkand, Bohol, Cartagena, Uyuni, Torres del Paine, Galápagos, Iguazú, Dakar, Timbuktu, Lalibela, Kigali og Sossusvlei. Hver by har postkort, tre severdigheter, tre spørsmål, lokal jobb, yrkesquiz og suvenir. Bildene (nr. 173–217) ligger i `photos/`
- Fullskjermskart: trykk på kartet (eller «Større kart») for å åpne det i fullskjerm. Man kan dra, knipe eller bruke ＋ og － for å zoome, hoppe til en region, trykke på en by og reise direkte derfra. Bynavnene plasseres automatisk så de ikke overlapper (`placeLabels()` i `index.html`)
- Reisekart: når spilleren reiser, zoomer kartet fra det lille kartet til full skjerm og kameraet følger fly, tog eller båt. Fly er raskest, båt middels og tog tregest, og «Hopp over» fører deg rett frem. Hastigheten styres i `travelDur()` i `index.html`
- Spillerplasser og lagring: tre spillerplasser på samme enhet, hver med navn og egen reise. Spillet lagres bare når spilleren sjekker inn på et hotell (eller trykker «Lagre nå» i hotellet), og plassen tømmes når målet er nådd. Lagringen ligger i nettleserens lagring på enheten
- Hall of Fame: etter «Jorda rundt» skriver spilleren navnet sitt og havner i en liste som kan sorteres på tid, penger tjent, land og sertifikater. Listen lagres på enheten (nettleserens lagring) og kan tømmes fra Hall of Fame-visningen
- Tegneserie-design: «reisedagbok med klistremerker» med reven Fia som guide, tykke konturer, varme farger og skrifter som fungerer uten nett
- Spørsmålsbank som blander håndskrevne spørsmål, spørsmål laget av sightseeing-faktaene og genererte kart- og flaggspørsmål, med forklaring etter hvert svar og vern mot gjentakelser
- Innsjekking på hotellet (to spørsmål og et kartspill der du finner byer på tid) som avgjør hvilke jobber i avisen du kan søke på
- Bilder av byer og severdigheter: egenlagde tegneserie-illustrasjoner (alle 217 bilder er på plass: 172 for de første 55 byene og 45 for de 15 nye er på plass i `photos/`, laget i ChatGPT etter `tools/image_prompts/`) eller foto fra Wikimedia Commons. Tegningene i koden brukes som reserve, så spillet fungerer uten bildene
- Foto fra Wikimedia Commons (pilot: 10 byer) med kreditering, via skript og kontaktark. Tegningene brukes som reserve. Se `tools/README_photos.md`
- Byhub med seks ikon-ruter, og sightseeing med tre severdigheter per by (hver gir et hint i byquizen)
- Jobbavis med tre annonser per by (enkel, vanlig og krevende), lønnsklasser og sertifikater som gjelder i alle byer
- Hotell (billig eller dyrt), telefonkiosk der du kan ringe hjem om penger, og souvenirhandel der du kjøper billig og selger dyrt
- Enspiller, uten nettspill og uten sporing. Fungerer uten nett etter første besøk (PWA)

## Spill

Spillet ligger her: `https://BRUKERNAVN.github.io/jorda-rundt/` (bytt ut BRUKERNAVN og repo-navn).

**På iPhone/iPad:** åpne adressen i Safari, trykk Del og velg *Legg til på Hjem-skjerm*.

## Kjøre lokalt

Ingen bygging trengs. Start en enkel webserver i mappen og åpne siden:

```
python3 -m http.server 8000
# åpne http://localhost:8000
```

Å åpne `index.html` direkte fra disk fungerer også, men uten offline-støtte.

## Filer

| Fil | Hva |
|---|---|
| `index.html` | Hele spillet (HTML, CSS og JavaScript i én fil) |
| `sw.js` | Offline-støtte (service worker) |
| `manifest.webmanifest`, `icons/` | Gjør siden til en installerbar app |
| `fonts/` | Skrifttypene Lilita One og Nunito, lagret lokalt så de fungerer uten nett |
| `tools/build_map.py` | Lager kartdata fra Natural Earth |
| `tools/generate_images.py`, `tools/review_images.py` | Lager illustrasjonene automatisk via bilde-API-et og lager kontaktark for kontroll (se `tools/image_prompts/hurtigere_prosess.md`) |
| `tools/import_images.py`, `tools/image_prompts/` | Importerer egenlagde illustrasjoner og inneholder prompter og arbeidsflyt for å lage dem |
| `tools/fetch_photos.py`, `tools/photo_slots.json` | Finner og laster ned foto fra Wikimedia Commons med lisenssjekk |
| `photos/` | Foto, `photos.json` og `CREDITS.md` (lages av skriptet) |

**Design:** fargene, skriftene og klistremerke-uttrykket styres av variabler (`--accent`, `--coral`, `--ol` og flere) og tema-blokken «Tegneserie-tema» sist i stilarket. Reven Fia tegnes av funksjonen `mascot()`, og humøret byttes med `mascot('hi' | 'win' | 'hmm')`.

I `index.html` ligger dataene tydelig adskilt: `COUNTRIES` (kart), `ART` (illustrasjoner), `CITIES` (byer, spørsmål og jobber) og `PACK` (kofferter).

**Spørsmål:** de håndskrevne ligger i `q` på hver by. Faktaspørsmål lages av `SIGHTS`, og kart- og flaggspørsmål genereres av `qCountry`, `qContinent`, `qFlagFor`, `qDirection`, `qNearest` og `qLandmark`. `pickQuestions()` velger tre per quiz. Forklaringer hentes fra sightseeing-faktaene når spørsmålet passer til en severdighet, ellers fra `EXPL` (nøkkel `byId:spørsmålsnummer`). Alle håndskrevne spørsmål har en forklaring.

**Nye minispill:** hvert spill er en funksjon `gameXxx(el,job,fin)` som bygger grensesnittet i `el`, kaller `fin(bestått,tekst)` når det er ferdig, og returnerer en opprydningsfunksjon. Registrer typen i `runJob`, `JOBINFO` og `TYPENAME`. For tester kan du sette `window.__speed` for å kjøre tidsstyrte spill raskere.

**Legge til en jobb:** felles yrker ligger i `COMMON` (brukes i flere byer), og byens eget yrke ligger i `job` på byen i `CITIES`. Annonsene velges av `adsFor()`.

**Legge til en by:** legg til en linje i `CITIES` og en illustrasjon i `ART` med samme `id`. Landet må ligge i `LANDNAVN` og `FLG`. Hvis landet er nytt, må det også med i `GAME`-listen i `tools/build_map.py`, og kartdata må bygges på nytt.

## Oppdatere

1. Endre `index.html`.
2. Øk versjonen i `sw.js`, for eksempel `jorda-rundt-v1` til `jorda-rundt-v2`. Ellers kan brukere beholde den gamle versjonen i hurtigbufferen.
3. Commit og push. GitHub Pages oppdaterer siden i løpet av et minutt eller to.

## Publisere på GitHub Pages

1. Lag et repository, for eksempel `jorda-rundt`, og last opp alle filene (se kommandoene under, eller dra filene inn i nettleseren).
2. Gå til *Settings → Pages*. Under *Build and deployment* velger du *Deploy from a branch*, branch `main` og mappe `/ (root)`, og trykker Save.
3. Vent litt, og åpne adressen som vises øverst på siden.

```
git init -b main
git add .
git commit -m "Første versjon av Jorda Rundt"
git remote add origin https://github.com/BRUKERNAVN/jorda-rundt.git
git push -u origin main
```

Alle stier i spillet er relative, så det fungerer både på `brukernavn.github.io/jorda-rundt/` og på eget domene.

## Lisens og kilder

Se [CREDITS.md](CREDITS.md) for kilder til kart og skrifttyper. Velg en lisens for selve spillet (for eksempel MIT for koden) før du gjør repoet offentlig, og legg den i en `LICENSE`-fil.
