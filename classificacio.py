#!/usr/bin/env python3
"""Classificació: una imatge per lliga (taula amb zones) i dues per la Copa (4 grups per imatge).
Ús: classificacio.py [--send] [--test]   (--test usa les lligues 25-26: 102, 103, 98)"""
import sys, os, re, json, subprocess, time
import proxims as P
V,RED,LOGO,COLORS,FONTS=P.V,P.RED,P.LOGO,P.COLORS,P.FONTS
UP='https://minifutboltarragones.mygol.es/upload/'
ZONES={'CAMPI':('#dff5e6','#1a9c5b','Campió'),'PROMOC':('#fff1cc','#b8860b','Promoció'),'ASCENS':('#dcefff','#1f6feb','Ascens'),'DESCENS':('#ffe3e3','#d60000','Descens')}
def zona(title):
    u=title.upper()
    for k,v in ZONES.items():
        if k in u: return v
    return ('#f0f0f0','#555',title.title())

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
    vist=[]; leg=''
    for a,b,t in zones:
        zz=zona(t)
        if zz[2] in vist: continue
        vist.append(zz[2]); leg+=f'<span class="lg"><i style="background:{zz[1]}"></i>{t.title()}</span>'
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
    q=max([b for a,b,t in zones if 'DESCENS' not in t.upper()] or [2])
    secs=''
    for g,rs in gs:
        secs+=f'<div class="sec"><div class="sh">{g}<small>Els {q} primers passen de ronda</small></div>'+''.join(f'<div class="r{" q" if i<q else ""}"><b class="pos">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span class="st">{r["pj"]}<small>PJ</small></span><span class="st">{r["g"]}-{r["e"]}-{r["p"]}<small>G-E-P</small></span><span class="st">{r["gf"]}:{r["gc"]}<small>Gols</small></span><span class="st">{r["dg"]:+d}<small>DG</small></span><b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(rs))+'</div>'
    return page(f""".wrap{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:14px}}
.sec{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);border-left:10px solid {RED}}}
.sh{{font-family:'Barlow Condensed';font-weight:700;font-size:24px;letter-spacing:2px;padding:8px 16px 4px;text-transform:uppercase;color:{RED};display:flex;justify-content:space-between;align-items:baseline}}.sh small{{font-family:Barlow;font-weight:600;font-size:12px;letter-spacing:1px;color:#9a9a9a;text-transform:none}}
.r{{display:grid;grid-template-columns:40px 40px 1fr 60px 90px 80px 60px 70px;align-items:center;gap:8px;padding:0 16px 0 10px;height:50px;border-top:1px solid #f0f0f0}}
.r.q{{background:#fff3f3}}
.r img{{width:34px;height:34px;object-fit:contain}}.r .n{{font-weight:600;font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:700;font-size:24px;text-align:center}}.r.q .pos{{color:{RED}}}
.st{{text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:20px;line-height:1}}.st small{{display:block;font-family:Barlow;font-size:9px;letter-spacing:1px;color:#9a9a9a;font-weight:700;margin-top:2px}}
.pts{{font-family:'Barlow Condensed';font-weight:700;font-size:28px;text-align:right}}
</style>""",f'<div class="wrap">{secs}</div>','Copa F11 · Fase de grups',f'<span class="pg">{pag}/{npag}</span>' if npag>1 else '')

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
    res=generar(outdir,[102,103,98,108] if '--test' in sys.argv else None)
    for e,p in res: print(e,'->',p)
    if '--send' in sys.argv:
        cfg=P.cfg()
        for e,p in res:
            for intent in range(4):
                r=subprocess.run(['curl','-s','-m','240','-X','POST',f'https://api.telegram.org/bot{cfg["telegram_bot_token"]}/sendDocument','-F',f'chat_id={cfg["telegram_chat_id"]}','-F',f'document=@{p}','-F',f'caption={e}','-o','/dev/null','-w','%{http_code}'],capture_output=True,text=True)
                print(e,'HTTP',r.stdout)
                if r.stdout=='200': break
                time.sleep(5)
