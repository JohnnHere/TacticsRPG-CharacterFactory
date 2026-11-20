import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const EXP = "c:/Users/João Orlando/Documents/Projetos Unity/TacticsRPG-CharacterFactory/experiments/main-orc-final-v10/pixellab";

function loadPixellabSettings() {
  const cfgPath = path.join(process.env.CODEX_HOME || path.join(os.homedir(), ".codex"), "config.toml");
  const txt = fs.readFileSync(cfgPath, "utf8");
  const secMatch = txt.match(/\[mcp_servers\.pixellab\]([\s\S]*?)(?=\n\[|$)/);
  if (!secMatch) throw new Error("Missing [mcp_servers.pixellab] in config.toml");
  const sec = secMatch[1];
  const urlMatch = sec.match(/^\s*url\s*=\s*"([^"]+)"/m);
  const url = urlMatch ? urlMatch[1] : "";
  if (url !== "https://api.pixellab.ai/mcp") throw new Error(`Unexpected endpoint: ${url}`);
  const headers = { "Content-Type": "application/json", Accept: "application/json, text/event-stream" };
  const hdrBlock = txt.match(/\[mcp_servers\.pixellab\.http_headers\]([\s\S]*?)(?=\n\[|$)/);
  if (hdrBlock) {
    for (const line of hdrBlock[1].split(/\r?\n/)) {
      const m = line.match(/^\s*"?([^"=\s]+)"?\s*=\s*"([^"]+)"/);
      if (m) headers[m[1]] = m[2];
    }
  }
  const inlineHdr = sec.match(/http_headers\s*=\s*\{([^}]+)\}/);
  if (inlineHdr) {
    for (const part of inlineHdr[1].split(",")) {
      const m = part.match(/^\s*"?([^"=\s]+)"?\s*=\s*"([^"]+)"/);
      if (m) headers[m[1]] = m[2];
    }
  }
  const envMatch = sec.match(/^\s*bearer_token_env_var\s*=\s*"([^"]+)"/m);
  if (envMatch && process.env[envMatch[1]]) {
    headers.Authorization = `Bearer ${process.env[envMatch[1]]}`;
  }
  return { url, headers };
}

async function createRpc() {
  const { url, headers } = loadPixellabSettings();
  let session = null;
  let nextId = 1;
  async function rpc(method, params, notify = false) {
    const id = notify ? undefined : nextId++;
    const payload = { jsonrpc: "2.0", method };
    if (params !== undefined) payload.params = params;
    if (id !== undefined) payload.id = id;
    const h = { ...headers };
    if (session) h["Mcp-Session-Id"] = session;
    const res = await fetch(url, { method: "POST", headers: h, body: JSON.stringify(payload) });
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
    const sid = res.headers.get("mcp-session-id");
    if (sid) session = sid;
    const body = await res.text();
    if (!body.trim()) return {};
    const messages = body.trimStart().startsWith("event:") || body.trimStart().startsWith("data:")
      ? body.split(/\r?\n/).filter(l => l.startsWith("data: ")).map(l => JSON.parse(l.slice(6)))
      : [JSON.parse(body)];
    const msg = messages.find(m => m.id === id) || messages[messages.length - 1];
    if (msg.error) throw new Error(JSON.stringify(msg.error));
    return msg.result || {};
  }
  await rpc("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "TacticsRPG-CharacterFactory", version: "0.1" },
  });
  await rpc("notifications/initialized", undefined, true);
  return rpc;
}

const rpc = await createRpc();

for (const [reqName, outName] of [
  ["sword_ne_request.json", "sword_ne_submit.json"],
  ["axe_ne_request.json", "axe_ne_submit.json"],
]) {
  const args = JSON.parse(fs.readFileSync(path.join(EXP, reqName), "utf8"));
  const result = await rpc("tools/call", { name: "animate_with_skeleton_v3", arguments: args });
  fs.writeFileSync(path.join(EXP, outName), JSON.stringify(result, null, 2) + "\n", "utf8");
  const text = (result.content || []).map(c => c.text || "").join("\n");
  console.log(`=== ${outName} (isError=${Boolean(result.isError)}) ===\n${text.slice(0, 600)}\n`);
}
