#!/usr/bin/env python3
"""Avisos dels equips i jugadors preferits (favorits.json) al tema ⭐ Favorits de Telegram.
  - Prèvia: el dia del partit, a partir de les 8h (rival, hora, camp i Google Maps).
  - Directe: inici, cada gol amb el marcador, descans, final (MyGol registra l'acta en directe).
  - Targetes i MVP dels favorits.
  - Crònica al final (la mateixa del tema Directe).
S'executa des de .github/workflows/favorits.yml: cada mitja hora mira si hi ha un partit preferit
a punt de començar o en joc i, si n'hi ha, el segueix cada 75 segons fins que acaba.
Ús:  python favorits.py            → prèvies + seguiment en directe
     python favorits.py --prova    → mostra què faria ara, sense enviar res"""
import os, sys, json, time, datetime, unicodedata, html, urllib.parse
V = os.path.dirname(os.path.abspath(__file__)); os.chdir(V); sys.path.insert(0, V)
import proxims as P, cronica as C

PROVA = '--prova' in sys.argv
FITXER_ESTAT = os.path.join(V, 'estat_favorits.json')
esc = lambda s: html.escape(str(s or ''), quote=False)
GOL, GOL_PROPIA, GOL_PENAL, ASSIST, GROGA, VERMELLA, MVP = 31, 32, 37, 30, 61, 62, 70
INICI, FI_1A, INICI_2A, FI_2A, FINAL = 1, 10, 11, 12, 13


def norm(s):
    s = unicodedata.normalize('NFD', (s or '').lower())
    return ' '.join(''.join(c for c in s if unicodedata.category(c) != 'Mn').replace('.', ' ').split())


def config():
    try: c = json.load(open(os.path.join(V, 'favorits.json'), encoding='utf-8'))
    except Exception: c = {}
    return [norm(e) for e in c.get('equips', []) if e], [norm(j) for j in c.get('jugadors', []) if j]


def estat():
    try: return json.load(open(FITXER_ESTAT, encoding='utf-8'))
    except Exception: return {'previes': {}, 'vistos': {}, 'acabats': {}}


