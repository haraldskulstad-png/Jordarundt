# Slik lager du bildene i ChatGPT (oppdatert etter bilde 1–72)

> **Raskere alternativ:** se `hurtigere_prosess.md`. Der lages bildene automatisk med et skript, med samme prompter og filnavn.

## Status
- Godkjent og lagt inn i spillet: **1–31 og 39–72** (65 bilder).
- Skal lages på nytt (stilen hadde glidd): **32–38**.
- Gjenstår: **73–172** (100 bilder).
- Alle blokkene du trenger ligger i `prompter_chatgpt.txt`: først de 7 som skal gjøres om, så 73–172.

## Oppsett (gjøres én gang)
1. Bytt ut instruksjonene i prosjektet med den oppdaterte teksten i `chatgpt_prosjektinstruksjoner.txt`. Den inneholder stilen, **reisegruppen** (tre barn med stråhatter nederst til venstre, alltid like) og regler for solen.
2. Fjern de gamle stilreferansene (tegningene fra spillet) og last opp de tre **godkjente bildene** som prosjektfiler: `godkjent_1_nuuk.jpg`, `godkjent_2_geysir.jpg`, `godkjent_3_bosporos.jpg`.

## Slik unngår du at stilen glir
Stilen glei over i et fotorealistisk uttrykk i bilde 32–38, midt i en lang chat. Derfor:
- **Start en ny chat i prosjektet for hver 15 bilder.**
- **Legg ved de tre godkjente bildene i første melding i hver ny chat**, med en linje som «Lag alle bilder i denne chatten i samme stil som disse».
- Hver blokk i `prompter_chatgpt.txt` ender med en **STILPÅMINNELSE**. La den stå, den er ment som sikkerhetsnett.
- Hvis et bilde likevel ser fotorealistisk ut (ingen tykke konturer, ingen smilende sol): skriv `rett: tegn dette som flat tegneserie med tykke mørke konturer og smilende sol, som de godkjente bildene` før du går videre.

## Rekkefølge
1. Lag om **32–38** først (Berlinmuren, Fjernsynstårnet, Riesenrad, Schönbrunn, Statsoperaen i Wien, Louvre, Notre-Dame).
2. Fortsett med **73–172** i rekkefølge, 15 om gangen.
3. Det kan være grenser for hvor mange bilder du kan lage per time eller dag, avhengig av abonnementet.

## Typiske rettelser (skriv rett etter bildet)
- `rett: fjern all tekst i bildet`
- `rett: motivet er for lite, gjør det større og plasser det midt i bildet`
- `rett: antall tårn er feil, det skal være fem, ett stort i midten og fire mindre`
- `rett: flytt solen litt ned slik at den er helt synlig`
- `rett: reisegruppen skal stå nederst til venstre og se ut som i de godkjente bildene`
- `rett: fjern bygningene bak, de skjuler motivet`

## Lagre og send
- Gi hver fil nummeret fra listen (for eksempel `73.png`) og send meg en zip, slik du gjorde nå. For de 7 som lages om, bruk samme nummer (`32.png` osv.), så erstatter de de gamle.
- Du kan bruke JPG i 1024 px bredde for mindre filer. Importen tåler det.
