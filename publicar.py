#!/usr/bin/env python3
"""Publicador: s'executa cada hora (launchd). Segons dia i hora decideix què generar i ho envia al bot.
Ús: publicar.py            → mode programat (surt si no toca res)
    publicar.py --ara      → força la comprovació de resultats ara mateix
    publicar.py --dilluns  → força el paquet del dilluns ara mateix"""
import os, sys, re, json, time, datetime, subprocess, hashlib, traceback
V=os.path.dirname(os.path.abspath(__file__)); os.chdir(V); sys.path.insert(0,V)
import proxims as P, resultats as R, classificacio as K, story as S, golejadors as G, peus as PE, partit as PJ, reel as RL
CFG=P.cfg(); ESTAT=os.path.join(V,'estat.json'); OUT=os.path.join(V,'out'); os.makedirs(OUT,exist_ok=True)
LOG=open(os.path.join(V,'publicar.log'),'a')
def log(*a):
    from zoneinfo import ZoneInfo
    s=datetime.datetime.now(ZoneInfo('Europe/Madrid')).strftime('%Y-%m-%d %H:%M')+' '+' '.join(str(x) for x in a); print(s); LOG.write(s+'\n'); LOG.flush()
def estat():
    try: return json.load(open(ESTAT))
    except Exception: return {'enviats':{},'fets':{}}
def desa(e): json.dump(e,open(ESTAT,'w'),indent=1,ensure_ascii=False)

def _temes():
    try: return json.load(open(os.path.join(V,'temes.json')))
    except Exception: return {}
TEMES=_temes()      # {"grup": -100..., "temes": {"directe": 12, "proxims": 14, ...}}
def tg(method,tema=None,**fields):
    grup=os.environ.get('TELEGRAM_GROUP_ID') or TEMES.get('grup')
    desti=grup if grup else CFG['telegram_chat_id']
    args=['curl','-s','-m','240','-X','POST',f'https://api.telegram.org/bot{CFG["telegram_bot_token"]}/{method}','-F',f'chat_id={desti}']
    fil=(TEMES.get('temes') or {}).get(tema) if (grup and tema) else None
    if fil: args+=['-F',f'message_thread_id={fil}']
    for k,v in fields.items(): args+=['-F',f'{k}={v}']
    for i in range(4):
        r=subprocess.run(args+['-o','/dev/null','-w','%{http_code}'],capture_output=True,text=True)
        if r.stdout=='200': return True
        time.sleep(5)
    log('ERROR telegram',method,tema,r.stdout); return False
def envia_fitxer(p,caption,tema=None): return tg('sendDocument',tema,document='@'+p,caption=caption)
def envia_text(t,tema='sistema'): return tg('sendMessage',tema,text=t)
def envia_peu(text,tema,de=''):
    """Peu de foto en un missatge sol, perquè es pugui copiar sencer amb una pulsació llarga."""
    if not text: return
    envia_text(f'📝 Peu de foto{(" · "+de) if de else ""}. Copia el missatge següent:',tema); envia_text(text,tema)

def cap_de_setmana(d):
    """Divendres..diumenge de la setmana de d (si d és dilluns-dijous, el cap de setmana anterior... no: el vinent)."""
    wd=d.weekday()
    dv=d-datetime.timedelta(days=(wd-4)%7) if wd>=4 else d+datetime.timedelta(days=4-wd)
    return dv,dv+datetime.timedelta(days=2)

def etiqueta_data(dt): return f'{P.DIES[dt.weekday()]} {dt.day} {P.MES[dt.month-1]} {dt.year}'

def historia_resultat(r):
    html=S.resultat(r['h'],r['a'],r['hl'],r['al'],r['hs'],r['as_'],etiqueta_data(r['dt']),r['hora'],r['camp'].upper(),
                    'COPA F11 VETERANS' if r['comp']=='COPA' else f"LLIGA {r['comp'].split()[-1]} DIVISIÓ",r['jornada'].replace('Jornada','J').strip(),r['grup'])
    nom=re.sub(r'[\\/:*?"<>|;,.]','',f"RESULTAT {P.etiqueta_comp(r['comp'])} {r['h']} {r['hs']}-{r['as_']} {r['a']}".upper())+' '+P.data_fitxer(r['dt'].date())
    png=os.path.join(OUT,nom+'.png'); tmp=png[:-4]+'.html'; open(tmp,'w').write(html)
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
        if envia_fitxer(png,f'🔴 FINAL · {r["h"]} {r["hs"]}-{r["as_"]} {r["a"]} · {r["comp"]}{" · "+r["grup"] if r["grup"] else ""}','directe'):
            e['enviats'][str(r['id'])]=f'{r["hs"]}-{r["as_"]}'; desa(e)
        if IG.auto('histories_resultats') and str(r['id']) not in e.setdefault('ig',{}):
            try:
                e['ig'][str(r['id'])]=IG.historia(png); desa(e); envia_text(f'📲 Publicada a Instagram com a història: {r["h"]} {r["hs"]}-{r["as_"]} {r["a"]}','directe')
            except Exception as ex:
                log('IG ERROR',ex); envia_text(f'⚠️ No s\'ha pogut publicar a Instagram ({r["h"]} – {r["a"]}): {ex}. Puja-la a mà.','directe')
    return len(nous)

