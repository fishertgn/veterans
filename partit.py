#!/usr/bin/env python3
"""El partit de la jornada: tria el duel més atractiu del cap de setmana i en fa post (1080x1350) i història (1080x1920).
Criteri: suma de punts per partit dels dos equips, penalitzant la desigualtat. Si encara no s'ha jugat res,
es fa servir la classificació final de la temporada anterior (PREV). Es pot forçar amb partit_jornada.json = {"id": 8056}."""
import os, json, datetime
import proxims as P, classificacio as K
V,RED,COLORS=P.V,P.RED,P.COLORS
PREV={'1a':102,'2a':103,'3a':98}          # lligues 25-26; actualitzar cada temporada
PREV_EXTRA=[97]                            # copa 25-26, només per als enfrontaments directes
_cache={}
def _dades(tid):
    if tid not in _cache: _cache[tid]=K.dades(tid)
    return _cache[tid]
def anterior():
    """nom d'equip -> (divisió, posició, punts) de la temporada passada."""
    if 'prev' in _cache: return _cache['prev']
    out={}
    for div,tid in PREV.items():
        try:
            for g,rs in _dades(tid)[2]:
                for i,r in enumerate(rs,1): out[r['n']]=(div,i,r['pts'],r)
        except Exception: pass
    _cache['prev']=out; return out
def actual(r):
    """(posició, fila) de cada equip al seu grup de la competició actual."""
    res={}
    for g,rs in _dades(r['tid'])[2]:
        for i,x in enumerate(rs,1):
            if x['n'] in (r['h'],r['a']): res[x['n']]=(i,x,g)
    return res
def directe(h,a):
    """Últim enfrontament entre tots dos la temporada passada."""
    if ('h2h',h,a) in _cache: return _cache[('h2h',h,a)]
    millor=None
    for tid in list(PREV.values())+PREV_EXTRA:
        try:
            t=P.get(f'/tournaments/{tid}'); noms={x['id']:P.nice(x['name']) for x in t['teams']}
            for j in P.get(f'/matches/fortournament/{tid}'):
                for x in j['matches']:
                    if x['status']!=5: continue
                    l,v=noms.get(x['idHomeTeam']),noms.get(x['idVisitorTeam'])
                    if {l,v}=={h,a}:
                        d=datetime.datetime.fromisoformat(x['startTime'])
                        if not millor or d>millor[0]: millor=(d,l,x['homeScore'],x['visitorScore'],v,P.curt(t['name']))
        except Exception: pass
    _cache[('h2h',h,a)]=millor; return millor
def tria(rows):
    try:
        f=json.load(open(os.path.join(V,'partit_jornada.json')))
        for r in rows:
            if r['id']==f.get('id'): return r
    except Exception: pass
    prev=anterior(); pes={'1a':60,'2a':40,'3a':20}; millor=None
    for r in rows:
        act=actual(r); vals=[]
        for n in (r['h'],r['a']):
            x=act.get(n)
            if x and x[1]['pj']>0: vals.append(30*x[1]['pts']/x[1]['pj'])
            elif n in prev: vals.append(pes[prev[n][0]]-prev[n][1])
            else: vals.append(0)
        s=sum(vals)-0.5*abs(vals[0]-vals[1])
        if not millor or s>millor[0]: millor=(s,r)
    return millor[1] if millor else None

def ordinal(n): return f"{n}{ {1:'r',2:'n',3:'r',4:'t'}.get(n,'è') }"
def _forma(s,px):
    m={'1':'#1a9c5b','X':'#b5b5b5','2':'#d60000'}
    return '<span class="fm">'+(''.join(f'<i style="background:{m.get(c,"#ddd")};width:{px}px;height:{px}px"></i>' for c in s) or '<em>—</em>')+'</span>'
