#!/usr/bin/env python3
"""Crònica d'un partit per a Telegram (HTML), amb les dades de l'acta de MyGol:
gols (minut, penal, en pròpia), assistències, targetes, penals fallats i MVP.
Ús de prova:  python cronica.py ID_PARTIT   (només imprimeix, no envia res)"""
import re, html
import proxims as P

# Tipus d'esdeveniment de MyGol
GOL, GOL_PROPIA, GOL_PENAL, ASSIST, PENAL_FALLAT, PENAL_ATURAT = 31, 32, 37, 30, 41, 42
GROGA, VERMELLA, MVP = 61, 62, 70
ICONA = {'LLIGA 1A': '🟡', 'LLIGA 2A': '🔵', 'LLIGA 3A': '🟢', 'COPA': '🏆'}
KEYCAP = {str(i): f'{i}️⃣' for i in range(10)}
esc = lambda s: html.escape(str(s or ''), quote=False)


def num_gran(n):
    """4 → 4️⃣ · 12 → 1️⃣2️⃣"""
    return ''.join(KEYCAP[c] for c in str(n))


def _nom_jugador(p):
    nom = P.nice(p.get('name') or '')
    cognom = P.nice(re.sub(r'\(.*?\)', '', p.get('surname') or '')).split(' ')
    return (nom + ' ' + (cognom[0] if cognom and cognom[0] else '')).strip()


def dades(id_partit):
    """Llegeix l'acta del partit. Torna llistes de gols, targetes, etc. ('L' local, 'V' visitant)."""
    d = P.get(f'/matches/{id_partit}')
    jug = {}
    for p in (d.get('homePlayers') or []) + (d.get('visitorPlayers') or []):
        md = p.get('matchData') or {}
        jug[md.get('idPlayer', p.get('id'))] = _nom_jugador(p)
    eq = lambda i: 'L' if i == d['idHomeTeam'] else 'V' if i == d['idVisitorTeam'] else '?'
    ev = [dict(t=e['type'], min=e.get('matchMinute') or 0, eq=eq(e.get('idTeam')), j=jug.get(e.get('idPlayer'), ''))
          for e in d.get('events') or []]
    gols = []
    for e in sorted([e for e in ev if e['t'] in (GOL, GOL_PROPIA, GOL_PENAL)], key=lambda e: e['min']):
        benef = ('V' if e['eq'] == 'L' else 'L') if e['t'] == GOL_PROPIA else e['eq']
        ass = next((a['j'] for a in ev if a['t'] == ASSIST and a['min'] == e['min'] and a['eq'] == e['eq']), '')
        gols.append(dict(min=e['min'], eq=benef, j=e['j'], tipus={GOL_PENAL: 'pen', GOL_PROPIA: 'pp'}.get(e['t'], ''), assist=ass))
    de = lambda t: [e for e in ev if e['t'] == t]
    mvp = next((e['j'] for e in ev if e['t'] == MVP), '')
    arbitre = ((d.get('referees') or [{}])[0].get('referee') or {}).get('name', '')
    return dict(gols=gols, grogues=de(GROGA), vermelles=de(VERMELLA), fallats=de(PENAL_FALLAT) + de(PENAL_ATURAT),
                mvp=mvp, arbitre=P.nice(arbitre) if arbitre else '')


def _curt(nom):
    """Àlex Gonzalez → Àlex G."""
    p = (nom or '').split()
    return p[0] + (' ' + p[1][0] + '.' if len(p) > 1 else '') if p else ''


def missatge(r, a=None):
    """r = fila de proxims.partits(); a = dades(r['id']). Torna el text HTML per a Telegram."""
    if a is None: a = dades(r['id'])
    sep = '━━━━━━━━━━━━━━━━━━'
    comp = 'COPA F11' + (f" · {r['grup']}" if r.get('grup') else '') if r['comp'] == 'COPA' else f"{r['comp'].split()[-1].replace('A', 'ª')} DIVISIÓ"
    t = [f"🚨🚨 <b>FINAL</b> 🚨🚨",
         f"{ICONA.get(r['comp'], '⚽')} <b>{esc(comp)}</b> · {esc(r['jornada'].upper())}",
         '',
         f"🏠 <b>{esc(r['h'].upper())}</b>",
         f"          {num_gran(r['hs'])} ➖ {num_gran(r['as_'])}",
         f"✈️ <b>{esc(r['a'].upper())}</b>",
         sep]
    if a['gols']:
        t.append('⚽ <b>GOLS</b>')
        for g in a['gols']:
            extra = ' <b>(penal 🎯)</b>' if g['tipus'] == 'pen' else ' <i>(en pròpia porta 🙈)</i>' if g['tipus'] == 'pp' else ''
            ass = f" <i>(ass. {esc(_curt(g['assist']))})</i>" if g['assist'] else ''
            t.append(f"{'🏠' if g['eq'] == 'L' else '✈️'} <code>{g['min']:>2}'</code> {esc(g['j'])}{extra}{ass}")
    elif r['hs'] + r['as_'] > 0:
        t.append('⚽ <i>Golejadors pendents a l\'acta</i>')
    t.append(sep)
    if a['mvp']: t.append(f"⭐️⭐️ <b>MVP · {esc(a['mvp'].upper())}</b> ⭐️⭐️")
    t.append(f"🟨 x{len(a['grogues'])}   🟥 x{len(a['vermelles'])}")
    for e in a['fallats']:
        t.append(f"❌ Penal fallat: {esc(e['j'])} ({e['min']}')")
    t += [sep, f"📍 {esc(r['camp'])} · {r['hora']} h"]
    if a['arbitre']: t.append(f"🧑‍⚖️ {esc(a['arbitre'])}")
    return '\n'.join(t)


if __name__ == '__main__':
    import sys, datetime
    idp = int(sys.argv[1])
    for r in P.partits(datetime.date(2020, 1, 1), datetime.date(2100, 1, 1), jugats=True):
        if r['id'] == idp:
            print(missatge(r)); break
