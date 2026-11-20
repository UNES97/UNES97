// Dev tool: render an SVG exactly like GitHub shows it (as an <img>), at real time points, to PNG.
//   node assets/src/render.mjs <file.svg> <outDir> [ms ...]      e.g. node assets/src/render.mjs assets/scene-light.svg /tmp 500 1500 4000
// Light SVGs render on GitHub's light background (#ffffff), dark ones on #0d1117.
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const [, , svgArg, outDir, ...times] = process.argv;
const svg = path.resolve(svgArg);
const shots = (times.length ? times : ["600", "1800", "5000"]).map(Number);
const bg = svg.includes("-dark") ? "#0d1117" : "#ffffff";
const html = path.join(outDir, `render-${path.basename(svg, ".svg")}.html`);
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(html, `<body style="margin:0;padding:20px;background:${bg};width:840px"><img src="${pathToFileURL(svg).href}" style="display:block;width:840px"></body>`);

const port = 9300 + Math.floor(Math.random() * 600);
const ch = spawn("C:/Program Files/Google/Chrome/Application/chrome.exe", [
  "--headless=new", "--hide-scrollbars", `--remote-debugging-port=${port}`,
  `--user-data-dir=${path.join(outDir, `.chrome-${port}`)}`, "--window-size=880,1000", "--allow-file-access-from-files", "about:blank",
]);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let tabs;
for (let i = 0; i < 60; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); if (tabs.length) break; } catch {} await sleep(250); }
const ws = new WebSocket(tabs.find((t) => t.type === "page").webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));
let id = 0; const pend = {};
ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m.result); delete pend[m.id]; } };
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await send("Page.enable");
await send("Page.navigate", { url: pathToFileURL(html).href });
const t0 = Date.now();
const size = await (async () => { await sleep(300); const r = await send("Runtime.evaluate", { expression: "JSON.stringify([document.images[0].naturalWidth, document.images[0].getBoundingClientRect().height])", returnByValue: true }); return JSON.parse(r.result.value); })();
for (const t of shots) {
  const wait = t - (Date.now() - t0); if (wait > 0) await sleep(wait);
  const r = await send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: 880, height: Math.ceil(size[1]) + 40, scale: 1 } });
  const out = path.join(outDir, `${path.basename(svg, ".svg")}-${t}ms.png`);
  fs.writeFileSync(out, Buffer.from(r.data, "base64"));
  console.log(out);
}
ws.close(); ch.kill();
