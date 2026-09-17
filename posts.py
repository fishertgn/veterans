import json, datetime
UP='https://minifutboltarragones.mygol.es/upload/'
RED='#d60000'; LOGO='file:///Users/luismartinez/veterans/logo_crop.png'
FONTS='<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@500;700&family=Montserrat:wght@700;900&display=swap" rel="stylesheet">'
t=json.load(open('tournaments_108.json')); teams={x['id']:x for x in t['teams']}; groups={g['id']:g['name'] for g in t['groups']}
m=json.load(open('m108.json'))
DIES=['DILLUNS','DIMARTS','DIMECRES','DIJOUS','DIVENDRES','DISSABTE','DIUMENGE']; MES=['GEN','FEB','MAR','ABR','MAI','JUN','JUL','AGO','SET','OCT','NOV','DES']
def nice(n):
    n=' '.join(n.split()).title().replace('Cf ','CF ').replace('Ce ','CE ').replace('Ue ','UE ').replace('Cd ','CD ').replace('Fc','FC').replace('Cfb','CFB').replace('Ucf','UCF').replace('Cfv','CFV').replace('Aev','AEV').replace('Cef','CEF').replace('Vet.','Vet. ').replace('P.Barça','P. Barça')
    return ' '.join(n.split())
rows=[]
for x in m[0]['matches']:
    if x['status']!=1: continue
    d=datetime.datetime.fromisoformat(x['startTime'])
    rows.append(dict(dt=d,dia=DIES[d.weekday()]+f' {d.day} '+MES[d.month-1],hora=d.strftime('%H:%M'),
        h=nice(teams[x['idHomeTeam']]['name']),hl=UP+teams[x['idHomeTeam']]['logoImgUrl'],
        a=nice(teams[x['idVisitorTeam']]['name']),al=UP+teams[x['idVisitorTeam']]['logoImgUrl'],
        camp=x['field']['name'],grup=groups[x['idGroup']],comp='COPA F11'))
rows.sort(key=lambda r:r['dt'])
dies=[]
for r in rows:
    if not dies or dies[-1][0]!=r['dia']: dies.append((r['dia'],[]))
    dies[-1][1].append(r)
BASE=f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1350px;overflow:hidden;position:relative}}img{{display:block}}'
def W(name,html): open(f'opcions/{name}.html','w').write(html)

# 1 LLISTA TIQUET
body=''
for dia,rs in dies:
    body+=f'<div class="dia">{dia}</div>'
    for r in rs:
        body+=f'<div class="r"><div class="h">{r["hora"]}</div><div class="t l"><span>{r["h"]}</span><img src="{r["hl"]}"></div><div class="vs">vs</div><div class="t"><img src="{r["al"]}"><span>{r["a"]}</span></div><div class="g">{r["grup"]}</div></div>'
W('P1_llista',BASE+f'''
body{{background:{RED};font-family:'Space Grotesk',sans-serif;color:#111}}
.logo{{position:absolute;left:50%;top:8px;transform:translateX(-50%);width:210px;height:210px}}
.tk{{position:absolute;left:50px;top:236px;width:980px;height:1074px;background:#fff;border-radius:30px;box-shadow:0 30px 80px rgba(0,0,0,.3);padding:34px 40px 0}}
.hd{{font-family:Anton;font-size:56px;letter-spacing:3px;text-align:center;line-height:1}}
.hd small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:22px;letter-spacing:5px;color:{RED};margin-top:8px}}
.dia{{margin:22px 0 6px;font-family:Anton;font-size:26px;letter-spacing:4px;color:#fff;background:#111;display:inline-block;padding:4px 16px}}
.r{{display:grid;grid-template-columns:86px 1fr 46px 1fr 92px;align-items:center;gap:8px;height:64px;border-bottom:2px solid #eee}}
.h{{font-family:Anton;font-size:32px;color:{RED}}}
.t{{display:flex;align-items:center;gap:10px;font-weight:700;font-size:21px;line-height:1.05}}
.t.l{{justify-content:flex-end;text-align:right}}
.t img{{width:46px;height:46px;object-fit:contain;flex:none}}
.vs{{text-align:center;font-weight:700;color:#999;font-size:18px}}
.g{{text-align:center;font-weight:700;font-size:16px;letter-spacing:1px;background:#ffe7e7;color:{RED};border-radius:8px;padding:6px 0}}
</style></head><body><img class="logo" src="{LOGO}"><div class="tk"><div class="hd">PRÒXIMS PARTITS<small>CAP DE SETMANA 26-27 SET · JORNADA 1</small></div>{body}</div></body></html>''')

