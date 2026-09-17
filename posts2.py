import importlib.util, sys, io
spec=importlib.util.spec_from_file_location('p','posts.py'); p=importlib.util.module_from_spec(spec); sys.stdout=io.StringIO(); spec.loader.exec_module(p); sys.stdout=sys.__stdout__
rows,dies,RED,LOGO,BASE,W=p.rows,p.dies,p.RED,p.LOGO,p.BASE,p.W
def card(r,cls=''):
    return f'<div class="c {cls}"><div class="top"><span class="d">{r["dia"][:3]} {r["dia"].split()[1]}</span><span class="h">{r["hora"]}</span><span class="g">{r["grup"]}</span></div><div class="vs"><div class="t"><img src="{r["hl"]}"><span>{r["h"]}</span></div><b>vs</b><div class="t"><img src="{r["al"]}"><span>{r["a"]}</span></div></div><div class="f">{r["camp"]}</div></div>'
COMMON=f'''
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.c{{background:#fff;border-radius:18px;padding:14px 18px;box-shadow:0 8px 24px rgba(0,0,0,.14)}}
.top{{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:16px;letter-spacing:2px;color:#888}}
.top .h{{font-family:Anton;font-size:36px;color:#111;letter-spacing:1px}}
.top .g{{background:#111;color:#fff;padding:3px 10px;border-radius:6px;font-size:14px}}
.vs{{display:grid;grid-template-columns:1fr 34px 1fr;align-items:center;margin-top:8px}}
.t{{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;font-weight:700;font-size:16px;line-height:1.05;height:98px}}
.t img{{width:58px;height:58px;object-fit:contain}}
.vs b{{text-align:center;color:{RED};font-size:15px;font-weight:700}}
.f{{margin-top:4px;text-align:center;font-size:14px;color:#888;font-weight:500;letter-spacing:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
'''
# 2A: fons vermell + logo centrat (com la història)
W('P2A_vermell',BASE+f'''
body{{background:{RED};font-family:'Space Grotesk',sans-serif;color:#111}}
.hd{{display:flex;align-items:center;justify-content:center;gap:30px;padding:10px 40px 6px;color:#fff}}
.hd img{{width:190px;height:190px}}
.hd .t{{font-family:Anton;font-size:66px;letter-spacing:3px;line-height:1}}
.hd .t small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:21px;letter-spacing:5px;color:#ffd0d0;margin-top:8px}}
.wrap{{padding:8px 40px}}{COMMON}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">PRÒXIMS PARTITS<small>COPA F11 VETERANS · JORNADA 1 · 26-27 SET</small></div></div><div class="wrap"><div class="grid">{''.join(card(r) for r in rows)}</div></div></body></html>''')

# 2B: agrupat per dia amb capçalera de dia
secs=''
for dia,rs in dies:
    secs+=f'<div class="dh">{dia}</div><div class="grid">{"".join(card(r) for r in rs)}</div>'
W('P2B_perdia',BASE+f'''
body{{background:{RED};font-family:'Space Grotesk',sans-serif;color:#111}}
.hd{{display:flex;align-items:center;gap:26px;padding:16px 40px 0;color:#fff}}
.hd img{{width:150px;height:150px}}
.hd .t{{font-family:Anton;font-size:62px;letter-spacing:3px;line-height:1}}
.hd .t small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:20px;letter-spacing:5px;color:#ffd0d0;margin-top:8px}}
.wrap{{padding:0 40px}}
.dh{{font-family:Anton;font-size:30px;letter-spacing:4px;color:#fff;margin:14px 0 8px;display:flex;align-items:center;gap:14px}}
.dh:after{{content:"";flex:1;height:3px;background:rgba(255,255,255,.4)}}
{COMMON}
.top .d{{display:none}}
.c{{padding:8px 18px 10px}}
.t{{height:96px;font-size:15px}}
.dh{{margin:10px 0 6px}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">PRÒXIMS PARTITS<small>COPA F11 VETERANS · JORNADA 1</small></div></div><div class="wrap">{secs}</div></body></html>''')

