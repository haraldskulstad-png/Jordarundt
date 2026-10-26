#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lager et kontaktark (generated/_oversikt.html) over alle bildene, for rask kontroll.

  python3 tools/review_images.py                 # leser generated/
  python3 tools/review_images.py --src mappe

Åpne _oversikt.html i nettleseren. For hvert bilde ser du motivet og de viktigste
kjennetegnene, og kan merke «lag på nytt». Krysset «Vis beskjæring» viser hva spillet viser
(bred stripe på bykortet og kvadrat i sightseeing-listen). Knappen «Kopier liste» gir en
liste du kan lagre som redo.txt og bruke slik:
  python3 tools/generate_images.py --only-file redo.txt --force
"""
import argparse, html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "tools" / "image_prompts" / "prompts.json"

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(ROOT / "generated"))
    a = ap.parse_args()
    src = Path(a.src); src.mkdir(parents=True, exist_ok=True)
    items = json.loads(PROMPTS.read_text(encoding="utf-8"))["items"]
    cards = []
    have = 0
    for i in items:
        exists = (src / i["file"]).exists()
        have += exists
        img = f'<img loading="lazy" src="{html.escape(i["file"])}" alt="">' if exists else '<div class="mangler">Mangler</div>'
        cards.append(
            f'<article class="card" data-file="{html.escape(i["file"])}" data-have="{int(exists)}" data-feat="{int(i["featured"])}">'
            f'<div class="th">{img}<i class="g2"></i><i class="gs"></i></div>'
            f'<div class="meta"><b>{i["n"]}. {html.escape(i["label"])}</b><span class="fn">{html.escape(i["file"])}</span>'
            f'<details><summary>Kjennetegn å sjekke</summary><p>{html.escape(i["subject"])}</p></details>'
            f'<button class="redo" type="button">Lag på nytt</button></div></article>')
    page = PAGE.replace("%%CARDS%%", "\n".join(cards)).replace("%%TOTAL%%", str(len(items))).replace("%%HAVE%%", str(have))
    out = src / "_oversikt.html"
    out.write_text(page, encoding="utf-8")
    print(f"Skrev {out}  ({have} av {len(items)} bilder finnes). Åpne filen i nettleseren.")

PAGE = """<!DOCTYPE html><html lang="nb"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bildekontroll: Jorda Rundt</title>
<style>
:root{--ol:#2A1B3D;--bg:#FFF0C9}*{box-sizing:border-box}
body{margin:0;font:15px/1.35 system-ui,sans-serif;background:var(--bg);color:var(--ol)}
header{position:sticky;top:0;z-index:5;background:#FFC22E;border-bottom:3px solid var(--ol);padding:10px 14px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
header h1{font-size:18px;margin:0 8px 0 0}
header label,header button{font-weight:700;font-size:14px}
button{font:inherit;border:2.5px solid var(--ol);background:#fff;color:var(--ol);border-radius:12px;padding:6px 12px;cursor:pointer;box-shadow:0 3px 0 var(--ol)}
button.on{background:#FF5E7E;color:#fff}
.chips button.on{background:var(--ol);color:#fff}
main{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;padding:14px}
.card{background:#fff;border:3px solid var(--ol);border-radius:16px;box-shadow:0 4px 0 var(--ol);overflow:hidden}
.card.marked{outline:5px solid #FF5E7E}
.th{position:relative;aspect-ratio:3/2;background:#eee;line-height:0}
.th img{width:100%;height:100%;object-fit:cover}
.mangler{display:grid;place-items:center;height:100%;font-weight:800;color:#999}
.g2,.gs{display:none;position:absolute;pointer-events:none;border:2.5px dashed #FF2D55}
.g2{left:0;right:0;top:12.5%;bottom:12.5%}
.gs{top:0;bottom:0;left:16.667%;right:16.667%;border-color:#1976ff}
body.guides .g2,body.guides .gs{display:block}
.meta{padding:8px 10px 10px}.fn{display:block;color:#6b5a85;font-size:12px}
details{margin:6px 0}summary{cursor:pointer;font-weight:700;font-size:13px}details p{margin:6px 0 0;font-size:13px}
.redo{width:100%;margin-top:4px}
.card.marked .redo{background:#FF5E7E;color:#fff}
footer{position:sticky;bottom:0;background:#fff;border-top:3px solid var(--ol);padding:8px 14px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
textarea{width:100%;height:90px;display:none}
.hide{display:none!important}
</style></head><body>
<header><h1>Bildekontroll</h1>
<span><b id="have">%%HAVE%%</b> av %%TOTAL%% finnes</span>
<span class="chips"><button data-f="all" class="on">Alle</button> <button data-f="feat">Utvalgte (55)</button> <button data-f="miss">Mangler</button> <button data-f="mark">Merket</button></span>
<label><input type="checkbox" id="g"> Vis beskjæring (rød = bykort, blå = liten rute)</label></header>
<main id="m">
%%CARDS%%
</main>
<footer><b id="cnt">0 merket</b><button id="copy">Kopier liste</button><button id="clear">Fjern alle merker</button><span style="font-size:13px">Lagre listen som redo.txt, og kjør: python3 tools/generate_images.py --only-file redo.txt --force</span><textarea id="ta" readonly></textarea></footer>
<script>
const KEY='jr-redo';let marked=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
const cards=[...document.querySelectorAll('.card')];
function refresh(){cards.forEach(c=>c.classList.toggle('marked',marked.has(c.dataset.file)));document.getElementById('cnt').textContent=marked.size+' merket';localStorage.setItem(KEY,JSON.stringify([...marked]));filter()}
cards.forEach(c=>c.querySelector('.redo').addEventListener('click',()=>{const f=c.dataset.file;marked.has(f)?marked.delete(f):marked.add(f);refresh()}));
let mode='all';
function filter(){cards.forEach(c=>{let ok=mode==='all'||(mode==='feat'&&c.dataset.feat==='1')||(mode==='miss'&&c.dataset.have==='0')||(mode==='mark'&&marked.has(c.dataset.file));c.classList.toggle('hide',!ok)})}
document.querySelectorAll('.chips button').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.chips button').forEach(x=>x.classList.remove('on'));b.classList.add('on');mode=b.dataset.f;filter()}));
document.getElementById('g').addEventListener('change',e=>document.body.classList.toggle('guides',e.target.checked));
document.getElementById('copy').addEventListener('click',()=>{const t=[...marked].join('\\n');const ta=document.getElementById('ta');ta.style.display='block';ta.value=t;ta.select();try{navigator.clipboard.writeText(t).catch(()=>{})}catch(e){}});
document.getElementById('clear').addEventListener('click',()=>{marked.clear();refresh()});
refresh();
</script></body></html>
"""
if __name__ == "__main__":
    main()
