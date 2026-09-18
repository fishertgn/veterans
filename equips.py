#!/usr/bin/env python3
"""Coneix els equips: una fitxa per club (post 1080x1350 + història 1080x1920) amb grup, camp, primer partit,
rivals i què va fer la temporada passada. Ús: equips.py [--nomes "CE Altafulla"] [--send]"""
import os, sys, re, json, time, datetime
import proxims as P, classificacio as K, golejadors as G, partit as PJ, peus as PE
V,RED=P.V,P.RED; UP='https://minifutboltarragones.mygol.es/upload/'
COPA=108
def recull():
    t=P.get(f'/tournaments/{COPA}'); teams={x['id']:x for x in t['teams']}; groups={g['id']:g['name'] for g in t['groups']}
    grup={}; 
    for tg in t.get('teamGroups') or []:
        if groups.get(tg['idGroup'],'').upper().startswith('GRUP'): grup[tg['idTeam']]=groups[tg['idGroup']]
    avui=P.avui_madrid(); cal=P.partits(avui,avui+datetime.timedelta(days=120),jugats=None,ids=[COPA])
    prev=PJ.anterior(); pichi={}
    for div,tid in PJ.PREV.items():
        try:
            for r in G.dades(tid,'scorers')[2]:
                if r['eq'] not in pichi: pichi[r['eq']]=r
        except Exception: pass
    out=[]
    for tid,g in sorted(grup.items(),key=lambda kv:(kv[1],teams[kv[0]]['name'])):
        n=P.nice(teams[tid]['name']); meus=sorted([r for r in cal if n in (r['h'],r['a'])],key=lambda r:r['dt'])
        casa=[r for r in meus if r['h']==n and r['camp']]
        out.append(dict(n=n,lg=UP+teams[tid]['logoImgUrl'],grup=g,camp=(casa[0]['camp'] if casa else ''),primer=(meus[0] if meus else None),
                        rivals=[(P.nice(teams[i]['name']),UP+teams[i]['logoImgUrl']) for i,gg in grup.items() if gg==g and i!=tid],prev=prev.get(n),pichi=pichi.get(n)))
    return out
def contingut(e,k):
    px=lambda v:int(v*k); p=e['prev']; r=e['primer']
    if p:
        x=p[3]; ant=f'<div class="c"><small>Temporada 25-26</small><div class="fila"><div class="gran">{PJ.ordinal(p[1])}<span>a {p[0]} Divisió</span></div><div class="st"><b>{x["pts"]}</b>punts</div><div class="st"><b>{x["g"]}-{x["e"]}-{x["p"]}</b>G-E-P</div><div class="st"><b>{x["gf"]}:{x["gc"]}</b>gols</div></div></div>'
    else: ant='<div class="c"><small>Temporada 25-26</small><div class="nou">Cara nova a la lliga de veterans</div></div>'
    gol=f'<div class="c"><small>Màxim golejador 25-26</small><div class="fila2"><b>{e["pichi"]["j"]}</b><span>{e["pichi"]["v"]} gols en {e["pichi"]["pj"]} partits</span></div></div>' if e['pichi'] else ''
    if r:
        rival,rl=(r['a'],r['al']) if r['h']==e['n'] else (r['h'],r['hl']); on='a casa' if r['h']==e['n'] else 'a fora'
        deb=f'<div class="c"><small>Primer partit · Copa F11</small><div class="fila2"><img src="{rl}"><b>vs {rival}</b><span>{P.DIES[r["dt"].weekday()].capitalize()} {r["dt"].day} {P.MES[r["dt"].month-1].lower()} · {r["hora"]} · {on}</span></div></div>'
    else: deb=''
    riv='<div class="c"><small>Rivals al '+e['grup'].title()+'</small><div class="rv">'+''.join(f'<div><img src="{l}"><span>{n}</span></div>' for n,l in e['rivals'])+'</div></div>'
    cos=f'<div class="top"><img src="{e["lg"]}"><div><b>{e["n"]}</b><span class="pill">Copa F11 · {e["grup"].title()}</span>{("<em>"+e["camp"]+"</em>") if e["camp"] else ""}</div></div>{ant}{gol}{deb}{riv}'
    css=f""".top{{flex:none;background:#151515;color:#fff;border-radius:{px(18)}px;padding:{px(26)}px {px(30)}px;display:grid;grid-template-columns:{px(230)}px 1fr;gap:{px(26)}px;align-items:center}}
.top img{{width:{px(230)}px;height:{px(230)}px;object-fit:contain;background:#fff;border-radius:{px(18)}px;padding:{px(14)}px}}
.top b{{display:block;font-family:'Barlow Condensed';font-weight:700;font-size:{px(62)}px;line-height:.98;text-transform:uppercase}}
.pill{{display:inline-block;margin-top:{px(14)}px;font-weight:700;font-size:{px(17)}px;letter-spacing:{px(2)}px;text-transform:uppercase;color:#151515;background:#ffd400;border-radius:999px;padding:{px(6)}px {px(16)}px}}
.top em{{display:block;font-style:normal;margin-top:{px(12)}px;font-weight:500;font-size:{px(19)}px;color:#bdbdbd}}
.c{{flex:none;background:#fff;border-radius:{px(14)}px;border-left:{px(10)}px solid {RED};box-shadow:0 2px 8px rgba(0,0,0,.05);padding:{px(14)}px {px(24)}px {px(16)}px}}
.c small{{display:block;font-family:'Barlow Condensed';font-weight:700;font-size:{px(19)}px;letter-spacing:{px(3)}px;text-transform:uppercase;color:{RED};margin-bottom:{px(8)}px}}
.fila{{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;align-items:end}}
.gran{{font-family:'Barlow Condensed';font-weight:700;font-size:{px(68)}px;line-height:.9}}.gran span{{font-family:Barlow;font-weight:600;font-size:{px(19)}px;color:#555;margin-left:{px(10)}px}}
.st{{text-align:center;font-weight:700;font-size:{px(12)}px;letter-spacing:{px(1.5)}px;color:#9a9a9a;text-transform:uppercase}}.st b{{display:block;font-family:'Barlow Condensed';font-size:{px(38)}px;color:#151515;letter-spacing:0}}
.nou{{font-family:'Barlow Condensed';font-weight:700;font-size:{px(40)}px;text-transform:uppercase}}
.fila2{{display:flex;align-items:center;gap:{px(14)}px;flex-wrap:wrap}}.fila2 img{{width:{px(50)}px;height:{px(50)}px;object-fit:contain}}.fila2 b{{font-family:'Barlow Condensed';font-weight:700;font-size:{px(38)}px;text-transform:uppercase;line-height:1}}.fila2 span{{font-weight:500;font-size:{px(19)}px;color:#666}}
.rv{{display:flex;gap:{px(10)}px}}.rv div{{flex:1;text-align:center;font-weight:600;font-size:{px(13)}px;line-height:1.05;min-width:0}}.rv img{{width:{px(64)}px;height:{px(64)}px;object-fit:contain;margin:0 auto {px(6)}px}}"""
    return css,cos
