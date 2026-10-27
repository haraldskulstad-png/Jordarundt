#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lager alle illustrasjonene automatisk med OpenAIs bilde-API, med de samme promptene,
filnavnene og stilreferansene som i det manuelle ChatGPT-oppsettet.

Forutsetninger:
  pip install openai
  Miljøvariabelen OPENAI_API_KEY med en API-nøkkel (API-bruk faktureres separat fra et
  ChatGPT-abonnement, per bilde).

Eksempler:
  python3 tools/generate_images.py --dry-run                 # vis antall og omtrentlig pris
  python3 tools/generate_images.py --only 1-4                # testserien (bilde 1-4)
  python3 tools/generate_images.py --phase featured          # de 55 utvalgte bildene først
  python3 tools/generate_images.py                           # alle 172 (hopper over ferdige)
  python3 tools/generate_images.py --only paris_s0,kairo_s0 --force   # lag disse på nytt
  python3 tools/generate_images.py --only-file redo.txt --force       # liste fra review_images.py

Bildene lagres i generated/. Kjør deretter:
  python3 tools/review_images.py          # kontaktark for rask kontroll
  python3 tools/import_images.py --src generated
"""
import argparse, base64, csv, json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "tools" / "image_prompts" / "prompts.json"
# Tre godkjente bilder (768x512) sendes med hver forespørsel som stilreferanse. De viser stilen og den faste
# reisegruppen. Referansebilder telles som inndata og øker prisen litt, så de holdes små.
REFS = [ROOT / "tools" / "image_prompts" / f for f in
        ("godkjent_1_nuuk_liten.jpg", "godkjent_2_geysir_liten.jpg", "godkjent_3_bosporos_liten.jpg")]
# Omtrentlige referansepriser per bilde i 1536x1024 (USD). Sjekk gjeldende priser på OpenAIs prisside.
PRICE = {"low": 0.013, "medium": 0.05, "high": 0.20}

def build_prompt(data, item, with_refs):
    parts = []
    if with_refs: parts.append(data["ref_note"])
    parts.append(data["style"])
    parts.append("SUBJECT: " + item["subject"])
    parts.append(data["format"])
    return "\n\n".join(parts)

def parse_only(spec, items):
    """'1-4', '5,9,12', 'paris_s0,kairo_s0' eller blanding."""
    keep = set()
    by_file = {i["file"]: i["n"] for i in items}
    by_stem = {i["file"][:-4]: i["n"] for i in items}
    for tok in [t.strip() for t in spec.split(",") if t.strip()]:
        if "-" in tok and tok.replace("-", "").isdigit():
            a, b = tok.split("-"); keep.update(range(int(a), int(b) + 1))
        elif tok.isdigit(): keep.add(int(tok))
        elif tok in by_file: keep.add(by_file[tok])
        elif tok in by_stem: keep.add(by_stem[tok])
        else: print(f"Ukjent bilde: {tok}")
    return keep

def make_client():
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("Installer først:  pip install openai")
    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("Sett miljøvariabelen OPENAI_API_KEY (API-nøkkel fra platform.openai.com).")
    return OpenAI(max_retries=0, timeout=600)

def generate_one(client, a, data, item, with_refs):
    prompt = build_prompt(data, item, with_refs)
    last = None
    for attempt in range(1, a.retries + 1):
        try:
            if with_refs:
                files = [open(p, "rb") for p in REFS]
                try:
                    res = client.images.edit(model=a.model, image=files, prompt=prompt, size=a.size, quality=a.quality)
                finally:
                    for f in files: f.close()
            else:
                res = client.images.generate(model=a.model, prompt=prompt, size=a.size, quality=a.quality)
            b64 = res.data[0].b64_json
            if not b64: raise RuntimeError("tomt svar fra API-et")
            return base64.b64decode(b64)
        except Exception as e:
            last = e
            msg = str(e)
            if any(k in msg.lower() for k in ("model_not_found", "does not exist", "invalid_api_key", "incorrect api key", "billing")):
                raise RuntimeError(msg)
            wait = min(60, 4 * 2 ** (attempt - 1))
            print(f"  {item['file']}: forsøk {attempt}/{a.retries} feilet ({msg[:120]}), venter {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"ga opp etter {a.retries} forsøk: {last}")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "generated"))
    ap.add_argument("--model", default=os.environ.get("IMAGE_MODEL", "gpt-image-2.5-sunburst"),
                    help="bildemodell (sjekk gjeldende navn i OpenAIs dokumentasjon)")
    ap.add_argument("--quality", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--size", default="1536x1024")
    ap.add_argument("--parallel", type=int, default=3, help="antall bilder som lages samtidig")
    ap.add_argument("--retries", type=int, default=4)
    ap.add_argument("--only", default="", help="for eksempel 1-4, 5,9 eller paris_s0,kairo_s0")
    ap.add_argument("--only-file", default="", help="fil med én filnavn per linje")
    ap.add_argument("--phase", choices=["all", "featured", "rest"], default="all",
                    help="featured = de 55 utvalgte bildene, rest = de andre 117")
    ap.add_argument("--no-refs", action="store_true", help="ikke send stilreferansene (raskere, men mindre jevn stil)")
    ap.add_argument("--force", action="store_true", help="lag bilder på nytt selv om filen finnes")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    data = json.loads(PROMPTS.read_text(encoding="utf-8"))
    items = data["items"]
    keep = {i["n"] for i in items}
    if a.phase == "featured": keep &= {i["n"] for i in items if i["featured"]}
    if a.phase == "rest": keep &= {i["n"] for i in items if not i["featured"]}
    if a.only: keep &= parse_only(a.only, items)
    if a.only_file:
        names = [l.strip() for l in Path(a.only_file).read_text(encoding="utf-8").splitlines() if l.strip()]
        keep &= parse_only(",".join(names), items)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    todo = [i for i in items if i["n"] in keep and (a.force or not (out / i["file"]).exists() or (out / i["file"]).stat().st_size < 20000)]
    skipped = len([i for i in items if i["n"] in keep]) - len(todo)
    with_refs = not a.no_refs
    if with_refs:
        for p in REFS:
            if not p.exists(): sys.exit(f"Mangler stilreferanse: {p}")
    est = len(todo) * PRICE.get(a.quality, 0.05)
    print(f"Modell: {a.model} | kvalitet: {a.quality} | størrelse: {a.size} | stilreferanser: {'ja' if with_refs else 'nei'}")
    print(f"Skal lage {len(todo)} bilder ({skipped} er ferdige og hoppes over). Omtrentlig pris: ca. {est:.2f} USD for selve bildene"
          + (" pluss litt for referansebildene" if with_refs else "") + " (referansepris, sjekk gjeldende priser).")
    print("Tips: lag testserien (--only 1-4) først og se på kostnaden per bilde i OpenAI-dashbordet før du kjører resten.")
    if a.dry_run or not todo:
        for i in todo[:8]: print(f"  {i['n']:3d} {i['file']:22s} {i['label']}")
        if len(todo) > 8: print(f"  … og {len(todo) - 8} til")
        return
    client = make_client()
    log = out / "_logg.csv"; lock = threading.Lock()
    if not log.exists(): log.write_text("tid;nr;fil;status;merknad\n", encoding="utf-8")
    done = fail = 0; t0 = time.time()
    def work(item):
        png = generate_one(client, a, data, item, with_refs)
        (out / item["file"]).write_bytes(png)
        return item
    with ThreadPoolExecutor(max_workers=max(1, a.parallel)) as ex:
        futs = {ex.submit(work, i): i for i in todo}
        for f in as_completed(futs):
            i = futs[f]
            try:
                f.result(); done += 1; status, note = "ok", ""
                print(f"[{done + fail}/{len(todo)}] {i['file']} ferdig")
            except Exception as e:
                fail += 1; status, note = "feil", str(e)[:200]
                print(f"[{done + fail}/{len(todo)}] {i['file']} FEILET: {note}")
                if "model" in note.lower() and "not" in note.lower():
                    print("  Tips: sjekk modellnavnet med --model, og at kontoen har tilgang til bilde-API-et.")
            with lock:
                with log.open("a", encoding="utf-8") as fh: fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')};{i['n']};{i['file']};{status};{note}\n")
    print(f"\nFerdig: {done} laget, {fail} feilet, på {time.time() - t0:.0f} s. Bildene ligger i {out}")
    if fail: print("Kjør samme kommando igjen for å prøve de som feilet (ferdige hoppes over).")

if __name__ == "__main__":
    main()
