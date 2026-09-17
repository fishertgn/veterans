#!/usr/bin/env python3
import os, random
import proxims as P
V,RED,LOGO,COLORS,FONTS=P.V,P.RED,P.LOGO,P.COLORS,P.FONTS
UP='https://minifutboltarragones.mygol.es/upload/'
def taula(tid):
    t=P.get(f'/tournaments/{tid}'); teams={x['id']:x for x in t['teams']}
    c=P.get(f"/tournaments/stageclassification/{t['stages'][0]['id']}")
    groups={g['id']:g['name'] for g in t['groups']}; out={}
    for r in c['leagueClassification']:
        tm=teams.get(r['idTeam']); 
        if not tm: continue
        out.setdefault(groups.get(r['idGroup'],''),[]).append(dict(n=P.nice(tm['name']),lg=UP+tm['logoImgUrl'],pj=r['gamesPlayed'],g=r['gamesWon'],e=r['gamesDraw'],p=r['gamesLost'],gf=r['points'],gc=r['pointsAgainst'],dg=r['pointDiff'],pts=r['tournamentPoints'],forma=(r.get('previousResult') or '')[-5:]))
    return t['name'],out
lliga_nom,lliga=taula(102); L=list(lliga.values())[0]
copa_nom,copa=taula(108)
random.seed(3)
for g,rs in copa.items():   # simulació d'una jornada jugada per veure la Copa amb dades
    for r in rs:
        o=random.choice(['g','e','p']); r['pj']=1; r['g']=int(o=='g'); r['e']=int(o=='e'); r['p']=int(o=='p'); r['gf']=random.randint(0,3); r['gc']=r['gf']+(-1 if o=='g' else 1 if o=='p' else 0); r['gc']=max(r['gc'],0); r['dg']=r['gf']-r['gc']; r['pts']=3*r['g']+r['e']; r['forma']='1' if o=='g' else 'X' if o=='e' else '2'
    rs.sort(key=lambda r:(-r['pts'],-r['dg'],-r['gf']))
HEAD=f"""*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1350px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:#f1f1f1;font-family:Barlow,sans-serif;color:#151515}}
.hd{{position:absolute;left:0;top:0;width:1080px;height:200px;background:{RED};color:#fff}}
.hd img{{position:absolute;left:44px;top:15px;width:170px;height:170px}}
.hd .t{{position:absolute;left:236px;top:44px;font-family:'Barlow Condensed';font-weight:800;font-size:58px;letter-spacing:1px;line-height:1;text-transform:uppercase;color:#fff}}
.hd .d{{position:absolute;left:238px;top:112px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:2px;color:#ffd6d6;text-transform:uppercase}}
.ft{{position:absolute;right:44px;bottom:26px;font-weight:600;font-size:16px;letter-spacing:2px;color:#b5b5b5}}
"""
def page(css,body,sub): return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{HEAD}{css}</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">Classificació</div><div class="d">{sub}</div></div>{body}<div class="ft">@veteranstarragona</div></body></html>'
def forma(s,size=14):
    m={'1':'#1a9c5b','X':'#b5b5b5','2':'#d60000'}
    return '<span class="fm">'+''.join(f'<i style="background:{m.get(ch,"#ddd")};width:{size}px;height:{size}px"></i>' for ch in s)+'</span>'
COL='#e6a800'  # Lliga 1A
def render(name,html): png=os.path.join(V,'out',f'{name}.png'); P.render(html,png); print(png)

