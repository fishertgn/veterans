#!/usr/bin/env python3
"""Publicador: s'executa cada hora (launchd). Segons dia i hora decideix què generar i ho envia al bot.
Ús: publicar.py            → mode programat (surt si no toca res)
    publicar.py --ara      → força la comprovació de resultats ara mateix
    publicar.py --dilluns  → força el paquet del dilluns ara mateix"""
import os, sys, json, time, datetime, subprocess, hashlib, traceback
V=os.path.dirname(os.path.abspath(__file__)); os.chdir(V); sys.path.insert(0,V)
import proxims as P, resultats as R, classificacio as K, story as S
CFG=P.cfg(); ESTAT=os.path.join(V,'estat.json'); OUT=os.path.join(V,'out'); os.makedirs(OUT,exist_ok=True)
LOG=open(os.path.join(V,'publicar.log'),'a')
def log(*a):
    from zoneinfo import ZoneInfo
    s=datetime.datetime.now(ZoneInfo('Europe/Madrid')).strftime('%Y-%m-%d %H:%M')+' '+' '.join(str(x) for x in a); print(s); LOG.write(s+'\n'); LOG.flush()
def estat():
    try: return json.load(open(ESTAT))
    except Exception: return {'enviats':{},'fets':{}}
def desa(e): json.dump(e,open(ESTAT,'w'),indent=1,ensure_ascii=False)

def tg(method,**fields):
    args=['curl','-s','-m','240','-X','POST',f'https://api.telegram.org/bot{CFG["telegram_bot_token"]}/{method}','-F',f'chat_id={CFG["telegram_chat_id"]}']
    for k,v in fields.items(): args+=['-F',f'{k}={v}']
    for i in range(4):
        r=subprocess.run(args+['-o','/dev/null','-w','%{http_code}'],capture_output=True,text=True)
        if r.stdout=='200': return True
        time.sleep(5)
    log('ERROR telegram',method,r.stdout); return False
def envia_fitxer(p,caption): return tg('sendDocument',document='@'+p,caption=caption)
def envia_text(t): return tg('sendMessage',text=t)

def cap_de_setmana(d):
    """Divendres..diumenge de la setmana de d (si d és dilluns-dijous, el cap de setmana anterior... no: el vinent)."""
    wd=d.weekday()
    dv=d-datetime.timedelta(days=(wd-4)%7) if wd>=4 else d+datetime.timedelta(days=4-wd)
    return dv,dv+datetime.timedelta(days=2)

def etiqueta_data(dt): return f'{P.DIES[dt.weekday()]} {dt.day} {P.MES[dt.month-1]} {dt.year}'

def historia_resultat(r):
    html=S.resultat(r['h'],r['a'],r['hl'],r['al'],r['hs'],r['as_'],etiqueta_data(r['dt']),r['hora'],r['camp'].upper(),
                    'COPA F11 VETERANS' if r['comp']=='COPA' else f"LLIGA {r['comp'].split()[-1]} DIVISIÓ",r['jornada'].replace('Jornada','J').strip(),r['grup'])
    png=os.path.join(OUT,f'historia_{r["id"]}.png'); tmp=png[:-4]+'.html'; open(tmp,'w').write(html)
    P.captura(tmp,png,1080,1920,10000)
    return png

def comprova_resultats(avui):
    """Historia per cada partit acabat del cap de setmana que encara no s'hagi enviat."""
    e=estat(); d0,d1=cap_de_setmana(avui)
    rows=[r for r in P.partits(d0,d1,jugats=True)]
    nous=[r for r in rows if str(r['id']) not in e['enviats']]
    log(f'resultats {d0}..{d1}: {len(rows)} jugats, {len(nous)} nous')
    for r in sorted(nous,key=lambda r:r['dt']):
        png=historia_resultat(r)
        if envia_fitxer(png,f'🔴 FINAL · {r["h"]} {r["hs"]}-{r["as_"]} {r["a"]} · {r["comp"]}{" · "+r["grup"] if r["grup"] else ""}'):
            e['enviats'][str(r['id'])]=f'{r["hs"]}-{r["as_"]}'; desa(e)
    return len(nous)

