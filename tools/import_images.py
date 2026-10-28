#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importerer egenlagde illustrasjoner (for eksempel fra ChatGPT) til spillet.

Bruk (krever Python 3.9+ og Pillow:  pip install pillow):

  Alternativ A, filene har riktige navn (anbefalt), for eksempel oslo_s0.png, dub_hero.png:
      python3 tools/import_images.py --src generated

  Alternativ A2, filene heter bare nummeret i prompter_chatgpt.txt (5.png, 05.png, "12 kairo.png"):
      python3 tools/import_images.py --src generated

  Alternativ B, filene har tilfeldige navn, men er lastet ned i samme rekkefølge som
  nummereringen i prompter_chatgpt.txt (sorteres etter endringstidspunkt):
      python3 tools/import_images.py --src generated --by-order --dry-run     (se hva som skjer)
      python3 tools/import_images.py --src generated --by-order               (utfør)

Verktøyet
  - beskjærer til 3:2 hvis nødvendig og skalerer til 768 x 512, lagret som WebP,
  - legger resultatet i photos/ og oppdaterer photos/photos.json,
  - lar det utvalgte bildet (hero) bruke sightseeing-bildet når motivet er det samme
    (se hero_same i tools/image_slots.json), så det trenger ikke lages to ganger,
  - skriver en rapport over hva som mangler.
Egenlagde bilder får ingen fotokreditt. Foto fra Wikimedia Commons (fetch_photos.py) kan
brukes side om side, og det som importeres her erstatter bare de rutene som importeres.
"""
import argparse, json, re, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SLOTS = json.loads((Path(__file__).resolve().parent / "image_slots.json").read_text(encoding="utf-8"))
ORDER_FILE = Path(__file__).resolve().parent / "bildeorden.txt"
EXT = {".png", ".jpg", ".jpeg", ".webp"}
NAME = re.compile(r"^([a-z0-9]+)_(hero|s[0-2])$")
NUM = re.compile(r"^(\d{1,3})(?:[ _.\-].*)?$")
BG = (255, 240, 201)  # kremfarge bak gjennomsiktige bilder

def to_webp(src: Path, dst: Path, width: int, quality: int):
    im = ImageOps.exif_transpose(Image.open(src))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, BG); bg.paste(im, mask=im.split()[3]); im = bg
    else:
        im = im.convert("RGB")
    w, h = im.size; target = 3 / 2; warn = ""
    if abs(w / h - target) > 0.02:
        warn = f"{w}x{h} er ikke 3:2, beskjærer midten"
        if w / h > target: nw = round(h * target); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else: nh = round(w / target); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    if min(im.size) < 500: warn = (warn + "; " if warn else "") + f"lav oppløsning ({im.size[0]}x{im.size[1]})"
    im = im.resize((width, round(width * 2 / 3)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=quality, method=6)
    return warn

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True, help="mappen med de ferdige bildene")
    ap.add_argument("--out", default=str(ROOT / "photos"))
    ap.add_argument("--width", type=int, default=768)
    ap.add_argument("--quality", type=int, default=70)
    ap.add_argument("--by-order", action="store_true", help="gi navn etter nedlastingsrekkefølge")
    ap.add_argument("--dry-run", action="store_true", help="vis hva som ville skjedd, uten å skrive filer")
    a = ap.parse_args()
    src = Path(a.src); out = Path(a.out)
    files = sorted([p for p in src.iterdir() if p.suffix.lower() in EXT], key=lambda p: (p.stat().st_mtime, p.name))
    if not files: sys.exit(f"Fant ingen bilder i {src}")
    mapping = {}   # (id, slot) -> fil
    problems = []
    if a.by_order:
        order = [l.strip() for l in ORDER_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
        if len(files) > len(order): sys.exit(f"{len(files)} bilder, men bare {len(order)} plasser i rekkefølgen.")
        if len(files) < len(order): print(f"NB: {len(files)} av {len(order)} bilder. De første {len(files)} plassene brukes.")
        for f, name in zip(files, order):
            m = NAME.match(Path(name).stem); mapping[(m.group(1), m.group(2))] = f
            print(f"  {f.name:40s} -> {name}")
    else:
        order = [l.strip() for l in ORDER_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
        for f in files:
            m = NAME.match(f.stem.lower())
            if not m:
                # filer som bare heter et nummer (for eksempel 5.png, 05_oslo.png, "12 kairo.jpg") = nummer i prompter_chatgpt.txt
                mn = NUM.match(f.stem)
                if mn and 1 <= int(mn.group(1)) <= len(order):
                    m = NAME.match(Path(order[int(mn.group(1)) - 1]).stem)
            if not m or m.group(1) not in SLOTS: problems.append(f"Ukjent filnavn: {f.name}"); continue
            if (m.group(1), m.group(2)) in mapping: problems.append(f"Dobbelt: {f.name} og {mapping[(m.group(1), m.group(2))].name} er samme plass, bruker den siste")
            mapping[(m.group(1), m.group(2))] = f
    if a.dry_run:
        print(f"\n{len(mapping)} bilder ville blitt importert."); [print(p) for p in problems]; return
    out.mkdir(parents=True, exist_ok=True)
    pj = out / "photos.json"
    photos = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
    warns = []
    for (cid, slot), f in sorted(mapping.items()):
        fname = f"{cid}_{slot}.webp"
        w = to_webp(f, out / fname, a.width, a.quality)
        if w: warns.append(f"{f.name}: {w}")
        e = photos.setdefault(cid, {"hero": None, "s": [None, None, None]})
        ent = {"f": fname, "a": "", "l": "", "u": "", "lu": ""}
        if slot == "hero": e["hero"] = ent
        else: e["s"][int(slot[1:])] = ent
    # hero som gjenbruker sightseeing-bildet
    for cid, cfg in SLOTS.items():
        same = cfg.get("hero_same")
        if same and (cid, same) in mapping:
            photos.setdefault(cid, {"hero": None, "s": [None, None, None]})["hero"] = {"f": f"{cid}_{same}.webp", "a": "", "l": "", "u": "", "lu": ""}
    pj.write_text(json.dumps(photos, ensure_ascii=False, indent=1), encoding="utf-8")
    # rapport
    missing = []
    for cid, cfg in SLOTS.items():
        e = photos.get(cid) or {"hero": None, "s": [None, None, None]}
        if not e.get("hero"): missing.append(f"{cid}_hero")
        for k in range(3):
            if not (e.get("s") or [None] * 3)[k]: missing.append(f"{cid}_s{k}")
    print(f"\nImportert: {len(mapping)} bilder -> {out}")
    for w in warns: print("  ADVARSEL:", w)
    for p in problems: print("  PROBLEM:", p)
    print(f"Mangler fortsatt {len(missing)} av {4*len(SLOTS)} plasser" + (": " + ", ".join(missing[:20]) + (" …" if len(missing) > 20 else "") if missing else "."))

if __name__ == "__main__":
    main()
