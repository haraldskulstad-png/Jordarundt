# Bilder til Jorda Rundt: liste og prompter

## Oversikt
- 55 byer. Hver by har **ett utvalgt bilde (hero)** og **tre sightseeing-bilder** = 220 plasser.
- 48 av de utvalgte bildene er samme motiv som et av sightseeing-bildene. De trenger du bare lage én gang, så er det **172 bilder** som må lages.
- Alle bilder skal lages med samme masterstil (under) og samme størrelse.

## Format og filer (slik at det er enkelt å bruke i spillet)
- **Størrelse:** 1536 × 1024 piksler (3:2, liggende), PNG, sRGB.
- **Fyller hele bildet:** ingen ramme, ingen avrundede hjørner, ingen gjennomsiktig bakgrunn. Spillet legger rammen på selv.
- **Sikker sone:** alt viktig innenfor midtre 66 % av bredden og midtre 70 % av høyden. Spillet beskjærer bildet til en bred stripe (2:1) på bykortet og til et kvadrat i sightseeing-listen.
- **Filnavn:** nøyaktig slik det står i listen, for eksempel `oslo_s0.png`. Legg alle i én mappe (eller zip).
- **Hero som gjenbruker:** lag bare `{by}_s0.png` (eller `s1` der det står), så kopierer jeg den til `{by}_hero`.
- **Etterarbeid hos meg:** jeg skalerer til 768 × 512 og lagrer som WebP (ca. 40–60 KB per bilde), og lager en importfil. Bildene trenger ingen kreditt, siden de er tegnet for spillet.

## Masterstil (legges først i hver prompt)
```
Cheerful children's picture-book cartoon illustration in a flat cel-shaded vector style (clearly a drawing, never a painting and never photo-realistic). Bold dark-plum outlines (color #2A1B3D) around every shape. Bold, warm, saturated colors with simple two-tone shading (one soft shadow tone per object, no realistic lighting, no photographic textures). Rounded, friendly shapes with a very slight hand-drawn wobble. Bright sunny daytime: light-blue sky fading to pale warm yellow at the horizon, puffy white clouds with the same dark outline, and a smiling sun with short rays in the upper right area, its center about 20% down from the top edge and fully visible (never cut off). Ground, water and backgrounds are clean color areas separated by a clear horizon line. The subject is drawn with accurate real-world proportions and ALL of its distinctive, recognizable features, large and clearly visible, not cut off. Keep the background simple so it never hides the subject. No text, no letters, no numbers, no logos, no watermark, no signature, no frame, no border, no vignette, no rounded corners (real inscriptions that belong to the place may stay small). Not a photograph, not 3D, not painterly, not blurry, not anime.

RECURRING TRAVEL TRIO (include in every image, always identical): three young travelers seen from behind in the bottom-left foreground, about 25% of the image height, facing the sight: (1) a boy in a bright blue T-shirt, tan straw sun hat with a dark-blue band and a big black backpack, taking a photo with a small black camera; (2) a girl with long brown hair, tan straw sun hat with a dark-blue band, orange-red T-shirt and a brown backpack, looking and pointing; (3) a smaller child in a blue baseball cap, green T-shirt and dark-gray backpack, pointing at the sight. They stand at the left edge, never cover the main subject, and for a close-up object or animal they stand a little behind or beside it, looking at it. All other people in the scene are tiny and simple.
```

## Format-tillegg (legges sist i hver prompt)
```
Image size: 1536 x 1024 pixels, 3:2 landscape, full-bleed scene that fills the entire canvas (no transparency). Safe zone: keep everything important inside the central 66% of the width and the central 70% of the height, because the game crops the image to a 2:1 banner and to a square thumbnail.
```

## Negativ prompt (hvis verktøyet har et felt for det)
```
photo, photorealistic, 3d render, painting, text, letters, numbers, watermark, logo, frame, border, vignette, blurry, thin lines, gradients, dark, gloomy, scary, anime
```

## Stilreferanse
Bruk de tre godkjente bildene `godkjent_1_nuuk.jpg`, `godkjent_2_geysir.jpg` og `godkjent_3_bosporos.jpg` som referanse. De er laget i prosjektet, viser riktig stil og har den faste **reisegruppen** (tre barn med stråhatter nederst til venstre). Last dem opp som prosjektfiler og i første melding i hver ny chat.

