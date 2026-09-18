#!/usr/bin/env python3
"""Reel de resultats (1080x1920, MP4): els resultats del cap de setmana entren un a un.
Es renderitzen els estats amb Chrome i ffmpeg els munta. Ús: reel.py AAAA-MM-DD AAAA-MM-DD [--test] [--send]"""
import os, sys, shutil, subprocess, datetime, random, tempfile
import proxims as P, resultats as R
V=P.V
T_INTRO,T_FILA,T_FINAL,T_PAUSA=0.9,0.55,2.6,1.2
def ffmpeg(): return shutil.which('ffmpeg')
def generar(d0,d1,outdir,test=False):
    ff=ffmpeg()
    rows=P.partits(d0,d1,jugats=None)
    if test:
        random.seed(7)
        for i,r in enumerate(rows): r['hs'],r['as_']=random.choice([0,1,1,2,2,3,4]),random.choice([0,1,1,2,2,3]); r['status']=1 if i in (2,9) else 5
    if not any(r['status']==5 for r in rows): return []
    tmp=tempfile.mkdtemp(prefix='reel_'); llista=[]; n=0
    dies=sorted({r['dt'].date() for r in rows})
    for dia in dies:
        rs=sorted([r for r in rows if r['dt'].date()==dia],key=lambda r:(r['dt'],r['comp'],r['grup'])); et=f'{P.DIES[dia.weekday()]} {dia.day} {P.MES[dia.month-1]}'
        for pag,tros in enumerate([rs[i:i+12] for i in range(0,len(rs),12)],1):
            base=R.html_story(et,tros,1,1)
            for k in range(len(tros)+1):
                html=base.replace('</style>',f'.sheet .r:nth-child(n+{k+1}){{visibility:hidden}}</style>',1)
                f=os.path.join(tmp,f'f{n:03d}.png'); h=f[:-4]+'.html'; open(h,'w').write(html); P.captura(h,f,1080,1920); n+=1
                dur=T_INTRO if k==0 else (T_FILA if k<len(tros) else (T_FINAL if dia==dies[-1] else T_PAUSA))
                llista.append((f,dur))
    if not ff: print('ffmpeg no disponible: fotogrames a',tmp); return []
    txt=os.path.join(tmp,'llista.txt')
    with open(txt,'w') as o:
        for f,d in llista: o.write(f"file '{f}'\nduration {d}\n")
        o.write(f"file '{llista[-1][0]}'\n")
    mp4=P.nom_fitxer(outdir,'RESULTATS',[r['comp'] for r in rows],dies[0],dies[-1],'REEL')[:-4]+'.mp4'
    r=subprocess.run([ff,'-y','-loglevel','error','-f','concat','-safe','0','-i',txt,'-vf','fps=30,scale=1080:1920,format=yuv420p','-c:v','libx264','-preset','medium','-crf','20','-movflags','+faststart',mp4],capture_output=True,text=True)
    if r.returncode!=0: print('ffmpeg ERROR',r.stderr[-400:]); return []
    shutil.rmtree(tmp,ignore_errors=True)
    return [(f'REEL · Resultats · {sum(d for _,d in llista):.0f} s',mp4)]
if __name__=='__main__':
    d0=datetime.date.fromisoformat(sys.argv[1]); d1=datetime.date.fromisoformat(sys.argv[2]); out=os.path.join(V,'out'); os.makedirs(out,exist_ok=True)
    res=generar(d0,d1,out,test='--test' in sys.argv)
    for e,p in res: print(e,'->',p,os.path.getsize(p)//1024,'KB')
    if '--send' in sys.argv and res:
        import publicar as U
        for e,p in res: print(U.envia_fitxer(p,e+' (prova)' if '--test' in sys.argv else e,'reels'))
