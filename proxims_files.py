#!/usr/bin/env python3
"""Variants de 'pròxims partits' amb un partit per fila. Ús: proxims_files.py AAAA-MM-DD [estil]"""
import sys, os, datetime
import proxims as P
V=P.V; RED=P.RED; LOGO=P.LOGO; COLORS=P.COLORS; FONTS=P.FONTS
HEAD="""<!doctype html><html><head><meta charset="utf-8">%s<style>
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1350px;overflow:hidden;position:relative}img{display:block}
body{background:#f1f1f1;font-family:Barlow,sans-serif;color:#151515}
.hd{position:absolute;left:0;top:0;width:1080px;height:200px;background:%s;color:#fff}
.hd img{position:absolute;left:44px;top:15px;width:170px;height:170px}
.hd .t{position:absolute;left:236px;top:44px;font-family:'Barlow Condensed';font-weight:800;font-size:58px;letter-spacing:1px;line-height:1;text-transform:uppercase}
.hd .d{position:absolute;left:238px;top:112px;font-family:'Barlow Condensed';font-weight:700;font-size:40px;letter-spacing:2px;color:#ffd6d6;text-transform:uppercase}
.list{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:%dpx}
.ft{position:absolute;right:44px;bottom:26px;font-weight:600;font-size:16px;letter-spacing:2px;color:#b5b5b5}
"""
def hdr(dia): return f'<div class="hd"><img src="{LOGO}"><div class="t">Pròxims partits</div><div class="d">{dia}</div></div>'
def pill(r): return f"{r['comp']}{' · '+r['grup'] if r['grup'] else ''}"

# R1: targeta blanca amb barra lateral · hora | local | – | visitant | camp | competició
def r1(dia,rs):
    rows=''.join(f'<div class="r" style="border-left-color:{COLORS.get(r["comp"],"#555")}"><span class="h">{r["hora"]}</span><span class="t l"><span>{r["h"]}</span><img src="{r["hl"]}"></span><span class="x">–</span><span class="t"><img src="{r["al"]}"><span>{r["a"]}</span></span><span class="c">{r["camp"]}</span><span class="g" style="color:{COLORS.get(r["comp"],"#555")};border-color:{COLORS.get(r["comp"],"#555")}">{pill(r)}</span></div>' for r in rs)
    return HEAD%(FONTS,RED,10)+f"""
.r{{height:78px;background:#fff;border-radius:12px;border-left:10px solid #999;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:78px 1fr 26px 1fr 150px 128px;align-items:center;gap:8px;padding:0 14px 0 12px}}
.h{{font-family:'Barlow Condensed';font-weight:800;font-size:34px}}
.t{{display:flex;align-items:center;gap:8px;font-weight:600;font-size:16px;line-height:1.05;min-width:0}}
.t.l{{justify-content:flex-end;text-align:right}}
.t img{{width:40px;height:40px;object-fit:contain;flex:none}}
.x{{text-align:center;color:{RED};font-weight:700;font-size:20px}}
.c{{font-size:12px;color:#9a9a9a;font-weight:500;line-height:1.1;text-align:right}}
.g{{font-weight:700;font-size:11.5px;letter-spacing:1.2px;border:2px solid;border-radius:999px;padding:4px 8px;text-transform:uppercase;text-align:center;white-space:nowrap}}
</style></head><body>{hdr(dia)}<div class="list">{rows}</div><div class="ft">@veteranstarragona</div></body></html>"""

# R2: taula neta sense targetes · franges alternes, hora en color, equips encarats al centre
def r2(dia,rs):
    rows=''.join(f'<div class="r"><span class="h" style="color:{COLORS.get(r["comp"],"#555")}">{r["hora"]}</span><span class="t l">{r["h"]}</span><img src="{r["hl"]}"><span class="x">vs</span><img src="{r["al"]}"><span class="t">{r["a"]}</span><span class="g"><b style="background:{COLORS.get(r["comp"],"#555")}"></b>{pill(r)}</span><span class="c">{r["camp"]}</span></div>' for r in rs)
    return HEAD%(FONTS,RED,0)+f"""
.list{{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.05)}}
.r{{height:88px;display:grid;grid-template-columns:86px 1fr 42px 40px 42px 1fr 150px 130px;align-items:center;gap:8px;padding:0 20px;border-bottom:1px solid #ececec}}
.r:nth-child(even){{background:#fafafa}}
.h{{font-family:'Barlow Condensed';font-weight:800;font-size:34px}}
.t{{font-weight:600;font-size:16.5px;line-height:1.05}}
.t.l{{text-align:right}}
.r img{{width:42px;height:42px;object-fit:contain}}
.x{{text-align:center;color:#c4c4c4;font-weight:700;font-size:13px;letter-spacing:1px}}
.g{{display:flex;align-items:center;gap:8px;font-weight:700;font-size:12px;letter-spacing:1.2px;color:#444;text-transform:uppercase;white-space:nowrap}}
.g b{{width:12px;height:12px;border-radius:50%;flex:none}}
.c{{font-size:12px;color:#9a9a9a;font-weight:500;line-height:1.1;text-align:right}}
</style></head><body>{hdr(dia)}<div class="list">{rows}</div><div class="ft">@veteranstarragona</div></body></html>"""

# R3: bloc d'hora en color de competició · equips amb escuts · camp · competició en text
def r3(dia,rs):
    rows=''.join(f'<div class="r"><span class="h" style="background:{COLORS.get(r["comp"],"#555")}">{r["hora"]}</span><span class="t"><img src="{r["hl"]}"><span>{r["h"]}</span></span><span class="x">–</span><span class="t"><img src="{r["al"]}"><span>{r["a"]}</span></span><span class="g" style="color:{COLORS.get(r["comp"],"#555")}">{pill(r)}</span><span class="c">{r["camp"]}</span></div>' for r in rs)
    return HEAD%(FONTS,RED,10)+f"""
.r{{height:78px;background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:92px 1fr 22px 1fr 124px 150px;align-items:center;gap:10px;padding:0 16px 0 0;overflow:hidden}}
.h{{height:78px;display:flex;align-items:center;justify-content:center;color:#fff;font-family:'Barlow Condensed';font-weight:800;font-size:32px}}
.t{{display:flex;align-items:center;gap:8px;font-weight:600;font-size:16px;line-height:1.05;min-width:0}}
.t img{{width:40px;height:40px;object-fit:contain;flex:none}}
.x{{text-align:center;color:#bbb;font-weight:700;font-size:18px}}
.g{{font-family:'Barlow Condensed';font-weight:700;font-size:20px;letter-spacing:1px;text-transform:uppercase;white-space:nowrap;text-align:right}}
.c{{font-size:12px;color:#9a9a9a;font-weight:500;line-height:1.1;text-align:right}}
</style></head><body>{hdr(dia)}<div class="list">{rows}</div><div class="ft">@veteranstarragona</div></body></html>"""

if __name__=='__main__':
    d=datetime.date.fromisoformat(sys.argv[1]); rows=P.partits(d,d)
    dia=f'{P.DIES[d.weekday()]} {d.day} {P.MES[d.month-1]}'
    os.makedirs(os.path.join(V,'out'),exist_ok=True)
    for nom,f in (('R1_targeta',r1),('R2_taula',r2),('R3_bloc',r3)):
        png=os.path.join(V,'out',f'{nom}_{d.isoformat()}.png'); P.render(f(dia,rows[:12]),png); print(png)
