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
if __name__=='__main__':
    if sys.argv[1:]==['check']:
        import publicar as U
        try:
            c=compte(); l=limit(c['user_id']); us=(l.get('data') or [{}])[0].get('quota_usage','?') if 'data' in l else '?'
            U.envia_text(f"✅ Instagram connectat: @{c.get('username')} · tipus {c.get('account_type')} · {c.get('media_count')} publicacions · publicades per API les últimes 24 h: {us}. Només s'ha LLEGIT el compte, no s'ha publicat res.",'sistema'); print('ok',c.get('username'))
        except Exception as e:
            U.envia_text(f'⚠️ Instagram: la comprovació ha fallat → {e}','sistema'); print('ERROR',e)
