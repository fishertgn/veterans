#!/usr/bin/env python3
"""Classificació: una imatge per lliga (taula amb zones) i dues per la Copa (4 grups per imatge).
Ús: classificacio.py [--send] [--test]   (--test usa les lligues 25-26: 102, 103, 98)"""
import sys, os, re, json, subprocess, time
import proxims as P
V,RED,LOGO,COLORS,FONTS=P.V,P.RED,P.LOGO,P.COLORS,P.FONTS
UP='https://minifutboltarragones.mygol.es/upload/'
ZONES={'BRONZE':('#fbe9dc','#b5651d','Copa Bronze'),'PLATA':('#ececec','#8a8a8a','Copa Plata'),'COPA OR':('#fff3c4','#d4a100','Copa Or'),'CONSOLACI':('#e3f3fb','#3d94c4','Consolació'),'CAMPI':('#dff5e6','#1a9c5b','Campió'),'PROMOC':('#fff1cc','#b8860b','Promoció'),'ASCENS':('#dcefff','#1f6feb','Ascens'),'DESCENS':('#ffe3e3','#d60000','Descens')}
def zona(title):
    u=title.upper()
    for k,v in ZONES.items():
        if k in u: return v
    return ('#f0f0f0','#555',title.title())

def zona_de(pos,zones):
    for a,b,t in zones:
        if a<=pos<=b: return zona(t)
    return None
COPES=("Copa Or","Copa Plata","Copa Bronze","Consolació")
def _titol_zona(zz,t):
    if zz[2] in COPES: return zz[2]
    return t.title().replace("Catalunta","Catalunya").replace("2ªdivisió","2ª Divisió")
def llegenda(zones,tag='span'):
    vist=[]; out=''
    for a,b,t in zones:
        zz=zona(t)
        if zz[2] in vist: continue
        vist.append(zz[2]); out+=f'<{tag} class="lg"><i style="background:{zz[1]}"></i>{_titol_zona(zz,t)}</{tag}>'
    return out

def dades(tid):
    t=P.get(f'/tournaments/{tid}'); teams={x['id']:x for x in t['teams']}; stage=t['stages'][0]
    c=P.get(f"/tournaments/stageclassification/{stage['id']}"); groups={g['id']:g['name'] for g in t['groups']}
    taules={}
    for r in c['leagueClassification']:
        tm=teams.get(r['idTeam'])
        if not tm: continue
        taules.setdefault(r['idGroup'],[]).append(dict(n=P.nice(tm['name']),lg=UP+tm['logoImgUrl'],pj=r['gamesPlayed'],g=r['gamesWon'],e=r['gamesDraw'],p=r['gamesLost'],gf=r['points'],gc=r['pointsAgainst'],dg=r['pointDiff'],pts=r['tournamentPoints'],forma=(r.get('previousResult') or '')[-5:]))
    try: zones=json.loads(c.get('colorConfig') or '[]')
    except Exception: zones=[]
    zones=[(int(z['start']),int(z['end']),z.get('title','')) for z in zones]
    return t['name'],P.curt(t['name']),[(groups.get(gid,''),rs) for gid,rs in taules.items()],zones

def forma(s):
    m={'1':'#1a9c5b','X':'#b5b5b5','2':'#d60000'}
    return '<span class="fm">'+''.join(f'<i style="background:{m.get(ch,"#ddd")}"></i>' for ch in s)+'</span>'
