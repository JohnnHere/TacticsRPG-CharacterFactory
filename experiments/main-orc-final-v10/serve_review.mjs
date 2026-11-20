import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const PORT = Number(process.env.PORT || 8788);
const REVIEW_URL = "/Biblioteca%20de%20Arte/Estudos%20Comparativos/Orc%20principal%20-%20Candidato%20Final%20e%20Arquitetura%20C/index.html";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".png": "image/png",
  ".json": "application/json; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".gif": "image/gif",
};

const server = http.createServer((req, res) => {
  const rawPath = (req.url || "/").split("?")[0];
  if (rawPath === "/" || rawPath === "/revisao" || rawPath === "/revisao/") {
    res.writeHead(302, { Location: REVIEW_URL });
    res.end();
    return;
  }
  let decoded;
  try { decoded = decodeURIComponent(rawPath); } catch { res.writeHead(400); res.end(); return; }
  const safePath = path.resolve(ROOT, "." + decoded);
  if (!safePath.startsWith(ROOT)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }
  let target = safePath;
  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
    target = path.join(target, "index.html");
  }
  if (!fs.existsSync(target) || !fs.statSync(target).isFile()) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }
  const ext = path.extname(target).toLowerCase();
  res.writeHead(200, {
    "Content-Type": MIME[ext] || "application/octet-stream",
    "Cache-Control": "no-cache",
  });
  fs.createReadStream(target).pipe(res);
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`Review server listening on http://127.0.0.1:${PORT}/`);
});
