#!/usr/bin/env python3
import os, io, sys
sys.stdout=io.StringIO(); import classificacio_opcions as K; sys.stdout=sys.__stdout__
L,copa,page,forma,render,COL,RED=K.L,K.copa,K.page,K.forma,K.render,K.COL,K.RED
grups=sorted(copa.items())

# ---- LLIGA: combinació 1+2 ----
def lliga_combo(name,pts_box):
    rows=''.join(f'<div class="r"><b class="pos" style="{"background:"+COL+";color:#fff" if i<1 else ""}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span>{r["g"]}</span><span>{r["e"]}</span><span>{r["p"]}</span><span>{r["gf"]}</span><span>{r["gc"]}</span><span class="dg">{r["dg"]:+d}</span>{forma(r["forma"],12)}<b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(L))
    ptscss = ".pts{font-family:'Barlow Condensed';font-weight:800;font-size:30px;text-align:center;background:#151515;color:#fff;border-radius:8px;height:44px;line-height:44px}" if pts_box else ".pts{font-family:'Barlow Condensed';font-weight:800;font-size:32px;text-align:center}"
    render(name,page(f""".tb{{position:absolute;left:40px;top:232px;width:1000px;background:#fff;border-radius:14px;border-left:10px solid {COL};box-shadow:0 2px 8px rgba(0,0,0,.05);overflow:hidden}}
.th,.r{{display:grid;grid-template-columns:48px 42px 1fr 44px 40px 40px 40px 46px 46px 56px 104px 74px;align-items:center;gap:5px;padding:0 14px 0 8px;height:72px}}
.th{{height:48px;font-weight:700;font-size:13px;letter-spacing:1.5px;color:#9a9a9a;text-transform:uppercase;border-bottom:2px solid #eee}}.th span,.r>span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #f0f0f0;font-weight:600;font-size:18px}}.r:last-child{{border-bottom:0}}
.r img{{width:40px;height:40px;object-fit:contain}}.r .n{{font-weight:700;font-size:18px;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:26px;width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center}}
.fm{{display:flex;gap:4px;justify-content:center}}.fm i{{border-radius:50%;display:block}}
.dg{{color:#777}}{ptscss}
</style>""",f'<div class="tb"><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>G</span><span>E</span><span>P</span><span>GF</span><span>GC</span><span>DG</span><span>Últims 5</span><span>PTS</span></div>{rows}</div>','Lliga 1a Divisió'))
lliga_combo('K12a_combo',False)
lliga_combo('K12b_combo_caixa',True)

# ---- COPA ----
def sub(): return 'Copa F11 · Fase de grups'
# KC3 · files d'ample complet amb franja, 4 grups per imatge, zona de classificació tintada
def kc3(gs):
    secs=''
    for g,rs in gs:
        secs+=f'<div class="sec"><div class="sh">{g}<small>Els 2 primers passen a vuitens</small></div>'+''.join(f'<div class="r{" q" if i<2 else ""}"><b class="pos">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span class="st">{r["pj"]}<small>PJ</small></span><span class="st">{r["g"]}-{r["e"]}-{r["p"]}<small>G-E-P</small></span><span class="st">{r["gf"]}:{r["gc"]}<small>Gols</small></span><span class="st">{r["dg"]:+d}<small>DG</small></span><b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(rs))+'</div>'
    return page(f""".wrap{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:14px}}
.sec{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);border-left:10px solid {RED}}}
.sh{{font-family:'Barlow Condensed';font-weight:800;font-size:24px;letter-spacing:2px;padding:8px 16px 4px;text-transform:uppercase;color:{RED};display:flex;justify-content:space-between;align-items:baseline}}.sh small{{font-family:Barlow;font-weight:600;font-size:12px;letter-spacing:1px;color:#9a9a9a;text-transform:none}}
.r{{display:grid;grid-template-columns:40px 40px 1fr 60px 90px 80px 60px 70px;align-items:center;gap:8px;padding:0 16px 0 10px;height:50px;border-top:1px solid #f0f0f0}}
.r.q{{background:#fff3f3}}
.r img{{width:34px;height:34px;object-fit:contain}}.r .n{{font-weight:700;font-size:17px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:24px;text-align:center}}.r.q .pos{{color:{RED}}}
.st{{text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:20px;line-height:1}}.st small{{display:block;font-family:Barlow;font-size:9px;letter-spacing:1px;color:#9a9a9a;font-weight:700;margin-top:2px}}
.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:28px;text-align:right}}
</style>""",f'<div class="wrap">{secs}</div>',sub())
render('KC3_franja_4',kc3(grups[:4]))
# KC4 · 2 grups per imatge, taula gran completa
def kc4(gs):
    secs=''
    for g,rs in gs:
        secs+=f'<div class="sec"><div class="sh">{g}</div><div class="th"><span>#</span><span></span><span class="n">Equip</span><span>PJ</span><span>G</span><span>E</span><span>P</span><span>GF</span><span>GC</span><span>DG</span><span>PTS</span></div>'+''.join(f'<div class="r"><b class="pos" style="{"background:"+RED+";color:#fff" if i<2 else ""}">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><span>{r["pj"]}</span><span>{r["g"]}</span><span>{r["e"]}</span><span>{r["p"]}</span><span>{r["gf"]}</span><span>{r["gc"]}</span><span class="dg">{r["dg"]:+d}</span><b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(rs))+'</div>'
    return page(f""".wrap{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:20px}}
.sec{{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);border-left:10px solid {RED}}}
.sh{{background:{RED};color:#fff;font-family:'Barlow Condensed';font-weight:800;font-size:30px;letter-spacing:3px;padding:8px 18px;text-transform:uppercase}}
.th,.r{{display:grid;grid-template-columns:52px 44px 1fr 52px 44px 44px 44px 52px 52px 62px 76px;align-items:center;gap:6px;padding:0 18px 0 10px;height:70px}}
.th{{height:44px;font-weight:700;font-size:13px;letter-spacing:2px;color:#9a9a9a;text-transform:uppercase;border-bottom:2px solid #eee}}.th span,.r>span{{text-align:center}}.th .n,.r .n{{text-align:left}}
.r{{border-bottom:1px solid #f0f0f0;font-weight:600;font-size:19px}}.r:last-child{{border-bottom:0}}
.r img{{width:40px;height:40px;object-fit:contain}}.r .n{{font-weight:700;font-size:19px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:26px;width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center}}
.dg{{color:#777}}.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:32px;text-align:center}}
</style>""",f'<div class="wrap">{secs}</div>',sub())
render('KC4_dos_grups',kc4(grups[:2]))
# KC5 · targeta per grup amb equips en horitzontal (escut gran + punts), 8 en una imatge
def kc5(gs):
    secs=''
    for g,rs in gs:
        secs+=f'<div class="sec"><div class="sh">{g}</div><div class="row">'+''.join(f'<div class="tm{" q" if i<2 else ""}"><b class="pos">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span><b class="pts">{r["pts"]}<small>PTS</small></b><span class="dg">{r["pj"]} PJ · {r["dg"]:+d}</span></div>' for i,r in enumerate(rs))+'</div></div>'
    return page(f""".grid{{position:absolute;left:40px;top:232px;width:1000px;display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.sec{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.05);padding:10px 10px 12px}}
.sh{{font-family:'Barlow Condensed';font-weight:800;font-size:22px;letter-spacing:2px;text-transform:uppercase;color:{RED};padding:0 4px 8px}}
.row{{display:flex;gap:6px}}
.tm{{flex:1;min-width:0;text-align:center;border-radius:10px;padding:8px 4px 6px;background:#f6f6f6;position:relative}}.tm.q{{background:#fff3f3;box-shadow:inset 0 0 0 2px {RED}}}
.pos{{position:absolute;left:6px;top:6px;font-family:'Barlow Condensed';font-weight:800;font-size:16px;color:#9a9a9a}}.tm.q .pos{{color:{RED}}}
.tm img{{width:44px;height:44px;object-fit:contain;margin:0 auto 4px}}
.n{{display:block;font-weight:700;font-size:11px;line-height:1.05;height:24px;overflow:hidden}}
.pts{{display:block;font-family:'Barlow Condensed';font-weight:800;font-size:26px;line-height:1;margin-top:4px}}.pts small{{font-family:Barlow;font-size:9px;letter-spacing:1px;color:#9a9a9a;margin-left:2px}}
.dg{{display:block;font-size:9.5px;color:#9a9a9a;font-weight:600;letter-spacing:.5px;margin-top:2px}}
</style>""",f'<div class="grid">{secs}</div>',sub())
render('KC5_horitzontal_8',kc5(grups))
# KC6 · una columna, 8 grups en 2 imatges, files estil resultats (només nom, PJ, DG, PTS) amb franja i zona tintada
def kc6(gs):
    secs=''
    for g,rs in gs:
        secs+=f'<div class="sh">{g}</div>'+''.join(f'<div class="r{" q" if i<2 else ""}"><b class="pos">{i+1}</b><img src="{r["lg"]}"><span class="n">{r["n"]}</span>{forma(r["forma"],12)}<span class="st">{r["pj"]}<small>PJ</small></span><span class="st">{r["dg"]:+d}<small>DG</small></span><b class="pts">{r["pts"]}</b></div>' for i,r in enumerate(rs))
    return page(f""".wrap{{position:absolute;left:40px;top:232px;width:1000px;display:flex;flex-direction:column;gap:6px}}
.sh{{font-family:'Barlow Condensed';font-weight:800;font-size:24px;letter-spacing:3px;text-transform:uppercase;color:#fff;background:{RED};display:inline-block;align-self:flex-start;padding:2px 14px;border-radius:6px;margin-top:8px}}
.r{{height:46px;background:#fff;border-radius:8px;border-left:8px solid #ddd;display:grid;grid-template-columns:36px 34px 1fr 90px 56px 60px 64px;align-items:center;gap:8px;padding:0 14px 0 8px;box-shadow:0 1px 4px rgba(0,0,0,.05)}}
.r.q{{border-left-color:{RED}}}
.r img{{width:30px;height:30px;object-fit:contain}}.r .n{{font-weight:700;font-size:16px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.pos{{font-family:'Barlow Condensed';font-weight:800;font-size:22px;text-align:center;color:#9a9a9a}}.r.q .pos{{color:{RED}}}
.fm{{display:flex;gap:4px;justify-content:center}}.fm i{{border-radius:50%;display:block}}
.st{{text-align:center;font-family:'Barlow Condensed';font-weight:700;font-size:19px;line-height:1}}.st small{{font-family:Barlow;font-size:9px;letter-spacing:1px;color:#9a9a9a;margin-left:3px}}
.pts{{font-family:'Barlow Condensed';font-weight:800;font-size:26px;text-align:right}}
</style>""",f'<div class="wrap">{secs}</div>',sub())
render('KC6_columna_4',kc6(grups[:4]))
