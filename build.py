import json, html, os
d=json.load(open('data.json')); e=html.escape
P=d['projects']; G=d['groups']
S=lambda b:f'<svg viewBox="0 0 48 48" width="44" height="44" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{b}</svg>'
ICON={
 'chip':S('<rect x="12" y="12" width="24" height="24" rx="3"/><rect x="19" y="19" width="10" height="10"/><path d="M18 6v6M24 6v6M30 6v6M18 36v6M24 36v6M30 36v6M6 18h6M6 24h6M6 30h6M36 18h6M36 24h6M36 30h6"/>'),
 'wave':S('<path d="M4 24h6l4-12 6 24 6-24 4 12h14"/>'),
 'nodes':S('<circle cx="10" cy="12" r="4"/><circle cx="38" cy="12" r="4"/><circle cx="24" cy="38" r="4"/><path d="M14 12h20M12 16l10 18M36 16L26 34"/>'),
 'board':S('<rect x="6" y="10" width="36" height="28" rx="3"/><circle cx="15" cy="19" r="2"/><circle cx="33" cy="29" r="2"/><path d="M17 19h8v10h8"/>'),
 'grid':S('<rect x="8" y="8" width="14" height="14"/><rect x="26" y="8" width="14" height="14"/><rect x="8" y="26" width="14" height="14"/><rect x="26" y="26" width="14" height="14"/>'),
 'code':S('<path d="M17 14L7 24l10 10M31 14l10 10-10 10M27 10L21 38"/>'),
 'bolt':S('<path d="M27 5L10 27h12l-3 16 19-24H26z"/>'),
 'shield':S('<path d="M24 5l16 6v12c0 10-7 17-16 20C15 40 8 33 8 23V11z"/><path d="M16 24l6 6 11-12"/>'),
 'radio':S('<circle cx="24" cy="26" r="4"/><path d="M14 16a14 14 0 000 20M34 16a14 14 0 010 20M8 10a22 22 0 000 32M40 10a22 22 0 010 32"/>'),
 'gear':S('<circle cx="24" cy="24" r="7"/><path d="M24 4v6M24 38v6M4 24h6M38 24h6M10 10l4 4M34 34l4 4M38 10l-4 4M14 34l-4 4"/>'),
 'stack':S('<path d="M24 6l18 9-18 9-18-9z"/><path d="M6 24l18 9 18-9M6 33l18 9 18-9"/>'),
}
IC={'sram':'chip','rtl2gds':'wave','innovus':'grid','datapath':'wave','abv':'shield','noc':'nodes','risc240':'chip','matmul':'grid','mastermind':'gear','harness':'board','fsae':'bolt','rfid':'radio','guitar':'gear','cache':'stack','fight':'code','c0vm':'code'}
STAT={'sram':('4 Kb','DRC/LVS-clean SRAM in 45 nm'),'rtl2gds':('10 to 200 MHz','MAC unit pushed and measured'),'abv':('7 of 7','injected faults detected')}
FEAT=['sram','rtl2gds','abv']; CLS=['green','purple','blue']
byid={p['id']:p for p in P}
def ul(items): return '<ul>'+''.join(f'<li>{e(i)}</li>' for i in items)+'</ul>'
def fcard(pid,c):
    p=byid[pid]; big,small=STAT[pid]
    thumb=f'<img src="{e(p["images"][0])}" alt="">' if p.get('images') else f'<div class="stat"><b>{e(big)}</b><span>{e(small)}</span></div>'
    return f'<a class="fcard {c}" href="#/p/{pid}"><div class="thumb">{thumb}</div><div class="ftxt"><h3>{e(p["title"])}</h3><p>{e(p["area"])}</p></div></a>'
def card(p):
    return f'<a class="pcard" href="#/p/{p["id"]}"><span class="ic">{ICON[IC[p["id"]]]}</span><h3>{e(p["title"])}</h3><p class="area">{e(p["area"])}</p><p class="hl">{e(p["highlight"])}</p></a>'
groups=''
for gi,g in enumerate(G):
    groups+=f'<h3 class="gh">{e(g["title"])}</h3><div class="pgrid">'+''.join(card(p) for p in P if p['g']==gi)+'</div>'
