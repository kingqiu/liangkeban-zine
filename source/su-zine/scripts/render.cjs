#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL, fileURLToPath } = require('node:url');
const { chromium } = require('playwright');
function scaleValue(value) {
  const n=Number(value);
  if (!Number.isFinite(n)||n<0.25||n>4) throw Error('scale must be 0.25–4');
  return n;
}
async function render(directory, {scale=2,overwrite=false}={}) {
  scale=scaleValue(scale);
  const dir=fs.realpathSync(directory);
  const files=fs.readdirSync(dir).filter(f=>/^page-\d+\.html$/.test(f)).sort();
  if(!files.length) throw Error('No page-NN.html files');
  const targets=[...files.map(f=>f.replace('.html','.png')),'render-report.json'];
  if(!overwrite && targets.some(f=>fs.existsSync(path.join(dir,f)))) throw Error('Existing output; use a fresh directory or --overwrite');
  const options={headless:true};
  if(process.env.CHROMIUM_PATH) options.executablePath=process.env.CHROMIUM_PATH;
  const browser=await chromium.launch(options);
  try {
    const context=await browser.newContext({viewport:{width:1200,height:900},deviceScaleFactor:scale,javaScriptEnabled:false,serviceWorkers:'block'});
    let allowed=new Set();
    await context.route('**/*',async route=>{
      try {
        const u=new URL(route.request().url());
        if(u.protocol==='file:' && allowed.has(fs.realpathSync(fileURLToPath(u)))) return route.continue();
      } catch {}
      return route.abort();
    });
    const page=await context.newPage(), report=[];
    for(const file of files) {
      const source=path.join(dir,file), css=path.join(dir,'style.css');
      // Reject symlinks that escape the output folder.
      for(const p of [source,css]) if(path.dirname(fs.realpathSync(p))!==dir) throw Error('Resource outside output directory');
      allowed=new Set([fs.realpathSync(source),fs.realpathSync(css)]);
      await page.goto(pathToFileURL(source).href,{waitUntil:'load'});
      await page.evaluate(()=>document.fonts.ready);
      const metrics=await page.evaluate(()=>{
        const sheet=document.querySelector('.sheet');
        if(!sheet) throw Error('Missing .sheet');
        const r=sheet.getBoundingClientRect();
        const overflow=[...sheet.querySelectorAll('*')].filter(el=>{
          const b=el.getBoundingClientRect();
          return b.left<r.left-1||b.right>r.right+1||b.top<r.top-1||b.bottom>r.bottom+1||el.scrollWidth>el.clientWidth+2;
        }).map(el=>({tag:el.tagName,class:el.className}));
        return {cssWidth:r.width,cssHeight:r.height,overflow,fonts:document.fonts.status};
      });
      if(metrics.cssWidth<=0 || metrics.cssHeight<=0 || metrics.cssHeight>10000 || Math.ceil(metrics.cssWidth*scale)*Math.ceil(metrics.cssHeight*scale)>80000000) throw Error('Image dimensions exceed limits; split the page');
      if(metrics.overflow.length) throw Error('Layout overflow: '+JSON.stringify(metrics.overflow));
      const output=file.replace('.html','.png');
      const buffer=await page.locator('.sheet').screenshot({path:path.join(dir,output),animations:'disabled'});
      report.push({file:output,...metrics,width:buffer.readUInt32BE(16),height:buffer.readUInt32BE(20),scale,browser:browser.version()});
    }
    fs.writeFileSync(path.join(dir,'render-report.json'),JSON.stringify(report,null,2)+'\n');
    return report;
  } finally {await browser.close();}
}
async function main() {
  const args=process.argv.slice(2), dir=args.shift();
  if(!dir) throw Error('Usage: node scripts/render.cjs OUTPUT [--scale 2] [--overwrite]');
  let scale=2,overwrite=false;
  while(args.length) {
    const flag=args.shift();
    if(flag==='--scale') scale=scaleValue(args.shift());
    else if(flag==='--overwrite') overwrite=true;
    else throw Error('Unknown argument: '+flag);
  }
  console.log(JSON.stringify(await render(dir,{scale,overwrite}),null,2));
}
module.exports={render,scaleValue};
if(require.main===module) main().catch(e=>{console.error('render:',e.message);process.exitCode=1;});
