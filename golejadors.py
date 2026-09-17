#!/usr/bin/env python3
"""Pichichi (golejadors) i Zamora (porters menys golejats): post 1080x1350 i història 1080x1920 per competició.
Ús: golejadors.py [--send] [--test]   (--test usa la 1a divisió 25-26, id 102)"""
import sys, os, re, json, subprocess, time
import proxims as P, classificacio as K
V,RED,COLORS=P.V,P.RED,P.COLORS
UP='https://minifutboltarragones.mygol.es/upload/'
PART=('de','del','la','las','los','da','van','von','el')
def nom_jugador(n,c):
    n=(n or '').split(); c=(c or '').split()
    nom=n[0].title() if n else ''
    cg=[]
    for w in c:
        cg.append(w.lower() if w.lower() in PART else w.title())
        if w.lower() not in PART: break
    return (nom+' '+' '.join(cg)).strip()

def dades(tid,tipus):
    t=P.get(f'/tournaments/{tid}'); teams={x['id']:x for x in t['teams']}
    rows=P.get(f'/tournaments/{tid}/ranking/players/{tipus}/1/999')
    out=[]
    for r in rows:
        tm=teams.get(r['idTeam'])
        if not tm or not r.get('gamesPlayed'): continue
        if tipus=='scorers':
            if r['points']<=0: continue
            out.append(dict(j=nom_jugador(r.get('playerName'),r.get('playerSurname')),eq=P.nice(tm['name']),lg=UP+tm['logoImgUrl'],pj=r['gamesPlayed'],v=r['points'],ratio=r['points']/r['gamesPlayed']))
        else:
            out.append(dict(j=nom_jugador(r.get('playerName'),r.get('playerSurname')),eq=P.nice(tm['name']),lg=UP+tm['logoImgUrl'],pj=r['gamesPlayed'],v=r['pointsAgainst'],ratio=r['pointsAgainst']/r['gamesPlayed']))
    out.sort(key=(lambda r:(-r['v'],r['pj'])) if tipus=='scorers' else (lambda r:(r['ratio'],-r['pj'])))
    return t['name'],P.curt(t['name']),out

CFG={'scorers':dict(titol='Golejadors',tag='PICHICHI',unitat='gols',col='GOLS'),'goalkeepers':dict(titol='Porters',tag='ZAMORA',unitat='encaixats',col='ENC.')}
def css(col,h_row,f_nom,f_eq,esc,f_v,h_hero,esc_h,f_h):
    return f""".hero{{height:{h_hero}px;flex:none;background:#151515;color:#fff;border-radius:14px;border-left:12px solid {col};display:grid;grid-template-columns:{esc_h+20}px 1fr auto;align-items:center;gap:18px;padding:0 26px 0 20px}}
.hero img{{width:{esc_h}px;height:{esc_h}px;object-fit:contain;background:#fff;border-radius:50%;padding:6px}}
.hero .tag{{font-family:'Barlow Condensed';font-weight:700;font-size:{int(f_h*0.42)}px;letter-spacing:5px;color:{col}}}
.hero .j{{font-family:'Barlow Condensed';font-weight:700;font-size:{f_h}px;line-height:1;text-transform:uppercase}}
.hero .e{{font-weight:500;font-size:{int(f_h*0.4)}px;color:#bdbdbd;margin-top:4px}}
.hero .hv{{font-family:'Barlow Condensed';font-weight:700;font-size:{int(f_h*1.9)}px;line-height:.9;color:{col};text-align:right}}.hero .hv small{{display:block;font-family:Barlow;font-weight:600;font-size:{int(f_h*0.3)}px;letter-spacing:3px;color:#bdbdbd;text-transform:uppercase}}
.r{{height:{h_row}px;flex:none;background:#fff;border-radius:12px;box-shadow:0 2px 6px rgba(0,0,0,.05);display:grid;grid-template-columns:50px {esc+8}px 1fr 70px 80px 92px;align-items:center;gap:8px;padding:0 14px 0 10px}}
.pos{{font-family:'Barlow Condensed';font-weight:700;font-size:{f_v-6}px;text-align:center;color:#9a9a9a}}
.r img{{width:{esc}px;height:{esc}px;object-fit:contain}}
.nm{{min-width:0}}.nm b{{display:block;font-weight:600;font-size:{f_nom}px;line-height:1.05;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.nm small{{display:block;font-weight:500;font-size:{f_eq}px;color:#8a8a8a;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.st{{text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:{f_v-8}px;line-height:1;color:#555}}.st small{{display:block;font-family:Barlow;font-size:10px;letter-spacing:1px;color:#9a9a9a;font-weight:700;margin-top:2px}}
.v{{font-family:'Barlow Condensed';font-weight:700;font-size:{f_v}px;text-align:center;background:{RED};color:#fff;border-radius:9px;height:{int(h_row*0.62)}px;line-height:{int(h_row*0.62)}px}}"""
def cos(rs,tipus):
    c=CFG[tipus]; h=rs[0]
    out=f'<div class="hero"><img src="{h["lg"]}"><div><div class="tag">{c["tag"]}</div><div class="j">{h["j"]}</div><div class="e">{h["eq"]} · {h["pj"]} partits · {h["ratio"]:.2f} per partit</div></div><div class="hv">{h["v"]}<small>{c["unitat"]}</small></div></div>'
    for i,r in enumerate(rs[1:],2):
        out+=f'<div class="r"><span class="pos">{i}</span><img src="{r["lg"]}"><span class="nm"><b>{r["j"]}</b><small>{r["eq"]}</small></span><span class="st">{r["pj"]}<small>PJ</small></span><span class="st">{r["ratio"]:.2f}<small>x PARTIT</small></span><b class="v">{r["v"]}</b></div>'
    return out
