const {chromium}=require('playwright');(async()=>{const jobs=JSON.parse(process.argv[2]);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const [h,o] of jobs){await p.goto('file://'+h);await p.evaluate(()=>document.fonts.ready);
const bad=await p.evaluate(()=>{const w=document.querySelector('.wrap');return w?w.scrollHeight>w.clientHeight+2:false});if(bad)console.log('ESTOURO',h);
await p.screenshot({path:o});console.log('ok',o)}await b.close()})();