def contingut(r,k):
    """k = escala (1 post, 1.28 història)."""
    act=actual(r); prev=anterior(); col=COLORS.get(r['comp'],'#d60000'); h2h=directe(r['h'],r['a'])
    def fitxa(n):
        x=act.get(n); p=prev.get(n)
        return dict(jugat=bool(x and x[1]['pj']>0),pos=(f"{ordinal(x[0])} · {x[1]['pts']} pts" if x else '—'),forma=(x[1]['forma'] if x else ''),
                    ant=(f"{ordinal(p[1])} a {p[0]} Divisió" if p else 'Sense dades'),bal=(f"{p[3]['g']}G · {p[3]['e']}E · {p[3]['p']}P" if p else '—'),gols=(f"{p[3]['gf']} a favor · {p[3]['gc']} en contra" if p else '—'))
    H,A=fitxa(r['h']),fitxa(r['a'])
    dia=f"{P.DIES[r['dt'].weekday()]} {r['dt'].day} {P.MES[r['dt'].month-1]}"
    if h2h: d,l,gl,gv,v,c=h2h; duel=f'<div class="h2h"><small>Últim enfrontament · {d.strftime("%d/%m/%Y")} · {c}</small><b>{l} {gl}-{gv} {v}</b></div>'
    else: duel='<div class="h2h"><small>Temporada 25-26</small><b>No es van enfrontar</b></div>'
    px=lambda v:int(v*k)
    F=lambda e,t,d: f'<div class="f"><span>{e}</span><small>{t}</small><span>{d}</span></div>'
    files=''
    if H['jugat'] or A['jugat']: files+=F(H['pos'],'Ara mateix',A['pos'])+f'<div class="f">{_forma(H["forma"],px(15))}<small>Últims 5</small>{_forma(A["forma"],px(15))}</div>'
    files+=F(H['ant'],'Temporada 25-26',A['ant'])+F(H['bal'],'Balanç 25-26',A['bal'])+F(H['gols'],'Gols 25-26',A['gols'])
    css=f""".pj{{background:#fff;border-radius:{px(16)}px;border-left:{px(12)}px solid {col};box-shadow:0 2px 8px rgba(0,0,0,.05);padding:{px(26)}px {px(24)}px;flex:none}}
.cara{{display:grid;grid-template-columns:1fr {px(150)}px 1fr;align-items:center}}
.eq{{display:flex;flex-direction:column;align-items:center;gap:{px(12)}px;text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:{px(34)}px;line-height:1;text-transform:uppercase}}.eq img{{width:{px(190)}px;height:{px(190)}px;object-fit:contain}}
.mig{{text-align:center}}.mig b{{display:block;font-family:'Barlow Condensed';font-weight:700;font-size:{px(64)}px;line-height:1}}.mig small{{display:block;font-weight:700;font-size:{px(14)}px;letter-spacing:{px(3)}px;color:{col};margin-bottom:{px(6)}px}}
.on{{margin-top:{px(18)}px;text-align:center;font-weight:600;font-size:{px(20)}px;color:#666}}.on span{{display:inline-block;margin-left:{px(10)}px;font-weight:700;font-size:{px(13)}px;letter-spacing:{px(1.5)}px;color:{col};border:2px solid {col};border-radius:999px;padding:{px(3)}px {px(10)}px;text-transform:uppercase;vertical-align:middle}}
.tb{{background:#fff;border-radius:{px(16)}px;box-shadow:0 2px 8px rgba(0,0,0,.05);overflow:hidden;flex:none}}
.f{{display:grid;grid-template-columns:1fr {px(210)}px 1fr;align-items:center;height:{px(64)}px;border-bottom:1px solid #f0f0f0;font-weight:600;font-size:{px(21)}px}}.f:last-child{{border-bottom:0}}
.f span{{text-align:center;font-size:{px(19)}px}}.f small{{text-align:center;font-weight:700;font-size:{px(12.5)}px;letter-spacing:{px(2)}px;color:#9a9a9a;text-transform:uppercase}}
.fm{{display:flex;gap:{px(5)}px;justify-content:center}}.fm i{{border-radius:50%;display:block}}.fm em{{font-style:normal;color:#bbb}}
.h2h{{background:#151515;color:#fff;border-radius:{px(16)}px;padding:{px(16)}px {px(24)}px;text-align:center;flex:none}}.h2h small{{display:block;font-weight:700;font-size:{px(12.5)}px;letter-spacing:{px(2)}px;color:#ffd400;text-transform:uppercase;margin-bottom:{px(6)}px}}.h2h b{{font-family:'Barlow Condensed';font-weight:700;font-size:{px(34)}px;text-transform:uppercase}}"""
    cos=f"""<div class="pj"><div class="cara"><div class="eq"><img src="{r['hl']}">{r['h']}</div><div class="mig"><small>{dia}</small><b>{r['hora']}</b></div><div class="eq"><img src="{r['al']}">{r['a']}</div></div>
<div class="on">{r['camp']}<span>{r['comp']}{' · '+r['grup'] if r['grup'] else ''}</span></div></div>
<div class="tb">{files}</div>{duel}"""
    info=(f"Últim enfrontament: {h2h[1]} {h2h[2]}-{h2h[3]} {h2h[4]} ({h2h[0].strftime('%d/%m/%Y')})" if h2h else '')
    return css,cos,info
