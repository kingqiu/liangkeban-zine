import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build',ROOT/'scripts/build.py')
build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
DATA=json.loads((ROOT/'assets/example.json').read_text())
class BuildTests(unittest.TestCase):
 def test_escape(self):
  d=copy.deepcopy(DATA);d['pages'][0]['title']='<script>x</script>\n&'
  s=build.page_html(build.validate(d),d['pages'][0],1)
  self.assertNotIn('<script>',s);self.assertIn('&lt;script&gt;',s);self.assertIn('<br>&amp;',s)
 def test_fields(self):
  for color in range(6):
   d=copy.deepcopy(DATA);p=d['pages'][0];p.update(checktitle='Check',checks=[['A','B']])
   p['blocks'][0].update(color=color,panel='Panel',rows=[['Label','Value']])
   s=build.page_html(build.validate(d),p,1)
   for token in [f'block c{color}','panel-row','checktitle']:self.assertIn(token,s)
 def test_invalid(self):
  for key,value in [('color',True),('color',6),('kind','bad'),('paras','bad'),('rows',[['one']])]:
   d=copy.deepcopy(DATA);d['pages'][0]['blocks'][0][key]=value
   with self.assertRaises(ValueError):build.validate(d)
 def test_fresh_directory(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'output';self.assertGreater(build.build(ROOT/'assets/example.json',out),0)
   with self.assertRaises(ValueError):build.build(ROOT/'assets/example.json',out)