HEAD=f"""*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1350px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:#f1f1f1;font-family:Barlow,sans-serif;color:#151515}}
.hd{{position:absolute;left:0;top:0;width:1080px;height:200px;background:{RED};color:#fff}}
.hd img{{position:absolute;left:44px;top:15px;width:170px;height:170px}}
.hd .t{{position:absolute;left:236px;top:44px;font-family:'Barlow Condensed';font-weight:700;font-size:58px;letter-spacing:1px;line-height:1;text-transform:uppercase;color:#fff}}
.hd .d{{position:absolute;left:238px;top:112px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:2px;color:#ffd6d6;text-transform:uppercase}}
.hd .pg{{position:absolute;right:44px;top:70px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;color:#fff;opacity:.8}}
.ft{{position:absolute;right:44px;bottom:26px;font-weight:600;font-size:16px;letter-spacing:2px;color:#b5b5b5}}
"""
def page(css,body,sub,pg=''): return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{HEAD}{css}</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">Classificació</div><div class="d">{sub}</div>{pg}</div>{body}<div class="ft">@veteranstarragona</div></body></html>'

def html_lliga(nom,comp,rs,zones):
    col=COLORS.get(comp,'#555')
    def z(pos):
        for a,b,t in zones:
            if a<=pos<=b: return zona(t)
        return None
    rows=''
    for i,r in enumerate(rs):
        zz=z(i+1); bg=f'background:{zz[0]}' if zz else ''; posc=f'background:{zz[1]};color:#fff' if zz else ''
        rows+=f'<div class="r" style="{bg}"><b class="pos" style="{posc}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span>{r["g"]}</span><span>{r["e"]}</span><span>{r["p"]}</span><span>{r["gf"]}</span><span>{r["gc"]}</span><span class="dg">{r["dg"]:+d}</span>{forma(r["forma"])}<b class="pts">{r["pts"]}</b></div>'
    leg=llegenda(zones)
    return page(f""".tb{{position:absolute;left:40px;top:232px;width:1000px;background:#fff;border-radius:14px;border-left:10px solid {col};box-shadow:0 2px 8px rgba(0,0,0,.05);overflow:hidden}}
.th,.r{{display:grid;grid-template-columns:48px 42px 1fr 44px 40px 40px 40px 46px 46px 56px 104px 74px;align-items:center;gap:5px;padding:0 14px 0 8px;height:72px}}
.th{{height:48px;font-weight:700;font-size:13px;letter-spacing:1.5px;color:#9a9a9a;text-transform:uppercase;border-bottom:2px solid #eee}}.th span,.r>span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #f0f0f0;font-weight:500;font-size:18px}}.r:last-child{{border-bottom:0}}
.r img{{width:40px;height:40px;object-fit:contain}}.r .n{{font-weight:600;font-size:18px;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:700;font-size:26px;width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center}}
.fm{{display:flex;gap:4px;justify-content:center}}.fm i{{width:12px;height:12px;border-radius:50%;display:block}}
.dg{{color:#777}}.pts{{font-family:'Barlow Condensed';font-weight:700;font-size:30px;text-align:center;background:{RED};color:#fff;border-radius:8px;height:44px;line-height:44px}}
.leg{{position:absolute;left:40px;bottom:26px;display:flex;gap:26px;font-weight:600;font-size:14px;letter-spacing:1px;color:#777}}.leg .lg{{display:flex;align-items:center;gap:8px}}.leg i{{width:14px;height:14px;border-radius:4px;display:block}}
</style>""",f'<div class="tb"><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>G</span><span>E</span><span>P</span><span>GF</span><span>GC</span><span>DG</span><span>Últims 5</span><span>PTS</span></div>{rows}</div><div class="leg">{leg}</div>',nom_curt(nom))

def nom_curt(nom):
    m=re.search(r'(\d)[ªA]\s*DIVISI',nom.upper()); return f'Lliga {m.group(1)}a Divisió' if m else nom.title()