def generar(d0,d1,outdir):
    rows=P.partits(d0,d1,jugats=False); r=tria(rows)
    if not r: return [],None,''
    sub=f"{P.DIES[r['dt'].weekday()]} {r['dt'].day} {P.MES[r['dt'].month-1]}"; out=[]
    css,cos,info=contingut(r,1.18); png=P.nom_fitxer(outdir,'PARTIT DE LA JORNADA',[r['comp']],r['dt'].date(),None,'POST')
    tmp=png[:-4]+'.html'; open(tmp,'w').write(P.post_shell('El partit de la jornada',sub,cos+'<div class="cta">Qui guanya?<small>Digues-ho als comentaris 👇</small></div>',css+'.cos{gap:16px}.cta{flex:none;background:#ffd400;border-radius:18px;padding:26px;text-align:center;font-family:\'Barlow Condensed\';font-weight:700;font-size:64px;line-height:1;text-transform:uppercase}.cta small{display:block;font-family:Barlow;font-weight:600;font-size:24px;text-transform:none;margin-top:8px}')); P.captura(tmp,png,1080,1350); out.append(('POST · El partit de la jornada',png))
    css,cos,info=contingut(r,1.15); png=P.nom_fitxer(outdir,'PARTIT DE LA JORNADA',[r['comp']],r['dt'].date(),None,'HISTORIA')
    html=P.story_shell('El partit de la jornada',sub,cos,css+'.sheet{gap:16px}.tt{font-size:66px!important}')
    html=html.replace('</body>','<div style="position:absolute;left:60px;top:1500px;width:470px;height:300px;display:flex;flex-direction:column;justify-content:center"><div style="color:#fff;font-family:\'Barlow Condensed\';font-weight:700;font-size:84px;line-height:.95;letter-spacing:2px;text-transform:uppercase">Qui<br>guanya?</div><div style="margin-top:14px;color:#ffd6d6;font-weight:600;font-size:30px;letter-spacing:1px">Vota a l\'enquesta 👉</div></div></body>')
    P.render_story(html,png); out.append(('HISTÒRIA · El partit de la jornada (posa-hi l\'enquesta a sota)',png))
    return out,r,info
if __name__=='__main__':
    import sys
    d0=datetime.date.fromisoformat(sys.argv[1]); d1=datetime.date.fromisoformat(sys.argv[2])
    res,r,info=generar(d0,d1,os.path.join(V,'out'))
    print(r['h'],'-',r['a'] if r else None,'|',info)
    for e,p in res: print(e,'->',p)
