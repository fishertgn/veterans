#!/usr/bin/env python3
import os, io, sys
sys.stdout=io.StringIO(); import resultats_a as A; sys.stdout=sys.__stdout__
build,wl,col,RED=A.build,A.wl,A.col,A.RED
# a · número del guanyador en color de la competició, perdedor en gris
def a(r):
    w=wl(r); c=col(r); g='#9a9a9a'
    return f'<span class="sc"><b style="color:{c if w[0]=="w" else (g if w[0]=="lo" else "#151515")}">{r["hs"]}</b><i></i><b style="color:{c if w[1]=="w" else (g if w[1]=="lo" else "#151515")}">{r["as"]}</b></span>'
build('RA2a_guanyador',".sc{gap:12px;font-size:48px}.sc i{width:12px;height:5px;background:#ccc;display:block}",a)
# b · números més grans, separador vertical del color de la competició
build('RA2b_gran',".sc{gap:16px;font-size:58px;color:#151515}.sc i{width:4px;height:44px;display:block;border-radius:2px}",
      lambda r:f'<span class="sc"><b>{r["hs"]}</b><i style="background:{col(r)}"></i><b>{r["as"]}</b></span>')
# c · números negres, subratllat de color sota el guanyador
def c_(r):
    w=wl(r); c=col(r)
    def n(v,st): return f'<b style="border-bottom:5px solid {c if st=="w" else "transparent"};padding-bottom:2px">{v}</b>'
    return f'<span class="sc">{n(r["hs"],w[0])}<i></i>{n(r["as"],w[1])}</span>'
build('RA2c_subratllat',".sc{gap:12px;font-size:48px;color:#151515}.sc i{width:12px;height:5px;background:"+RED+";display:block;margin-bottom:6px}",c_)
# d · tots dos números en color de la competició, guió gris
build('RA2d_color',".sc{gap:12px;font-size:48px}.sc i{width:12px;height:5px;background:#ccc;display:block}",
      lambda r:f'<span class="sc" style="color:{col(r)}"><b>{r["hs"]}</b><i></i><b>{r["as"]}</b></span>')