def paquet_dilluns(avui):
    e=estat(); clau='dilluns_'+avui.isoformat()
    if clau in e['fets']: log('dilluns ja fet'); return
    d0,d1=avui-datetime.timedelta(days=3),avui-datetime.timedelta(days=1)   # divendres..diumenge passats
    envia_text(f'📊 Paquet del dilluns · cap de setmana {d0.day}-{d1.day} {P.MES[d1.month-1]}')
    for et,n,p in R.generar(d0,d1,OUT): envia_fitxer(p,f'{et} · {n} partits')
    for et,p in K.generar(OUT): envia_fitxer(p,et)
    n0,n1=cap_de_setmana(avui+datetime.timedelta(days=4))
    for et,n,p in P.generar(n0,n1,OUT): envia_fitxer(p,f'📅 Pròxims partits · {et} · {n} partits')
    for et,n,p in P.generar_story(n0,n1,OUT): envia_fitxer(p,f'📅 {et} · {n} partits')
    e['fets'][clau]=True; e['calendari_hash']=hash_calendari(n0,n1); desa(e); log('dilluns enviat')

def hash_calendari(d0,d1):
    rows=P.partits(d0,d1,jugats=None)
    return hashlib.md5(json.dumps([(r['id'],r['startTime'] if 'startTime' in r else r['dt'].isoformat(),r['camp']) for r in rows],sort_keys=True).encode()).hexdigest()

def divendres_calendari(avui):
    """Si el calendari ha canviat des del dilluns, torna a enviar pròxims partits."""
    e=estat(); clau='divendres_'+avui.isoformat()
    if clau in e['fets']: return
    d0,d1=cap_de_setmana(avui); h=hash_calendari(d0,d1)
    if h!=e.get('calendari_hash'):
        envia_text('📅 El calendari del cap de setmana ha canviat des de dilluns. Versió actualitzada:')
        for et,n,p in P.generar(d0,d1,OUT): envia_fitxer(p,f'Pròxims partits · {et} · {n} partits')
        for et,n,p in P.generar_story(d0,d1,OUT): envia_fitxer(p,f'{et} · {n} partits')
        e['calendari_hash']=h; log('divendres: calendari actualitzat enviat')
    else: log('divendres: calendari sense canvis')
    e['fets'][clau]=True; desa(e)

def main():
    from zoneinfo import ZoneInfo
    ara=datetime.datetime.now(ZoneInfo('Europe/Madrid')).replace(tzinfo=None); avui=ara.date(); wd=ara.weekday(); h=ara.hour
    try:
        if os.path.exists(os.path.join(V,'PROVA')):
            os.remove(os.path.join(V,'PROVA'))
            r=dict(id=0,h='UE Veterans Creixell',a='CE Altafulla',hl='https://minifutboltarragones.mygol.es/upload/46/57/skry502u.png',al='https://minifutboltarragones.mygol.es/upload/7F/78/o3xgkgdj.png',hs=2,as_=3,dt=datetime.datetime(2026,9,26,16,0),hora='16:00',camp='F11 Camp UE Creixell',comp='COPA',jornada='Jornada 1',grup='GRUP C')
            ok=envia_fitxer(historia_resultat(r),'✅ Prova del publicador automàtic (GitHub Actions)'); log('PROVA enviada',ok); return
        if '--ara' in sys.argv: return comprova_resultats(avui)
        if '--dilluns' in sys.argv: return paquet_dilluns(avui)
        if wd==0 and 9<=h<=13: paquet_dilluns(avui)      # tolera retards del programador; l'estat evita repetir
        elif wd==4 and 17<=h<=21: divendres_calendari(avui)
        elif (wd==4 and h>=22) or (wd==5 and 14<=h<=23) or (wd==6 and 9<=h<=18): comprova_resultats(avui)
        else: log('fora d\'horari, res a fer')
    except Exception as ex:
        log('ERROR',traceback.format_exc()); envia_text(f'⚠️ Error al publicador: {ex}')
if __name__=='__main__': main()
