const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {execFileSync}=require('node:child_process');
const {render,scaleValue}=require('../scripts/render.cjs');
const root=path.resolve(__dirname,'..');
test('scale validation',()=>{for(const n of [0,-1,5,NaN,Infinity,'bad']) assert.throws(()=>scaleValue(n));assert.equal(scaleValue(2),2)});
test('browser rendering and guards',async()=>{
 const temp=fs.mkdtempSync(path.join(os.tmpdir(),'su-zine-test-'));
 try {
  await assert.rejects(()=>render(temp),/No page/);
  const out=path.join(temp,'out');
  execFileSync('python3',[path.join(root,'scripts/build.py'),path.join(root,'assets/example.json'),'--out',out]);
  const report=await render(out);
  assert.equal(report[0].width,2400);assert.deepEqual(report[0].overflow,[]);
  assert(!fs.readdirSync(out).some(f=>f.endsWith('.pdf')));
  await assert.rejects(()=>render(out),/Existing output/);
  fs.appendFileSync(path.join(out,'style.css'),'\n.sheet{height:10001px}');
  await assert.rejects(()=>render(out,{overwrite:true}),/dimensions/);
  fs.appendFileSync(path.join(out,'style.css'),'\n.sheet{height:auto}.title{width:2000px}');
  await assert.rejects(()=>render(out,{overwrite:true}),/overflow/);
 } finally {fs.rmSync(temp,{recursive:true,force:true})}
});
