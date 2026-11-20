#!/usr/bin/env python3
"""Genera al PC totes les imatges del publicador SENSE ENVIAR RES (ni Telegram ni Instagram).
Ús:  python previsualitzar.py                 → pròxim cap de setmana + l'últim jugat
     python previsualitzar.py 2026-11-14      → el cap de setmana d'aquest divendres
Les imatges queden a la carpeta  previsualitzacio/ ."""
import os, sys, datetime
os.environ.setdefault('TELEGRAM_BOT_TOKEN', 'previsualitzacio')   # perquè publicar.py es pugui importar
os.environ.setdefault('TELEGRAM_CHAT_ID', '0')
os.environ.pop('INSTAGRAM_TOKEN', None)                              # mai publicar des d'aquí
try:
    import certifi; os.environ.setdefault('SSL_CERT_FILE', certifi.where())   # Windows: certificats de confiança
except ImportError: pass
V = os.path.dirname(os.path.abspath(__file__)); os.chdir(V); sys.path.insert(0, V)
import proxims as P, resultats as R, classificacio as K, publicar as U

OUT = os.path.join(V, 'previsualitzacio'); os.makedirs(OUT, exist_ok=True)
avui = P.avui_madrid() if hasattr(P, 'avui_madrid') else datetime.date.today()

def mostra(tipus, llista):
    for x in llista: print(f'  {tipus}: {x[-1]}')

if len(sys.argv) > 1:
    dv = datetime.date.fromisoformat(sys.argv[1]); passat = (dv, dv + datetime.timedelta(days=2)); vinent = passat
else:
    vinent = U.cap_de_setmana(avui)
    dl = avui - datetime.timedelta(days=avui.weekday())            # dilluns d'aquesta setmana
    passat = (dl - datetime.timedelta(days=3), dl - datetime.timedelta(days=1))
    if avui.weekday() >= 5: passat = vinent                         # dissabte/diumenge: el cap de setmana en curs

print(f'Pròxims {vinent[0]}..{vinent[1]}')
mostra('post', P.generar(*vinent, OUT)); mostra('història', P.generar_story(*vinent, OUT))
print(f'Resultats {passat[0]}..{passat[1]}')
mostra('post', R.generar(*passat, OUT)); mostra('història', R.generar_story(*passat, OUT))
print('Classificacions')
mostra('post', K.generar(OUT))
jugats = P.partits(*passat, jugats=True)
if jugats:
    print('Història de resultat (exemple)'); print('  ', U.historia_resultat(jugats[0]))
print(f'\nFet. Obre la carpeta: {OUT}')