def html_copa(gs,zones,pag,npag):
    secs=''
    for g,rs in gs:
        files=''
        for i,r in enumerate(rs):
            zz=zona_de(i+1,zones); bg=f'background:{zz[0]}' if zz else ''; pc=f'color:{zz[1]}' if zz else ''
            files+=f'<div class="r" style="{bg}"><b class="pos" style="{pc}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span class="st">{r["pj"]}<small>PJ</small></span><span class="st">{r["g"]}-{r["e"]}-{r["p"]}<small>G-E-P</small></span><span class="st">{r["gf"]}:{r["gc"]}<small>Gols</small></span><span class="st">{r["dg"]:+d}<small>DG</small></span><b class="pts">{r["pts"]}</b></div>'
        secs+=f'<div class="sec"><div class="sh">{g}</div>{files}</div>'
    return page(f""".wrap{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:14px}}
.sec{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);border-left:10px solid {RED}}}
.sh{{font-family:'Barlow Condensed';font-weight:700;font-size:24px;letter-spacing:2px;padding:8px 16px 4px;text-transform:uppercase;color:{RED}}}
.r{{display:grid;grid-template-columns:40px 40px 1fr 60px 90px 80px 60px 70px;align-items:center;gap:8px;padding:0 16px 0 10px;height:50px;border-top:1px solid rgba(0,0,0,.05)}}
.r img{{width:34px;height:34px;object-fit:contain}}.r .n{{font-weight:600;font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:700;font-size:24px;text-align:center}}
.st{{text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:20px;line-height:1}}.st small{{display:block;font-family:Barlow;font-size:9px;letter-spacing:1px;color:#9a9a9a;font-weight:700;margin-top:2px}}
.pts{{font-family:'Barlow Condensed';font-weight:700;font-size:28px;text-align:right}}
.leg{{position:absolute;left:40px;bottom:26px;display:flex;gap:22px;font-weight:600;font-size:14px;letter-spacing:1px;color:#777}}.leg .lg{{display:flex;align-items:center;gap:8px}}.leg i{{width:14px;height:14px;border-radius:4px;display:block}}
</style>""",f'<div class="wrap">{secs}</div><div class="leg">{llegenda(zones)}</div>','Copa F11 · Fase de grups',f'<span class="pg">{pag}/{npag}</span>' if npag>1 else '')

CSS_STORY_K=""".th,.r{display:grid;grid-template-columns:54px 52px 1fr 56px 64px 112px 84px;align-items:center;gap:8px;padding:0 14px 0 10px}
.th{height:30px;flex:none;font-weight:700;font-size:15px;letter-spacing:2px;color:#9a9a9a;text-transform:uppercase}.th span{text-align:center}.th .n{text-align:left}
.sheet{gap:8px}
.r{height:76px;flex:none;background:#fff;border-radius:12px;box-shadow:0 2px 6px rgba(0,0,0,.05);font-weight:500;font-size:24px}.r>span{text-align:center}
.r img{width:46px;height:46px;object-fit:contain}.r .n{text-align:left;font-weight:600;font-size:24px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pos{font-family:'Barlow Condensed';font-weight:700;font-size:30px;width:44px;height:44px;border-radius:9px;display:flex;align-items:center;justify-content:center}
.fm{display:flex;gap:5px;justify-content:center}.fm i{width:14px;height:14px;border-radius:50%;display:block}
.dg{color:#777}.pts{font-family:'Barlow Condensed';font-weight:700;font-size:36px;text-align:center;background:#d60000;color:#fff;border-radius:9px;height:52px;line-height:52px}
.leg{display:flex;flex-wrap:wrap;gap:8px 22px;font-weight:600;font-size:16px;letter-spacing:1px;color:#777;padding:6px 8px 0;flex:none}.leg .lg{display:flex;align-items:center;gap:8px}.leg i{width:16px;height:16px;border-radius:4px;display:block}
.sh{font-family:'Barlow Condensed';font-weight:700;font-size:34px;letter-spacing:3px;color:#d60000;text-transform:uppercase;padding:6px 8px 0;flex:none;display:flex;justify-content:space-between;align-items:baseline}.sh small{font-family:Barlow;font-weight:600;font-size:15px;letter-spacing:1px;color:#9a9a9a;text-transform:none}"""
TH='<div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>DG</span><span>Últims 5</span><span>PTS</span></div>'
def _fila_story(i,r,zz):
    bg=f'background:{zz[0]}' if zz else ''; posc=f'background:{zz[1]};color:#fff' if zz else ''
    return f'<div class="r" style="{bg}"><b class="pos" style="{posc}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span class="dg">{r["dg"]:+d}</span>{forma(r["forma"])}<b class="pts">{r["pts"]}</b></div>'

