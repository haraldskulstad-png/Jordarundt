#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Henter foto fra Wikimedia Commons til Jorda Rundt, med lisenssjekk og kreditering.

Bruk (krever Python 3.9+ og Pillow:  pip install pillow):

  1) Finn kandidater og lag kontaktark:
       python3 tools/fetch_photos.py search --contact "https://github.com/BRUKERNAVN/jorda-rundt"
     Åpne tools/contact_sheet.html i nettleseren, velg ett bilde per rute, og trykk
     «Last ned valg». Flytt photo_selection.json til tools/.

  2) Last ned de valgte bildene, lag photos/photos.json og photos/CREDITS.md:
       python3 tools/fetch_photos.py fetch --contact "https://github.com/BRUKERNAVN/jorda-rundt"

  Test av selve koden uten nett:
       python3 tools/fetch_photos.py selftest

Wikimedia krever at programmer identifiserer seg med kontaktinformasjon (--contact eller
miljøvariabelen JR_CONTACT). Skriptet venter ett sekund mellom forespørsler.
Lisenser som godtas: CC0, offentlig eie, CC BY og CC BY-SA (slå av BY-SA med --no-sa).
Bilder med NC/ND, bare GFDL, eller merket personality/insignia/currency avvises,
og det samme gjelder filnavn som tyder på nattbilder (f.eks. Eiffeltårnets lysshow).
En voksen må likevel se over valgene: riktig sted, ingen gjenkjennelige personer eller barn.
"""
import argparse, html, io, json, os, re, sys, tempfile, time, urllib.parse, urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
PHOTOS = ROOT / "photos"
SLOTS_FILE = TOOLS / "photo_slots.json"
CAND_FILE = TOOLS / "photo_candidates.json"
SHEET_FILE = TOOLS / "contact_sheet.html"
SELECTION_FILE = TOOLS / "photo_selection.json"
OUT_WIDTH = 640          # bredde på bildene som lagres i spillet
DELAY = 1.0              # sekunder mellom forespørsler
UA = None
AVOID_TITLE = re.compile(r"night|nacht|nuit|noche|notte|natt\b|illuminat|lit up|lights? show", re.I)
BAD_RESTRICTIONS = ("personality", "insignia", "currency")


# ---------- hjelpefunksjoner (testes av selftest) ----------
def strip_html(s, limit=90):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"

def meta_val(meta, key):
    return ((meta or {}).get(key) or {}).get("value", "") or ""

def license_class(short_name):
    """Returnerer 'pd', 'by', 'by-sa' eller None for ikke godkjent lisens."""
    ls = (short_name or "").strip().lower()
    if not ls:
        return None
    if re.search(r"(?<![a-z])(nc|nd)(?![a-z])", ls):
        return None
    if ls.startswith("cc0") or "public domain" in ls or ls.startswith("pd"):
        return "pd"
    if re.match(r"cc[ -]by[ -]sa", ls):
        return "by-sa"
    if re.match(r"cc[ -]by(?![a-z-])", ls):
        return "by"
    return None

def parse_page(page):
    info = (page.get("imageinfo") or [None])[0]
    if not info:
        return None
    meta = info.get("extmetadata") or {}
    lic = meta_val(meta, "LicenseShortName")
    return {
        "title": page.get("title", ""),
        "page": info.get("descriptionurl", ""),
        "thumb": info.get("thumburl", ""),
        "width": info.get("width", 0), "height": info.get("height", 0),
        "mime": info.get("mime", ""),
        "license": lic,
        "license_url": meta_val(meta, "LicenseUrl"),
        "lclass": license_class(lic),
        "author": strip_html(meta_val(meta, "Artist")) or strip_html(meta_val(meta, "Credit")) or "Ukjent",
        "restrictions": [r.strip().lower() for r in meta_val(meta, "Restrictions").split(",") if r.strip()],
    }

def accept(c, allow_sa=True):
    if not c: return False, "ingen bildeinfo"
    if not c["mime"].startswith("image/") or c["mime"] in ("image/svg+xml", "image/gif"):
        return False, "ikke et vanlig bilde"
    if c["lclass"] is None: return False, "lisens ikke godkjent: " + c["license"]
    if c["lclass"] == "by-sa" and not allow_sa: return False, "BY-SA er slått av"
    if any(r in BAD_RESTRICTIONS for r in c["restrictions"]): return False, "begrensninger: " + ",".join(c["restrictions"])
    if AVOID_TITLE.search(c["title"]): return False, "ser ut som nattbilde"
    w, h = c["width"], c["height"]
    if w < 1200 or not h or w / h < 1.25: return False, "for lite eller ikke liggende"
    return True, ""

def process_image(data, width=OUT_WIDTH):
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(io.BytesIO(data))).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    out = io.BytesIO()
    im.save(out, "WEBP", quality=72, method=6)
    return out.getvalue()

def credit_entry(c, fname):
    return {"f": fname, "a": c["author"], "l": c["license"], "u": c["page"], "lu": c["license_url"]}

def credits_markdown(photos, slots):
    lines = ["# Bildekreditter", "",
             "Fotografiene i denne mappen er hentet fra Wikimedia Commons og har hver sin lisens.",
             "De er skalert ned og lagret som WebP. Lisensen gjelder bildene, ikke spillets kode.", ""]
    for cid, e in photos.items():
        cfg = slots.get(cid, {}); name = cfg.get("name", cid); labels = cfg.get("labels", [])
        items = [("Byen", e.get("hero"))] + [(labels[i] if i < len(labels) else f"Sted {i+1}", x) for i, x in enumerate(e.get("s", []))]
        for lab, x in items:
            if x:
                lines.append(f"- **{name} – {lab}** ({x['f']}): {x['a']}, {x['l']}. [{x['u']}]({x['u']})")
    return "\n".join(lines) + "\n"

def make_sheet(cands):
    data = json.dumps(cands, ensure_ascii=False).replace("</", "<\\/")
    return SHEET_TEMPLATE.replace("__DATA__", data)

SHEET_TEMPLATE = """<!DOCTYPE html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bildevalg – Jorda Rundt</title>
<style>body{font:16px system-ui,sans-serif;margin:0;padding:12px 12px 90px;background:#f3f6f9;color:#14213d}h1{font-size:22px;margin:0 0 6px}section{background:#fff;border:2px solid #d3dde6;border-radius:12px;padding:10px;margin:12px 0}h2{font-size:17px;margin:0}.q{color:#5b6b82;font-size:13px;margin:2px 0 8px}.row{display:flex;gap:10px;overflow-x:auto;padding-bottom:6px}.card{flex:none;width:230px;border:2px solid #d3dde6;border-radius:10px;padding:6px;font-size:12px;background:#fff;cursor:pointer}.card.sel{border-color:#14213d;box-shadow:0 0 0 3px #fca311}.card img{width:100%;height:130px;object-fit:cover;border-radius:6px;background:#eee}.b{display:inline-block;border-radius:6px;padding:0 6px;font-weight:700;background:#dfe9f2}.b.sa{background:#fde7b3}.none{color:#5b6b82}.chk{background:#fff;border:2px solid #fca311;border-radius:10px;padding:8px 12px;font-size:14px}#bar{position:fixed;left:0;right:0;bottom:0;background:#14213d;color:#fff;padding:10px 12px;display:flex;gap:10px;align-items:center}#bar button{font:inherit;font-weight:700;border-radius:8px;border:0;padding:8px 12px;background:#fca311;color:#14213d;cursor:pointer}a{color:#1b7f8c}</style></head><body>
<h1>Velg bilder til Jorda Rundt</h1>
<div class="chk"><b>Sjekkliste for den voksne:</b> riktig sted og landemerke · dagslys (ikke lysshow om natten) · ingen gjenkjennelige personer eller barn · ingenting upassende · åpne «Filside» ved tvil og les lisensen. Trykk på et bilde for å velge, og trykk på det igjen for å fjerne valget.</div>
<div id="app"></div>
<div id="bar"><span id="cnt"></span><button id="dl">Last ned valg</button></div>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent),KEY='jr-photo-selection';
let sel={};try{sel=JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){}
const app=document.getElementById('app'),esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function draw(){
  app.innerHTML=Object.keys(D).map(k=>{const s=D[k];return `<section><h2>${esc(s.city)} – ${esc(s.label)}</h2><div class="q">Søk: «${esc(s.query)}» · ${s.cands.length} forslag</div><div class="row">${s.cands.length?s.cands.map(c=>`<div class="card ${sel[k]===c.title?'sel':''}" data-k="${esc(k)}" data-t="${esc(c.title)}"><img loading="lazy" src="${esc(c.thumb)}" alt=""><div><span class="b ${c.lclass==='by-sa'?'sa':''}">${esc(c.license)}</span></div><div>${esc(c.author)}</div><div><a href="${esc(c.page)}" target="_blank" rel="noopener">Filside</a> · ${c.width}×${c.height}</div></div>`).join(''):'<div class="none">Ingen godkjente forslag. Prøv et annet søk i photo_slots.json.</div>'}</div></section>`}).join('');
  document.getElementById('cnt').textContent='Valgt '+Object.values(sel).filter(Boolean).length+' av '+Object.keys(D).length;
}
app.addEventListener('click',e=>{if(e.target.closest('a'))return;const c=e.target.closest('.card');if(!c)return;const k=c.dataset.k,t=c.dataset.t;sel[k]=(sel[k]===t)?'':t;try{localStorage.setItem(KEY,JSON.stringify(sel));}catch(x){}draw();});
document.getElementById('dl').onclick=()=>{const out={};Object.keys(sel).forEach(k=>{if(sel[k])out[k]=sel[k];});const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(out,null,2)],{type:'application/json'}));a.download='photo_selection.json';a.click();};
draw();
</script></body></html>
"""


# ---------- nettverk ----------
def set_contact(contact):
    global UA
    contact = (contact or os.environ.get("JR_CONTACT", "")).strip()
    if not contact or "BRUKERNAVN" in contact:
        sys.exit("Oppgi kontaktinfo (nettadresse eller e-post) med --contact eller JR_CONTACT. Wikimedia krever det.")
    UA = f"JordaRundtPhotoTool/1.0 ({contact})"

def api_get(params):
    params = dict(params, format="json", formatversion="2")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            time.sleep(DELAY)
            return data
        except Exception as e:
            if attempt == 2: raise
            print("  prøver igjen etter feil:", e)
            time.sleep(3 * (attempt + 1))

def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    time.sleep(DELAY)
    return data

IIPROPS = "url|size|mime|extmetadata"

def cmd_search(args):
    set_contact(args.contact)
    slots = json.loads(SLOTS_FILE.read_text(encoding="utf-8"))
    only = set(args.only.split(",")) if args.only else None
    out = {}
    for cid, cfg in slots.items():
        if only and cid not in only: continue
        jobs = [("hero", "Byen", cfg["hero"])] + [(f"s{i}", cfg.get("labels", [""] * 3)[i], q) for i, q in enumerate(cfg["s"])]
        for slot, label, q in jobs:
            print(f"Søker: {cfg['name']} / {label}: {q}")
            data = api_get({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap",
                            "gsrnamespace": "6", "gsrlimit": "30", "prop": "imageinfo", "iiprop": IIPROPS, "iiurlwidth": "500"})
            pages = sorted(data.get("query", {}).get("pages", []), key=lambda p: p.get("index", 999))
            cands = []
            for p in pages:
                c = parse_page(p)
                ok, _ = accept(c, not args.no_sa)
                if ok: cands.append(c)
                if len(cands) >= args.per_slot: break
            out[f"{cid}/{slot}"] = {"city": cfg["name"], "label": label, "query": q, "cands": cands}
            print(f"  {len(cands)} godkjente forslag")
    CAND_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    SHEET_FILE.write_text(make_sheet(out), encoding="utf-8")
    print(f"\nFerdig. Åpne {SHEET_FILE} i nettleseren, velg bilder og last ned valget.")

def cmd_fetch(args):
    set_contact(args.contact)
    sel_path = Path(args.selection) if args.selection else SELECTION_FILE
    selection = json.loads(sel_path.read_text(encoding="utf-8"))
    slots = json.loads(SLOTS_FILE.read_text(encoding="utf-8"))
    PHOTOS.mkdir(exist_ok=True)
    pj = PHOTOS / "photos.json"
    photos = json.loads(pj.read_text(encoding="utf-8")) if pj.exists() else {}
    for key, title in selection.items():
        if not title: continue
        cid, slot = key.split("/")
        print(f"Henter {key}: {title}")
        data = api_get({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": IIPROPS, "iiurlwidth": "960"})
        pages = data.get("query", {}).get("pages", [])
        c = parse_page(pages[0]) if pages else None
        ok, why = accept(c, not args.no_sa)
        if not ok:
            print("  AVVIST:", why); continue
        webp = process_image(download(c["thumb"]))
        fname = f"{cid}_{slot}.webp"
        (PHOTOS / fname).write_bytes(webp)
        entry = photos.setdefault(cid, {"hero": None, "s": [None, None, None]})
        ce = credit_entry(c, fname)
        if slot == "hero": entry["hero"] = ce
        else: entry["s"][int(slot[1:])] = ce
        print(f"  lagret {fname} ({len(webp)//1024} KB) – {c['author']}, {c['license']}")
    pj.write_text(json.dumps(photos, ensure_ascii=False, indent=1), encoding="utf-8")
    (PHOTOS / "CREDITS.md").write_text(credits_markdown(photos, slots), encoding="utf-8")
    print("\nFerdig. Legg photos/ i git og øk versjonen i sw.js.")


# ---------- selvtest uten nett ----------
def cmd_selftest(_):
    from PIL import Image
    cases = {"CC BY-SA 4.0": "by-sa", "CC BY 2.0": "by", "CC0": "pd", "Public domain": "pd", "PD-old-70": "pd",
             "CC BY-NC 2.0": None, "CC BY-ND 4.0": None, "CC BY-NC-SA 3.0": None, "GFDL": None, "": None, "Attribution": None}
    for k, v in cases.items():
        assert license_class(k) == v, (k, license_class(k), v)
    assert strip_html('<a href="x">Jane &amp; Co</a><br>  Doe') == "Jane & Co Doe"
    def page(title, lic, w=2400, h=1600, restr="", mime="image/jpeg"):
        return {"title": title, "imageinfo": [{"descriptionurl": "https://commons.wikimedia.org/wiki/" + title, "thumburl": "https://x/y.jpg",
                "width": w, "height": h, "mime": mime, "extmetadata": {"LicenseShortName": {"value": lic}, "LicenseUrl": {"value": "https://cc/"},
                "Artist": {"value": '<a href="u">Ola Nordmann</a>'}, "Restrictions": {"value": restr}}}]}
    good = parse_page(page("File:Oslo Opera House.jpg", "CC BY-SA 4.0"))
    assert accept(good)[0] and not accept(good, allow_sa=False)[0]
    assert good["author"] == "Ola Nordmann"
    bad = [page("File:Eiffel Tower at night.jpg", "CC BY 2.0"), page("File:A.jpg", "CC BY-NC 2.0"),
           page("File:B.jpg", "CC0", restr="personality"), page("File:C.jpg", "CC0", w=800, h=500),
           page("File:D.jpg", "CC0", w=1500, h=2400), page("File:E.svg", "CC0", mime="image/svg+xml")]
    assert not any(accept(parse_page(p))[0] for p in bad)
    buf = io.BytesIO(); Image.new("RGB", (1600, 900), (40, 120, 200)).save(buf, "JPEG")
    webp = process_image(buf.getvalue()); im = Image.open(io.BytesIO(webp))
    assert im.format == "WEBP" and im.width == OUT_WIDTH
    photos = {"oslo": {"hero": credit_entry(good, "oslo_hero.webp"), "s": [None, None, None]}}
    md = credits_markdown(photos, {"oslo": {"name": "Oslo", "labels": []}})
    assert "Ola Nordmann" in md and "oslo_hero.webp" in md
    sheet = make_sheet({"oslo/hero": {"city": "Oslo", "label": "Byen", "query": "q", "cands": [good]}})
    assert "Ola Nordmann" in sheet and "</script><script" not in sheet.split('id="data"')[1].split("</script>")[0]
    slots = json.loads(SLOTS_FILE.read_text(encoding="utf-8"))
    assert len(slots) == 10 and all(len(v["s"]) == 3 and len(v["labels"]) == 3 for v in slots.values())
    print("Selvtest OK: lisenssjekk, filtre, bildebehandling, kreditter og kontaktark fungerer.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("search", cmd_search), ("fetch", cmd_fetch), ("selftest", cmd_selftest)):
        p = sub.add_parser(name); p.set_defaults(fn=fn)
        p.add_argument("--contact", default=""); p.add_argument("--no-sa", action="store_true")
        p.add_argument("--only", default=""); p.add_argument("--per-slot", type=int, default=8)
        p.add_argument("--selection", default="")
    args = ap.parse_args(); args.fn(args)

if __name__ == "__main__":
    main()
