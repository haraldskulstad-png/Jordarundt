# Raskere bildeproduksjon: samme system, mindre manuelt arbeid

## Kort fortalt
Alt du har fra før beholdes: de samme 172 promptene, de samme filnavnene, den samme stilen og samme import til spillet. Det som tar tid i dag er det manuelle rundløpet per bilde (kopiere prompt, vente, laste ned, gi navn, kontrollere). Det kan automatiseres.

## Tre grep (de kan kombineres)

### A. La et skript lage bildene via OpenAIs bilde-API (størst gevinst)
Skriptet `tools/generate_images.py` bruker nøyaktig de samme promptene og sender de tre stilreferansene med hver gang, og lagrer bildene med riktig filnavn i `generated/`. Du slipper å kopiere, laste ned og gi navn. Stilen blir jevnere siden referansene følger med hver forespørsel (i chatten glir stilen ofte etter hvert). Skriptet hopper over bilder som er ferdige, prøver på nytt ved feil, og kan lage flere bilder samtidig.

Det krever en OpenAI API-konto. **API-bruk betales per bilde og er adskilt fra ChatGPT-abonnementet.**

### B. Rask kontroll med kontaktark
`tools/review_images.py` lager én nettside med alle bildene, kjennetegnene som skal sjekkes og et valg for å vise hvordan spillet beskjærer bildet. Du merker de som skal lages på nytt, og kopierer lista rett inn i skriptet (`--only-file redo.txt --force`). Det er mye raskere enn å gå gjennom bilde for bilde.

### C. Jobb i faser
1. **Bilde 1–4:** testserien. Kostnad og stil sjekkes før du bruker mer.
2. **De 55 utvalgte bildene** (`--phase featured`): de vises på bykortet og i quizen, og det er dem spillerne ser mest. Spillet fungerer godt med bare disse, resten viser tegningene.
3. **De 117 andre** (`--phase rest`): sightseeing-bildene, som bare vises når man åpner sightseeing.

## Slik gjør du det (fremgangsmåte for A)
1. Lag en konto og en API-nøkkel på platform.openai.com. **Sett en månedlig utgiftsgrense** (for eksempel 20 dollar), slik at du ikke kan bruke mer enn du vil.
2. Installer: `pip install openai pillow`
3. Sett nøkkelen i terminalen (aldri i en fil som ligger på GitHub):
   - Mac/Linux: `export OPENAI_API_KEY="sk-..."`
   - Windows (PowerShell): `$env:OPENAI_API_KEY="sk-..."`
4. Se hva som skjer uten å bruke penger: `python3 tools/generate_images.py --dry-run`
5. Lag testserien: `python3 tools/generate_images.py --only 1-4`
6. Se på dem: `python3 tools/review_images.py`, og åpne `generated/_oversikt.html`. Sjekk også kostnaden per bilde i OpenAI-dashbordet.
7. Lag de utvalgte bildene: `python3 tools/generate_images.py --phase featured`
8. Kontroller på kontaktarket, merk de som må gjøres om, lagre lista som `redo.txt` og kjør: `python3 tools/generate_images.py --only-file redo.txt --force`
9. Når du er fornøyd: `python3 tools/import_images.py --src generated`, og kjør deretter resten (`--phase rest`) på samme måte.

Nyttige valg: `--quality low|medium|high` (standard medium), `--parallel 3` (antall samtidig), `--model ...`, `--no-refs` (uten stilreferanser, billigere men mindre jevn stil).

## Modell og pris (viktig å vite)
- OpenAI stengte bildemodellen `gpt-image-1` 23. oktober 2026 og anbefaler nå GPT-Image-2.5 Sunburst for bildegenerering og -redigering. Det finnes også en raskere variant, Flare. Skriptet bruker `gpt-image-2.5-sunburst` som standard. Hvis modellnavnet er endret igjen, gir skriptet beskjed, og du kan bytte med `--model`.
- Prisene regnes per token og varierer med kvalitet og størrelse. For den forrige modellen (gpt-image-1.5) var referanseprisen i 1536 × 1024 omtrent 0,013 dollar (lav), 0,05 (medium) og 0,20 (høy) per bilde. Nyere modeller skal ligge på omtrent samme nivå eller litt lavere, men jeg har ikke fått bekreftet prisen for 2.5. Med medium kvalitet blir 172 bilder omtrent 9 dollar for selve bildene, pluss noe for referansebildene som sendes med. Regn heller på tallene fra testserien i dashbordet.
- Hvor lang tid det tar avhenger av modell og kvalitet. Med tre bilder om gangen er det realistisk å regne med noen titalls minutter til en time for alle 172, mot flere timer for hånd. Dette har jeg ikke målt.

## Hvis du heller vil holde deg i ChatGPT
- Be om flere bilder i samme melding («lag tre separate bilder, ett for hvert motiv, ikke et rutenett») og se om ChatGPT gjør det. Da halveres antall meldinger.
- Jobb i faser som over, og bruk `review_images.py` til kontrollen.
- Last ned i samme rekkefølge som nummereringen, så kan importverktøyet gi riktig navn (`--by-order`).
- Ikke be om fire motiver i ett rutenettbilde og skjære det opp. Detaljene blir for dårlige til at stedene kan kjennes igjen.

## Sikkerhet og kontroll
- Del aldri API-nøkkelen i en chat, og ikke legg den i GitHub. Slett den på platform.openai.com hvis den kommer på avveie.
- Se alltid over bildene mot ekte foto. Skriptet sjekker ikke at motivet er riktig, bare at filen er laget.