def desa(e):
    if not PROVA: json.dump(e, open(FITXER_ESTAT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


def ara():
    from zoneinfo import ZoneInfo
    if '--ara' in sys.argv:            # proves: simula una hora (p. ex. --ara 2026-11-21T17:30)
        return datetime.datetime.fromisoformat(sys.argv[sys.argv.index('--ara') + 1])
    return datetime.datetime.now(ZoneInfo('Europe/Madrid')).replace(tzinfo=None)


def envia(text):
    if PROVA:
        print('--- (no s\'envia) ---\n' + text + '\n'); return True
    import publicar as U
    tema = 'favorits' if (U.TEMES.get('temes') or {}).get('favorits') else 'directe'
    return U.tg('sendMessage', tema, text=text, parse_mode='HTML', disable_web_page_preview='true')


def es_equip_fav(nom, equips):
    n = norm(nom)
    return any(e and (e in n or n in e) for e in equips)


def es_jugador_fav(nom, jugadors):
    n = norm(nom)
    return any(j and (j in n or n in j) for j in jugadors)


def partits_avui(equips, jugadors):
    """Partits d'avui on juga un equip preferit, o qualsevol si hi ha jugadors preferits
    (el jugador es busca a l'alineació quan comença el partit)."""
    avui = ara().date()
    rows = P.partits(avui, avui, jugats=None)
    if jugadors: return rows
    return [r for r in rows if es_equip_fav(r['h'], equips) or es_equip_fav(r['a'], equips)]


def detall(id_partit):
    """Acta en brut + noms dels jugadors."""
    d = P.get(f'/matches/{id_partit}')
    noms = {}
    for p in (d.get('homePlayers') or []) + (d.get('visitorPlayers') or []):
        md = p.get('matchData') or {}
        noms[md.get('idPlayer', p.get('id'))] = C._nom_jugador(p)
    return d, noms


def te_jugador_fav(noms, jugadors):
    return [n for n in noms.values() if es_jugador_fav(n, jugadors)]


def previa(r, d, motiu):
    camp = d.get('field') or {}
    loc = camp.get('location') or ''
    mapa = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(loc or (camp.get('name', '') + ' ' + (camp.get('address') or '')))}"
    comp = 'COPA F11' + (f" · {r['grup']}" if r.get('grup') else '') if r['comp'] == 'COPA' else f"{r['comp'].split()[-1].replace('A', 'ª')} DIVISIÓ"
    return '\n'.join([
        f"⭐ <b>AVUI JUGA {esc(motiu.upper())}</b>",
        f"{C.ICONA.get(r['comp'], '⚽')} <b>{esc(comp)}</b> · {esc(r['jornada'].upper())}",
        '',
        f"🏠 <b>{esc(r['h'])}</b>",
        f"✈️ <b>{esc(r['a'])}</b>",
        '',
        f"🕒 <b>{r['hora']} h</b>",
        f"📍 {esc(camp.get('name', r['camp']))}" + (f"\n      <i>{esc(camp.get('address'))}</i>" if camp.get('address') else ''),
        f"🗺️ <a href=\"{mapa}\">Com arribar-hi</a>"])


def text_esdeveniment(r, d, ev, noms, marcador, jugadors, equips, evs=()):
    """Text d'un esdeveniment nou, o None si no s'ha d'avisar."""
    t, minut = ev['type'], ev.get('matchMinute') or 0
    eq = 'L' if ev.get('idTeam') == d['idHomeTeam'] else 'V'
    jug = noms.get(ev.get('idPlayer'), '')
    equip = r['h'] if eq == 'L' else r['a']
    fav_j = jug and es_jugador_fav(jug, jugadors)
    fav_e = es_equip_fav(equip, equips)
    m = f"{esc(r['h'])} <b>{marcador[0]}-{marcador[1]}</b> {esc(r['a'])}"
    if t == INICI: return f"▶️ <b>COMENÇA!</b>\n{esc(r['h'])} – {esc(r['a'])}"
    if t == FI_1A: return f"⏸️ <b>DESCANS</b>\n{m}"
    if t == INICI_2A: return f"▶️ <b>Comença la segona part</b>\n{m}"
    if t in (GOL, GOL_PENAL, GOL_PROPIA):
        tipus = ' (penal 🎯)' if t == GOL_PENAL else ' (en pròpia porta 🙈)' if t == GOL_PROPIA else ''
        cap = f"🔥⚽ <b>GOOOL DE {esc(jug.upper())}!!</b> ⭐" if fav_j and t != GOL_PROPIA else '⚽ <b>GOL!</b>'
        a = next((noms.get(x.get('idPlayer'), '') for x in evs
                  if x['type'] == ASSIST and x.get('matchMinute') == minut and x.get('idTeam') == ev.get('idTeam')), '')
        ass = ''
        if a: ass = f" <i>(ass. {esc(a)})</i> ⭐" if es_jugador_fav(a, jugadors) else f" <i>(ass. {esc(C._curt(a))})</i>"
        return f"{cap}\n<code>{minut}'</code> {esc(jug)}{tipus}{ass} · {esc(equip)}\n{m}"
    if t in (GROGA, VERMELLA) and (fav_j or fav_e):
        return f"{'🟨' if t == GROGA else '🟥'} <b>Targeta {'groga' if t == GROGA else 'vermella'}</b> · {esc(jug)} ({minut}')\n{esc(equip)}"
    if t == MVP and (fav_j or fav_e):
        return f"⭐⭐ <b>MVP DEL PARTIT: {esc(jug.upper())}</b> ⭐⭐\n{esc(equip)}"
    return None


def segueix(r, e, jugadors, equips):
    """Mira l'acta d'un partit i envia els esdeveniments nous. Torna True si el partit ha acabat."""
    k = str(r['id'])
    d, noms = detall(r['id'])
    if jugadors and not equips_fav_partit(r, equips) and not te_jugador_fav(noms, jugadors):
        if noms: e['acabats'][k] = 'no hi juga'; desa(e)   # alineació feta i el jugador no hi és
        return True
    vistos = set(e['vistos'].get(k, []))
    evs = sorted(d.get('events') or [], key=lambda x: (x.get('timeStamp') or '', x.get('id') or 0))
    l = v = 0
    for ev in evs:
        t = ev['type']
        if t in (GOL, GOL_PENAL, GOL_PROPIA):
            eq = 'L' if ev.get('idTeam') == d['idHomeTeam'] else 'V'
            if t == GOL_PROPIA: eq = 'V' if eq == 'L' else 'L'
            if eq == 'L': l += 1
            else: v += 1
        if ev['id'] in vistos: continue
        txt = text_esdeveniment(r, d, ev, noms, (l, v), jugadors, equips, evs)
        if txt and not envia(txt): return False          # si Telegram falla, es reintenta a la volta següent
        vistos.add(ev['id'])
    e['vistos'][k] = sorted(vistos)
    acabat = d.get('status') == 5 or any(x['type'] == FINAL for x in evs)
    if acabat and not e['acabats'].get(k):
        r2 = dict(r, hs=d.get('homeScore', l), as_=d.get('visitorScore', v))
        if envia(f"🏁 <b>FINAL</b>\n{esc(r['h'])} <b>{r2['hs']}-{r2['as_']}</b> {esc(r['a'])}"):
            try: envia(C.missatge(r2))
            except Exception as ex: print('crònica', ex)
            e['acabats'][k] = True
    desa(e)
    return acabat


def equips_fav_partit(r, equips):
    return es_equip_fav(r['h'], equips) or es_equip_fav(r['a'], equips)


def main():
    equips, jugadors = config()
    if not equips and not jugadors:
        print('favorits.json buit: res a fer.'); return
    e = estat()
    for clau in ('previes', 'vistos', 'acabats'): e.setdefault(clau, {})
    rows = partits_avui(equips, jugadors)
    n = ara()
    # 1) Prèvies (a partir de les 8h)
    if n.hour >= 8:
        for r in rows:
            k = str(r['id'])
            if e['previes'].get(k) or r['status'] not in (1,): continue
            d, noms = detall(r['id'])
            motiu = r['h'] if es_equip_fav(r['h'], equips) else r['a'] if es_equip_fav(r['a'], equips) else ''
            if not motiu and jugadors:
                fav = te_jugador_fav(noms, jugadors)
                if not fav: continue                         # alineació encara buida: es torna a mirar més tard
                motiu = fav[0]
            if envia(previa(r, d, motiu)): e['previes'][k] = True; desa(e)
    # 2) Directe: partits que comencen d'aquí a 35 min o que estan en joc
    limit = time.time() + 3.5 * 3600
    while True:
        n = ara()
        actius = [r for r in rows if not e['acabats'].get(str(r['id']))
                  and r['dt'] - datetime.timedelta(minutes=35) <= n <= r['dt'] + datetime.timedelta(hours=3)]
        if not actius or time.time() > limit or PROVA:
            if PROVA:
                for r in actius: segueix(r, e, jugadors, equips)
            break
        for r in actius:
            try: segueix(r, e, jugadors, equips)
            except Exception as ex: print('ERROR', r['id'], repr(ex)[:200])
        time.sleep(75)
    print('fet', n.strftime('%H:%M'), len(rows), 'partits candidats')


if __name__ == '__main__':
    main()
