import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build',ROOT/'scripts/build.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
DATA=json.loads((ROOT/'examples/demo/content.json').read_text())
class BuildTests(unittest.TestCase):
 def test_upstream_integrity(self):
  for f in json.loads((ROOT/'references/upstream-manifest.json').read_text())['files']:self.assertEqual(hashlib.sha256((ROOT/f['installed_path']).read_bytes()).hexdigest(),f['sha256'],f['upstream_path'])
 def test_escape(self):self.assertEqual(build.render_node({'tag':'p','children':['<script>x</script>\n&']},set()),'<p>&lt;script&gt;x&lt;/script&gt;<br>&amp;</p>')
 def test_reject_active_input(self):
  for n in [{'tag':'script'},{'tag':'img','attrs':{'src':'https://evil.test/a.png'}},{'tag':'img','attrs':{'src':'assets/../a.png'}},{'tag':'p','attrs':{'onclick':'alert(1)'}},{'tag':'div','attrs':{'style':'background:url(https://evil.test)'}}]:
   with self.assertRaises(ValueError):build.render_node(n,set())
 def test_all_reference_nodes(self):
  assets=set()
  for p in DATA['pages']:
   for n in p['body']:build.render_node(n,assets)
  self.assertEqual(assets,{'assets/demo.png'})
 def test_palettes(self):
  self.assertEqual(build.palette('original'),'')
  rows=json.loads((ROOT/'assets/palettes.json').read_text());self.assertEqual(len(rows),6)
  for p in rows:self.assertIn('--paper:'+p['official']['canvas'],build.palette(p['name']))
  self.assertIn('--onAccent:#0A0A0A;',build.palette('safety-orange'))
  self.assertIn('--accentInk:#2A1E13;',build.palette('kraft-paper'))
  with self.assertRaises(ValueError):build.palette('invented')
 def test_original_byte_equivalence(self):
  with tempfile.TemporaryDirectory() as td:
   a=Path(td)/'a';b=Path(td)/'b';src=ROOT/'source/su-zine/assets/example.json';build.build(src,a,'original');build.upstream.build(src,b)
   for f in b.iterdir():self.assertEqual(f.read_bytes(),(a/f.name).read_bytes())
 def test_magazine_source_footer_and_fresh_output(self):
  with tempfile.TemporaryDirectory() as td:
   td=Path(td);d=copy.deepcopy(DATA);d['pages']=[d['pages'][1]];d['pages'][0]['source']='新来源 · 新文章 · 2030.01';src=td/'input.json';src.write_text(json.dumps(d));out=td/'out';build.build(src,out)
   html=(out/'page-01.html').read_text();self.assertIn('新来源 · 新文章 · 2030.01',html);self.assertIn(build.BRAND,html);self.assertIn(build.LICENSE_URL,html);self.assertTrue((out/'ATTRIBUTION.md').exists())
   footer=html.split('<footer')[1];self.assertEqual(footer.count('<br>'),1);self.assertNotIn('a16z',footer)
   with self.assertRaises(ValueError):build.build(src,out)
 def test_invalid_brand_source(self):
  with tempfile.TemporaryDirectory() as td:
   td=Path(td)
   for key,val in [('brand','两克伴出品'),('source','a\nb')]:
    d=copy.deepcopy(DATA);d['pages']=[d['pages'][1]]
    if key=='brand':d[key]=val
    else:d['pages'][0][key]=val
    src=td/'in.json';src.write_text(json.dumps(d))
    with self.assertRaises(ValueError):build.build(src,td/key)
 def test_original_blocks_in_magazine(self):
  with tempfile.TemporaryDirectory() as td:
   out=Path(td)/'out';d=json.loads((ROOT/'source/su-zine/assets/example.json').read_text());d['brand']=build.BRAND;d['pages'][0]['source']='Su · 示例说明';src=Path(td)/'in.json';src.write_text(json.dumps(d));build.build(src,out,'magazine')
   self.assertIn('upstream-blocks',(out/'page-01.html').read_text())

 def test_empty_or_repeated_intro(self):
  for intro in ['', '同一句话']:
   with tempfile.TemporaryDirectory() as td:
    td=Path(td);d=json.loads((ROOT/'source/su-zine/assets/example.json').read_text());d['brand']=build.BRAND
    for page in d['pages']:page['intro']=intro;page['sub']=intro;page['source']='独立测试来源'
    src=td/'input.json';src.write_text(json.dumps(d));build.build(src,td/'out','magazine')
    for page in (td/'out').glob('page-*.html'):self.assertEqual(page.read_text().count('<h1>'),1)