def html_story_lliga(nom,rs,zones):
    rows=''.join(_fila_story(i,r,zona_de(i+1,zones)) for i,r in enumerate(rs)); leg=llegenda(zones)
    return P.story_shell('Classificació',nom_curt(nom),TH+rows+(f'<div class="leg">{leg}</div>' if leg else ''),CSS_STORY_K)

def html_story_copa(gs,zones,pag,npag):
    cos=''
    for g,rs in gs:
        cos+=f'<div class="sh">{g}</div>'+TH+''.join(_fila_story(i,r,zona_de(i+1,zones)) for i,r in enumerate(rs))
    leg=llegenda(zones)
    return P.story_shell('Classificació','Copa F11 · Fase de grups',cos+(f'<div class="leg">{leg}</div>' if leg else ''),CSS_STORY_K,pag,npag)

def generar_story(outdir,ids=None):
    out=[]
    ts=[t['id'] for t in P.competicions()] if ids is None else ids
    for tid in ts:
        nom,comp,taules,zones=dades(tid)
        if not taules: continue
        if len(taules)>1:
            gs=sorted(taules,key=lambda x:x[0]); pags=[gs[i:i+2] for i in range(0,len(gs),2)]
            for i,p in enumerate(pags,1):
                png=os.path.join(outdir,f'story_classificacio_copa_{i}.png'); P.render_story(html_story_copa(p,zones,i,len(pags)),png); out.append((f'Història classificació Copa {i}/{len(pags)}',png))
        else:
            png=os.path.join(outdir,f'story_classificacio_{comp.lower().replace(" ","_")}.png')
            P.render_story(html_story_lliga(nom,taules[0][1],zones),png); out.append((f'Història classificació {nom_curt(nom)}',png))
    return out

def generar(outdir,ids=None):
    out=[]
    ts=[t['id'] for t in P.competicions()] if ids is None else ids
    for tid in ts:
        nom,comp,taules,zones=dades(tid)
        if not taules: continue
        if len(taules)>1:
            gs=sorted(taules,key=lambda x:x[0]); pags=[gs[i:i+4] for i in range(0,len(gs),4)]
            for i,p in enumerate(pags,1):
                png=os.path.join(outdir,f'classificacio_copa_{i}.png'); P.render(html_copa(p,zones,i,len(pags)),png); out.append((f'Classificació Copa {i}/{len(pags)}',png))
        else:
            rs=taules[0][1]; png=os.path.join(outdir,f'classificacio_{comp.lower().replace(" ","_")}.png')
            P.render(html_lliga(nom,comp,rs,zones),png); out.append((f'Classificació {nom_curt(nom)}',png))
    return out

if __name__=='__main__':
    outdir=os.path.join(V,'out'); os.makedirs(outdir,exist_ok=True)
    ids=[102,103,98,108] if '--test' in sys.argv else None
    res=generar(outdir,ids)
    if '--story' in sys.argv: res+=generar_story(outdir,ids)
    for e,p in res: print(e,'->',p)
    if '--send' in sys.argv:
        cfg=P.cfg()
        for e,p in res:
            for intent in range(4):
                r=subprocess.run(['curl','-s','-m','240','-X','POST',f'https://api.telegram.org/bot{cfg["telegram_bot_token"]}/sendDocument','-F',f'chat_id={cfg["telegram_chat_id"]}','-F',f'document=@{p}','-F',f'caption={e}','-o','/dev/null','-w','%{http_code}'],capture_output=True,text=True)
                print(e,'HTTP',r.stdout)
                if r.stdout=='200': break
                time.sleep(5)