# 2C: targeta amb banda vermella (hora dins la banda)
def card_c(r):
    return f'<div class="c"><div class="band"><span class="h">{r["hora"]}</span><span class="d">{r["dia"][:3]} {r["dia"].split()[1]}</span><span class="g">{r["grup"]}</span></div><div class="body"><div class="vs"><div class="t"><img src="{r["hl"]}"><span>{r["h"]}</span></div><b>vs</b><div class="t"><img src="{r["al"]}"><span>{r["a"]}</span></div></div><div class="f">{r["camp"]}</div></div></div>'
W('P2C_banda',BASE+f'''
body{{background:#f2f2f2;font-family:'Space Grotesk',sans-serif;color:#111}}
.hd{{display:flex;align-items:flex-start;justify-content:space-between;padding:14px 40px 0;height:230px}}
.hd img{{width:170px;height:170px}}
.hd .t{{font-family:Anton;font-size:70px;letter-spacing:3px;line-height:.95;text-align:right;color:{RED}}}
.hd .t small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:20px;letter-spacing:5px;color:#111;margin-top:8px;white-space:nowrap}}
.wrap{{padding:16px 40px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.c{{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.08)}}
.band{{background:{RED};color:#fff;display:flex;align-items:center;gap:14px;padding:6px 16px}}
.band .h{{font-family:Anton;font-size:34px;letter-spacing:1px}}
.band .d{{font-weight:700;font-size:15px;letter-spacing:2px;opacity:.85;flex:1}}
.band .g{{background:#111;padding:3px 10px;border-radius:6px;font-size:14px;font-weight:700;letter-spacing:2px}}
.body{{padding:10px 16px 12px}}
.vs{{display:grid;grid-template-columns:1fr 34px 1fr;align-items:center}}
.t{{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;font-weight:700;font-size:16px;line-height:1.05;height:96px}}
.t img{{width:58px;height:58px;object-fit:contain}}
.vs b{{text-align:center;color:{RED};font-size:15px}}
.f{{margin-top:2px;text-align:center;font-size:14px;color:#888;font-weight:500;letter-spacing:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">PRÒXIMS<br>PARTITS<small>COPA F11 VETERANS · JORNADA 1 · 26-27 SET</small></div></div><div class="wrap"><div class="grid">{''.join(card_c(r) for r in rows)}</div></div></body></html>''')

# 2D: tres columnes compactes (per quan hi hagi copa + 3 lligues)
def card_d(r):
    return f'<div class="c"><div class="top"><span class="h">{r["hora"]}</span><span class="d">{r["dia"][:3]} {r["dia"].split()[1]}</span></div><div class="vs"><div class="t"><img src="{r["hl"]}"><span>{r["h"]}</span></div><div class="t"><img src="{r["al"]}"><span>{r["a"]}</span></div></div><div class="g">{r["grup"]}</div></div>'
W('P2D_tres',BASE+f'''
body{{background:{RED};font-family:'Space Grotesk',sans-serif;color:#111}}
.hd{{display:flex;align-items:center;justify-content:center;gap:30px;padding:10px 40px 4px;color:#fff}}
.hd img{{width:170px;height:170px}}
.hd .t{{font-family:Anton;font-size:64px;letter-spacing:3px;line-height:1}}
.hd .t small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:20px;letter-spacing:5px;color:#ffd0d0;margin-top:8px}}
.wrap{{padding:6px 34px}}
.grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px}}
.c{{background:#fff;border-radius:16px;padding:12px 12px 10px;box-shadow:0 8px 24px rgba(0,0,0,.14);text-align:center}}
.top{{display:flex;justify-content:space-between;align-items:baseline}}
.top .h{{font-family:Anton;font-size:34px}}
.top .d{{font-weight:700;font-size:13px;letter-spacing:2px;color:#888}}
.vs{{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px}}
.t{{display:flex;flex-direction:column;align-items:center;gap:5px;font-weight:700;font-size:13.5px;line-height:1.05;height:92px}}
.t img{{width:54px;height:54px;object-fit:contain}}
.g{{margin-top:4px;background:#111;color:#fff;display:inline-block;padding:3px 12px;border-radius:6px;font-size:13px;font-weight:700;letter-spacing:2px}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">PRÒXIMS PARTITS<small>COPA F11 VETERANS · JORNADA 1 · 26-27 SET</small></div></div><div class="wrap"><div class="grid">{''.join(card_d(r) for r in rows)}</div></div></body></html>''')
print('ok')
