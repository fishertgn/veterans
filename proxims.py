#!/usr/bin/env python3
"""Pròxims partits: una imatge (1080x1350) per dia amb tots els partits de les competicions
de veterans F11 actives a MyGol. Ús: proxims.py AAAA-MM-DD AAAA-MM-DD [--send]"""
import json, sys, os, re, math, datetime, subprocess, urllib.request
V=os.path.dirname(os.path.abspath(__file__))
API='https://minifutboltarragones.mygol.es/api'; UP='https://minifutboltarragones.mygol.es/upload/'
RED='#d60000'; LOGO='file://'+V+'/logo_crop.png'
import shutil
def _chrome():
    c=os.environ.get('CHROME_BIN')
    if c: return c
    mac='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    if os.path.exists(mac): return mac
    return shutil.which('google-chrome') or shutil.which('chromium-browser') or shutil.which('chromium') or 'google-chrome'
CHROME=_chrome()
CHROME_FLAGS=['--headless=new','--disable-gpu','--hide-scrollbars','--allow-file-access-from-files']+([] if sys.platform=='darwin' else ['--no-sandbox','--disable-dev-shm-usage'])
def cfg():
    if os.environ.get('TELEGRAM_BOT_TOKEN'): return {'telegram_bot_token':os.environ['TELEGRAM_BOT_TOKEN'],'telegram_chat_id':os.environ['TELEGRAM_CHAT_ID']}
    return json.load(open(os.path.join(V,'config.json')))
