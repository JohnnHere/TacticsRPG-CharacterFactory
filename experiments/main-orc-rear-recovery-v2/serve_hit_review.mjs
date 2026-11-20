import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd();
const html=path.join(root,'experiments/main-orc-rear-recovery-v2/hit-playback-review.html');
const hitRoot=path.join(root,'characters/orc-v1/sprites/Animations/Hit');
const sourceRoot=path.join(root,'characters/orc-v1/source/complete-v1');
http.createServer((req,res)=>{
 const pathname=new URL(req.url,'http://127.0.0.1').pathname;
 if(pathname==='/hit-playback-review.html'){res.writeHead(200,{'content-type':'text/html; charset=utf-8','cache-control':'no-store'});fs.createReadStream(html).pipe(res);return;}
 const c=pathname.match(/^\/characters\/orc-v1\/source\/complete-v1\/(front_r|front_l|back_r|back_l)\/Hit\/clip\.json$/);
 if(c){res.writeHead(200,{'content-type':'application/json','cache-control':'no-store'});fs.createReadStream(path.join(sourceRoot,c[1],'Hit','clip.json')).pipe(res);return;}
 const m=pathname.match(/^\/characters\/orc-v1\/sprites\/Animations\/Hit\/(hit_(?:front_r|front_l|back_r|back_l)_0[0-4]\.png)$/);
 if(m){const f=path.join(hitRoot,m[1]);res.writeHead(200,{'content-type':'image/png','cache-control':'no-store'});fs.createReadStream(f).pipe(res);return;}
 res.writeHead(404);res.end('not found');
}).listen(4173,'127.0.0.1');
console.log('Hit review server listening on 127.0.0.1:4173');
