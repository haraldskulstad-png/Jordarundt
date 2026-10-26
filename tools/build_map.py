"""Bygger kartdata (land som SVG-stier) fra Natural Earth.

Bruk:
  pip install shapely
  curl -LO https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson
  python3 tools/build_map.py ne_50m_admin_0_countries.geojson countries.js

Lim innholdet i countries.js inn i index.html i stedet for linjene som begynner med
"const COUNTRIES=" og "const CLBL=". Nye land i spillet legges til i GAME-listen under.
"""
import sys
import json
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.strtree import STRtree

d=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'ne_50m_admin_0_countries.geojson'))
GAME=['NOR','DNK','GBR','FRA','NLD','DEU','ESP','ITA','GRC','TUR','RUS','ISL','EGY','MAR','KEN','ZAF','MDG',
      'SWE','AUT','PRT','IRL','FIN','TZA','ZWE','IDN','KHM','CUB','GRL','ECU','ARE','IND','NPL','THA','SGP','CHN','MNG','KOR','JPN','AUS','NZL','USA','CAN','MEX','BRA','PER','ARG']
def px(lon): return (lon+180)/360*1000
def py(lat): return (90-lat)/180*500

feats=[]
for f in d['features']:
    p=f['properties']; iso=p['ADM0_A3']
    if iso=='ATA': continue
    g=shape(f['geometry'])
    polys=list(g.geoms) if isinstance(g,MultiPolygon) else [g]
    polys=sorted(polys,key=lambda x:-x.area)
    keep=[polys[0]]+[q for q in polys[1:] if q.area>0.03]
    feats.append((iso,p['NAME'],keep))
print(len(feats),'land')

# fargelegging (graf)
geoms=[MultiPolygon(k) for _,_,k in feats]
tree=STRtree(geoms)
nb=[set() for _ in feats]
for i,g in enumerate(geoms):
    gb=g.buffer(0.05)
    for j in tree.query(gb):
        j=int(j)
        if j!=i and gb.intersects(geoms[j]): nb[i].add(j)
order=sorted(range(len(feats)),key=lambda i:-len(nb[i]))
col=[-1]*len(feats); N=6
for i in order:
    used={col[j] for j in nb[i] if col[j]>=0}
    col[i]=next((c for c in range(N) if c not in used),i%N)
print('maks farger brukt',max(col)+1)

def ring(r):
    pts=[(round(px(x),1),round(py(y),1)) for x,y in r.coords]
    out=[];last=None
    for q in pts:
        if q!=last: out.append(q)
        last=q
    if len(out)<3: return ''
    return 'M'+' '.join(f'{a:g},{b:g}' for a,b in out)+'Z'

res=[]; lbl={}
for (iso,name,keep),c in zip(feats,col):
    ds=''
    for q in keep:
        q=q.simplify(0.035,preserve_topology=True)
        if q.is_empty: continue
        ps=list(q.geoms) if isinstance(q,MultiPolygon) else [q]
        for pp in ps:
            ds+=ring(pp.exterior)
            for h in pp.interiors:
                if Polygon(h).area>0.3: ds+=ring(h)
    res.append([iso,c,ds])
    if iso in GAME:
        rp=keep[0].representative_point()
        lbl[iso]=[round(px(rp.x),1),round(py(rp.y),1)]
js='const COUNTRIES='+json.dumps(res,separators=(',',':'),ensure_ascii=False)+';\nconst CLBL='+json.dumps(lbl,separators=(',',':'))+';'
open(sys.argv[2] if len(sys.argv)>2 else 'countries.js','w').write(js)
print(len(js)//1024,'KB', 'mangler label:',[g for g in GAME if g not in lbl])