## Slik får du jevn stil gjennom alle 172 bilder
- Lag bildene i samme prosjekt, men start en **ny chat for hver 15 bilder** og legg ved de tre godkjente referansebildene i første melding. Stilen glir ellers i lange chatter (det skjedde fra bilde 32).
- Behold masterstilen ordrett. Bytt bare ut SUBJECT-linjen.
- Hvis et bilde ser annerledes ut enn de andre (andre linjer, mykere skygger, foto-lignende), generer det på nytt heller enn å godta det.
- Lag en prøveserie først: ett bilde fra hver av fire verdensdeler (for eksempel `paris_s0`, `kairo_s0`, `tokyo_s0`, `rio_s0`) og se at stilen er lik før du lager resten.

## Spesialtilfeller
- **Nattbilder** (Rovaniemi: Nordlys, Reykjavik: Nordlys over Island): nattehimmel med stjerner og halvmåne i stedet for dag og sol. Beskrivelsen sier det.
- **Hollywood-skiltet** (Los Angeles) er det eneste bildet der bokstaver er tillatt.
- **Louvre** (Paris): vis selve palasset, ikke glasspyramiden. Pyramiden er opphavsrettslig vernet i Frankrike.
- **Eiffeltårnet** vises alltid på dagtid. Lysshowet om natten er vernet.
- Moderne bygg (Burj Khalifa, Marina Bay Sands, CN Tower, Sky Tower) kan være vernet i noen land. Jeg er ikke jurist, så vurder det om bildene skal brukes kommersielt.

## Kontroll av hvert bilde
1. Legg bildet ved siden av 2–3 ekte foto av stedet. Kjenner du det igjen på silhuetten alene?
2. Sjekk antall og form på de viktigste delene (for eksempel åtte søyler på Parthenon, fem tårn på Angkor Wat, fire ben på Eiffeltårnet).
3. Ingen tekst, ingen merkevarer, ingen forstyrrende ekstra bygg som skjuler motivet.
4. Motivet ligger i sikker sone og er ikke kuttet.
5. Samme linjetykkelse og fargestil som de andre bildene. Gjenta heller bildet enn å godta en avvikende stil.

## Liste per by

### 1. Oslo (Norge)
- **Utvalgt (hero):** Operahuset, samme motiv som `oslo_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Operahuset → lag `oslo_s0.png`
- **Sightseeing 2:** Slottet → lag `oslo_s1.png`
- **Sightseeing 3:** Holmenkollen → lag `oslo_s2.png`

### 2. Bergen (Norge)
- **Utvalgt (hero):** Bryggen, samme motiv som `bergen_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Bryggen → lag `bergen_s0.png`
- **Sightseeing 2:** Fløibanen → lag `bergen_s1.png`
- **Sightseeing 3:** Fisketorget → lag `bergen_s2.png`

### 3. København (Danmark)
- **Utvalgt (hero):** Den lille havfrue, samme motiv som `kbh_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Den lille havfrue → lag `kbh_s0.png`
- **Sightseeing 2:** Tivoli → lag `kbh_s1.png`
- **Sightseeing 3:** Nyhavn → lag `kbh_s2.png`

### 4. Stockholm (Sverige)
- **Utvalgt (hero):** Gamla stan, samme motiv som `sto_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Gamla stan → lag `sto_s0.png`
- **Sightseeing 2:** Vasamuseet → lag `sto_s1.png`
- **Sightseeing 3:** Kongeslottet → lag `sto_s2.png`

### 5. Rovaniemi (Finland)
- **Utvalgt (hero):** Julenissens landsby, samme motiv som `rov_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Julenissens landsby → lag `rov_s0.png`
- **Sightseeing 2:** Nordlys → lag `rov_s1.png`
- **Sightseeing 3:** Reinsdyr → lag `rov_s2.png`

### 6. London (Storbritannia)
- **Utvalgt (hero):** Big Ben, samme motiv som `london_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Big Ben → lag `london_s0.png`
- **Sightseeing 2:** Tower Bridge → lag `london_s1.png`
- **Sightseeing 3:** Buckingham Palace → lag `london_s2.png`