def captura(html_path,png,w,h,budget=20000):
    subprocess.run([CHROME]+CHROME_FLAGS+[f'--window-size={w},{h}',f'--virtual-time-budget={budget}',f'--screenshot={png}','file://'+html_path],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return png
DIES=['DILLUNS','DIMARTS','DIMECRES','DIJOUS','DIVENDRES','DISSABTE','DIUMENGE']; MES=['GEN','FEB','MAR','ABR','MAI','JUN','JUL','AGO','SET','OCT','NOV','DES']
FONTS='<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600;700&display=swap" rel="stylesheet">'
PER_PAG=12
COLORS={'COPA':'#d60000','LLIGA 1A':'#e6a800','LLIGA 2A':'#1f6feb','LLIGA 3A':'#1a9c5b'}

def get(path, intents=4):
    import time
    for i in range(intents):
        try:
            req=urllib.request.Request(API+path, headers={'User-Agent':'Mozilla/5.0','Accept':'application/json'})
            return json.load(urllib.request.urlopen(req, timeout=40))
        except Exception as e:
            if i==intents-1: raise
            time.sleep(3*(i+1))

def nice(n):
    n=' '.join(n.split()).title()
    for a,b in (('Cf ','CF '),('Ce ','CE '),('Ue ','UE '),('Cd ','CD '),('Fc','FC'),('Cfb','CFB'),('Ucf','UCF'),('Cfv','CFV'),('Aev','AEV'),('Cef','CEF'),('Vet.','Vet. '),('P.Barça','P. Barça')):
        n=n.replace(a,b)
    return ' '.join(n.split())

def curt(name):
    """Nom curt de la competició per a l'etiqueta."""
    u=name.upper()
    if 'COPA' in u: return 'COPA'
    m=re.search(r'(\d)[ªA]\s*DIVISI', u)
    return f'LLIGA {m.group(1)}A' if m else 'LLIGA'

def competicions():
    ts=get('/tournaments')
    return [t for t in ts if t.get('status')==1 and 'VETERANS' in t['name'].upper() and 'F' in t['name'].upper() and '11' in t['name']]

def partits(d0,d1,jugats=False):
    rows=[]
    for t in competicions():
        info=get(f'/tournaments/{t["id"]}')
        teams={x['id']:x for x in info['teams']}; groups={g['id']:g['name'] for g in info['groups']}
        for jornada in get(f'/matches/fortournament/{t["id"]}'):
            for x in jornada['matches']:
                if x['idHomeTeam']<0 or x['idVisitorTeam']<0 or x['status']==10: continue
                if jugats is True and x['status']!=5: continue
                if jugats is False and x['status']!=1: continue
                d=datetime.datetime.fromisoformat(x['startTime'])
                if not (d0<=d.date()<=d1): continue
                h,a=teams[x['idHomeTeam']],teams[x['idVisitorTeam']]
                rows.append(dict(dt=d,hora=d.strftime('%H:%M'),h=nice(h['name']),hl=UP+h['logoImgUrl'],a=nice(a['name']),al=UP+a['logoImgUrl'],
                    camp=(x.get('field') or {}).get('name',''),grup=groups.get(x['idGroup'],''),comp=curt(t['name']),jornada=jornada['name'],hs=x['homeScore'],as_=x['visitorScore'],status=x['status'],id=x['id'],startTime=x['startTime']))
    rows.sort(key=lambda r:(r['dt'],r['comp'],r['grup']))
    return rows

def html_pagina(dia,rs,pag,npag):
    def row(r):
        col=COLORS.get(r['comp'],'#555'); et=f"{r['comp']}{' · '+r['grup'] if r['grup'] else ''}"
        return (f'<div class="r" style="border-left-color:{col}"><span class="h">{r["hora"]}</span>'
                f'<span class="t l"><span>{r["h"]}</span><img src="{r["hl"]}"></span><span class="x">–</span>'
                f'<span class="t"><img src="{r["al"]}"><span>{r["a"]}</span></span>'
                f'<span class="c">{r["camp"]}</span><span class="g" style="color:{col};border-color:{col}">{et}</span></div>')
    rows=''.join(row(r) for r in rs)
    pg=f'<span class="pg">{pag}/{npag}</span>' if npag>1 else ''
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1350px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:#f1f1f1;font-family:Barlow,sans-serif;color:#151515}}
.hd{{position:absolute;left:0;top:0;width:1080px;height:200px;background:{RED};color:#fff}}
.hd img{{position:absolute;left:44px;top:15px;width:170px;height:170px}}
.hd .t{{position:absolute;left:236px;top:44px;font-family:'Barlow Condensed';font-weight:700;font-size:58px;letter-spacing:1px;line-height:1;text-transform:uppercase}}
.hd .d{{position:absolute;left:238px;top:112px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:2px;color:#ffd6d6;text-transform:uppercase}}
.hd .pg{{position:absolute;right:44px;top:70px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;color:#fff;opacity:.8}}
.list{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:10px}}
.r{{height:78px;background:#fff;border-radius:12px;border-left:10px solid #999;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:78px 1fr 26px 1fr 150px 128px;align-items:center;gap:8px;padding:0 14px 0 12px}}
.h{{font-family:'Barlow Condensed';font-weight:700;font-size:34px}}
.t{{display:flex;align-items:center;gap:8px;font-weight:500;font-size:16px;line-height:1.05;min-width:0}}
.t.l{{justify-content:flex-end;text-align:right}}
.t img{{width:40px;height:40px;object-fit:contain;flex:none}}
.x{{text-align:center;color:{RED};font-weight:700;font-size:20px}}
.c{{font-size:12px;color:#9a9a9a;font-weight:500;line-height:1.1;text-align:right}}
.g{{font-weight:700;font-size:11.5px;letter-spacing:1.2px;border:2px solid;border-radius:999px;padding:4px 8px;text-transform:uppercase;text-align:center;white-space:nowrap}}
.ft{{position:absolute;right:44px;bottom:26px;font-weight:600;font-size:16px;letter-spacing:2px;color:#b5b5b5}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">Pròxims partits</div><div class="d">{dia}</div>{pg}</div><div class="list">{rows}</div><div class="ft">@veteranstarragona</div></body></html>"""

def story_shell(titol,sub,cos,css,pag=1,npag=1):
    """Carcassa comuna de les històries 1080x1920: logo gran, títol, subtítol i full clar."""
    pg=f'<span class="pg">{pag}/{npag}</span>' if npag>1 else ''
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:{RED};font-family:Barlow,sans-serif;color:#151515}}
.logo{{position:absolute;left:50%;top:30px;transform:translateX(-50%);width:330px;height:330px}}
.tt{{position:absolute;left:0;top:360px;width:1080px;text-align:center;color:#fff;font-family:'Barlow Condensed';font-weight:700;font-size:76px;letter-spacing:2px;line-height:1;text-transform:uppercase}}
.dd{{position:absolute;left:0;top:440px;width:1080px;text-align:center;color:#ffd6d6;font-family:'Barlow Condensed';font-weight:700;font-size:46px;letter-spacing:3px;line-height:1;text-transform:uppercase}}
.pg{{position:absolute;right:50px;top:60px;color:#fff;font-family:'Barlow Condensed';font-weight:700;font-size:44px;opacity:.85}}
.sheet{{position:absolute;left:40px;top:520px;width:1000px;max-height:1320px;background:#f1f1f1;border-radius:24px;padding:22px 20px;display:flex;flex-direction:column;gap:10px;overflow:hidden}}
.ft{{position:absolute;left:0;bottom:28px;width:1080px;text-align:center;color:#ffb3b3;font-weight:600;font-size:20px;letter-spacing:3px}}
{css}
</style></head><body><img class="logo" src="{LOGO}">{pg}<div class="tt">{titol}</div><div class="dd">{sub}</div><div class="sheet">{cos}</div><div class="ft">@veteranstarragona</div></body></html>"""

def render_story(html,png):
    tmp=png[:-4]+'.html'; open(tmp,'w').write(html); return captura(tmp,png,1080,1920)

def html_story(dia,rs,pag,npag):
    """Història 1080x1920: un dia per història, files grans (12 màxim)."""
    def row(r):
        col=COLORS.get(r['comp'],'#555'); et=f"{r['comp']}{' · '+r['grup'] if r['grup'] else ''}"
        return (f'<div class="r" style="border-left-color:{col}"><span class="h">{r["hora"]}</span>'
                f'<span class="eq"><span class="t"><img src="{r["hl"]}"><span>{r["h"]}</span></span><span class="t"><img src="{r["al"]}"><span>{r["a"]}</span></span></span>'
                f'<span class="g" style="color:{col};border-color:{col}">{et}</span></div>')
    rows=''.join(row(r) for r in rs)
    pg=f'<span class="pg">{pag}/{npag}</span>' if npag>1 else ''
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:{RED};font-family:Barlow,sans-serif;color:#151515}}
.logo{{position:absolute;left:50%;top:30px;transform:translateX(-50%);width:330px;height:330px}}
.tt{{position:absolute;left:0;top:360px;width:1080px;text-align:center;color:#fff;font-family:'Barlow Condensed';font-weight:700;font-size:76px;letter-spacing:2px;line-height:1;text-transform:uppercase}}
.dd{{position:absolute;left:0;top:440px;width:1080px;text-align:center;color:#ffd6d6;font-family:'Barlow Condensed';font-weight:700;font-size:46px;letter-spacing:3px;line-height:1;text-transform:uppercase}}
.pg{{position:absolute;right:50px;top:60px;color:#fff;font-family:'Barlow Condensed';font-weight:700;font-size:44px;opacity:.85}}
.sheet{{position:absolute;left:40px;top:520px;width:1000px;max-height:1320px;background:#f1f1f1;border-radius:24px;padding:22px 20px;display:flex;flex-direction:column;gap:10px;overflow:hidden}}
.r{{height:96px;flex:none;background:#fff;border-radius:12px;border-left:12px solid #999;box-shadow:0 2px 6px rgba(0,0,0,.05);display:grid;grid-template-columns:110px 1fr 170px;align-items:center;gap:8px;padding:0 14px 0 12px}}
.h{{font-family:'Barlow Condensed';font-weight:700;font-size:44px}}
.eq{{display:flex;flex-direction:column;gap:6px;min-width:0}}
.t{{display:flex;align-items:center;gap:10px;font-weight:500;font-size:24px;line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.t img{{width:36px;height:36px;object-fit:contain;flex:none}}
.g{{font-weight:700;font-size:15px;letter-spacing:1.5px;border:3px solid;border-radius:999px;padding:6px 8px;text-transform:uppercase;text-align:center;white-space:nowrap}}
.ft{{position:absolute;left:0;bottom:28px;width:1080px;text-align:center;color:#ffb3b3;font-weight:600;font-size:20px;letter-spacing:3px}}
</style></head><body><img class="logo" src="{LOGO}">{pg}<div class="tt">Pròxims partits</div><div class="dd">{dia}</div><div class="sheet">{rows}</div><div class="ft">@veteranstarragona</div></body></html>"""

def generar_story(d0,d1,outdir,per_pag=12):
    rows=partits(d0,d1); out=[]
    for dia in sorted({r['dt'].date() for r in rows}):
        rs=[r for r in rows if r['dt'].date()==dia]; et=f'{DIES[dia.weekday()]} {dia.day} {MES[dia.month-1]}'
        pags=[rs[i:i+per_pag] for i in range(0,len(rs),per_pag)]
        for i,p in enumerate(pags,1):
            png=os.path.join(outdir,f'story_proxims_{dia.isoformat()}'+(f'_{i}' if len(pags)>1 else '')+'.png')
            tmp=png[:-4]+'.html'; open(tmp,'w').write(html_story(et,p,i,len(pags)))
            captura(tmp,png,1080,1920)
            out.append(('Història '+et+(f' ({i}/{len(pags)})' if len(pags)>1 else ''),len(p),png))
    return out

def render(html,png):
    tmp=png[:-4]+'.html'; open(tmp,'w').write(html)
    captura(tmp,png,1080,1350)
    return png

def generar(d0,d1,outdir):
    rows=partits(d0,d1); out=[]
    for dia in sorted({r['dt'].date() for r in rows}):
        rs=[r for r in rows if r['dt'].date()==dia]
        etiqueta=f'{DIES[dia.weekday()]} {dia.day} {MES[dia.month-1]}'
        pags=[rs[i:i+PER_PAG] for i in range(0,len(rs),PER_PAG)]
        for i,p in enumerate(pags,1):
            png=os.path.join(outdir,f'proxims_{dia.isoformat()}'+(f'_{i}' if len(pags)>1 else '')+'.png')
            out.append((etiqueta+(f' ({i}/{len(pags)})' if len(pags)>1 else ''),len(p),render(html_pagina(etiqueta,p,i,len(pags)),png)))
    return out

if __name__=='__main__':
    d0=datetime.date.fromisoformat(sys.argv[1]); d1=datetime.date.fromisoformat(sys.argv[2])
    outdir=os.path.join(V,'out'); os.makedirs(outdir,exist_ok=True)
    res=generar(d0,d1,outdir)
    if '--story' in sys.argv: res+=generar_story(d0,d1,outdir)
    for e,n,p in res: print(e,n,'partits ->',p)
    if '--send' in sys.argv:
        cfg=cfg()
        import time
        for e,n,p in res:
            for intent in range(4):
                r=subprocess.run(['curl','-s','-m','240','-X','POST',f'https://api.telegram.org/bot{cfg["telegram_bot_token"]}/sendDocument','-F',f'chat_id={cfg["telegram_chat_id"]}','-F',f'document=@{p}','-F',f'caption=Pròxims partits · {e} · {n} partits','-o','/dev/null','-w','%{http_code}'],capture_output=True,text=True)
                print(e,'HTTP',r.stdout)
                if r.stdout=='200': break
                time.sleep(5)
