import json, html
d=json.load(open('data.json'))
e=html.escape
tags=[]
for p in d['projects']:
    for t in p['tags']:
        if t not in tags: tags.append(t)
def card(p):
    li=''.join(f'<li>{e(b)}</li>' for b in p['bullets'])
    tg=''.join(f'<span class="tag">{e(t)}</span>' for t in p['tags'])
    ds=' '.join(t.replace(' ','_') for t in p['tags'])
    fig=''.join(f'<img src="{e(i)}" alt="{e(p["title"])}">' for i in p.get('images',[]))
    figs=f'<div class="figs">{fig}</div>' if fig else ''
    link=f'<a class="plink" href="{e(p["repo"])}">Code on GitHub</a>' if p.get('repo') else ''
    cls='card featured' if p.get('featured') else 'card'
    return f'''<article class="{cls}" data-tags="{ds}" id="{p['id']}">
<header><h3>{e(p['title'])}</h3><span class="date">{e(p['date'])}</span></header>
<p class="sub">{e(p['sub'])}</p>{figs}
<ul>{li}</ul>
<p class="skills"><span>Skills used</span> {e(p['skills'])}</p>
<div class="foot">{tg}{link}</div></article>'''
cards='\n'.join(card(p) for p in d['projects'])
filters='<button class="f active" data-f="all">All</button>'+''.join(f'<button class="f" data-f="{t.replace(" ","_")}">{e(t)}</button>' for t in tags)
page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ethan Liu | Project Portfolio</title>
<meta name="description" content="Hardware and IC design project portfolio of Ethan Liu, Carnegie Mellon ECE.">
<link rel="stylesheet" href="style.css"></head><body>
<nav><a href="#top" class="brand">Ethan Liu</a><div><a href="#projects">Projects</a><a href="#contact">Contact</a></div></nav>
<main id="top">
<section class="hero"><p class="eyebrow">Electrical and Computer Engineering, Carnegie Mellon University</p>
<h1>Ethan Liu</h1><p class="lead">{e(d['tagline'])}</p>
<p class="links"><a class="btn" href="#projects">View projects</a><a class="btn ghost" href="{e(d['github'])}">GitHub</a><a class="btn ghost" href="{e(d['linkedin'])}">LinkedIn</a></p></section>
<section id="projects"><h2>Projects</h2><div class="filters">{filters}</div><div class="grid">
{cards}
</div></section>
<section id="contact"><h2>Contact</h2><p><a href="mailto:{e(d['email'])}">{e(d['email'])}</a> &middot; <a href="{e(d['linkedin'])}">LinkedIn</a> &middot; <a href="{e(d['github'])}">GitHub</a></p></section>
</main><footer>Ethan Liu</footer>
<script>
document.querySelectorAll('.f').forEach(b=>b.addEventListener('click',()=>{{
 document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));b.classList.add('active');
 const f=b.dataset.f;document.querySelectorAll('.card').forEach(c=>{{c.hidden=!(f==='all'||c.dataset.tags.split(' ').includes(f));}});
}}));
</script></body></html>'''
open('index.html','w').write(page)
