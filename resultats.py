#!/usr/bin/env python3
"""Resultats: post 1080x1350, un partit per fila, 12 per imatge. Ús: resultats.py AAAA-MM-DD AAAA-MM-DD [--send] [--test]"""
import sys, os, datetime, subprocess, json, random
import proxims as P
V,RED,LOGO,COLORS,FONTS,DIES,MES=P.V,P.RED,P.LOGO,P.COLORS,P.FONTS,P.DIES,P.MES
PER_PAG=12

def html_pagina(sub,rs,pag,npag):
    def row(r):
        col=COLORS.get(r['comp'],'#555'); et=f"{r['comp']}{' · '+r['grup'] if r['grup'] else ''}"
        jugat=r['status']==5
        w=('e','e') if not jugat else ('w','lo') if r['hs']>r['as_'] else ('lo','w') if r['hs']<r['as_'] else ('e','e')
        marc=f'<b>{r["hs"]}</b><i style="background:{col}"></i><b>{r["as_"]}</b>' if jugat else '<b class="np">–</b>'
        d=f"{DIES[r['dt'].weekday()][:3]} {r['dt'].day}"
        return (f'<div class="r" style="border-left-color:{col}"><span class="dd">{d}</span>'
                f'<span class="t l {w[0]}"><span>{r["h"]}</span><img src="{r["hl"]}"></span>'
                f'<span class="sc">{marc}</span>'
                f'<span class="t {w[1]}"><img src="{r["al"]}"><span>{r["a"]}</span></span>'
                f'<span class="g" style="color:{col};border-color:{col}">{et}</span></div>')
    rows=''.join(row(r) for r in rs); pg=f'<span class="pg">{pag}/{npag}</span>' if npag>1 else ''
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1350px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:#f1f1f1;font-family:Barlow,sans-serif;color:#151515}}
.hd{{position:absolute;left:0;top:0;width:1080px;height:200px;background:{RED};color:#fff}}
.hd img{{position:absolute;left:44px;top:15px;width:170px;height:170px}}
.hd .t{{position:absolute;left:236px;top:44px;font-family:'Barlow Condensed';font-weight:700;font-size:58px;letter-spacing:1px;line-height:1;text-transform:uppercase;color:#fff}}
.hd .d{{position:absolute;left:238px;top:112px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:2px;color:#ffd6d6;text-transform:uppercase}}
.hd .pg{{position:absolute;right:44px;top:70px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;color:#fff;opacity:.8}}
.list{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:10px}}
.r{{height:78px;background:#fff;border-radius:12px;border-left:10px solid #999;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:64px 1fr 150px 1fr 128px;align-items:center;gap:8px;padding:0 14px 0 12px}}
.dd{{font-family:'Barlow Condensed';font-weight:700;font-size:20px;color:#9a9a9a;text-transform:uppercase}}
.t{{display:flex;align-items:center;gap:8px;font-weight:500;font-size:16px;line-height:1.05;min-width:0;color:#777}}.t.w{{color:#111;font-weight:600}}.t.l{{justify-content:flex-end;text-align:right}}.t img{{width:40px;height:40px;object-fit:contain;flex:none}}
.sc{{display:flex;justify-content:center;align-items:center;gap:16px;font-family:'Barlow Condensed';font-weight:700;font-size:58px;line-height:1;color:#151515}}.sc i{{width:4px;height:44px;display:block;border-radius:2px}}.sc .np{{color:#bbb}}
.g{{font-weight:700;font-size:11.5px;letter-spacing:1.2px;border:2px solid;border-radius:999px;padding:4px 8px;text-transform:uppercase;text-align:center;white-space:nowrap}}
.ft{{position:absolute;right:44px;bottom:26px;font-weight:600;font-size:16px;letter-spacing:2px;color:#b5b5b5}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">Resultats</div><div class="d">{sub}</div>{pg}</div><div class="list">{rows}</div><div class="ft">@veteranstarragona</div></body></html>"""

def subtitol(rows,d0,d1):
    j=sorted({r['jornada'] for r in rows}); jt=j[0] if len(j)==1 else 'Cap de setmana'
    dates=f'{d0.day}-{d1.day} {MES[d1.month-1]}' if d0.month==d1.month else f'{d0.day} {MES[d0.month-1]} - {d1.day} {MES[d1.month-1]}'
    return f'{jt} · {dates}'

def generar(d0,d1,outdir,test=False):
    rows=P.partits(d0,d1,jugats=None)
    if test:
        random.seed(7)
        for i,r in enumerate(rows):
            r['hs'],r['as_']=random.choice([0,1,1,2,2,3,4]),random.choice([0,1,1,2,2,3]); r['status']=1 if i in (2,9) else 5
    rows.sort(key=lambda r:(r['dt'],r['comp'],r['grup'])); out=[]
    if not rows: return out
    sub=subtitol(rows,d0,d1); pags=[rows[i:i+PER_PAG] for i in range(0,len(rows),PER_PAG)]
    for i,p in enumerate(pags,1):
        png=os.path.join(outdir,f'resultats_{d0.isoformat()}'+(f'_{i}' if len(pags)>1 else '')+'.png')
        P.render(html_pagina(sub,p,i,len(pags)),png); out.append((f'Resultats {i}/{len(pags)}' if len(pags)>1 else 'Resultats',len(p),png))
    return out

if __name__=='__main__':
    d0=datetime.date.fromisoformat(sys.argv[1]); d1=datetime.date.fromisoformat(sys.argv[2])
    outdir=os.path.join(V,'out'); os.makedirs(outdir,exist_ok=True)
    res=generar(d0,d1,outdir,test='--test' in sys.argv)
    if not res: print('Cap partit jugat en aquest període.')
    for e,n,p in res: print(e,n,'partits ->',p)
    if '--send' in sys.argv:
        import time; cfg=P.cfg()
        for e,n,p in res:
            for intent in range(4):
                r=subprocess.run(['curl','-s','-m','240','-X','POST',f'https://api.telegram.org/bot{cfg["telegram_bot_token"]}/sendDocument','-F',f'chat_id={cfg["telegram_chat_id"]}','-F',f'document=@{p}','-F',f'caption={e} · {n} partits','-o','/dev/null','-w','%{http_code}'],capture_output=True,text=True)
                print(e,'HTTP',r.stdout)
                if r.stdout=='200': break
                time.sleep(5)
