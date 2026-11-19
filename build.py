import json, html
d=json.load(open('data.json')); e=html.escape
P=d['projects']; G=d['groups']
def ul(items): return '<ul>'+''.join(f'<li>{e(i)}</li>' for i in items)+'</ul>'
def card(p):
    cls='card featured' if p.get('featured') else 'card'
    date=f'<span class="date">{e(p["date"])}</span>' if p.get('date') else ''
    return f'''<a class="{cls}" href="#/p/{p['id']}"><div class="ctop"><span class="area">{e(p['area'])}</span>{date}</div>
<h3>{e(p['title'])}</h3><p>{e(p['highlight'])}</p><span class="more">View details <i>&rarr;</i></span></a>'''
home=''
for gi,g in enumerate(G):
    cs=''.join(card(p) for p in P if p['g']==gi)
    home+=f'<section class="group"><h2>{e(g["title"])}</h2><p class="blurb">{e(g["blurb"])}</p><div class="grid">{cs}</div></section>\n'
def detail(i,p):
    fig=''.join(f'<img src="{e(x)}" alt="{e(p["title"])}">' for x in p.get('images',[]))
    figs=f'<div class="figs">{fig}</div>' if fig else ''
    extra=''
    if p.get('extra'): extra=f'<h4>{e(p["extra"][0])}</h4>'+ul(p['extra'][1])
    code=f'<a class="btn" href="{e(p["repo"])}">Code on GitHub</a>' if p.get('repo') else ''
    prev=P[i-1] if i>0 else None; nxt=P[i+1] if i<len(P)-1 else None
    pn=''
    pn+=f'<a href="#/p/{prev["id"]}">&larr; {e(prev["title"])}</a>' if prev else '<span></span>'
    pn+=f'<a href="#/p/{nxt["id"]}">{e(nxt["title"])} &rarr;</a>' if nxt else '<span></span>'
    return f'''<article class="detail" id="p-{p['id']}" hidden>
<a class="back" href="#/">&larr; Back to all projects</a>
<p class="area">{e(G[p['g']]['title'])}</p><h1>{e(p['title'])}</h1><p class="meta">{e(p['meta'])}</p>
{figs}
<h4>Overview</h4><p>{e(p['overview'])}</p>
<h4>What I built and did</h4>{ul(p['did'])}
<h4>Results and impact</h4>{ul(p['results'])}
{extra}
<p class="skills"><span>Skills and tools</span> {e(p['skills'])}</p>{code}
<div class="pn">{pn}</div>
<a class="back bottom" href="#/">&larr; Back to all projects</a></article>'''
details='\n'.join(detail(i,p) for i,p in enumerate(P))
themes=''.join(f'<div class="theme"><h4>{e(a)}</h4><p>{e(b)}</p></div>' for a,b in d['themes'])
page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ethan Liu | Project Portfolio</title>
<meta name="description" content="Hardware and IC design project portfolio of Ethan Liu, Carnegie Mellon ECE.">
<link rel="stylesheet" href="style.css"></head><body>
<nav><a href="#/" class="brand">Ethan Liu</a><div><a href="#/">Projects</a><a href="{e(d['github'])}">GitHub</a><a href="{e(d['linkedin'])}">LinkedIn</a></div></nav>
<main>
<div id="home">
<section class="hero"><p class="eyebrow">{e(d['eyebrow'])}</p><h1>{e(d['name'])}</h1><p class="lead">{e(d['tagline'])}</p>
<p class="links"><a class="btn" href="#projects">View projects</a><a class="btn ghost" href="mailto:{e(d['email'])}">Email</a></p></section>
<div id="projects">{home}</div>
<section class="group"><h2>Themes across my work</h2><div class="themes">{themes}</div><h4>Areas of interest</h4><p class="blurb">{e(d['interest'])}</p></section>
<section class="group" id="contact"><h2>Contact</h2><p class="blurb"><a href="mailto:{e(d['email'])}">{e(d['email'])}</a> &middot; <a href="{e(d['linkedin'])}">LinkedIn</a> &middot; <a href="{e(d['github'])}">GitHub</a></p></section>
</div>
{details}
</main><footer>Ethan Liu</footer>
<script>
const home=document.getElementById('home'),details=[...document.querySelectorAll('.detail')];
function route(){{
 const m=location.hash.match(/^#\\/p\\/([\\w-]+)/);
 let t=m&&document.getElementById('p-'+m[1]);
 home.hidden=!!t;details.forEach(x=>x.hidden=x!==t);
 if(t){{document.title=t.querySelector('h1').textContent+' | Ethan Liu';window.scrollTo(0,0);}}
 else{{document.title='Ethan Liu | Project Portfolio';}}
}}
window.addEventListener('hashchange',()=>{{ if(location.hash==='#projects'){{home.hidden=false;details.forEach(x=>x.hidden=true);document.getElementById('projects').scrollIntoView();return;}} route();}});
if(history.scrollRestoration)history.scrollRestoration='manual';
route();
</script></body></html>'''
open('index.html','w').write(page)
