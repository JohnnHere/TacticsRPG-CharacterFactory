import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const PORT = Number(process.env.PORT || 8791);
const MIME = new Map([
  ['.html', 'text/html; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.png', 'image/png'],
  ['.gif', 'image/gif'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'],
  ['.aseprite', 'application/octet-stream'],
]);

http
  .createServer((req, res) => {
    const url = decodeURIComponent((req.url || '/').split('?')[0]);
    const file = path.join(ROOT, url);
    if (!file.startsWith(ROOT)) {
      res.writeHead(403).end('forbidden');
      return;
    }
    fs.stat(file, (err, st) => {
      if (err || !st.isFile()) {
        res.writeHead(404, { 'content-type': 'text/plain' }).end(`404 ${url}`);
        return;
      }
      res.writeHead(200, {
        'content-type': MIME.get(path.extname(file).toLowerCase()) || 'application/octet-stream',
        'cache-control': 'no-store',
        'content-length': st.size,
      });
      fs.createReadStream(file).pipe(res);
    });
  })
  .listen(PORT, '127.0.0.1', () => console.log(`serving ${ROOT} on http://127.0.0.1:${PORT}`));
