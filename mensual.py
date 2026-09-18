#!/usr/bin/env python3
"""Resum mensual: equip del mes, millor atac, millor defensa, golejada i partit amb més gols.
Post 1080x1350 i història 1080x1920. Ús: mensual.py AAAA-MM [--test] [--send]   (--test = lligues 25-26)"""
import os, sys, calendar, datetime, collections
import proxims as P
V,RED=P.V,P.RED
MESOS=['GENER','FEBRER','MARÇ','ABRIL','MAIG','JUNY','JULIOL','AGOST','SETEMBRE','OCTUBRE','NOVEMBRE','DESEMBRE']
def calcula(any_,mes,ids=None):
    d0=datetime.date(any_,mes,1); d1=datetime.date(any_,mes,calendar.monthrange(any_,mes)[1])
    rows=[r for r in P.partits(d0,d1,jugats=True,ids=ids)]
    if len(rows)<4: return None
    eq=collections.defaultdict(lambda:dict(pj=0,pts=0,gf=0,gc=0,g=0,lg='',comp=''))
    for r in rows:
        for n,lg,f,c in ((r['h'],r['hl'],r['hs'],r['as_']),(r['a'],r['al'],r['as_'],r['hs'])):
            e=eq[n]; e['pj']+=1; e['gf']+=f; e['gc']+=c; e['lg']=lg; e['comp']=r['comp']
            if f>c: e['pts']+=3; e['g']+=1
            elif f==c: e['pts']+=1
    mx=max(e['pj'] for e in eq.values()); prou={n:e for n,e in eq.items() if e['pj']>=max(2,mx-1)} or eq
    top=lambda d,k: sorted(d.items(),key=k)[0]
    crit=lambda x:(-x[1]['pts']/x[1]['pj'],-(x[1]['gf']-x[1]['gc']),-x[1]['gf'])
    equips=[]
    for comp in sorted({e['comp'] for e in prou.values()},key=lambda c:(c!='LLIGA 1A',c!='LLIGA 2A',c!='LLIGA 3A',c)):
        equips.append((comp,top({n:e for n,e in prou.items() if e['comp']==comp},crit)))
    equip=equips[0][1]
    atac=top(prou,lambda x:(-x[1]['gf']/x[1]['pj'],-x[1]['gf']))
    defensa=top(prou,lambda x:(x[1]['gc']/x[1]['pj'],x[1]['gc']))
    golejada=max(rows,key=lambda r:(abs(r['hs']-r['as_']),r['hs']+r['as_']))
    festa=max(rows,key=lambda r:(r['hs']+r['as_'],-abs(r['hs']-r['as_'])))
    return dict(equips=equips,n=len(rows),gols=sum(r['hs']+r['as_'] for r in rows),equip=equip,atac=atac,defensa=defensa,golejada=golejada,festa=festa)
