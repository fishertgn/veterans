import json, sys
UP='https://minifutboltarragones.mygol.es/upload/'
RED='#d60000'
import os as _os; LOGO='file://'+_os.path.dirname(_os.path.abspath(__file__))+'/logo_crop.png'
FONTS='<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">'
def resultat(home,away,hl,al,hs,as_,data,hora,camp,comp,jornada,grup):
    guany = home if hs>as_ else away if as_>hs else 'EMPAT'
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;position:relative}}
body{{background:{RED};font-family:'Space Grotesk',sans-serif;color:#111}}
.logo{{position:absolute;left:50%;top:40px;transform:translateX(-50%);width:520px;height:520px}}
.tk{{position:absolute;left:80px;top:640px;width:920px;height:1220px;background:#fff;border-radius:36px;box-shadow:0 40px 100px rgba(0,0,0,.35)}}
.hd{{padding:48px 70px 0;text-align:center}}
.hd .l{{font-family:Anton;font-size:60px;letter-spacing:4px;line-height:1}}
.hd .l small{{display:block;font-family:'Space Grotesk';font-weight:600;font-size:26px;letter-spacing:5px;color:{RED};margin-top:12px}}
.vs{{margin-top:36px;display:flex;justify-content:space-around;align-items:flex-start;padding:0 40px}}
.tm{{width:340px;text-align:center}}
.tm img{{width:190px;height:190px;object-fit:contain;margin:0 auto 20px}}
.tm .n{{font-weight:600;font-size:32px;line-height:1.15;text-transform:uppercase}}
.sc{{margin:20px auto 0;text-align:center;font-family:Anton;font-size:230px;line-height:1;letter-spacing:6px}}
.sc span{{color:{RED}}}
.fin{{text-align:center;font-family:Anton;font-size:36px;letter-spacing:12px;color:#fff;background:#111;display:table;margin:6px auto 0;padding:8px 36px;transform:rotate(-3deg)}}
.cut{{margin:34px 60px 0;border-top:6px dashed #ccc}}
.stub{{padding:10px 70px 0}}
.row{{display:flex;justify-content:space-between;font-weight:600;font-size:28px;letter-spacing:3px;color:#666;margin-top:22px}}
.row b{{color:#111;font-size:34px;text-transform:uppercase}}
</style></head><body>
<img class="logo" src="{LOGO}">
<div class="tk">
 <div class="hd"><div class="l">RESULTAT<small>{comp} · {jornada} · {grup}</small></div></div>
 <div class="vs"><div class="tm"><img src="{hl}"><div class="n">{home}</div></div><div class="tm"><img src="{al}"><div class="n">{away}</div></div></div>
 <div class="sc">{hs}<span>-</span>{as_}</div>
 <div class="fin">FINAL</div>
 <div class="cut"></div>
 <div class="stub">
  <div class="row"><span>DATA</span><b>{data}</b></div>
  <div class="row"><span>HORA</span><b>{hora}</b></div>
  <div class="row"><span>CAMP</span><b>{camp}</b></div>
  <div class="row"><span>GUANYADOR</span><b>{guany}</b></div>
 </div>
</div>
</body></html>'''
if __name__=='__main__':
    html=resultat('UE Veterans Creixell','CE Altafulla',UP+'46/57/skry502u.png',UP+'7F/78/o3xgkgdj.png',2,3,'DISSABTE 26 SET 2026','16:00','F11 CAMP UE CREIXELL','COPA F11 VETERANS','J1','GRUP C')
    open('opcions/resultat_v2.html','w').write(html)
