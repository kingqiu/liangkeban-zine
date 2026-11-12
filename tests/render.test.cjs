const {test}=require('node:test');const assert=require('node:assert/strict');
const {scaleValue,within,safeOutput}=require('../scripts/render.cjs');
test('scale guard',()=>{for(const n of [0,-1,5,NaN,Infinity,'bad'])assert.throws(()=>scaleValue(n));assert.equal(scaleValue(2),2)});
test('resource containment',()=>{assert(within('/tmp/z/a.png','/tmp/z'));assert(!within('/tmp/z-other/a.png','/tmp/z'));assert(!within('/tmp/a.png','/tmp/z'))});

const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
test('output symlink guard',()=>{const root=fs.mkdtempSync(path.join(os.tmpdir(),'zine-test-'));try{const outside=path.join(root,'other');fs.mkdirSync(outside);const link=path.join(root,'qa-phone');fs.symlinkSync(outside,link);assert.throws(()=>safeOutput(path.join(link,'a.png'),root),/symlinks/);assert.equal(safeOutput(path.join(root,'fresh.png'),root),path.join(root,'fresh.png'));fs.symlinkSync(path.join(root,'missing'),path.join(root,'broken.png'));assert.throws(()=>safeOutput(path.join(root,'broken.png'),root),/symlinks/)}finally{fs.rmSync(root,{recursive:true,force:true})}});