# 2 GRAELLA DE TARGETES
cards=''.join(f'<div class="c"><div class="top"><span class="d">{r["dia"][:3]} {r["dia"].split()[1]}</span><span class="h">{r["hora"]}</span><span class="g">{r["grup"]}</span></div><div class="vs"><div class="t"><img src="{r["hl"]}"><span>{r["h"]}</span></div><b>-</b><div class="t"><img src="{r["al"]}"><span>{r["a"]}</span></div></div><div class="f">{r["camp"]}</div></div>' for r in rows)
W('P2_graella',BASE+f'''
body{{background:#f4f4f4;font-family:'Space Grotesk',sans-serif;color:#111}}
.hd{{background:{RED};height:190px;display:flex;align-items:center;gap:30px;padding:0 50px;color:#fff}}
.hd img{{width:170px;height:170px}}
.hd .t{{font-family:Anton;font-size:64px;letter-spacing:3px;line-height:1}}
.hd .t small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:22px;letter-spacing:5px;color:#ffd0d0;margin-top:8px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:24px 40px}}
.c{{background:#fff;border-radius:18px;padding:14px 18px;box-shadow:0 6px 18px rgba(0,0,0,.08);border-left:8px solid {RED}}}
.top{{display:flex;justify-content:space-between;align-items:center;font-weight:700;font-size:16px;letter-spacing:2px;color:#888}}
.top .h{{font-family:Anton;font-size:34px;color:#111;letter-spacing:1px}}
.top .g{{background:#111;color:#fff;padding:3px 10px;border-radius:6px;font-size:14px}}
.vs{{display:grid;grid-template-columns:1fr 24px 1fr;align-items:center;margin-top:8px}}
.t{{display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center;font-weight:700;font-size:16px;line-height:1.05;height:96px}}
.t img{{width:56px;height:56px;object-fit:contain}}
.vs b{{text-align:center;color:{RED};font-size:22px}}
.f{{margin-top:6px;text-align:center;font-size:14px;color:#888;font-weight:500;letter-spacing:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">PRÒXIMS PARTITS<small>26-27 SET · COPA F11 · JORNADA 1</small></div></div><div class="grid">{cards}</div></body></html>''')

# 3 DOS COLUMNES PER DIA (agenda)
cols=''
for dia,rs in dies:
    items=''.join(f'<div class="it"><div class="h">{r["hora"]}</div><div class="m"><div class="l"><img src="{r["hl"]}"><span>{r["h"]}</span></div><div class="l"><img src="{r["al"]}"><span>{r["a"]}</span></div></div><div class="g">{r["grup"]}<small>{r["camp"]}</small></div></div>' for r in rs)
    cols+=f'<div class="col"><div class="dh">{dia}</div>{items}</div>'
W('P3_agenda',BASE+f'''
body{{background:#fff;font-family:'Space Grotesk',sans-serif;color:#111}}
.hd{{display:flex;align-items:center;justify-content:space-between;padding:26px 50px 10px}}
.hd img{{width:180px;height:180px}}
.hd .t{{font-family:Anton;font-size:74px;letter-spacing:3px;line-height:.95;text-align:right;color:{RED}}}
.hd .t small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:22px;letter-spacing:5px;color:#111;margin-top:10px}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:26px;padding:0 50px}}
.dh{{font-family:Anton;font-size:34px;letter-spacing:4px;background:{RED};color:#fff;padding:8px 18px;margin-bottom:8px}}
.it{{display:grid;grid-template-columns:70px 1fr 120px;gap:8px;align-items:center;padding:8px 0;border-bottom:2px solid #eee}}
.h{{font-family:Anton;font-size:30px}}
.l{{display:flex;align-items:center;gap:8px;font-weight:700;font-size:16px;line-height:1.05;height:34px}}
.l img{{width:30px;height:30px;object-fit:contain}}
.g{{text-align:right;font-weight:700;font-size:15px;letter-spacing:1px;color:{RED}}}
.g small{{display:block;color:#999;font-size:11px;letter-spacing:0;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.st{{position:absolute;left:0;bottom:0;width:1080px;height:40px;background:linear-gradient(90deg,{RED} 60%,#ffd400 60% 80%,#111 80%)}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">PRÒXIMS<br>PARTITS<small>COPA F11 VETERANS · JORNADA 1</small></div></div><div class="cols">{cols}</div><div class="st"></div></body></html>''')