# L1 · taula clàssica en targeta, top marcat amb color de la competició
def L1():
    rows=''.join(f'<div class="r{" top" if i<1 else ""}"><b class="pos" style="{"background:"+COL+";color:#fff" if i<1 else ""}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span>{r["g"]}</span><span>{r["e"]}</span><span>{r["p"]}</span><span>{r["gf"]}</span><span>{r["gc"]}</span><span class="dg">{r["dg"]:+d}</span><b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(L))
    return page(f""".tb{{position:absolute;left:40px;top:232px;width:1000px;background:#fff;border-radius:14px;border-left:10px solid {COL};box-shadow:0 2px 8px rgba(0,0,0,.05);overflow:hidden}}
.th,.r{{display:grid;grid-template-columns:56px 44px 1fr 56px 46px 46px 46px 56px 56px 66px 80px;align-items:center;gap:6px;padding:0 18px 0 10px;height:72px}}
.th{{height:48px;font-weight:700;font-size:14px;letter-spacing:2px;color:#9a9a9a;text-transform:uppercase;border-bottom:2px solid #eee}}.th span,.r span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #f0f0f0;font-weight:600;font-size:19px}}.r:last-child{{border-bottom:0}}
.r img{{width:40px;height:40px;object-fit:contain}}.r .n{{font-weight:700;font-size:19px;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:26px;width:40px;height:40px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#151515}}
.dg{{color:#777}}.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:32px;text-align:center}}
</style>""",f'<div class="tb"><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>G</span><span>E</span><span>P</span><span>GF</span><span>GC</span><span>DG</span><span>PTS</span></div>{rows}</div>',lliga_nom.replace('V LLIGA F 11 VETERANS','Lliga').replace('ª DIVISIÓ','a Divisió'))
render('K1_classica',L1())

# L2 · amb racha (últims 5) i punts destacats
def L2():
    rows=''.join(f'<div class="r"><b class="pos" style="{"background:"+COL+";color:#fff" if i<1 else ""}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}<small>{r["g"]}G · {r["e"]}E · {r["p"]}P</small></span><span>{r["pj"]}</span><span class="dg">{r["dg"]:+d}</span>{forma(r["forma"])}<b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(L))
    return page(f""".tb{{position:absolute;left:40px;top:232px;width:1000px;background:#fff;border-radius:14px;border-left:10px solid {COL};box-shadow:0 2px 8px rgba(0,0,0,.05);overflow:hidden}}
.th,.r{{display:grid;grid-template-columns:56px 48px 1fr 70px 80px 130px 90px;align-items:center;gap:8px;padding:0 18px 0 10px;height:74px}}
.th{{height:46px;font-weight:700;font-size:14px;letter-spacing:2px;color:#9a9a9a;text-transform:uppercase;border-bottom:2px solid #eee}}.th span,.r>span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #f0f0f0;font-weight:600;font-size:19px}}.r:last-child{{border-bottom:0}}
.r img{{width:44px;height:44px;object-fit:contain}}.r .n{{font-weight:700;font-size:20px;line-height:1.05;min-width:0}}.r .n small{{display:block;font-weight:600;font-size:13px;color:#9a9a9a;letter-spacing:1px;margin-top:3px}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:26px;width:40px;height:40px;border-radius:8px;display:flex;align-items:center;justify-content:center}}
.fm{{display:flex;gap:5px;justify-content:center}}.fm i{{border-radius:50%;display:block}}
.dg{{color:#777}}.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:34px;text-align:center;background:#151515;color:#fff;border-radius:8px;height:46px;line-height:46px}}
</style>""",f'<div class="tb"><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>DG</span><span>Últims 5</span><span>PTS</span></div>{rows}</div>','Lliga 1a Divisió')
render('K2_racha',L2())

# L3 · barra de punts proporcional
def L3():
    mx=max(r['pts'] for r in L) or 1
    rows=''.join(f'<div class="r"><b class="pos">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span class="bar"><i style="width:{r["pts"]/mx*100:.0f}%;background:{COL if i<1 else "#151515"}"></i></span><b class="pts">{r["pts"]}</b><span class="mini">{r["pj"]} PJ · {r["dg"]:+d}</span></div>' for i,r in enumerate(L))
    return page(f""".tb{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:8px}}
.r{{height:78px;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:48px 44px 300px 1fr 70px 110px;align-items:center;gap:10px;padding:0 18px 0 14px}}
.r img{{width:40px;height:40px;object-fit:contain}}.r .n{{font-weight:700;font-size:19px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:28px;color:#9a9a9a}}
.bar{{height:16px;background:#eee;border-radius:8px;overflow:hidden;display:block}}.bar i{{display:block;height:100%;border-radius:8px}}
.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:36px;text-align:right}}.mini{{font-size:13px;color:#9a9a9a;font-weight:600;letter-spacing:1px;text-align:right}}
</style>""",f'<div class="tb">{rows}</div>','Lliga 1a Divisió')
render('K3_barres',L3())

# L4 · files-targeta com resultats, amb franja lateral de color i tot el detall
def L4():
    rows=''.join(f'<div class="r" style="border-left-color:{COL if i<1 else "#ddd"}"><b class="pos">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span class="st"><b>{r["pj"]}</b>PJ</span><span class="st"><b>{r["g"]}</b>G</span><span class="st"><b>{r["e"]}</b>E</span><span class="st"><b>{r["p"]}</b>P</span><span class="st"><b>{r["gf"]}:{r["gc"]}</b>GOLS</span><span class="st"><b>{r["dg"]:+d}</b>DG</span><b class="pts">{r["pts"]}<small>PTS</small></b></div>' for i,r in enumerate(L))
    return page(f""".tb{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:8px}}
.r{{height:78px;background:#fff;border-radius:12px;border-left:10px solid #ddd;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:40px 44px 1fr 54px 44px 44px 44px 80px 60px 90px;align-items:center;gap:8px;padding:0 14px 0 10px}}
.r img{{width:40px;height:40px;object-fit:contain}}.r .n{{font-weight:700;font-size:19px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:28px;text-align:center}}
.st{{text-align:center;font-size:10px;font-weight:700;letter-spacing:1px;color:#9a9a9a;line-height:1}}.st b{{display:block;font-family:'Barlow Condensed';font-weight:700;font-size:24px;color:#151515;margin-bottom:2px}}
.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:36px;text-align:right;line-height:1}}.pts small{{display:block;font-family:Barlow;font-size:10px;letter-spacing:1px;color:#9a9a9a}}
</style>""",f'<div class="tb">{rows}</div>','Lliga 1a Divisió')
render('K4_targetes',L4())

# L5 · fosc
def L5():
    rows=''.join(f'<div class="r"><b class="pos" style="{"color:"+COL if i<1 else ""}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span>{r["g"]}-{r["e"]}-{r["p"]}</span><span>{r["gf"]}:{r["gc"]}</span><span class="dg">{r["dg"]:+d}</span>{forma(r["forma"],12)}<b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(L))
    return page(f"""body{{background:#111}}.tb{{position:absolute;left:40px;top:232px;width:1000px;background:#1b1b1b;border-radius:14px;overflow:hidden}}
.th,.r{{display:grid;grid-template-columns:50px 44px 1fr 56px 90px 80px 66px 110px 80px;align-items:center;gap:6px;padding:0 18px 0 12px;height:72px;color:#fff}}
.th{{height:46px;font-weight:700;font-size:13px;letter-spacing:2px;color:#777;text-transform:uppercase;border-bottom:1px solid #2a2a2a}}.th span,.r>span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #262626;font-weight:600;font-size:18px}}.r img{{width:38px;height:38px;object-fit:contain;background:#fff;border-radius:50%;padding:2px}}.r .n{{font-weight:700;font-size:19px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:26px;text-align:center;color:#777}}
.fm{{display:flex;gap:4px;justify-content:center}}.fm i{{border-radius:50%;display:block}}
.dg{{color:#999}}.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:34px;text-align:center;color:#ffd400}}.ft{{color:#555}}
</style>""",f'<div class="tb"><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>G-E-P</span><span>Gols</span><span>DG</span><span>Racha</span><span>PTS</span></div>{rows}</div>','Lliga 1a Divisió')
render('K5_fosc',L5())

# Copa: 8 grups en una imatge (estil K1) i 4 grups per imatge
def copa_html(grups,cols):
    secs=''
    for g,rs in grups:
        secs+=f'<div class="sec"><div class="sh">{g}</div><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>DG</span><span>PTS</span></div>'+''.join(f'<div class="r"><b class="pos" style="{"background:"+RED+";color:#fff" if i<2 else ""}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span class="dg">{r["dg"]:+d}</span><b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(rs))+'</div>'
    big = cols==2 and len(grups)<=4
    rh,fs,esc = (60,17,32) if big else (44,14,26)
    return page(f""".grid{{position:absolute;left:40px;top:232px;width:1000px;display:grid;grid-template-columns:repeat({cols},1fr);gap:14px;align-content:start}}
.sec{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);border-left:8px solid {RED}}}
.sh{{font-family:'Barlow Condensed';font-weight:800;font-size:{24 if big else 20}px;letter-spacing:2px;padding:{8 if big else 5}px 14px;text-transform:uppercase;color:{RED}}}
.th,.r{{display:grid;grid-template-columns:34px 34px 1fr 40px 46px 50px;align-items:center;gap:5px;padding:0 12px 0 8px;height:{rh}px}}
.th{{height:26px;font-weight:700;font-size:11px;letter-spacing:1.5px;color:#9a9a9a;text-transform:uppercase;border-bottom:2px solid #eee}}.th span,.r>span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #f0f0f0;font-weight:600;font-size:{fs}px}}.r:last-child{{border-bottom:0}}
.r img{{width:{esc}px;height:{esc}px;object-fit:contain}}.r .n{{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:{22 if big else 18}px;width:{30 if big else 24}px;height:{30 if big else 24}px;border-radius:6px;display:flex;align-items:center;justify-content:center}}
.dg{{color:#777}}.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:{28 if big else 22}px;text-align:center}}
</style>""",f'<div class="grid">{secs}</div>','Copa F11 · Fase de grups')
grups=sorted(copa.items())
render('KC1_copa_8',copa_html(grups,2))
render('KC2_copa_4a',copa_html(grups[:4],2))
