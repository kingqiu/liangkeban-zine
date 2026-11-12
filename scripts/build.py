#!/usr/bin/env python3
"""Build su-zine original or Two-Gram Companion magazine cards from structured JSON.
Derived from su-zine by Su (@Sukiea1008), PolyForm Noncommercial 1.0.0.
Local adaptation 2026-11-12. See NOTICE.md and MODIFICATIONS.md.
"""
import argparse, html, importlib.util, json, re, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('su_zine_build',ROOT/'source/su-zine/scripts/build.py')
upstream=importlib.util.module_from_spec(spec);spec.loader.exec_module(upstream)
BRAND='「两克伴」出品'
LICENSE_URL='polyformproject.org/licenses/noncommercial/1.0.0/'
TAGS=set('div span p b strong small em i br h2 h3 aside section img svg circle text line rect path g polyline polygon'.split())
ATTRS=set('class role aria-label alt src viewBox cx cy r x y x1 x2 y1 y2 width height fill stroke stroke-width stroke-dasharray transform text-anchor font-family font-weight font-size d points rx ry opacity style'.split())
VOID={'br','img'}
def esc(s):
 if not isinstance(s,str): raise ValueError('Text must be a string')
 return html.escape(s,quote=True).replace('\n','<br>')
def render_node(n,assets,depth=0):
 if depth>24:raise ValueError('Node tree is too deep')
 if isinstance(n,str):return esc(n)
 if not isinstance(n,dict) or n.get('tag') not in TAGS:raise ValueError('Unsupported node tag')
 t=n['tag']; attrs=n.get('attrs',{});children=n.get('children',[])
 if not isinstance(attrs,dict) or not isinstance(children,list):raise ValueError('Invalid node shape')
 out=[]
 for k,v in attrs.items():
  # HTMLParser normalizes attribute case; restore SVG viewBox.
  if k=='viewbox':k='viewBox'
  if k not in ATTRS or not isinstance(v,str):raise ValueError('Unsupported node attribute: '+k)
  if k=='src':
   if t!='img' or not v.startswith('assets/') or '..' in Path(v).parts or '\\' in v or Path(v).suffix.lower() not in {'.png','.jpg','.jpeg','.webp'}:raise ValueError('Images must be local raster files under assets/')
   assets.add(v)
  elif k=='style':
   for pair in v.split(';'):
    if not pair.strip():continue
    key,sep,val=pair.partition(':')
    if not sep or key.strip() not in {'width','height','background'} or not re.fullmatch(r'(?:[0-9]+(?:\.[0-9]+)?(?:px|%)|#[0-9a-fA-F]{3,8})',val.strip()):raise ValueError('Only numeric geometry and hex backgrounds are allowed in node style')
  elif any(x in v.lower() for x in ['url(','javascript:','data:']):raise ValueError('External/active node value rejected')
  out.append(' '+k+'="'+html.escape(v,quote=True)+'"')
 inner=''.join(render_node(c,assets,depth+1) for c in children)
 if t in VOID and children:raise ValueError('Void element cannot have children')
 return '<'+t+''.join(out)+'>'+('' if t in VOID else inner+'</'+t+'>')
def palette(theme):
 if theme=='original':return ''
 rows=json.loads((ROOT/'assets/palettes.json').read_text())
 found=[p for p in rows if theme in [p['slug'],p['name']]]
 if not found:raise ValueError('Unknown theme: '+theme)
 p=found[0]['colors']
 return ':root{--themeAccent:'+p['accent']+';'+''.join('--'+k+':'+v+';' for k,v in p.items())+'}\n'+(ROOT/'assets/theme.css').read_text()
def module_css():
 s=(ROOT/'source/su-zine/assets/style.css').read_text()
 s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
 return '\n'.join(','.join('.upstream-blocks '+v.strip() for v in selector.split(','))+'{'+body+'}' for selector,body in re.findall(r'([^{}]+)\{([^{}]*)\}',s))+'\n.upstream-blocks p{font-size:32px;line-height:1.6}.upstream-blocks .block{gap:29px}.upstream-blocks .graphic{padding:24px}.upstream-blocks .item{font-size:26px}.upstream-blocks{flex:1}'
def copy_legal(out):
 for name in ['LICENSE','NOTICE.md','LICENSE-SCOPE.md','THIRD-PARTY-NOTICES.md','MODIFICATIONS.md']:
  shutil.copy2(ROOT/name,out/name)
 shutil.copytree(ROOT/'LICENSES',out/'LICENSES')
 (out/'ATTRIBUTION.md').write_text('分享自 Su 𝕏 @Sukiea1008\n\nBased on su-zine: https://github.com/doublesq97-ui/su-zine\nCode/templates: https://polyformproject.org/licenses/noncommercial/1.0.0/\nOriginal documentation/example prose: https://creativecommons.org/licenses/by-nc/4.0/\nModified for 两克伴: branding, compact footers, cover variety, palettes, structured layout and validation.\nThis is noncommercial source-available, not OSI-defined open source. Article and user-input rights are separate.\nDistribute this notice with the image set or include the same attribution in its accompanying caption.\n',encoding='utf-8')