### 7. Dublin (Irland)
- **Utvalgt (hero):** Kløver og rundtårn → lag `dub_hero.png`
- **Sightseeing 1:** Trinity College → lag `dub_s0.png`
- **Sightseeing 2:** Dublin Castle → lag `dub_s1.png`
- **Sightseeing 3:** Kløveren → lag `dub_s2.png`

### 8. Amsterdam (Nederland)
- **Utvalgt (hero):** Vindmøller og kanaler → lag `ams_hero.png`
- **Sightseeing 1:** Vindmøller → lag `ams_s0.png`
- **Sightseeing 2:** Syklene → lag `ams_s1.png`
- **Sightseeing 3:** Rijksmuseum → lag `ams_s2.png`

### 9. Berlin (Tyskland)
- **Utvalgt (hero):** Brandenburger Tor, samme motiv som `berlin_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Brandenburger Tor → lag `berlin_s0.png`
- **Sightseeing 2:** Berlinmuren → lag `berlin_s1.png`
- **Sightseeing 3:** Fjernsynstårnet → lag `berlin_s2.png`

### 10. Wien (Østerrike)
- **Utvalgt (hero):** Riesenrad, samme motiv som `wien_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Riesenrad → lag `wien_s0.png`
- **Sightseeing 2:** Schönbrunn → lag `wien_s1.png`
- **Sightseeing 3:** Statsoperaen → lag `wien_s2.png`

### 11. Paris (Frankrike)
- **Utvalgt (hero):** Eiffeltårnet, samme motiv som `paris_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Eiffeltårnet → lag `paris_s0.png`
- **Sightseeing 2:** Louvre → lag `paris_s1.png`
- **Sightseeing 3:** Notre-Dame → lag `paris_s2.png`

### 12. Lisboa (Portugal)
- **Utvalgt (hero):** Gul trikk, samme motiv som `lis_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Trikk 28 → lag `lis_s0.png`
- **Sightseeing 2:** Belém-tårnet → lag `lis_s1.png`
- **Sightseeing 3:** Klippfisk → lag `lis_s2.png`

### 13. Barcelona (Spania)
- **Utvalgt (hero):** Sagrada Família, samme motiv som `bcn_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Sagrada Família → lag `bcn_s0.png`
- **Sightseeing 2:** Park Güell → lag `bcn_s1.png`
- **Sightseeing 3:** Camp Nou → lag `bcn_s2.png`

### 14. Roma (Italia)
- **Utvalgt (hero):** Colosseum, samme motiv som `roma_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Colosseum → lag `roma_s0.png`
- **Sightseeing 2:** Trevifontenen → lag `roma_s1.png`
- **Sightseeing 3:** Pantheon → lag `roma_s2.png`

### 15. Pisa (Italia)
- **Utvalgt (hero):** Det skjeve tårn, samme motiv som `pisa_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Det skjeve tårn → lag `pisa_s0.png`
- **Sightseeing 2:** Domkirken → lag `pisa_s1.png`
- **Sightseeing 3:** Galileo → lag `pisa_s2.png`

### 16. Athen (Hellas)
- **Utvalgt (hero):** Parthenon, samme motiv som `athen_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Parthenon → lag `athen_s0.png`
- **Sightseeing 2:** Det gamle stadion → lag `athen_s1.png`
- **Sightseeing 3:** Akropolismuseet → lag `athen_s2.png`

### 17. Istanbul (Tyrkia)
- **Utvalgt (hero):** Hagia Sophia, samme motiv som `ist_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Hagia Sophia → lag `ist_s0.png`
- **Sightseeing 2:** Storbasaren → lag `ist_s1.png`
- **Sightseeing 3:** Bosporos → lag `ist_s2.png`

### 18. Moskva (Russland)
- **Utvalgt (hero):** Vasilijkatedralen, samme motiv som `moskva_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Vasilijkatedralen → lag `moskva_s0.png`
- **Sightseeing 2:** Kreml → lag `moskva_s1.png`
- **Sightseeing 3:** Metroen → lag `moskva_s2.png`

