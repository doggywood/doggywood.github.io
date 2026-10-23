# Builds a private, offline copy of the game with Nightcall baked in as the car radio.
# Output goes to the Desktop (outside the repo), so the song is never published.
import base64, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
s = open(os.path.join(root, 'index.html'), encoding='utf8').read()
song = base64.b64encode(open(os.path.join(root, 'music', 'nightcall.mp3'), 'rb').read()).decode()
inj = '''<script>
// Nightcall, baked in. Played at a third of the game's normal music volume.
(()=>{ const b=atob("%s"), u=new Uint8Array(b.length); for(let i=0;i<b.length;i++) u[i]=b.charCodeAt(i); localSongs.push(u.buffer); })();
music.vol = 0.55/3;
$('songbtn').parentNode.style.display='none';
$('musicnote').textContent='Car radio: Kavinsky - Nightcall';
</script>
''' % song
i = s.rindex('</body>')
out = os.path.join(os.path.dirname(root), 'DOGGYWOOD (Nightcall).html')
open(out, 'w', encoding='utf8').write(s[:i] + inj + s[i:])
print(out, os.path.getsize(out) // 1024, 'KB')
