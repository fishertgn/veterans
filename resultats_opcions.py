#!/usr/bin/env python3
import sys, os, datetime, random
import proxims as P
V=P.V; RED=P.RED; LOGO=P.LOGO; COLORS=P.COLORS; FONTS=P.FONTS
d0=datetime.date(2026,9,26); d1=datetime.date(2026,9,27)
rows=P.partits(d0,d1)[:12]
random.seed(7)
for r in rows: r['hs'],r['as']=random.choice([0,1,1,2,2,3,4]),random.choice([0,1,1,2,2,3])
def col(r): return COLORS.get(r['comp'],'#555')
def pill(r): return f"{r['comp']}{' · '+r['grup'] if r['grup'] else ''}"
def dia(r): return f"{P.DIES[r['dt'].weekday()][:3]} {r['dt'].day}"
CSS0=f"""*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1350px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:#f1f1f1;font-family:Barlow,sans-serif;color:#151515}}
.hd{{position:absolute;left:0;top:0;width:1080px;height:200px;background:{RED};color:#fff}}
.hd img{{position:absolute;left:44px;top:15px;width:170px;height:170px}}
.hd .t{{position:absolute;left:236px;top:44px;font-family:'Barlow Condensed';font-weight:800;font-size:58px;letter-spacing:1px;line-height:1;text-transform:uppercase;color:#fff}}
.hd .d{{position:absolute;left:238px;top:112px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:2px;color:#ffd6d6;text-transform:uppercase}}
.list{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:10px}}
.ft{{position:absolute;right:44px;bottom:26px;font-weight:600;font-size:16px;letter-spacing:2px;color:#b5b5b5}}
"""
def page(css,body,title='Resultats',sub='Jornada 1 · 26-27 set'):
    return f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>{CSS0}{css}</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">{title}</div><div class="d">{sub}</div></div>{body}<div class="ft">@veteranstarragona</div></body></html>'
def wl(r): 
    if r['hs']>r['as']: return 'w','lo'
    if r['hs']<r['as']: return 'lo','w'
    return 'e','e'
