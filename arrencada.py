#!/usr/bin/env python3
"""Carrusel de presentació de temporada + portades de destacats."""
import os, math
import proxims as P
V,RED,LOGO,FONTS=P.V,P.RED,P.LOGO,P.FONTS
UP='https://minifutboltarragones.mygol.es/upload/'
OUT=os.path.join(V,'out','arrencada'); os.makedirs(OUT,exist_ok=True)
FONTS2=FONTS.replace('&display=swap','&family=Barlow+Condensed:wght@900&display=swap')
BASE=f"""*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1350px;overflow:hidden;position:relative}}img{{display:block}}
body{{font-family:Barlow,sans-serif;color:#151515;background:{RED}}}
.ft{{position:absolute;left:0;bottom:30px;width:1080px;text-align:center;font-weight:600;font-size:18px;letter-spacing:3px;color:#ffb3b3}}
"""
def render(name,html,w=1080,h=1350):
    png=os.path.join(OUT,name+'.png'); tmp=png[:-4]+'.html'; open(tmp,'w').write(html)
    import subprocess
    subprocess.run([P.CHROME,'--headless=new','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files',f'--window-size={w},{h}','--virtual-time-budget=15000',f'--screenshot={png}','file://'+tmp],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); print(png); return png

t=P.get('/tournaments/108'); teams={x['id']:x for x in t['teams']}; groups={g['id']:g['name'] for g in t['groups']}
grups={}
for tg in t.get('teamGroups',[]) or []:
    grups.setdefault(groups.get(tg['idGroup'],''),[]).append(teams[tg['idTeam']])
if not grups:
    c=P.get(f"/tournaments/stageclassification/{t['stages'][0]['id']}")
    for r in c['leagueClassification']:
        if r['idTeam'] in teams: grups.setdefault(groups.get(r['idGroup'],''),[]).append(teams[r['idTeam']])
grups=dict(sorted(grups.items())); n_eq=sum(len(v) for v in grups.values())

# ---- 1 · PORTADA ----
escuts=[UP+x['logoImgUrl'] for x in t['teams']]
wall=''.join(f'<img src="{e}" style="left:{(i%7)*160-20}px;top:{(i//7)*160-30}px;transform:rotate({(i*37)%21-10}deg)">' for i,e in enumerate(escuts[:35]))
render('01_portada',f"""<!doctype html><html><head><meta charset="utf-8">{FONTS2}<style>{BASE}
.wall{{position:absolute;inset:0;opacity:.13}}.wall img{{position:absolute;width:130px;height:130px;object-fit:contain;filter:grayscale(1) brightness(3)}}
.logo{{position:absolute;left:50%;top:70px;transform:translateX(-50%);width:420px;height:420px}}
.k{{position:absolute;left:0;top:520px;width:1080px;text-align:center;color:#fff;font-family:'Barlow Condensed';font-weight:900;font-size:190px;line-height:.86;letter-spacing:-2px;text-transform:uppercase}}
.k small{{display:block;font-size:110px;color:#ffd400;letter-spacing:2px}}
.s{{position:absolute;left:0;top:930px;width:1080px;text-align:center;color:#fff;font-weight:600;font-size:34px;letter-spacing:6px;text-transform:uppercase}}
.tag{{position:absolute;left:50%;top:1030px;transform:translateX(-50%) rotate(-2deg);background:#151515;color:#ffd400;font-family:'Barlow Condensed';font-weight:700;font-size:52px;letter-spacing:4px;padding:10px 40px;text-transform:uppercase;white-space:nowrap}}
.n{{position:absolute;left:0;top:1180px;width:1080px;text-align:center;color:#ffb3b3;font-weight:500;font-size:26px;letter-spacing:2px}}
</style></head><body><div class="wall">{wall}</div><img class="logo" src="{LOGO}"><div class="k">Torna<small>la lliga</small></div>
<div class="s">Temporada 2026 · 2027</div><div class="tag">Copa F11 · 26 de setembre</div><div class="n">{n_eq} equips · 8 grups · 4 divisions · cada cap de setmana aquí</div><div class="ft">@veteranstarragona</div></body></html>""")

# ---- 2-3 · GRUPS (4 per imatge) ----
def grups_html(gs,pag):
    secs=''
    for g,eqs in gs:
        secs+=f'<div class="sec"><div class="sh">{g}</div>'+''.join(f'<div class="r"><img src="{UP+e["logoImgUrl"]}"><span>{P.nice(e["name"])}</span></div>' for e in eqs)+'</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS2}<style>{BASE}