def fitxer(outdir,e,fmt): return os.path.join(outdir,re.sub(r'[\\/:*?"<>|;,.]','',f'EQUIP {e["grup"].upper()} {e["n"].upper()}')+f' {fmt}.png')
def genera(e,outdir):
    out=[]
    css,cos=contingut(e,1.2); png=fitxer(outdir,e,'POST'); tmp=png[:-4]+'.html'; open(tmp,'w').write(P.post_shell('Coneix els equips','Copa F11 Veterans 26-27',cos,css+'.cos{gap:14px}')); P.captura(tmp,png,1080,1350); out.append(png)
    css,cos=contingut(e,1.42); png=fitxer(outdir,e,'HISTORIA'); P.render_story(P.story_shell('Coneix els equips','Copa F11 Veterans 26-27',cos,css+'.sheet{gap:14px}'),png); out.append(png)
    return out
def peu(e):
    p=e['prev']; r=e['primer']
    t=[f"👥 CONEIX ELS EQUIPS · {e['n']}",'',f"📍 {e['grup'].title()} de la Copa F11 Veterans 26-27"]
    if e['camp']: t.append(f"🏟 Juga a: {e['camp']}")
    if p: t.append(f"📊 Temporada passada: {PJ.ordinal(p[1])} a {p[0]} Divisió amb {p[3]['pts']} punts")
    else: t.append('🆕 Cara nova a la lliga de veterans')
    if e['pichi']: t.append(f"⚽ Màxim golejador 25-26: {e['pichi']['j']} ({e['pichi']['v']} gols)")
    if r: t.append(f"🗓 Debuta el {P.DIES[r['dt'].weekday()].lower()} {r['dt'].day} {P.MES[r['dt'].month-1].lower()} a les {r['hora']} contra {r['a'] if r['h']==e['n'] else r['h']}")
    return PE._tanca('\n'.join(t),[e['n']]+[n for n,_ in e['rivals']],'Fins on arribaran aquest any? 👇')
if __name__=='__main__':
    out=os.path.join(V,'out','equips'); os.makedirs(out,exist_ok=True); eqs=recull()
    if '--nomes' in sys.argv: eqs=[e for e in eqs if e['n']==sys.argv[sys.argv.index('--nomes')+1]]
    print(len(eqs),'equips')
    for e in eqs:
        fs=genera(e,out); print(e['grup'],e['n'],'| camp:',e['camp'] or '-','| prev:',bool(e['prev']),'| pichi:',bool(e['pichi']))
        if '--send' in sys.argv:
            import publicar as U
            U.envia_fitxer(fs[0],f"POST · {e['n']} ({e['grup'].title()})",'equips'); time.sleep(3.2); U.envia_fitxer(fs[1],f"HISTÒRIA · {e['n']}",'equips'); time.sleep(3.2); U.envia_text(peu(e),'equips'); time.sleep(3.2)