# 4 NEGRE
body=''
for dia,rs in dies:
    body+=f'<div class="dia"><span>{dia}</span></div>'
    for r in rs:
        body+=f'<div class="r"><div class="h">{r["hora"]}</div><div class="t l"><span>{r["h"]}</span><img src="{r["hl"]}"></div><div class="g">{r["grup"].replace("GRUP ","")}</div><div class="t"><img src="{r["al"]}"><span>{r["a"]}</span></div><div class="c">{r["camp"].replace("F11 Camp ","").replace("F11 ","")}</div></div>'
W('P4_negre',BASE+f'''
body{{background:#0d0d0d;font-family:'Space Grotesk',sans-serif;color:#fff}}
.hd{{display:flex;align-items:center;gap:26px;padding:24px 50px 6px}}
.hd img{{width:150px;height:150px;border-radius:50%}}
.hd .t{{font-family:Anton;font-size:60px;letter-spacing:3px;line-height:1}}
.hd .t small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:20px;letter-spacing:4px;color:#ffd400;margin-top:8px;white-space:nowrap}}
.list{{padding:0 50px}}
.dia{{margin:16px 0 4px;font-family:Anton;font-size:24px;letter-spacing:4px;color:{RED}}}
.r{{display:grid;grid-template-columns:80px 1fr 60px 1fr 150px;align-items:center;gap:8px;height:66px;border-bottom:1px solid #2a2a2a}}
.h{{font-family:Anton;font-size:32px;color:#ffd400}}
.t{{display:flex;align-items:center;gap:10px;font-weight:700;font-size:19px;line-height:1.05}}
.t.l{{justify-content:flex-end;text-align:right}}
.t img{{width:44px;height:44px;object-fit:contain;flex:none;background:#fff;border-radius:50%;padding:3px}}
.g{{text-align:center;font-family:Anton;font-size:26px;background:{RED};color:#fff;border-radius:8px;padding:2px 0}}
.c{{text-align:right;font-size:13px;color:#888;font-weight:500;line-height:1.1}}
</style></head><body><div class="hd"><img src="{LOGO}"><div class="t">PRÒXIMS PARTITS<small>COPA F11 VETERANS · JORNADA 1 · 26-27 SET</small></div></div><div class="list">{body}</div></body></html>''')

# 5 CARTELL TIPOGRÀFIC
body=''
for dia,rs in dies:
    body+=f'<div class="blk"><div class="dh">{dia.split()[0]}<b>{" ".join(dia.split()[1:])}</b></div>'
    for r in rs:
        body+=f'<div class="r"><b>{r["hora"]}</b><span>{r["h"]} <i>–</i> {r["a"]}</span><em>{r["grup"]}</em></div>'
    body+='</div>'
W('P5_cartell',BASE+f'''
body{{background:{RED};font-family:'Space Grotesk',sans-serif;color:#fff}}
.big{{position:absolute;left:50px;top:30px;font-family:Anton;font-size:150px;line-height:.86;letter-spacing:2px}}
.big small{{display:block;font-family:'Space Grotesk';font-weight:700;font-size:22px;letter-spacing:6px;margin-top:16px;color:#ffd0d0}}
.logo{{position:absolute;right:30px;top:20px;width:260px;height:260px}}
.wrap{{position:absolute;left:50px;right:50px;top:400px}}
.blk{{background:#fff;color:#111;border-radius:16px;padding:14px 26px 10px;margin-bottom:16px}}
.dh{{font-family:Anton;font-size:30px;letter-spacing:3px;color:{RED};margin-bottom:4px}}
.dh b{{color:#111;margin-left:12px}}
.r{{display:grid;grid-template-columns:90px 1fr 100px;align-items:center;gap:10px;height:44px;border-top:1px solid #eee;font-weight:700;font-size:20px}}
.r b{{font-family:Anton;font-size:28px;letter-spacing:1px}}
.r i{{font-style:normal;color:{RED};margin:0 6px}}
.r em{{font-style:normal;text-align:right;font-size:15px;letter-spacing:2px;color:#888}}
</style></head><body><div class="big">PRÒXIMS<br>PARTITS<small>COPA F11 VETERANS · JORNADA 1</small></div><img class="logo" src="{LOGO}"><div class="wrap">{body}</div></body></html>''')
print(len(rows),'partits')