OUT={}
# A · continuïtat: fila R1 amb marcador al centre en caixa negra
def A():
    rs=''.join(f'<div class="r" style="border-left-color:{col(r)}"><span class="dd">{dia(r)}</span><span class="t l {wl(r)[0]}"><span>{r["h"]}</span><img src="{r["hl"]}"></span><span class="sc"><b>{r["hs"]}</b><i>-</i><b>{r["as"]}</b></span><span class="t {wl(r)[1]}"><img src="{r["al"]}"><span>{r["a"]}</span></span><span class="g" style="color:{col(r)};border-color:{col(r)}">{pill(r)}</span></div>' for r in rows)
    return page(f""".r{{height:78px;background:#fff;border-radius:12px;border-left:10px solid #999;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:64px 1fr 130px 1fr 128px;align-items:center;gap:8px;padding:0 14px 0 12px}}
.dd{{font-family:'Barlow Condensed';font-weight:700;font-size:20px;color:#9a9a9a;text-transform:uppercase}}
.t{{display:flex;align-items:center;gap:8px;font-weight:600;font-size:16px;line-height:1.05;min-width:0}}.t.l{{justify-content:flex-end;text-align:right}}.t img{{width:40px;height:40px;object-fit:contain;flex:none}}
.t.w{{font-weight:700}}.t.l.w span,.t.w span{{color:#111}}.t.l span,.t span{{color:#666}}
.sc{{display:flex;justify-content:center;align-items:center;gap:6px;background:#151515;color:#fff;border-radius:8px;height:46px;font-family:'Barlow Condensed';font-weight:800;font-size:34px}}.sc i{{font-style:normal;color:{RED};font-size:26px}}
.g{{font-weight:700;font-size:11.5px;letter-spacing:1.2px;border:2px solid;border-radius:999px;padding:4px 8px;text-transform:uppercase;text-align:center;white-space:nowrap}}""",f'<div class="list">{rs}</div>')
OUT['RA_continuitat']=A
# B · marcador en bloc de color a l'esquerra (com la hora)
def B():
    rs=''.join(f'<div class="r"><span class="sc" style="background:{col(r)}">{r["hs"]}<i>-</i>{r["as"]}</span><span class="t {wl(r)[0]}"><img src="{r["hl"]}"><span>{r["h"]}</span></span><span class="x">·</span><span class="t {wl(r)[1]}"><img src="{r["al"]}"><span>{r["a"]}</span></span><span class="g" style="color:{col(r)}">{pill(r)}</span><span class="c">{dia(r)} · {r["hora"]}</span></div>' for r in rows)
    return page(f""".r{{height:78px;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:118px 1fr 18px 1fr 124px 96px;align-items:center;gap:10px;padding:0 16px 0 0;overflow:hidden}}
.sc{{height:78px;display:flex;align-items:center;justify-content:center;gap:4px;color:#fff;font-family:'Barlow Condensed';font-weight:800;font-size:38px}}.sc i{{font-style:normal;opacity:.7;font-size:26px}}
.t{{display:flex;align-items:center;gap:8px;font-weight:600;font-size:16px;line-height:1.05;min-width:0;color:#777}}.t.w{{color:#111;font-weight:700}}.t img{{width:40px;height:40px;object-fit:contain;flex:none}}
.x{{text-align:center;color:#ccc}}
.g{{font-family:'Barlow Condensed';font-weight:700;font-size:20px;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;text-align:right}}
.c{{font-size:12px;color:#9a9a9a;font-weight:600;text-align:right;text-transform:uppercase;letter-spacing:1px}}""",f'<div class="list">{rs}</div>')
OUT['RB_bloc']=B
# C · seccions per competició/grup, files compactes
def C():
    grups={}
    for r in rows: grups.setdefault(pill(r),[]).append(r)
    secs=''
    for g,rs in sorted(grups.items()):
        c=col(rs[0])
        secs+=f'<div class="sec"><div class="sh" style="background:{c}">{g}</div>'+''.join(f'<div class="r"><span class="t l {wl(r)[0]}"><span>{r["h"]}</span><img src="{r["hl"]}"></span><span class="sc">{r["hs"]} - {r["as"]}</span><span class="t {wl(r)[1]}"><img src="{r["al"]}"><span>{r["a"]}</span></span></div>' for r in rs)+'</div>'
    return page(f""".list{{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-content:start}}
.sec{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05)}}
.sh{{color:#fff;font-family:'Barlow Condensed';font-weight:800;font-size:22px;letter-spacing:2px;padding:6px 14px}}
.r{{height:62px;display:grid;grid-template-columns:1fr 84px 1fr;align-items:center;gap:6px;padding:0 12px;border-top:1px solid #eee}}
.t{{display:flex;align-items:center;gap:7px;font-weight:600;font-size:14.5px;line-height:1.05;min-width:0;color:#777}}.t.w{{color:#111;font-weight:700}}.t.l{{justify-content:flex-end;text-align:right}}.t img{{width:34px;height:34px;object-fit:contain;flex:none}}
.sc{{text-align:center;font-family:'Barlow Condensed';font-weight:800;font-size:30px;background:#151515;color:#fff;border-radius:6px;height:40px;line-height:40px}}""",f'<div class="list">{secs}</div>')
OUT['RC_grups']=C
# D · marcador gegant centrat, equips als costats
def D():
    rs=''.join(f'<div class="r" style="border-left-color:{col(r)}"><span class="t l {wl(r)[0]}"><span>{r["h"]}</span><img src="{r["hl"]}"></span><span class="sc"><b>{r["hs"]}</b><i></i><b>{r["as"]}</b></span><span class="t {wl(r)[1]}"><img src="{r["al"]}"><span>{r["a"]}</span></span><span class="meta"><span class="g" style="color:{col(r)}">{pill(r)}</span><span class="c">{dia(r)} · {r["hora"]}</span></span></div>' for r in rows)
    return page(f""".r{{height:78px;background:#fff;border-radius:12px;border-left:10px solid #999;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:1fr 150px 1fr 150px;align-items:center;gap:8px;padding:0 14px 0 12px}}
.t{{display:flex;align-items:center;gap:9px;font-weight:600;font-size:17px;line-height:1.05;min-width:0;color:#777}}.t.w{{color:#111;font-weight:700}}.t.l{{justify-content:flex-end;text-align:right}}.t img{{width:44px;height:44px;object-fit:contain;flex:none}}
.sc{{display:flex;justify-content:center;align-items:center;gap:14px;font-family:'Barlow Condensed';font-weight:800;font-size:56px;line-height:1}}.sc i{{width:14px;height:5px;background:{RED};display:block}}
.meta{{display:flex;flex-direction:column;align-items:flex-end;gap:4px}}
.g{{font-family:'Barlow Condensed';font-weight:700;font-size:19px;letter-spacing:1px;text-transform:uppercase;white-space:nowrap}}
.c{{font-size:11.5px;color:#9a9a9a;font-weight:600;text-transform:uppercase;letter-spacing:1px}}""",f'<div class="list">{rs}</div>')
OUT['RD_gegant']=D
# E · fons fosc
def E():
    rs=''.join(f'<div class="r"><span class="g" style="color:{col(r)};border-color:{col(r)}">{pill(r)}</span><span class="t l {wl(r)[0]}"><span>{r["h"]}</span><img src="{r["hl"]}"></span><span class="sc">{r["hs"]}<i>:</i>{r["as"]}</span><span class="t {wl(r)[1]}"><img src="{r["al"]}"><span>{r["a"]}</span></span><span class="c">{dia(r)}</span></div>' for r in rows)
    return page(f"""body{{background:#111}}.list{{gap:0;background:#1b1b1b;border-radius:14px;overflow:hidden}}
.r{{height:80px;display:grid;grid-template-columns:118px 1fr 120px 1fr 54px;align-items:center;gap:8px;padding:0 16px;border-bottom:1px solid #2a2a2a;color:#fff}}
.t{{display:flex;align-items:center;gap:9px;font-weight:600;font-size:16.5px;line-height:1.05;min-width:0;color:#9a9a9a}}.t.w{{color:#fff;font-weight:700}}.t.l{{justify-content:flex-end;text-align:right}}.t img{{width:40px;height:40px;object-fit:contain;flex:none;background:#fff;border-radius:50%;padding:2px}}
.sc{{text-align:center;font-family:'Barlow Condensed';font-weight:800;font-size:44px;color:#ffd400}}.sc i{{font-style:normal;color:#666;margin:0 4px}}
.g{{font-weight:700;font-size:10.5px;letter-spacing:1.2px;border:2px solid;border-radius:999px;padding:4px 6px;text-transform:uppercase;text-align:center;white-space:nowrap}}
.c{{font-family:'Barlow Condensed';font-weight:700;font-size:18px;color:#777;text-align:right;text-transform:uppercase}}
.ft{{color:#555}}""",f'<div class="list">{rs}</div>')
OUT['RE_fosc']=E
# F · guanyador ressaltat amb el color de la competició
def F():
    def side(r,side):
        w=wl(r)[0 if side=='h' else 1]; c=col(r)
        st=f'background:{c};color:#fff' if w=='w' else ('background:#eee;color:#666' if w=='e' else 'background:#f7f7f7;color:#999')
        nm=r['h'] if side=='h' else r['a']; lg=r['hl'] if side=='h' else r['al']; sc=r['hs'] if side=='h' else r['as']
        return f'<span class="team" style="{st}"><img src="{lg}"><span class="n">{nm}</span><b>{sc}</b></span>'
    rs=''.join(f'<div class="r"><span class="dd">{dia(r)}<small>{r["hora"]}</small></span>{side(r,"h")}{side(r,"a")}<span class="g" style="color:{col(r)}">{pill(r).replace(" · ","<br>")}</span></div>' for r in rows)
    return page(f""".r{{height:78px;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:70px 1fr 1fr 110px;align-items:center;gap:8px;padding:0 12px}}
.dd{{font-family:'Barlow Condensed';font-weight:800;font-size:22px;color:#333;text-transform:uppercase;line-height:1}}.dd small{{display:block;font-size:15px;color:#9a9a9a;font-weight:700}}
.team{{height:54px;border-radius:10px;display:grid;grid-template-columns:40px 1fr 40px;align-items:center;gap:8px;padding:0 8px 0 6px;font-weight:700;font-size:15.5px;line-height:1.05}}
.team img{{width:36px;height:36px;object-fit:contain;background:#fff;border-radius:50%;padding:2px}}.team .n{{min-width:0}}.team b{{font-family:'Barlow Condensed';font-size:34px;text-align:right}}
.g{{font-family:'Barlow Condensed';font-weight:700;font-size:17px;letter-spacing:1px;text-transform:uppercase;text-align:right;line-height:1.05}}""",f'<div class="list">{rs}</div>')
OUT['RF_guanyador']=F
for nom,f in OUT.items():
    png=os.path.join(V,'out',f'{nom}.png'); P.render(f(),png); print(png)