### 19. Reykjavik (Island)
- **Utvalgt (hero):** Hallgrímskirkja, samme motiv som `rey_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Hallgrímskirkja → lag `rey_s0.png`
- **Sightseeing 2:** Geysir → lag `rey_s1.png`
- **Sightseeing 3:** Nordlys → lag `rey_s2.png`

### 20. Nuuk (Grønland)
- **Utvalgt (hero):** Fargerike hus og isfjell → lag `nuuk_hero.png`
- **Sightseeing 1:** Fargerike hus → lag `nuuk_s0.png`
- **Sightseeing 2:** Isfjell → lag `nuuk_s1.png`
- **Sightseeing 3:** Hvaler → lag `nuuk_s2.png`

### 21. Kairo (Egypt)
- **Utvalgt (hero):** Pyramidene i Giza, samme motiv som `kairo_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Pyramidene i Giza → lag `kairo_s0.png`
- **Sightseeing 2:** Sfinksen → lag `kairo_s1.png`
- **Sightseeing 3:** Museet → lag `kairo_s2.png`

### 22. Marrakech (Marokko)
- **Utvalgt (hero):** Koutoubia-moskeen, samme motiv som `marr_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Koutoubia-moskeen → lag `marr_s0.png`
- **Sightseeing 2:** Jemaa el-Fnaa → lag `marr_s1.png`
- **Sightseeing 3:** Atlasfjellene → lag `marr_s2.png`

### 23. Nairobi (Kenya)
- **Utvalgt (hero):** Safari → lag `nai_hero.png`
- **Sightseeing 1:** Nairobi nasjonalpark → lag `nai_s0.png`
- **Sightseeing 2:** Sjiraffsenteret → lag `nai_s1.png`
- **Sightseeing 3:** Elefantbarnehjemmet → lag `nai_s2.png`

### 24. Zanzibar (Tanzania)
- **Utvalgt (hero):** Stone Town og dhow → lag `zan_hero.png`
- **Sightseeing 1:** Stone Town → lag `zan_s0.png`
- **Sightseeing 2:** Krydderfarmer → lag `zan_s1.png`
- **Sightseeing 3:** Strendene → lag `zan_s2.png`

### 25. Victoria Falls (Zimbabwe)
- **Utvalgt (hero):** Victoriafallene, samme motiv som `vic_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Victoriafallene → lag `vic_s0.png`
- **Sightseeing 2:** Regnbuene → lag `vic_s1.png`
- **Sightseeing 3:** Elefantene → lag `vic_s2.png`

### 26. Kappstaden (Sør-Afrika)
- **Utvalgt (hero):** Taffelfjellet, samme motiv som `kapp_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Taffelfjellet → lag `kapp_s0.png`
- **Sightseeing 2:** Pingvinene → lag `kapp_s1.png`
- **Sightseeing 3:** Robben Island → lag `kapp_s2.png`

### 27. Antananarivo (Madagaskar)
- **Utvalgt (hero):** Lemurer og baobab → lag `mad_hero.png`
- **Sightseeing 1:** Lemurene → lag `mad_s0.png`
- **Sightseeing 2:** Baobabtrærne → lag `mad_s1.png`
- **Sightseeing 3:** Rismarkene → lag `mad_s2.png`

### 28. Dubai (De forente arabiske emirater)
- **Utvalgt (hero):** Burj Khalifa, samme motiv som `dubai_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Burj Khalifa → lag `dubai_s0.png`
- **Sightseeing 2:** Ørkensafari → lag `dubai_s1.png`
- **Sightseeing 3:** Palm Jumeirah → lag `dubai_s2.png`

### 29. Agra (India)
- **Utvalgt (hero):** Taj Mahal, samme motiv som `agra_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Taj Mahal → lag `agra_s0.png`
- **Sightseeing 2:** Agra fort → lag `agra_s1.png`
- **Sightseeing 3:** Elefanter → lag `agra_s2.png`

### 30. Mumbai (India)
- **Utvalgt (hero):** Gateway of India, samme motiv som `mumbai_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Gateway of India → lag `mumbai_s0.png`
- **Sightseeing 2:** Bollywood → lag `mumbai_s1.png`
- **Sightseeing 3:** Lokaltogene → lag `mumbai_s2.png`

### 31. Kathmandu (Nepal)
- **Utvalgt (hero):** Boudhanath-stupaen, samme motiv som `kath_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Boudhanath → lag `kath_s0.png`
- **Sightseeing 2:** Himalaya → lag `kath_s1.png`
- **Sightseeing 3:** Bønneflagg → lag `kath_s2.png`

### 32. Bangkok (Thailand)
- **Utvalgt (hero):** Wat Arun, samme motiv som `bkk_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Wat Arun → lag `bkk_s0.png`
- **Sightseeing 2:** Flytende marked → lag `bkk_s1.png`
- **Sightseeing 3:** Tuk-tuk → lag `bkk_s2.png`