def contingut(d,alt):
    n=len(d['equips'])+3; k=min(1.25,(alt-40-14*n)/(158*n)); px=lambda v:int(v*k)
    def eq(tag,col,x,xifra,unitat,detall):
        n,e=x; return f'<div class="c" style="border-left-color:{col}"><img src="{e["lg"]}"><div class="m"><small style="color:{col}">{tag}</small><b>{n}</b><span>{detall}</span></div><div class="v" style="color:{col}">{xifra}<small>{unitat}</small></div></div>'
    def pt(tag,col,r,detall):
        return f'<div class="c" style="border-left-color:{col}"><div class="dos"><img src="{r["hl"]}"><img src="{r["al"]}"></div><div class="m pt"><small style="color:{col}">{tag}</small><b>{r["h"]} – {r["a"]}</b><span>{detall}</span></div><div class="v" style="color:{col}">{r["hs"]}-{r["as_"]}</div></div>'
    a=d['atac'][1]; f=d['defensa'][1]; g=d['golejada']; cos=''
    for comp,x in d['equips']:
        e=x[1]; nomc={'COPA':'Copa'}.get(comp,comp.replace('LLIGA ','').replace('A','a')+' Divisió')
        cos+=eq(f'Equip del mes · {nomc}',P.COLORS.get(comp,'#1a9c5b'),x,e['pts'],'punts',f"{e['g']} victòries en {e['pj']} partits · {e['gf']}-{e['gc']} en gols")
    cos+=(eq('Millor atac del mes','#151515',d['atac'],a['gf'],'gols',f"{a['gf']/a['pj']:.1f} per partit en {a['pj']} partits")
        +eq('Millor defensa del mes','#151515',d['defensa'],f['gc'],'encaixats',f"{f['gc']/f['pj']:.1f} per partit en {f['pj']} partits")
        +pt('Golejada del mes','#8e44ad',g,f"{g['dt'].day} {P.MES[g['dt'].month-1].lower()} · {g['comp']}")
        +f'<div class="tot"><b>{d["n"]}</b> partits · <b>{d["gols"]}</b> gols · <b>{d["gols"]/d["n"]:.1f}</b> per partit</div>')
    css=f""".c{{flex:none;height:{px(158)}px;background:#fff;border-radius:{px(14)}px;border-left:{px(12)}px solid #999;box-shadow:0 2px 8px rgba(0,0,0,.05);display:grid;grid-template-columns:{px(120)}px 1fr auto;align-items:center;gap:{px(16)}px;padding:0 {px(26)}px 0 {px(18)}px}}
.c>img{{width:{px(104)}px;height:{px(104)}px;object-fit:contain}}.dos{{display:flex;flex-direction:column;gap:{px(6)}px;align-items:center}}.dos img{{width:{px(62)}px;height:{px(62)}px;object-fit:contain}}
.m{{min-width:0}}.m small{{display:block;font-family:'Barlow Condensed';font-weight:700;font-size:{px(22)}px;letter-spacing:{px(3)}px;text-transform:uppercase}}
.m b{{display:block;font-family:'Barlow Condensed';font-weight:700;font-size:{px(36)}px;line-height:1.02;text-transform:uppercase;margin:{px(2)}px 0 {px(4)}px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.m span{{display:block;font-weight:500;font-size:{px(16)}px;color:#777}}
.m.pt b{{white-space:normal;font-size:{px(25)}px;line-height:1.05}}
.v{{font-family:'Barlow Condensed';font-weight:700;font-size:{px(78)}px;line-height:.9;text-align:right;white-space:nowrap}}.v small{{display:block;font-family:Barlow;font-weight:700;font-size:{px(12)}px;letter-spacing:{px(2)}px;color:#9a9a9a;text-transform:uppercase}}
.tot{{flex:none;text-align:center;font-weight:500;font-size:{px(20)}px;color:#777;padding-top:{px(6)}px}}.tot b{{font-family:'Barlow Condensed';font-weight:700;font-size:{px(28)}px;color:#151515}}"""
    return css,cos
def generar(any_,mes,outdir,ids=None):
    d=calcula(any_,mes,ids)
    if not d: return [],None
    sub=f'{MESOS[mes-1]} {any_}'; dia=datetime.date(any_,mes,1); out=[]
    nom=lambda f: os.path.join(outdir,f'RESUM MENSUAL {mes:02d}.{any_} {f}.png')
    css,cos=contingut(d,1040); png=nom('POST'); tmp=png[:-4]+'.html'; open(tmp,'w').write(P.post_shell('El resum del mes',sub,cos,css+'.cos{gap:14px}',peu='Dades oficials de Minifutbol Tarragonès')); P.captura(tmp,png,1080,1350); out.append(('POST · Resum mensual '+sub.title(),png))
    css,cos=contingut(d,1270); png=nom('HISTORIA'); P.render_story(P.story_shell('El resum del mes',sub,cos,css+'.sheet{gap:14px}'),png); out.append(('HISTÒRIA · Resum mensual '+sub.title(),png))
    return out,d
def peu(d,any_,mes):
    import peus as PE
    a,f=d['atac'],d['defensa']; g=d['golejada']
    eqs='\n'.join(f"🥇 Equip del mes ({c}): {x[0]} · {x[1]['pts']} punts en {x[1]['pj']} partits" for c,x in d['equips'])
    cos=(f"📆 EL RESUM DEL MES · {MESOS[mes-1].title()} {any_}\n\n{eqs}\n⚽ Millor atac: {a[0]} ({a[1]['gf']} gols)\n🧤 Millor defensa: {f[0]} ({f[1]['gc']} encaixats)\n"
         f"💥 Golejada: {g['h']} {g['hs']}-{g['as_']} {g['a']}\n\n{d['n']} partits i {d['gols']} gols aquest mes.")
    return PE._tanca(cos,[x[0] for c,x in d['equips']]+[a[0],f[0],g['h'],g['a']],'Hi estàs d\'acord? 👇')
if __name__=='__main__':
    a,m=map(int,sys.argv[1].split('-')); out=os.path.join(V,'out'); os.makedirs(out,exist_ok=True)
    res,d=generar(a,m,out,[102,103,98] if '--test' in sys.argv else None)
    if not res: print('Menys de 4 partits jugats aquest mes: no es genera.')
    for e,p in res: print(e,'->',p)
    if d: print(peu(d,a,m)[:500])
    if '--send' in sys.argv and res:
        import publicar as U
        for e,p in res: U.envia_fitxer(p,e,'mensual')
        U.envia_peu(peu(d,a,m),'mensual','resum mensual')
