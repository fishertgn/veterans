#!/usr/bin/env python3
"""Targeta de victòria per equip (història 1080x1920) pensada perquè el club la comparteixi."""
import os, json
import proxims as P
V,RED,LOGO,FONTS,COLORS=P.V,P.RED,P.LOGO,P.FONTS,P.COLORS
def clubs():
    try: return json.load(open(os.path.join(V,'clubs.json')))
    except Exception: return {}
ORD={1:'1r',2:'2n',3:'3r',4:'4t'}
def html_victoria(r,pos=None,pts=None):
    """r: fila de partits() jugada. Es fa per al guanyador."""
    casa=r['hs']>r['as_']
    g=dict(n=r['h'],lg=r['hl'],gols=r['hs']) if casa else dict(n=r['a'],lg=r['al'],gols=r['as_'])
    p=dict(n=r['a'],lg=r['al'],gols=r['as_']) if casa else dict(n=r['h'],lg=r['hl'],gols=r['hs'])
    col=COLORS.get(r['comp'],'#d60000'); comp=f"{r['comp']}{' · '+r['grup'] if r['grup'] else ''}"
    handle=clubs().get(g['n'],''); on='a casa' if casa else 'a fora'
    classi=f'<div class="chip"><b>{ORD.get(pos,str(pos)+"è")}</b>{(" del "+r["grup"].title()) if r["grup"] else " de la lliga"} · {pts} punts</div>' if pos else ''
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS.replace('&display=swap','&family=Barlow+Condensed:wght@900&display=swap')}<style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;position:relative}}img{{display:block}}
body{{background:#151515;font-family:Barlow,sans-serif;color:#fff}}
.bg{{position:absolute;left:-200px;top:-260px;width:1480px;height:1480px;border-radius:50%;background:{RED}}}
.logo{{position:absolute;left:44px;top:40px;width:150px;height:150px;border-radius:24px}}
.comp{{position:absolute;right:50px;top:84px;font-family:'Barlow Condensed';font-weight:700;font-size:34px;letter-spacing:4px;border:3px solid #fff;border-radius:999px;padding:8px 24px;text-transform:uppercase}}
.esc{{position:absolute;left:50%;top:250px;transform:translateX(-50%);width:520px;height:520px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 80px rgba(0,0,0,.35)}}
.esc img{{width:400px;height:400px;object-fit:contain}}
.k{{position:absolute;left:0;top:810px;width:1080px;text-align:center;font-family:'Barlow Condensed';font-weight:900;font-size:210px;line-height:.9;letter-spacing:-2px;text-transform:uppercase;color:#fff}}
.n{{position:absolute;left:60px;right:60px;top:1010px;text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:72px;line-height:1;text-transform:uppercase;color:#ffd400}}
.sc{{position:absolute;left:60px;top:1180px;width:960px;height:230px;background:#fff;color:#151515;border-radius:24px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding:0 40px}}
.sc .t{{display:flex;flex-direction:column;align-items:center;gap:10px;font-weight:600;font-size:24px;text-align:center;line-height:1.05}}.sc .t img{{width:110px;height:110px;object-fit:contain}}.sc .t.lo{{color:#8a8a8a}}
.sc .m{{font-family:'Barlow Condensed';font-weight:700;font-size:150px;line-height:1;display:flex;align-items:center;gap:22px;padding:0 20px}}.sc .m i{{width:6px;height:100px;background:{col};border-radius:3px;display:block}}.sc .m .lo{{color:#9a9a9a}}
.chips{{position:absolute;left:0;top:1450px;width:1080px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap}}
.chip{{font-weight:600;font-size:32px;background:#2a2a2a;border-radius:999px;padding:12px 30px}}.chip b{{color:#ffd400;font-family:'Barlow Condensed';font-size:40px;margin-right:6px}}
.cta{{position:absolute;left:0;bottom:120px;width:1080px;text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:44px;letter-spacing:3px;text-transform:uppercase;color:#fff}}
.cta small{{display:block;font-family:Barlow;font-weight:500;font-size:28px;letter-spacing:1px;text-transform:none;color:#bdbdbd;margin-top:10px}}
</style></head><body><div class="bg"></div><img class="logo" src="{LOGO}"><div class="comp">{comp}</div>
<div class="esc"><img src="{g['lg']}"></div><div class="k">Victòria!</div><div class="n">{g['n']}</div>
<div class="sc"><div class="t{'' if casa else ' lo'}"><img src="{r['hl']}">{r['h']}</div><div class="m"><span class="{'' if casa else 'lo'}">{r['hs']}</span><i></i><span class="{'lo' if casa else ''}">{r['as_']}</span></div><div class="t{' lo' if casa else ''}"><img src="{r['al']}">{r['a']}</div></div>
<div class="chips"><div class="chip">Victòria {on}</div>{classi}</div>
<div class="cta">Comparteix-la al teu perfil{' · '+handle if handle else ''}<small>Tots els resultats a @veteranstarragona</small></div></body></html>"""
if __name__=='__main__':
    import datetime
    r=dict(h='UE Veterans Creixell',a='CE Altafulla',hl='https://minifutboltarragones.mygol.es/upload/46/57/skry502u.png',al='https://minifutboltarragones.mygol.es/upload/7F/78/o3xgkgdj.png',hs=2,as_=3,comp='COPA',grup='GRUP C',dt=datetime.datetime(2026,9,26,16,0))
    png=os.path.join(V,'out','equip_victoria_prova.png'); P.render_story(html_victoria(r,1,3),png); print(png)