def paquet_dilluns(avui):
    e=estat(); clau='dilluns_'+avui.isoformat()
    if clau in e['fets']: log('dilluns ja fet'); return
    d0,d1=avui-datetime.timedelta(days=3),avui-datetime.timedelta(days=1)   # divendres..diumenge passats
    envia_text(f'📊 Paquet del dilluns · cap de setmana {d0.day}-{d1.day} {P.MES[d1.month-1]}. Trobaràs cada cosa al seu tema.','sistema')
    for et,n,p in R.generar(d0,d1,OUT): envia_fitxer(p,f'POST · {et} · {n} partits','resultats')
    for et,n,p in R.generar_story(d0,d1,OUT): envia_fitxer(p,f'HISTÒRIA · {et} · {n} partits','resultats')
    envia_peu(PE.resultats(sorted(P.partits(d0,d1,jugats=None),key=lambda r:(r['comp'],r['grup'],r['dt']))),'resultats','post de resultats')
    for et,p in K.generar(OUT): envia_fitxer(p,'POST · '+et,'classificacio')
    for et,p in K.generar_story(OUT): envia_fitxer(p,'HISTÒRIA · '+et.replace('Història ',''),'classificacio')
    for t in P.competicions():
        nom,comp,taules,zones=K.dades(t['id'])
        if taules: envia_peu(PE.classificacio(K.nom_curt(nom) if 'DIVISI' in nom.upper() else 'Copa F11 Veterans',sorted(taules,key=lambda x:x[0])),'classificacio','classificació '+comp)
    for et,p in G.generar(OUT): envia_fitxer(p,et,'golejadors')      # pichichi i Zamora (si ja hi ha dades)
    for t in P.competicions():
        for tipus in ('scorers','goalkeepers','assistances','mvps'):
            nom,comp,rs=G.dades(t['id'],tipus)
            if len(rs)>=3: envia_peu(PE.golejadors(K.nom_curt(nom) if 'DIVISI' in nom.upper() else 'Copa F11 Veterans',rs,tipus),'golejadors',G.CFG[tipus]['titol'].lower()+' '+comp)
    try:
        for et,p in RL.generar(d0,d1,OUT): envia_fitxer(p,et,'reels')
    except Exception as ex: log('reel ERROR',ex)
    n0,n1=cap_de_setmana(avui+datetime.timedelta(days=4))
    for et,n,p in P.generar(n0,n1,OUT): envia_fitxer(p,f'📅 Pròxims partits · {et} · {n} partits','proxims')
    for et,n,p in P.generar_story(n0,n1,OUT): envia_fitxer(p,f'📅 {et} · {n} partits','proxims')
    e['fets'][clau]=True; e['calendari_hash']=hash_calendari(n0,n1); desa(e); log('dilluns enviat')

def hash_calendari(d0,d1):
    rows=P.partits(d0,d1,jugats=None)
    return hashlib.md5(json.dumps([(r['id'],r['startTime'] if 'startTime' in r else r['dt'].isoformat(),r['camp']) for r in rows],sort_keys=True).encode()).hexdigest()

