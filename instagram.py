#!/usr/bin/env python3
"""Connexió amb Instagram (API amb inici de sessió d'Instagram). El token es llegeix de la variable d'entorn
INSTAGRAM_TOKEN (secret de GitHub); mai s'escriu a cap fitxer ni es mostra.
  instagram.py check     → llegeix el compte i avisa al tema Sistema. NO publica res."""
import os, sys, json, time, urllib.request, urllib.parse, urllib.error
API='https://graph.instagram.com/v23.0'
def token():
    t=os.environ.get('INSTAGRAM_TOKEN','').strip()
    if not t: raise SystemExit('Falta INSTAGRAM_TOKEN')
    return t
def crida(path,params=None,post=False):
    p=dict(params or {}); p['access_token']=token(); q=urllib.parse.urlencode(p)
    req=urllib.request.Request(f'{API}/{path}',data=q.encode()) if post else urllib.request.Request(f'{API}/{path}?{q}')
    try: return json.load(urllib.request.urlopen(req,timeout=60))
    except urllib.error.HTTPError as e:
        cos=e.read().decode('utf-8','ignore')
        try: err=json.loads(cos).get('error',{}); msg=f"{err.get('code')} · {err.get('message')}"
        except Exception: msg=cos[:200]
        raise RuntimeError(msg.replace(token(),'***'))
def compte(): return crida('me',{'fields':'user_id,username,account_type,media_count'})
def limit(uid):
    try: return crida(f'{uid}/content_publishing_limit',{'fields':'quota_usage,config'})
    except Exception as e: return {'error':str(e)}
# ---- publicació (encara no connectada al publicador) ----
def _espera(cid,intents=20):
    for _ in range(intents):
        s=crida(cid,{'fields':'status_code'}).get('status_code')
        if s=='FINISHED': return True
        if s in ('ERROR','EXPIRED'): raise RuntimeError(f'contenidor {s}')
        time.sleep(3)
    raise RuntimeError('contenidor: temps esgotat')
def publica_imatge(uid,url,peu='',historia=False):
    p={'image_url':url}
    if historia: p['media_type']='STORIES'
    elif peu: p['caption']=peu
    cid=crida(f'{uid}/media',p,post=True)['id']; _espera(cid)
    return crida(f'{uid}/media_publish',{'creation_id':cid},post=True)['id']
def publica_carrusel(uid,urls,peu=''):
    fills=[]
    for u in urls[:10]:
        c=crida(f'{uid}/media',{'image_url':u,'is_carousel_item':'true'},post=True)['id']; _espera(c); fills.append(c)
    cid=crida(f'{uid}/media',{'media_type':'CAROUSEL','children':','.join(fills),'caption':peu},post=True)['id']; _espera(cid)
    return crida(f'{uid}/media_publish',{'creation_id':cid},post=True)['id']
# ---- del PNG a una URL pública: JPEG dins pub/ del repositori (públic) ----
import subprocess, hashlib, shutil
V=os.path.dirname(os.path.abspath(__file__))
def auto(clau):
    try: return bool(json.load(open(os.path.join(V,'ig_auto.json'))).get(clau)) and bool(os.environ.get('INSTAGRAM_TOKEN'))
    except Exception: return False
def a_jpeg(png):
    os.makedirs(os.path.join(V,'pub'),exist_ok=True)
    jpg=os.path.join(V,'pub',hashlib.md5((png+str(os.path.getmtime(png))).encode()).hexdigest()[:16]+'.jpg')
    try:
        from PIL import Image
        Image.open(png).convert('RGB').save(jpg,'JPEG',quality=92)
    except ImportError:
        if shutil.which('sips'): subprocess.run(['sips','-s','format','jpeg','-s','formatOptions','92',png,'--out',jpg],stdout=subprocess.DEVNULL,check=True)
        else: subprocess.run(['convert',png,'-quality','92',jpg],check=True)
    return jpg
def url_publica(jpg):
    """Puja el JPEG al repositori i torna la URL raw. Només funciona dins de GitHub Actions."""
    repo=os.environ.get('GITHUB_REPOSITORY')
    if not repo: raise RuntimeError('fora de GitHub Actions: no hi ha URL pública')
    rel=os.path.relpath(jpg,V); g=lambda *a: subprocess.run(['git','-C',V,*a],capture_output=True,text=True)
    g('config','user.name','publicador'); g('config','user.email','publicador@users.noreply.github.com'); g('add',rel); g('commit','-m','imatge per a Instagram','--',rel)
    for _ in range(3):
        if g('push').returncode==0: break
        g('pull','--rebase','-q'); time.sleep(2)
    url=f'https://raw.githubusercontent.com/{repo}/main/{rel}'
    for _ in range(30):
        try:
            if urllib.request.urlopen(urllib.request.Request(url,method='HEAD'),timeout=20).status==200: return url
        except Exception: pass
        time.sleep(4)
    raise RuntimeError('la imatge no és accessible públicament')
def historia(png):
    """Publica un PNG 1080x1920 com a història. Torna l'id de la publicació."""
    return publica_imatge(compte()['user_id'],url_publica(a_jpeg(png)),historia=True)

if __name__=='__main__':
    if sys.argv[1:]==['prova-historia']:
        # Publica DE VERITAT la història de pròxims partits del primer dia amb partits. Només s'executa si algú llança aquest mode a mà.
        import datetime, publicar as U, proxims as P
        d0,d1=U.cap_de_setmana(P.avui_madrid())
        if not P.partits(d0,d1,jugats=False): d0,d1=d0+datetime.timedelta(days=7),d1+datetime.timedelta(days=7)
        res=P.generar_story(d0,d1,U.OUT); e=U.estat(); fetes=e.setdefault('ig_proxims',[]); n=0
        for et,_,png in res:
            clau=f'{d0.isoformat()}·{et}'
            if clau in fetes: continue
            try: mid=historia(png); fetes.append(clau); U.desa(e); n+=1; U.envia_text(f'✅ Publicada a Instagram: {et}. Id {mid}.','sistema'); print('ok',et)
            except Exception as ex: U.envia_text(f'⚠️ Instagram: no s\'ha pogut publicar {et} → {ex}','sistema'); print('ERROR',ex)
        if not n: U.envia_text('ℹ️ Instagram: totes les històries de pròxims partits d\'aquest cap de setmana ja estaven publicades.','sistema')
    elif sys.argv[1:]==['check']:
        import publicar as U
        try:
            c=compte(); l=limit(c['user_id']); us=(l.get('data') or [{}])[0].get('quota_usage','?') if 'data' in l else '?'
            U.envia_text(f"✅ Instagram connectat: @{c.get('username')} · tipus {c.get('account_type')} · {c.get('media_count')} publicacions · publicades per API les últimes 24 h: {us}. Només s'ha LLEGIT el compte, no s'ha publicat res.",'sistema'); print('ok',c.get('username'))
        except Exception as e:
            U.envia_text(f'⚠️ Instagram: la comprovació ha fallat → {e}','sistema'); print('ERROR',e)