def generar(outdir,ids=None,stories=True):
    out=[]; ts=[t['id'] for t in P.competicions()] if ids is None else ids
    for tid in ts:
        for tipus in ('scorers','goalkeepers'):
            nom,comp,rs=dades(tid,tipus)
            if len(rs)<3: continue
            col=COLORS.get(comp,'#d60000'); col='#ffd400' if comp=='COPA' else col; sub=K.nom_curt(nom) if 'DIVISI' in nom.upper() else 'Copa F11 Veterans'; c=CFG[tipus]
            png=P.nom_fitxer(outdir,c['titol'].upper(),[comp],P.avui_madrid(),None,'POST'); tmp=png[:-4]+'.html'
            open(tmp,'w').write(P.post_shell(c['titol'],sub,cos(rs[:10],tipus),css(col,82,20,14,44,34,150,96,48),peu='Dades oficials de Minifutbol Tarragonès'))
            P.captura(tmp,png,1080,1350); out.append((f'POST · {c["titol"]} {sub}',png))
            if stories:
                png=P.nom_fitxer(outdir,c['titol'].upper(),[comp],P.avui_madrid(),None,'HISTORIA')
                P.render_story(P.story_shell(c['titol'],sub,cos(rs[:10],tipus),css(col,96,24,16,50,38,170,110,54)),png); out.append((f'HISTÒRIA · {c["titol"]} {sub}',png))
    return out
def generar_pichichi(outdir,ids=None):
    """Història curta del dijous: el pichichi i els tres perseguidors de cada competició."""
    out=[]; ts=[t['id'] for t in P.competicions()] if ids is None else ids
    for tid in ts:
        nom,comp,rs=dades(tid,'scorers')
        if len(rs)<3: continue
        col='#ffd400' if comp=='COPA' else COLORS.get(comp,'#d60000'); sub=K.nom_curt(nom) if 'DIVISI' in nom.upper() else 'Copa F11 Veterans'
        png=P.nom_fitxer(outdir,'PICHICHI',[comp],P.avui_madrid(),None,'HISTORIA')
        P.render_story(P.story_shell('Pichichi',sub,cos(rs[:4],'scorers'),css(col,110,28,18,58,42,220,140,64)),png); out.append((f'HISTÒRIA · Pichichi {sub}',png))
    return out

if __name__=='__main__':
    outdir=os.path.join(V,'out'); os.makedirs(outdir,exist_ok=True)
    res=generar(outdir,[102] if '--test' in sys.argv else None)
    if not res: print('Encara no hi ha dades de golejadors.')
    for e,p in res: print(e,'->',p)
    if '--send' in sys.argv:
        cfg=P.cfg()
        for e,p in res:
            for i in range(4):
                r=subprocess.run(['curl','-s','-m','240','-X','POST',f'https://api.telegram.org/bot{cfg["telegram_bot_token"]}/sendDocument','-F',f'chat_id={cfg["telegram_chat_id"]}','-F',f'document=@{p}','-F',f'caption={e}','-o','/dev/null','-w','%{http_code}'],capture_output=True,text=True)
                print(e,r.stdout)
                if r.stdout=='200': break
                time.sleep(5)