def proxims_setmana(avui):
    """Dijous i divendres al matí: pròxims partits del cap de setmana (post + històries). Un cop per dia."""
    e=estat(); clau='proxims_'+avui.isoformat()
    if clau in e['fets']: return
    d0,d1=cap_de_setmana(avui); h=hash_calendari(d0,d1); dia=P.DIES[avui.weekday()].capitalize()
    if not P.partits(d0,d1,jugats=None):
        envia_text(f'ℹ️ {dia}: no hi ha partits programats el cap de setmana {d0.day}-{d1.day} {P.MES[d1.month-1]}. No s\'envia res.','sistema')
        e['fets'][clau]=True; desa(e); log('proxims: cap partit'); return
    if avui.weekday()==4:
        nota='⚠️ El calendari ha CANVIAT des d\'ahir. Fes servir aquesta versió.' if h!=e.get('calendari_hash') else 'Sense canvis des d\'ahir.'
    else: nota='Primera versió de la setmana.'
    envia_text(f'📅 {dia} · Pròxims partits del cap de setmana {d0.day}-{d1.day} {P.MES[d1.month-1]}. {nota}','proxims')
    for et,n,p in P.generar(d0,d1,OUT): envia_fitxer(p,f'Pròxims partits · {et} · {n} partits','proxims')
    for et,n,p in P.generar_story(d0,d1,OUT): envia_fitxer(p,f'{et} · {n} partits','proxims')
    envia_peu(PE.proxims(P.partits(d0,d1,jugats=False)),'proxims','post de pròxims partits')
    if avui.weekday()==3:
        try:
            for et,p in RL.generar(d0,d1,OUT,tipus='proxims'): envia_fitxer(p,et,'reels')
        except Exception as ex: log('reel proxims ERROR',ex)
        for et,p in G.generar_pichichi(OUT): envia_fitxer(p,et,'golejadors')
        res,pj,info=PJ.generar(d0,d1,OUT)
        for et,p in res: envia_fitxer(p,et,'partit')
        if pj: envia_peu(PE.partit(pj,info),'partit','partit de la jornada')
    e['calendari_hash']=h; e['fets'][clau]=True; desa(e); log('proxims enviat',dia)

def resum_mensual(avui):
    """Primer dilluns de cada mes: resum del mes anterior."""
    e=estat(); ant=(avui.replace(day=1)-datetime.timedelta(days=1)); clau=f'mensual_{ant.year}-{ant.month:02d}'
    if clau in e['fets']: return
    res,d=MS.generar(ant.year,ant.month,OUT)
    for et,p in res: envia_fitxer(p,et,'mensual')
    if d: envia_peu(MS.peu(d,ant.year,ant.month),'mensual','resum mensual')
    e['fets'][clau]=True; desa(e); log('mensual',clau,'enviat' if res else 'sense prou partits')

def main():
    from zoneinfo import ZoneInfo
    ara=datetime.datetime.now(ZoneInfo('Europe/Madrid')).replace(tzinfo=None); avui=ara.date(); wd=ara.weekday(); h=ara.hour
    try:
        if os.path.exists(os.path.join(V,'PROVA')):
            os.remove(os.path.join(V,'PROVA'))
            r=dict(id=0,h='UE Veterans Creixell',a='CE Altafulla',hl='https://minifutboltarragones.mygol.es/upload/46/57/skry502u.png',al='https://minifutboltarragones.mygol.es/upload/7F/78/o3xgkgdj.png',hs=2,as_=3,dt=datetime.datetime(2026,9,26,16,0),hora='16:00',camp='F11 Camp UE Creixell',comp='COPA',jornada='Jornada 1',grup='GRUP C')
            ok=envia_fitxer(historia_resultat(r),'✅ Prova del publicador automàtic (GitHub Actions)','sistema'); log('PROVA enviada',ok); return
        if '--ara' in sys.argv: return comprova_resultats(avui)
        if '--dilluns' in sys.argv: return paquet_dilluns(avui)
        if '--proxims' in sys.argv: return proxims_setmana(avui)
        if '--mensual' in sys.argv: return resum_mensual(avui)
        if '--partit' in sys.argv:
            d0,d1=cap_de_setmana(avui); res,pj,info=PJ.generar(d0,d1,OUT)
            for et,p in res: envia_fitxer(p,et,'partit')
            if pj: envia_peu(PE.partit(pj,info),'partit','partit de la jornada')
            return
        if wd==0 and 9<=h<=13:
            paquet_dilluns(avui)
            if avui.day<=7: resum_mensual(avui)      # tolera retards del programador; l'estat evita repetir
        elif wd in (3,4) and 10<=h<=13: proxims_setmana(avui)
        elif (wd==4 and h>=22) or (wd==5 and 14<=h<=23) or (wd==6 and 9<=h<=18): comprova_resultats(avui)
        else: print('fora d\'horari, res a fer')      # sense escriure al registre: amb el disparador extern s'executa cada mitja hora
    except Exception as ex:
        log('ERROR',traceback.format_exc()); envia_text(f'⚠️ Error al publicador: {ex}')
if __name__=='__main__': main()
