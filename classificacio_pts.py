#!/usr/bin/env python3
import os, io, sys
sys.stdout=io.StringIO(); import classificacio_opcions as K; sys.stdout=sys.__stdout__
L,page,forma,render,COL,RED=K.L,K.page,K.forma,K.render,K.COL,K.RED
def build(name,bg,fg,lider=None):
    rows=''
    for i,r in enumerate(L):
        b,f=(lider if (lider and i<1) else (bg,fg))
        rows+=f'<div class="r"><b class="pos" style="{"background:"+COL+";color:#fff" if i<1 else ""}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span>{r["g"]}</span><span>{r["e"]}</span><span>{r["p"]}</span><span>{r["gf"]}</span><span>{r["gc"]}</span><span class="dg">{r["dg"]:+d}</span>{forma(r["forma"],12)}<b class="pts" style="background:{b};color:{f}">{r["pts"]}</b></div>'
    render(name,page(f""".tb{{position:absolute;left:40px;top:232px;width:1000px;background:#fff;border-radius:14px;border-left:10px solid {COL};box-shadow:0 2px 8px rgba(0,0,0,.05);overflow:hidden}}
.th,.r{{display:grid;grid-template-columns:48px 42px 1fr 44px 40px 40px 40px 46px 46px 56px 104px 74px;align-items:center;gap:5px;padding:0 14px 0 8px;height:72px}}
.th{{height:48px;font-weight:700;font-size:13px;letter-spacing:1.5px;color:#9a9a9a;text-transform:uppercase;border-bottom:2px solid #eee}}.th span,.r>span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #f0f0f0;font-weight:600;font-size:18px}}.r:last-child{{border-bottom:0}}
.r img{{width:40px;height:40px;object-fit:contain}}.r .n{{font-weight:700;font-size:18px;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:26px;width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center}}
.fm{{display:flex;gap:4px;justify-content:center}}.fm i{{border-radius:50%;display:block}}
.dg{{color:#777}}.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:30px;text-align:center;border-radius:8px;height:44px;line-height:44px}}
</style>""",f'<div class="tb"><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>G</span><span>E</span><span>P</span><span>GF</span><span>GC</span><span>DG</span><span>Últims 5</span><span>PTS</span></div>{rows}</div>','Lliga 1a Divisió'))
build('KP1_vermell',RED,'#fff')
build('KP2_competicio',COL,'#151515')
build('KP3_gris',"#f0f0f0",'#151515')
build('KP4_vermell_clar',"#ffe5e5",RED)
build('KP5_lider_color',"#f0f0f0",'#151515',lider=(COL,'#151515'))
