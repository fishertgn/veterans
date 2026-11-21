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


def _titular(r, a):
    """Titular segons com ha anat el partit."""
    hs, as_, loc, vis = r['hs'], r['as_'], r['h'], r['a']
    dif, total = hs - as_, hs + as_
    guanya = loc if dif > 0 else vis
    # remuntada: el guanyador va anar perdent en algun moment
    l = v = 0; perdia = False
    for g in a['gols']:
        if g['eq'] == 'L': l += 1
        else: v += 1
        if (dif > 0 and l < v) or (dif < 0 and v < l): perdia = True
    if dif == 0:
        return '🧱 EMPAT SENSE GOLS 🧱' if total == 0 else f'⚖️ EMPAT A {hs}! PUNTS REPARTITS ⚖️'
    if perdia:
        return f'🔄 REMUNTADA ÈPICA DEL {guanya.upper()}! 🔄'
    if total >= 7:
        return f'🎆 FESTIVAL DE GOLS! GUANYA EL {guanya.upper()} 🎆'
    if abs(dif) >= 4:
        return f'💥 GOLEJADA DEL {guanya.upper()}! 💥'
    if dif < 0:
        return f'✈️ ASSALT A DOMICILI DEL {guanya.upper()}! ✈️'
    if abs(dif) == 1:
        return f'😮‍💨 PER LA MÍNIMA! GUANYA EL {guanya.upper()}'
    return f'🔥 VICTÒRIA CONTUNDENT DEL {guanya.upper()} 🔥'


def missatge(r, a=None):
    """r = fila de proxims.partits(); a = dades(r['id']). Torna el text HTML per a Telegram."""
    if a is None: a = dades(r['id'])
    sep = '━━━━━━━━━━━━━━━━━━'
    comp = 'COPA F11' + (f" · {r['grup']}" if r.get('grup') else '') if r['comp'] == 'COPA' else f"{r['comp'].split()[-1].replace('A', 'ª')} DIVISIÓ"
    t = [f"🚨🚨 <b>FINAL</b> 🚨🚨",
         f"{ICONA.get(r['comp'], '⚽')} <b>{esc(comp)}</b> · {esc(r['jornada'].upper())}",
         '',
         f"<b>{esc(_titular(r, a))}</b>",
         '',
         f"🏠 <b>{esc(r['h'].upper())}</b>",
         f"          {num_gran(r['hs'])} ➖ {num_gran(r['as_'])}",
         f"✈️ <b>{esc(r['a'].upper())}</b>",
         sep]
    if a['gols']:
        t.append('⚽ <b>GOLS</b>')
        for g in a['gols']:
            extra = ' <b>(penal 🎯)</b>' if g['tipus'] == 'pen' else ' <i>(en pròpia porta 🙈)</i>' if g['tipus'] == 'pp' else ''
            ass = f"\n        🅰️ <i>{esc(g['assist'])}</i>" if g['assist'] else ''
            t.append(f"{'🏠' if g['eq'] == 'L' else '✈️'} <code>{g['min']:>2}'</code> {esc(g['j'])}{extra}{ass}")
    elif r['hs'] + r['as_'] > 0:
        t.append('⚽ <i>Golejadors pendents a l\'acta</i>')
    # Destacats
    dest = []
    comptes = {}
    for g in a['gols']:
        if g['tipus'] != 'pp': comptes[(g['j'], g['eq'])] = comptes.get((g['j'], g['eq']), 0) + 1
    for (j, eq), n in sorted(comptes.items(), key=lambda x: -x[1]):
        if n >= 4: dest.append(f"🤯 <b>PÒQUER DE {esc(j.upper())}!!!</b> ({n} gols)")
        elif n == 3: dest.append(f"🎩 <b>HAT-TRICK DE {esc(j.upper())}!!</b>")
        elif n == 2: dest.append(f"✌️ Doblet de <b>{esc(j)}</b>")
    if r['as_'] == 0 and r['hs'] > 0: dest.append(f"🧤 Porteria a zero del <b>{esc(r['h'])}</b>")
    if r['hs'] == 0 and r['as_'] > 0: dest.append(f"🧤 Porteria a zero del <b>{esc(r['a'])}</b>")
    tard = [g for g in a['gols'] if g['min'] >= 88]
    if tard and abs(r['hs'] - r['as_']) <= 1: dest.append(f"⏱️ Gol al límit de <b>{esc(tard[-1]['j'])}</b> ({tard[-1]['min']}')")
    for e in a['vermelles']:
        dest.append(f"🟥 Expulsat: <b>{esc(e['j'])}</b> ({e['min']}')")
    if dest:
        t += [sep] + dest
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
