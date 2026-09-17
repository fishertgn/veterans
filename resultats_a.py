#!/usr/bin/env python3
import os, io, sys
sys.stdout=io.StringIO(); import resultats_opcions as R; sys.stdout=sys.__stdout__
rows,col,pill,dia,wl,page,RED,V,P=R.rows,R.col,R.pill,R.dia,R.wl,R.page,R.RED,R.V,R.P
BASE=f""".r{{height:78px;background:#fff;border-radius:12px;border-left:10px solid #999;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:64px 1fr 150px 1fr 128px;align-items:center;gap:8px;padding:0 14px 0 12px}}
.dd{{font-family:'Barlow Condensed';font-weight:700;font-size:20px;color:#9a9a9a;text-transform:uppercase}}
.t{{display:flex;align-items:center;gap:8px;font-weight:600;font-size:16px;line-height:1.05;min-width:0;color:#777}}.t.w{{color:#111;font-weight:700}}.t.l{{justify-content:flex-end;text-align:right}}.t img{{width:40px;height:40px;object-fit:contain;flex:none}}
.g{{font-weight:700;font-size:11.5px;letter-spacing:1.2px;border:2px solid;border-radius:999px;padding:4px 8px;text-transform:uppercase;text-align:center;white-space:nowrap}}
.sc{{display:flex;justify-content:center;align-items:center;font-family:'Barlow Condensed';font-weight:800;line-height:1}}"""
def rowhtml(r,sc):
    return f'<div class="r" style="border-left-color:{col(r)}"><span class="dd">{dia(r)}</span><span class="t l {wl(r)[0]}"><span>{r["h"]}</span><img src="{r["hl"]}"></span>{sc}<span class="t {wl(r)[1]}"><img src="{r["al"]}"><span>{r["a"]}</span></span><span class="g" style="color:{col(r)};border-color:{col(r)}">{pill(r)}</span></div>'
def build(name,css,scfn):
    html=page(BASE+css,'<div class="list">'+''.join(rowhtml(r,scfn(r)) for r in rows)+'</div>')
    png=os.path.join(V,'out',f'{name}.png'); P.render(html,png); print(png)
# A1 · caixa del color de la competició
build('RA1_color',".sc{gap:8px;height:46px;border-radius:8px;color:#fff;font-size:34px}.sc i{font-style:normal;opacity:.75;font-size:24px}",
      lambda r:f'<span class="sc" style="background:{col(r)}"><b>{r["hs"]}</b><i>-</i><b>{r["as"]}</b></span>')
# A2 · sense caixa, números grans i guió vermell
build('RA2_net',".sc{gap:12px;font-size:48px;color:#151515}.sc i{width:12px;height:5px;background:"+RED+";display:block}",
      lambda r:f'<span class="sc"><b>{r["hs"]}</b><i></i><b>{r["as"]}</b></span>')
# A3 · caixa gris clar, números foscos, guió de color
build('RA3_suau',".sc{gap:8px;height:46px;border-radius:8px;background:#f2f2f2;color:#151515;font-size:34px}.sc i{font-style:normal;font-size:24px}",
      lambda r:f'<span class="sc"><b>{r["hs"]}</b><i style="color:{col(r)}">-</i><b>{r["as"]}</b></span>')
# A4 · dos quadrats, el del guanyador ple de color
def a4(r):
    w=wl(r); c=col(r)
    def box(n,st): return f'<b style="{ "background:"+c+";color:#fff;border-color:"+c if st=="w" else "background:#fff;color:#151515;border-color:#ddd"}">{n}</b>'
    return f'<span class="sc">{box(r["hs"],w[0])}<i></i>{box(r["as"],w[1])}</span>'
build('RA4_quadrats',".sc{gap:6px;font-size:30px}.sc b{width:46px;height:46px;border-radius:8px;border:2px solid;display:flex;align-items:center;justify-content:center}.sc i{width:8px;height:3px;background:#ccc;display:block}",a4)
# A5 · caixa blanca amb vora de color, número del guanyador en color
def a5(r):
    w=wl(r); c=col(r)
    return f'<span class="sc" style="border-color:{c}"><b style="color:{c if w[0]=="w" else "#151515"}">{r["hs"]}</b><i>-</i><b style="color:{c if w[1]=="w" else "#151515"}">{r["as"]}</b></span>'
build('RA5_vora',".sc{gap:8px;height:46px;border-radius:8px;border:3px solid;background:#fff;font-size:34px}.sc i{font-style:normal;color:#bbb;font-size:24px}",a5)