### 33. Siem Reap (Kambodsja)
- **Utvalgt (hero):** Angkor Wat, samme motiv som `sie_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Angkor Wat → lag `sie_s0.png`
- **Sightseeing 2:** Ta Prohm → lag `sie_s1.png`
- **Sightseeing 3:** Lotusblomster → lag `sie_s2.png`

### 34. Singapore (Singapore)
- **Utvalgt (hero):** Marina Bay Sands, samme motiv som `sgp_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Marina Bay Sands → lag `sgp_s0.png`
- **Sightseeing 2:** Supertrærne → lag `sgp_s1.png`
- **Sightseeing 3:** Merlion → lag `sgp_s2.png`

### 35. Bali (Indonesia)
- **Utvalgt (hero):** Risterrasser og tempel → lag `bali_hero.png`
- **Sightseeing 1:** Risterrasser → lag `bali_s0.png`
- **Sightseeing 2:** Templer → lag `bali_s1.png`
- **Sightseeing 3:** Vulkaner → lag `bali_s2.png`

### 36. Beijing (Kina)
- **Utvalgt (hero):** Den forbudte by, samme motiv som `bj_s1.png` (lages ikke på nytt)
- **Sightseeing 1:** Den kinesiske mur → lag `bj_s0.png`
- **Sightseeing 2:** Den forbudte by → lag `bj_s1.png`
- **Sightseeing 3:** Pandaer → lag `bj_s2.png`

### 37. Ulaanbaatar (Mongolia)
- **Utvalgt (hero):** Ger-telt på steppen, samme motiv som `ulan_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Ger-telt → lag `ulan_s0.png`
- **Sightseeing 2:** Djengis Khan → lag `ulan_s1.png`
- **Sightseeing 3:** Hestene → lag `ulan_s2.png`

### 38. Seoul (Sør-Korea)
- **Utvalgt (hero):** N Seoul Tower, samme motiv som `seoul_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** N Seoul Tower → lag `seoul_s0.png`
- **Sightseeing 2:** Gyeongbokgung → lag `seoul_s1.png`
- **Sightseeing 3:** Kimchi → lag `seoul_s2.png`

### 39. Tokyo (Japan)
- **Utvalgt (hero):** Fuji-fjellet, samme motiv som `tokyo_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Fuji → lag `tokyo_s0.png`
- **Sightseeing 2:** Shinkansen → lag `tokyo_s1.png`
- **Sightseeing 3:** Kirsebærblomster → lag `tokyo_s2.png`

### 40. Sydney (Australia)
- **Utvalgt (hero):** Operahuset, samme motiv som `syd_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Operahuset → lag `syd_s0.png`
- **Sightseeing 2:** Harbour Bridge → lag `syd_s1.png`
- **Sightseeing 3:** Kenguruer → lag `syd_s2.png`

### 41. Alice Springs (Australia)
- **Utvalgt (hero):** Uluru, samme motiv som `alice_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Uluru → lag `alice_s0.png`
- **Sightseeing 2:** Outback → lag `alice_s1.png`
- **Sightseeing 3:** Kenguruer → lag `alice_s2.png`

### 42. Auckland (New Zealand)
- **Utvalgt (hero):** Sky Tower, samme motiv som `akl_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Sky Tower → lag `akl_s0.png`
- **Sightseeing 2:** Seilbåtene → lag `akl_s1.png`
- **Sightseeing 3:** Vulkanene → lag `akl_s2.png`

### 43. Honolulu (Hawaii, USA)
- **Utvalgt (hero):** Diamond Head, samme motiv som `hnl_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Diamond Head → lag `hnl_s0.png`
- **Sightseeing 2:** Waikiki → lag `hnl_s1.png`
- **Sightseeing 3:** Blomsterkrans → lag `hnl_s2.png`

### 44. New York (USA)
- **Utvalgt (hero):** Frihetsgudinnen, samme motiv som `ny_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Frihetsgudinnen → lag `ny_s0.png`
- **Sightseeing 2:** Central Park → lag `ny_s1.png`
- **Sightseeing 3:** Empire State Building → lag `ny_s2.png`

