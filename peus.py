#!/usr/bin/env python3
"""Peus de foto per als posts d'Instagram: text a punt per copiar, amb mencions als clubs (clubs.json) i hashtags.
clubs.json = {"CE Altafulla": "@cealtafulla", ...}  (clau = nom tal com surt a les imatges)"""
import os, json
import proxims as P
HASHTAGS='#veteranstarragona #lligaveterans #futbolveterans #futbolcatala #tarragona #minifutbol #veterans'
FONT='Dades: @minifutbol_tarragones'
def clubs():
    try: return {k:(v if v.startswith('@') else '@'+v) for k,v in json.load(open(os.path.join(P.V,'clubs.json'))).items() if v}
    except Exception: return {}
def mencions(noms):
    c=clubs(); vist=[]
    for n in noms:
        h=c.get(n)
        if h and h not in vist: vist.append(h)
    return ' '.join(vist[:20])          # Instagram admet 20 mencions per publicació
def _tanca(cos,noms,extra=''):
    m=mencions(noms); parts=[cos.strip()]
    if extra: parts.append(extra)
    parts.append(FONT)
    if m: parts.append(m)
    parts.append(HASHTAGS)
    return '\n\n'.join(parts)[:2200]    # límit d'Instagram
def _dates(rows):
    ds=sorted({r['dt'].date() for r in rows}); a,b=ds[0],ds[-1]
    return f'{a.day} {P.MES[a.month-1].lower()}' if a==b else (f'{a.day}-{b.day} {P.MES[b.month-1].lower()}' if a.month==b.month else f'{a.day} {P.MES[a.month-1].lower()} - {b.day} {P.MES[b.month-1].lower()}')
def _et(r): return f"{r['comp']}{' · '+r['grup'] if r['grup'] else ''}"
def proxims(rows):
    if not rows: return ''
    t=[f'📅 PRÒXIMS PARTITS · {_dates(rows)}','']
    for dia in sorted({r['dt'].date() for r in rows}):
        t.append(f'{P.DIES[dia.weekday()].capitalize()} {dia.day}')
        t+= [f"{r['hora']} · {r['h']} – {r['a']} ({_et(r)})" for r in rows if r['dt'].date()==dia]; t.append('')
    return _tanca('\n'.join(t),[x for r in rows for x in (r['h'],r['a'])],'Qui guanyarà el cap de setmana? 👇')
def resultats(rows):
    if not rows: return ''
    j=sorted({r['jornada'] for r in rows}); cap=j[0] if len(j)==1 else 'Cap de setmana'
    t=[f'📊 RESULTATS · {cap} · {_dates(rows)}','']
    for et in sorted({_et(r) for r in rows}):
        t.append(et)
        for r in [r for r in rows if _et(r)==et]:
            t.append(f"{r['h']} {r['hs']}-{r['as_']} {r['a']}" if r['status']==5 else f"{r['h']} – {r['a']} (no jugat)")
        t.append('')
    return _tanca('\n'.join(t),[x for r in rows for x in (r['h'],r['a'])],'Classificacions al següent post 👉')
def classificacio(nom,taules):
    """taules = [(grup, files)] de classificacio.dades()."""
    t=[f'🏆 CLASSIFICACIÓ · {nom}','']; noms=[]
    for g,rs in taules:
        if g and len(taules)>1: t.append(g)
        for i,r in enumerate(rs[:3] if len(taules)>1 else rs[:5],1): t.append(f"{i}. {r['n']} · {r['pts']} pts"); noms.append(r['n'])
        t.append('')
    return _tanca('\n'.join(t),noms,'Taula completa a la imatge 👆')
def golejadors(nom,rs,tipus):
    cap='⚽ GOLEJADORS' if tipus=='scorers' else '🧤 PORTERS MENYS GOLEJATS'; u='gols' if tipus=='scorers' else 'encaixats'
    t=[f'{cap} · {nom}','']+[f"{i}. {r['j']} ({r['eq']}) · {r['v']} {u}" for i,r in enumerate(rs[:5],1)]
    return _tanca('\n'.join(t),[r['eq'] for r in rs[:5]])
def partit(r,info=''):
    cos=f"⭐ EL PARTIT DE LA JORNADA\n\n{r['h']} – {r['a']}\n{P.DIES[r['dt'].weekday()].capitalize()} {r['dt'].day} {P.MES[r['dt'].month-1].lower()} · {r['hora']} · {r['camp']}\n{_et(r)}"
    return _tanca(cos+(('\n\n'+info) if info else ''),[r['h'],r['a']],'Qui guanya? Digues-ho als comentaris 👇')
