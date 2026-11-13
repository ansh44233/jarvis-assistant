"""Local browser dashboard. Binds to loopback only; no remote access by default."""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

_PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#080d18"><title>JARVIS • Personal Command Center</title>
<style>
:root{color-scheme:dark;--bg:#080d18;--panel:#101a2b;--line:#20334c;--cyan:#63e6ff;--muted:#91a4bc;--text:#edf6ff}*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 15% 0%,#122b43 0,transparent 42%),var(--bg);font:15px/1.5 Inter,ui-sans-serif,system-ui;color:var(--text)}main{max-width:1120px;margin:auto;padding:32px 22px}.top{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:28px}.brand{display:flex;align-items:center;gap:14px}.orb{width:46px;height:46px;border:1px solid var(--cyan);border-radius:50%;box-shadow:0 0 28px #63e6ff55;display:grid;place-items:center;color:var(--cyan);font-weight:800}.eyebrow{color:var(--cyan);letter-spacing:.22em;font-size:11px}.muted{color:var(--muted)}.status{border:1px solid var(--line);padding:8px 12px;border-radius:99px;color:#a6f3d1;font-size:12px}.grid{display:grid;grid-template-columns:1.35fr .65fr;gap:18px}.panel{background:linear-gradient(145deg,#111d30ee,#0c1524ee);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 16px 50px #0003}.panel h2{font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 16px}.console{height:390px;overflow:auto;background:#070c14;border:1px solid #1a2b40;border-radius:12px;padding:15px;font:13px/1.65 ui-monospace,monospace}.msg{margin:0 0 12px;white-space:pre-wrap}.you{color:#9fb8d2}.jarvis{color:#7deaff}.form{display:flex;gap:9px;margin-top:12px}input{min-width:0;flex:1;background:#0a1321;border:1px solid var(--line);border-radius:10px;padding:13px;color:var(--text);outline:none}input:focus{border-color:var(--cyan)}button{border:1px solid #3b9fb9;background:#12354a;color:#c9f8ff;border-radius:10px;padding:11px 15px;cursor:pointer;font-weight:650}button:hover{background:#19465d}.secondary{background:#111d30;border-color:var(--line)}.cards{display:grid;grid-template-columns:1fr 1fr;gap:12px}.stat{padding:16px;background:#0a1422;border:1px solid var(--line);border-radius:13px}.num{font-size:28px;font-weight:750;color:var(--cyan)}.stat small{color:var(--muted)}.actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.hint{font-size:12px;color:var(--muted);margin-top:12px}.wide{grid-column:1/-1}.footer{margin-top:22px;color:#60758d;font-size:12px;text-align:center}@media(max-width:760px){.grid{grid-template-columns:1fr}.top{align-items:flex-start}.wide{grid-column:auto}}
</style></head><body><main>
<header class="top"><div class="brand"><div class="orb">J</div><div><div class="eyebrow">PERSONAL COMMAND CENTER</div><div style="font-size:24px;font-weight:800;letter-spacing:.08em">J.A.R.V.I.S.</div><div class="muted" style="font-size:12px">Local-first assistant · private by design</div></div></div><div class="status">● SYSTEM ONLINE · LOCALHOST</div></header>
<div class="grid"><section class="panel"><h2>Command interface</h2><div class="console" id="log"><p class="msg jarvis">JARVIS online. Your workspace is stored locally. Type “help” to see commands, or try “chat hello” when Ollama is running.</p></div><form class="form" id="form"><input id="command" autocomplete="off" placeholder="Ask JARVIS or enter a command…"><button>Send</button><button type="button" class="secondary" id="mic" title="Voice input">🎙</button><button type="button" class="secondary" id="speak" aria-pressed="false">🔊 Voice replies: off</button></form><div class="hint">Voice input uses your browser's built-in speech recognition when supported. Nothing is sent to a cloud voice service by this dashboard.</div></section>
<aside class="panel"><h2>Workspace overview</h2><div class="cards"><div class="stat"><div class="num" id="notes">—</div><small>Saved notes</small></div><div class="stat"><div class="num" id="tasks">—</div><small>Open tasks</small></div><div class="stat"><div class="num" id="reminders">—</div><small>Pending reminders</small></div><div class="stat"><div class="num" id="memory">—</div><small>Chat memories</small></div></div><div class="actions"><button class="secondary" data-cmd="brief">Daily brief</button><button class="secondary" data-cmd="notes">Notes</button><button class="secondary" data-cmd="tasks">Tasks</button><button class="secondary" data-cmd="reminders">Reminders</button></div><p class="hint">AI chat is optional. Install Ollama separately and pull a model, then use <code>chat your question</code>.</p></aside>
<section class="panel wide"><h2>Quick start</h2><div class="muted">Try these commands in the console:</div><div class="actions"><button class="secondary" data-cmd="note Project idea: build a private assistant">Save a note</button><button class="secondary" data-cmd="task Review my portfolio tomorrow">Create a task</button><button class="secondary" data-cmd="remind me to take a break in 30 minutes">Set reminder</button><button class="secondary" data-cmd="help">Show help</button></div></section></div><div class="footer">JARVIS · Open source personal productivity assistant · Runs on this device</div></main>
<script>
const log=document.querySelector('#log'),input=document.querySelector('#command');let voiceReplies=false;function add(who,text){const p=document.createElement('p');p.className='msg '+who;p.textContent=(who==='you'?'YOU › ':'JARVIS › ')+text;log.append(p);log.scrollTop=log.scrollHeight;if(who==='jarvis'&&voiceReplies&&'speechSynthesis'in window){speechSynthesis.cancel();speechSynthesis.speak(new SpeechSynthesisUtterance(text))}}async function send(command){if(!command.trim())return;add('you',command);input.value='';try{const r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({command})});const d=await r.json();add('jarvis',d.reply||d.error||'No response');await status()}catch(e){add('jarvis','Dashboard connection error. Is the local server running?')}}document.querySelector('#form').addEventListener('submit',e=>{e.preventDefault();send(input.value)});document.querySelectorAll('[data-cmd]').forEach(b=>b.addEventListener('click',()=>send(b.dataset.cmd)));async function status(){try{const d=await(await fetch('/api/status')).json();for(const k of ['notes','tasks','reminders','memory'])document.querySelector('#'+k).textContent=d[k]}catch(e){}}document.querySelector('#speak').addEventListener('click',e=>{voiceReplies=!voiceReplies;e.currentTarget.textContent=voiceReplies?'🔊 Voice replies: on':'🔊 Voice replies: off';e.currentTarget.setAttribute('aria-pressed',String(voiceReplies))});const SR=window.SpeechRecognition||window.webkitSpeechRecognition;document.querySelector('#mic').addEventListener('click',()=>{if(!SR){add('jarvis','Voice recognition is not supported in this browser. Try a Chromium-based browser.');return}const rec=new SR();rec.lang='en-IN';rec.interimResults=false;rec.onresult=e=>{input.value=e.results[0][0].transcript;send(input.value)};rec.onerror=()=>add('jarvis','Microphone unavailable. Check browser permission.');rec.start()});status();
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    assistant=None
    store=None
    def _json(self,payload: dict,status: int=200) -> None:
        raw=json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(raw)))
        self.send_header("Cache-Control","no-store")
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self) -> None:
        if urlparse(self.path).path=="/api/status":
            data=self.store.export_data()
            self._json({"notes":len(data["notes"]),"tasks":sum(not r["done"] for r in data["tasks"]),"reminders":sum(not r["fired"] for r in data["reminders"]),"memory":len(data["conversation"])})
            return
        if self.path!="/":
            self.send_error(404); return
        raw=_PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type","text/html; charset=utf-8")
        self.send_header("Content-Length",str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
    def do_POST(self) -> None:
        if urlparse(self.path).path!="/api/command":
            self.send_error(404); return
        try:
            length=int(self.headers.get("Content-Length","0"))
            if length<=0:
                self._json({"error":"Request body is required."},400); return
            if length>16384:
                self._json({"error":"Request too large."},413); return
            payload=json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(payload,dict) or not isinstance(payload.get("command"),str):
                self._json({"error":"Expected a JSON object with a string 'command'."},400); return
            command=payload["command"][:2000]
            self._json({"reply":self.assistant.handle(command)})
        except (ValueError,TypeError,UnicodeDecodeError):
            self._json({"error":"Invalid request."},400)
    def log_message(self,fmt: str,*args) -> None:
        return

def serve(assistant,store,host: str="127.0.0.1",port: int=8765) -> None:
    Handler.assistant,Handler.store=assistant,store
    server=HTTPServer((host,port),Handler)
    print(f"JARVIS dashboard: http://{host}:{port}  (Ctrl+C to stop)")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