### 45. Washington (USA)
- **Utvalgt (hero):** Washington-monumentet, samme motiv som `dc_s1.png` (lages ikke på nytt)
- **Sightseeing 1:** Det hvite hus → lag `dc_s0.png`
- **Sightseeing 2:** Washington-monumentet → lag `dc_s1.png`
- **Sightseeing 3:** Kongressbygningen → lag `dc_s2.png`

### 46. Los Angeles (USA)
- **Utvalgt (hero):** Hollywood-skiltet, samme motiv som `la_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Hollywood-skiltet → lag `la_s0.png`
- **Sightseeing 2:** Walk of Fame → lag `la_s1.png`
- **Sightseeing 3:** Santa Monica → lag `la_s2.png`

### 47. San Francisco (USA)
- **Utvalgt (hero):** Golden Gate Bridge, samme motiv som `sf_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Golden Gate Bridge → lag `sf_s0.png`
- **Sightseeing 2:** Kabelbanene → lag `sf_s1.png`
- **Sightseeing 3:** Alcatraz → lag `sf_s2.png`

### 48. Toronto (Canada)
- **Utvalgt (hero):** CN Tower, samme motiv som `tor_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** CN Tower → lag `tor_s0.png`
- **Sightseeing 2:** Niagarafallene → lag `tor_s1.png`
- **Sightseeing 3:** Ishockeymuseet → lag `tor_s2.png`

### 49. Havana (Cuba)
- **Utvalgt (hero):** Gamle amerikanerbiler, samme motiv som `hav_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Gamle biler → lag `hav_s0.png`
- **Sightseeing 2:** Gamlebyen → lag `hav_s1.png`
- **Sightseeing 3:** Musikken → lag `hav_s2.png`

### 50. Mexico by (Mexico)
- **Utvalgt (hero):** Pyramidene, samme motiv som `mex_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Teotihuacan → lag `mex_s0.png`
- **Sightseeing 2:** Zócalo → lag `mex_s1.png`
- **Sightseeing 3:** De dødes dag → lag `mex_s2.png`

### 51. Quito (Ecuador)
- **Utvalgt (hero):** Ekvator-monumentet, samme motiv som `quito_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Ekvator-monumentet → lag `quito_s0.png`
- **Sightseeing 2:** Vulkanene → lag `quito_s1.png`
- **Sightseeing 3:** Gamlebyen → lag `quito_s2.png`

### 52. Manaus (Brasil)
- **Utvalgt (hero):** Amazonas-regnskogen, samme motiv som `manaus_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Amazonas → lag `manaus_s0.png`
- **Sightseeing 2:** Elvemøtet → lag `manaus_s1.png`
- **Sightseeing 3:** Papegøyene → lag `manaus_s2.png`

### 53. Rio de Janeiro (Brasil)
- **Utvalgt (hero):** Kristusstatuen, samme motiv som `rio_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Kristusstatuen → lag `rio_s0.png`
- **Sightseeing 2:** Sukkertoppen → lag `rio_s1.png`
- **Sightseeing 3:** Copacabana → lag `rio_s2.png`

### 54. Lima (Peru)
- **Utvalgt (hero):** Machu Picchu, samme motiv som `lima_s0.png` (lages ikke på nytt)
- **Sightseeing 1:** Machu Picchu → lag `lima_s0.png`
- **Sightseeing 2:** Lamaene → lag `lima_s1.png`
- **Sightseeing 3:** Potetene → lag `lima_s2.png`

### 55. Buenos Aires (Argentina)
- **Utvalgt (hero):** Fargerike hus i La Boca, samme motiv som `bsas_s1.png` (lages ikke på nytt)
- **Sightseeing 1:** Obelisken → lag `bsas_s0.png`
- **Sightseeing 2:** La Boca → lag `bsas_s1.png`
- **Sightseeing 3:** Tango → lag `bsas_s2.png`

## Tillegg: 15 nye byer (bilde 173–217)
De 15 nye byene har egne prompter i `prompter_nye_byer.txt`, i samme format og med samme stil. Hver by har tre bilder (`s0`, `s1`, `s2`), og det utvalgte bildet på bykortet gjenbruker `s0`. Nummereringen fortsetter fra 173, så import etter nummer fungerer som før.