def build(source,out,profile=None,theme=None):
 source=Path(source).resolve();out=Path(out).resolve(); data=json.loads(source.read_text())
 profile=profile or data.get('profile','magazine'); theme=theme or data.get('theme','original')
 if profile not in ['original','magazine']:raise ValueError('profile must be original or magazine')
 if out.exists() and (not out.is_dir() or any(out.iterdir())):raise ValueError('--out must be new or empty')
 extra=palette(theme)
 if profile=='original':
  count=upstream.build(source,out)
  if extra:(out/'style.css').write_text((out/'style.css').read_text()+'\n'+extra)
 else:
  if not isinstance(data,dict) or not isinstance(data.get('pages'),list) or not data['pages']:raise ValueError('pages must be nonempty')
  if data.get('brand',BRAND)!=BRAND:raise ValueError('magazine brand must be exactly '+BRAND)
  series=data.get('series');esc(series)
  documents=[];assets=set()
  for i,p in enumerate(data['pages'],1):
   if not isinstance(p,dict):raise ValueError('page must be an object')
   source_line=p.get('source',data.get('source',''))
   if not isinstance(source_line,str) or not source_line.strip() or '\n' in source_line:raise ValueError('Each footer requires a single nonempty article source line')
   layout=p.get('layout','body')
   if layout not in ['body','cover']:raise ValueError('layout must be body or cover')
   if 'body' in p:
    if not isinstance(p['body'],list):raise ValueError('body must be a node array')
    body=''.join(render_node(n,assets) for n in p['body'])
   else:
    # Compatibility with all four original block types and optional rows/checks.
    q=dict(p);q.setdefault('source',source_line)
    d={'brand':BRAND,'series':series,'pages':[q]};upstream.validate(d)
    u=upstream.page_html(d,q,i)
    # Only reuse blocks/checks/closing, not the original header/footer.
    body='<div class="upstream-blocks">'+u.split('<div class="intro">'+esc(p['intro'])+'</div>',1)[1].split('<footer',1)[0]+'</div>'
   title=esc(p['title']);intro=esc(p['intro']);section=esc(p.get('section',p.get('sub','')))
   body='<main class="sheet'+(' cover' if layout=='cover' else '')+'" data-profile="magazine" data-page="'+str(i)+'"><header class="mast"><span>'+esc(series)+'</span><span class="brand">'+BRAND+'</span></header><div class="section">'+section+'</div><h1>'+title+'</h1><div class="intro">'+intro+'</div><div class="content">'+body+'</div><footer class="footer"><div class="sources"><span class="source-line">'+esc(source_line)+'</span><br><span class="license-line">'+LICENSE_URL+'</span></div><div class="folio">'+f'{i:02}'+'<small> / '+f'{len(data["pages"]):02}'+'</small></div></footer></main>'
   documents.append('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+title+'</title><link rel="stylesheet" href="style.css"></head><body>'+body+'</body></html>')
  for rel in assets:
   a=(source.parent/rel).resolve()
   if not a.is_relative_to(source.parent) or not a.is_file():raise ValueError('Missing asset or asset symlink outside content folder: '+rel)
  out.mkdir(parents=True,exist_ok=True)
  for rel in assets:
   dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source.parent/rel,dst)
  css=(ROOT/'assets/magazine.css').read_text()+'\n'+module_css()+'\n'+(ROOT/'assets/layout.css').read_text()+'\n'+extra
  (out/'style.css').write_text(css)
  for i,s in enumerate(documents,1):(out/f'page-{i:02}.html').write_text(s)
  count=len(documents)
 copy_legal(out)
 shutil.copy2(source,out/'content.json')
 for name in ['sources.md','caption.md']:
  if (source.parent/name).is_file():shutil.copy2(source.parent/name,out/name)
 (out/'build-report.json').write_text(json.dumps({'profile':profile,'theme':theme,'pages':count,'brand':data.get('brand',BRAND),'upstream_commit':'a877f7f76adb64278d22716f31e28138bfc6724c','assets':sorted(assets) if profile=='magazine' else [],'limitations':['Fonts and browser can affect pixel identity.','Theme changes typography/panels/charts, not pixels inside illustration bitmaps.','Sources copied for regression are historical fixtures, not fresh verification.']},ensure_ascii=False,indent=2)+'\n')
 return count
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('content',type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--profile',choices=['original','magazine']);p.add_argument('--theme');a=p.parse_args()
 try:print('Built',build(a.content,a.out,a.profile,a.theme),'pages in',a.out)
 except (ValueError,KeyError,TypeError,OSError) as e:p.exit(2,'build: '+str(e)+'\n')
