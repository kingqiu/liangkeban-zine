#!/usr/bin/env node
'use strict';
// Adapted from su-zine by Su (@Sukiea1008), PolyForm Noncommercial 1.0.0.
const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {chromium}=require('playwright');
function scaleValue(v){const n=Number(v);if(!Number.isFinite(n)||n<.25||n>4)throw Error('scale must be 0.25–4');return n}
function within(p,root){const r=path.relative(root,p);return !r.startsWith('..'+path.sep)&&r!=='..'&&!path.isAbsolute(r)}
function safeOutput(p,root){if(!within(p,root))throw Error('Output escapes directory');let current=p;while(current!==root){if(fs.existsSync(current)||(()=>{try{fs.lstatSync(current);return true}catch{return false}})()){if(fs.lstatSync(current).isSymbolicLink())throw Error('Output symlinks are not allowed: '+current)}const parent=path.dirname(current);if(parent===current)throw Error('Invalid output root');current=parent}return p}
async function render(directory,{scale=1,overwrite=false,phone=true}={}){
 scale=scaleValue(scale);const dir=fs.realpathSync(directory),files=fs.readdirSync(dir).filter(f=>/^page-\d+\.html$/.test(f)).sort();
 if(!files.length)throw Error('No page-NN.html files');
 const targets=[...files.map(f=>f.replace('.html','.png')),'render-report.json'];
 for(const f of targets)safeOutput(path.join(dir,f),dir);
 if(phone){safeOutput(path.join(dir,'qa-phone'),dir);for(const f of files)safeOutput(path.join(dir,'qa-phone',f.replace('.html','.png')),dir)}
 if(!overwrite&&targets.some(f=>fs.existsSync(path.join(dir,f))))throw Error('Existing output; choose a fresh directory or explicitly --overwrite');
 const options={headless:true};
 if(process.env.CHROMIUM_PATH)options.executablePath=process.env.CHROMIUM_PATH;
 else if(process.platform==='darwin'&&fs.existsSync('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'))options.executablePath='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
 const browser=await chromium.launch(options),report=[];
 try{
  const context=await browser.newContext({viewport:{width:1200,height:1920},deviceScaleFactor:scale,javaScriptEnabled:false,serviceWorkers:'block'});
  await context.route('**/*',async route=>{try{const u=new URL(route.request().url());if(u.protocol==='file:'){const f=fs.realpathSync(fileURLToPath(u));if(within(f,dir)&&/\.(?:html|css|png|jpe?g|webp)$/i.test(f))return route.continue()}}catch{}return route.abort()});
  const page=await context.newPage();
  for(const file of files){
   const src=fs.realpathSync(path.join(dir,file));if(!within(src,dir))throw Error('HTML symlink escapes output');
   await page.goto(pathToFileURL(src).href,{waitUntil:'load'});await page.evaluate(()=>document.fonts.ready);
   const m=await page.evaluate(()=>{
    const sheet=document.querySelector('.sheet');if(!sheet)throw Error('Missing .sheet');const r=sheet.getBoundingClientRect();
    const overflow=[];
    for(const el of sheet.querySelectorAll('*')){const b=el.getBoundingClientRect();let horizontal=el instanceof HTMLElement&&el.clientWidth>0&&el.scrollWidth>el.clientWidth+2&&!el.parentElement?.classList.contains('arrowflow');if(b.width&&b.height&&(b.left<r.left-1||b.right>r.right+1||b.top<r.top-1||b.bottom>r.bottom+1||horizontal))overflow.push({tag:el.tagName,class:String(el.className),text:el.textContent.slice(0,45)})}
    const overlap=[];for(const parent of [sheet,sheet.querySelector('.content')].filter(Boolean)){const children=[...parent.children];for(let i=1;i<children.length;i++){const a=children[i-1].getBoundingClientRect(),b=children[i].getBoundingClientRect();if(b.top<a.bottom-.5)overlap.push({a:children[i-1].className,b:children[i].className,pixels:a.bottom-b.top})}}
    const footer=sheet.querySelector('footer'),brand=sheet.querySelector('.brand'),sources=sheet.querySelector('.sources'),folio=sheet.querySelector('.folio');
    const f=footer?.getBoundingClientRect(),b=brand?.getBoundingClientRect(),s=sources?.getBoundingClientRect(),n=folio?.getBoundingClientRect();
    const magazine=sheet.dataset.profile==='magazine',checks={};
    if(magazine){checks.brandExact=brand?.textContent==='「两克伴」出品';checks.brandUpperRight=b&&b.top<r.top+140&&b.right>r.right-80;checks.footerTwoLines=!!sources&&sources.querySelectorAll('br').length===1&&Math.abs(s.height-parseFloat(getComputedStyle(sources).lineHeight)*2)<2;checks.folioSeparate=s&&n&&s.right+20<=n.left;checks.compactBottom=f&&r.bottom-f.bottom<=36&&r.bottom-f.bottom>=20;checks.footerCompact=f&&f.height<=72;checks.dimensions=r.width===1080&&r.height===1920;checks.sourceNonempty=!!sheet.querySelector('.source-line')?.textContent.trim()}
    const broken=[...sheet.querySelectorAll('img')].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'));
    return{cssWidth:r.width,cssHeight:r.height,overflow,overlap,checks,brokenImages:broken,fonts:document.fonts.status,bodyFont:getComputedStyle(sheet).fontFamily,footerBottomInset:f?r.bottom-f.bottom:null,footerHeight:f?.height,sourceText:sources?.textContent||'',brand:brand?.textContent||''}
   });
   if(m.cssWidth<=0||m.cssHeight<=0||m.cssHeight>10000||Math.ceil(m.cssWidth*scale)*Math.ceil(m.cssHeight*scale)>8e7)throw Error('Image dimensions exceed limits; split page');
   const errors=[...m.overflow,...m.overlap,...m.brokenImages,...Object.entries(m.checks).filter(([k,v])=>!v).map(([k])=>k)];
   const result={file:file.replace('.html','.png'),...m,scale,browser:browser.version(),pass:!errors.length};report.push(result);
   fs.writeFileSync(path.join(dir,'render-report.json'),JSON.stringify(report,null,2)+'\n');
   if(errors.length)throw Error(file+' failed layout QA: '+JSON.stringify(errors));
   const png=await page.locator('.sheet').screenshot({path:path.join(dir,result.file),animations:'disabled'});result.width=png.readUInt32BE(16);result.height=png.readUInt32BE(20);
   if(phone){const pc=await browser.newContext({viewport:{width:1200,height:1920},deviceScaleFactor:390/m.cssWidth,javaScriptEnabled:false,serviceWorkers:'block'});await pc.route('**/*',route=>{try{const u=new URL(route.request().url());if(u.protocol==='file:'&&within(fs.realpathSync(fileURLToPath(u)),dir))return route.continue()}catch{}return route.abort()});const pp=await pc.newPage();await pp.goto(pathToFileURL(src).href);await pp.evaluate(()=>document.fonts.ready);const pd=path.join(dir,'qa-phone');fs.mkdirSync(pd,{recursive:true});await pp.locator('.sheet').screenshot({path:path.join(pd,result.file),animations:'disabled'});await pc.close()}
   console.log(file+' passed '+result.width+'×'+result.height);
  }
  fs.writeFileSync(path.join(dir,'render-report.json'),JSON.stringify(report,null,2)+'\n');return report;
 }finally{await browser.close()}
}
async function main(){const a=process.argv.slice(2),dir=a.shift();if(!dir)throw Error('Usage: node scripts/render.cjs OUTPUT [--scale 1] [--overwrite] [--no-phone]');const opts={};while(a.length){const f=a.shift();if(f==='--scale')opts.scale=scaleValue(a.shift());else if(f==='--overwrite')opts.overwrite=true;else if(f==='--no-phone')opts.phone=false;else throw Error('Unknown argument '+f)}await render(dir,opts)}
module.exports={render,scaleValue,within,safeOutput};if(require.main===module)main().catch(e=>{console.error('render:',e.message);process.exitCode=1});