body{{background:#f1f1f1}}
.hd{{position:absolute;left:0;top:0;width:1080px;height:200px;background:{RED};color:#fff}}
.hd img{{position:absolute;left:44px;top:15px;width:170px;height:170px}}
.hd .t{{position:absolute;left:236px;top:44px;font-family:'Barlow Condensed';font-weight:700;font-size:58px;line-height:1;text-transform:uppercase}}
.hd .d{{position:absolute;left:238px;top:112px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:2px;color:#ffd6d6;text-transform:uppercase}}
.hd .pg{{position:absolute;right:44px;top:70px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;opacity:.8}}
.grid{{position:absolute;left:40px;top:232px;width:1000px;display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.sec{{background:#fff;border-radius:14px;border-left:10px solid {RED};box-shadow:0 2px 8px rgba(0,0,0,.05);padding:10px 16px 12px}}
.sh{{font-family:'Barlow Condensed';font-weight:700;font-size:34px;letter-spacing:3px;color:{RED};text-transform:uppercase;margin-bottom:6px}}
.r{{display:flex;align-items:center;gap:12px;height:66px;border-top:1px solid #f0f0f0;font-weight:600;font-size:21px}}.r img{{width:50px;height:50px;object-fit:contain}}
.ft{{color:#b5b5b5;text-align:right;left:auto;right:44px;width:auto}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">Els grups de la Copa</div><div class="d">Copa F11 Veterans 26-27</div><span class="pg">{pag}/2</span></div><div class="grid">{secs}</div><div class="ft">@veteranstarragona</div></body></html>"""
gl=list(grups.items()); render('02_grups_A-D',grups_html(gl[:4],1)); render('03_grups_E-H',grups_html(gl[4:],2))

# ---- 4 · QUÈ TROBARÀS ----
items=[('DILLUNS','Resultats i classificació','Totes les divisions, en una sola imatge per lliga.'),('DIVENDRES','Pròxims partits','Hora, camp i grup de tots els partits del cap de setmana.'),('DISSABTE I DIUMENGE','Resultats en directe','Cada partit acabat, a les històries en menys d’una hora.'),('SEMPRE','Destacats','Resultats, classificació i calendari guardats a dalt del perfil.')]
li=''.join(f'<div class="it"><div class="d">{d}</div><div class="t">{t}</div><div class="s">{s}</div></div>' for d,t,s in items)
render('04_que_trobaras',f"""<!doctype html><html><head><meta charset="utf-8">{FONTS2}<style>{BASE}
.logo{{position:absolute;left:44px;top:40px;width:160px;height:160px}}
.k{{position:absolute;left:230px;top:56px;color:#fff;font-family:'Barlow Condensed';font-weight:900;font-size:86px;line-height:.9;text-transform:uppercase}}.k small{{display:block;font-size:40px;color:#ffd400;letter-spacing:4px;font-weight:700;margin-top:10px}}
.list{{position:absolute;left:44px;top:260px;width:992px;display:flex;flex-direction:column;gap:18px}}
.it{{background:#fff;border-radius:16px;padding:22px 30px;border-left:12px solid #151515}}
.it .d{{font-family:'Barlow Condensed';font-weight:700;font-size:26px;letter-spacing:4px;color:{RED};text-transform:uppercase}}
.it .t{{font-family:'Barlow Condensed';font-weight:700;font-size:54px;line-height:1;margin:4px 0 8px;text-transform:uppercase}}
.it .s{{font-weight:500;font-size:24px;color:#666;line-height:1.3}}
.cta{{position:absolute;left:44px;top:1140px;width:992px;background:#ffd400;border-radius:16px;padding:26px 30px;font-family:'Barlow Condensed';font-weight:700;font-size:48px;line-height:1;text-transform:uppercase;text-align:center}}
.cta small{{display:block;font-family:Barlow;font-weight:500;font-size:22px;text-transform:none;margin-top:8px;letter-spacing:1px}}
</style></head><body><img class="logo" src="{LOGO}"><div class="k">Què hi trobaràs<small>Cada setmana, sense fallar</small></div><div class="list">{li}</div>
<div class="cta">Segueix-nos i activa les notificacions 🔔<small>Comparteix-ho amb el teu equip · Compte no oficial · Dades de @minifutbol_tarragones</small></div></body></html>""")

# ---- PORTADES DE DESTACATS (1080x1920, icona al centre) ----
ICON={'resultats':'<path d="M20 30h60v40H20z" fill="none" stroke="#fff" stroke-width="6"/><text x="50" y="62" text-anchor="middle" font-family="Barlow Condensed" font-weight="700" font-size="34" fill="#fff">2-1</text>',
 'classificacio':'<rect x="22" y="58" width="14" height="24" fill="#fff"/><rect x="43" y="34" width="14" height="48" fill="#ffd400"/><rect x="64" y="46" width="14" height="36" fill="#fff"/>',
 'proxims':'<circle cx="50" cy="50" r="30" fill="none" stroke="#fff" stroke-width="6"/><path d="M50 30v22l14 8" fill="none" stroke="#ffd400" stroke-width="6" stroke-linecap="round"/>',
 'copa':'<path d="M32 22h36v18a18 18 0 0 1-36 0z" fill="#ffd400"/><path d="M32 28h-10v8a10 10 0 0 0 10 8M68 28h10v8a10 10 0 0 1-10 8" fill="none" stroke="#ffd400" stroke-width="5"/><rect x="44" y="58" width="12" height="10" fill="#fff"/><rect x="36" y="68" width="28" height="8" fill="#fff"/>'}
NOM={'resultats':'Resultats','classificacio':'Classificació','proxims':'Pròxims','copa':'Copa'}
for k,svg in ICON.items():
    render('destacat_'+k,f"""<!doctype html><html><head><meta charset="utf-8">{FONTS2}<style>*{{margin:0;padding:0}}html,body{{width:1080px;height:1920px;overflow:hidden;position:relative;background:{RED};font-family:Barlow}}
.c{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:640px;height:640px;border-radius:50%;border:14px solid #fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}}
svg{{width:300px;height:300px}}.n{{color:#fff;font-family:'Barlow Condensed';font-weight:700;font-size:64px;letter-spacing:4px;text-transform:uppercase}}
</style></head><body><div class="c"><svg viewBox="0 0 100 100">{svg}</svg><div class="n">{NOM[k]}</div></div></body></html>""",1080,1920)
