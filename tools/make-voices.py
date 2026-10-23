# Records every line of dialogue with natural neural voices (edge-tts) into voice/*.mp3 + voice/lines.json
import re, json, os, subprocess, sys, hashlib
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(os.path.join(root,'index.html'),encoding='utf8').read()
BS=chr(92)
def unq(t): return t.replace(BS+"'","'")
PAT=lambda fn: fn+BS+"('((?:[^'"+BS+BS+"]|"+BS+BS+".)*)'"
dale=[unq(m) for m in re.findall(PAT('dale'), s)]
liam=[unq(m) for m in re.findall(PAT('liam'), s)]
teens={w:[unq(m) for m in re.findall(PAT(w), s)] for w in ('teenA','teenB','teenC')}
VO={'dale':('en-US-GuyNeural','-5%','-6Hz'),'liam':('en-US-AndrewNeural','+0%','+0Hz'),'teenA':('en-US-BrianNeural','+6%','+16Hz'),'teenB':('en-US-AvaNeural','+4%','+10Hz'),'teenC':('en-US-ChristopherNeural','+8%','+26Hz')}
out=os.path.join(root,'voice'); os.makedirs(out,exist_ok=True)
man={}
for who,lines in [('dale',dale),('liam',liam)]+list(teens.items()):
  for t in dict.fromkeys(lines):
    if t=='t' or not t.strip(): continue
    fn=who+'_'+hashlib.md5(t.encode()).hexdigest()[:8]+'.mp3'; man[who+'|'+t]=fn
    path=os.path.join(out,fn)
    if os.path.exists(path) and os.path.getsize(path)>2000: continue
    v,rate,pitch=VO[who]
    spoken=t.replace('--','...')
    if spoken.startswith('Mm.'): spoken='Mmmm...'+spoken[3:]   # a hum, not the letters M M
    import time
    for attempt in range(5):
      r=subprocess.run([sys.executable,'-m','edge_tts','--voice',v,'--rate='+rate,'--pitch='+pitch,'--text',spoken,'--write-media',path],capture_output=True,text=True)
      if r.returncode==0 and os.path.exists(path) and os.path.getsize(path)>2000: break
      time.sleep(2+attempt*2)
    print(('ok  ' if r.returncode==0 else 'ERR '+r.stderr.strip().split(chr(10))[-1][:80]+' ')+who+': '+t[:60])
json.dump(man,open(os.path.join(out,'lines.json'),'w',encoding='utf8'),ensure_ascii=False,indent=0)
print(len(man),'lines')