def detail(i,p):
    fig=''.join(f'<img src="{e(x)}" alt="{e(p["title"])}">' for x in p.get('images',[]))
    figs=f'<div class="figs">{fig}</div>' if fig else ''
    extra=f'<h2>{e(p["extra"][0])}</h2>'+ul(p['extra'][1]) if p.get('extra') else ''
    code=f'<a class="btn" href="{e(p["repo"])}">Code on GitHub</a>' if p.get('repo') else ''
    prev=P[i-1] if i>0 else None; nxt=P[i+1] if i<len(P)-1 else None
    pn=(f'<a href="#/p/{prev["id"]}">&larr; {e(prev["title"])}</a>' if prev else '<span></span>')+(f'<a href="#/p/{nxt["id"]}">{e(nxt["title"])} &rarr;</a>' if nxt else '<span></span>')
    return f'''<article class="detail" id="p-{p['id']}" hidden><div class="wrap narrow">
<a class="back" href="#/">&larr; Back to all projects</a>
<p class="kicker">{e(G[p['g']]['title'])}</p><h1>{e(p['title'])}</h1><p class="meta">{e(p['meta'])}</p>{figs}
<h2>Overview</h2><p>{e(p['overview'])}</p>
<h2>What I built and did</h2>{ul(p['did'])}
<h2>Results and impact</h2>{ul(p['results'])}
{extra}
<p class="skills"><span>Skills and tools</span> {e(p['skills'])}</p>{code}
<div class="pn">{pn}</div><a class="back" href="#/">&larr; Back to all projects</a></div></article>'''
details='\n'.join(detail(i,p) for i,p in enumerate(P))
themes=''.join(f'<div class="theme"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a,b in d['themes'])
photo='img/photo.jpg'
avatar=f'<img src="{photo}" alt="Ethan Liu">' if os.path.exists(photo) else '<span>EL</span>'
nav=lambda:f'<a class="logo" href="#/">EL</a><div class="links"><a class="ul" href="#projects">Projects</a><a class="ul" href="#about">About</a><a class="ul" href="#contact">Contact</a></div><a class="cta" href="mailto:{e(d["email"])}">Contact Me</a>'
page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ethan Liu | Project Portfolio</title>
<meta name="description" content="Hardware and IC design project portfolio of Ethan Liu, Carnegie Mellon ECE.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v=3"></head><body>
<div class="topbar"></div>
<header id="nav"><div class="wrap navin">{nav()}</div></header>
<main>
<div id="home">
<section class="hero wrap"><div class="avatar">{avatar}</div>
<p class="eyebrow">{e(d['eyebrow'])}</p>
<h1 class="big">Hey, I'm <em>Ethan Liu.</em> Here, you can check out what I'm building: chips, circuits, and the code around them. I try my best to measure before I trust.</h1>
<p class="sub">{e(d['tagline'])}</p></section>
<section class="featured"><div class="wrap"><h2 class="sec light">Featured Work</h2><div class="fgrid">{''.join(fcard(i,c) for i,c in zip(FEAT,CLS))}</div></div></section>
<section class="wrap" id="projects"><h2 class="sec">My Projects</h2><p class="lede">Every project below opens into the full story: the problem, what I built, how I approached it, and what I measured.</p>{groups}</section>
<section class="wrap" id="about"><h2 class="sec">How I Work</h2><div class="themes">{themes}</div><p class="lede mt">{e(d['interest'])}</p></section>
<section class="wrap" id="contact"><h2 class="sec">Contact</h2><p class="lede"><a class="ul" href="mailto:{e(d['email'])}">{e(d['email'])}</a> &nbsp; <a class="ul" href="{e(d['linkedin'])}">LinkedIn</a> &nbsp; <a class="ul" href="{e(d['github'])}">GitHub</a></p></section>
</div>
{details}
</main>
<footer><div class="wrap navin">{nav()}</div><p class="copy">&copy; Ethan Liu</p></footer>
<script>
const home=document.getElementById('home'),details=[...document.querySelectorAll('.detail')],nav=document.getElementById('nav');
function route(){{
 const m=location.hash.match(/^#\\/p\\/([\\w-]+)/);const t=m&&document.getElementById('p-'+m[1]);
 home.hidden=!!t;details.forEach(x=>x.hidden=x!==t);
 if(t){{document.title=t.querySelector('h1').textContent+' | Ethan Liu';window.scrollTo({{top:0,behavior:'instant'}});}}else document.title='Ethan Liu | Project Portfolio';
}}
window.addEventListener('hashchange',()=>{{
 const h=location.hash;
 if(['#projects','#about','#contact'].includes(h)){{home.hidden=false;details.forEach(x=>x.hidden=true);document.title='Ethan Liu | Project Portfolio';document.querySelector(h).scrollIntoView();return;}}
 route();}});
window.addEventListener('scroll',()=>nav.classList.toggle('stuck',window.scrollY>60),{{passive:true}});
route();
</script></body></html>'''
open('index.html','w').write(page)
