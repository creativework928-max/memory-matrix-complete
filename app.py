import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Memory Matrix — Futuristic Memory Puzzle Game",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Memory Matrix is intentionally self-contained.
# The game itself runs inside the browser component so its timer, animations,
# keyboard interactions, Web Audio effects, and localStorage are not dependent
# on Streamlit reruns or a Python polling loop.

GAME_HTML = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#050b18">
<meta name="description" content="Memory Matrix — a futuristic real-time memory puzzle game.">
<title>Memory Matrix</title>
<style>
:root{
  --void:#020617;--bg:#050b18;--bg2:#081226;
  --surface:rgba(11,22,41,.78);--surface2:rgba(16,29,53,.84);
  --surface3:#162542;--primary:#8b5cf6;--primary2:#a78bfa;
  --cyan:#22d3ee;--cyan2:#67e8f9;--magenta:#ec4899;
  --success:#34d399;--warning:#fbbf24;--danger:#fb7185;
  --text:#f8fafc;--muted:#94a3b8;--border:rgba(148,163,184,.16);
  --shadow:0 24px 80px rgba(0,0,0,.38);
  --glow:0 0 28px rgba(139,92,246,.28);
  --radius:18px;
}
:root.light{
  --void:#eef2ff;--bg:#f5f7ff;--bg2:#e8edff;
  --surface:rgba(255,255,255,.82);--surface2:rgba(248,250,255,.92);
  --surface3:#e8edff;--text:#111827;--muted:#64748b;
  --border:rgba(71,85,105,.16);--shadow:0 24px 70px rgba(51,65,85,.16);
}
*{box-sizing:border-box}
html{min-height:100%;background:var(--bg)}
body{
  margin:0;min-height:100%;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,
  "Segoe UI",sans-serif;color:var(--text);background:
  radial-gradient(circle at 15% 15%,rgba(139,92,246,.16),transparent 30%),
  radial-gradient(circle at 85% 82%,rgba(34,211,238,.12),transparent 30%),
  linear-gradient(135deg,var(--void),var(--bg2));overflow-x:hidden;
}
button{font:inherit}
button:focus-visible{outline:2px solid var(--cyan2);outline-offset:3px}
.app{min-height:100vh;position:relative;padding:22px clamp(14px,3vw,42px) 38px;isolation:isolate}
.app:before{
  content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:.24;
  background-image:linear-gradient(rgba(103,232,249,.08) 1px,transparent 1px),
    linear-gradient(90deg,rgba(103,232,249,.08) 1px,transparent 1px);
  background-size:42px 42px;mask-image:linear-gradient(to bottom,#000,transparent 90%);
}
.app:after{
  content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.36));
}
.shell{max-width:1450px;margin:0 auto}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:20px}
.brand{display:flex;align-items:center;gap:13px;min-width:0}
.brand-mark{
  width:48px;height:48px;border:1px solid rgba(103,232,249,.45);border-radius:14px;
  display:grid;place-items:center;color:var(--cyan2);font-size:25px;
  background:linear-gradient(145deg,rgba(139,92,246,.26),rgba(34,211,238,.08));
  box-shadow:var(--glow),inset 0 0 22px rgba(34,211,238,.08);
}
.brand h1{font-size:clamp(20px,2.5vw,29px);margin:0;letter-spacing:.08em;font-weight:850}
.brand p{margin:2px 0 0;color:var(--muted);font-size:11px;letter-spacing:.22em;font-weight:700}
.top-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}
.icon-btn,.control-btn{
  border:1px solid var(--border);background:var(--surface);color:var(--text);cursor:pointer;
  border-radius:12px;transition:.18s ease;backdrop-filter:blur(14px);
}
.icon-btn{width:42px;height:42px;font-size:17px}
.icon-btn:hover,.control-btn:hover{border-color:rgba(103,232,249,.42);transform:translateY(-1px);box-shadow:0 0 18px rgba(34,211,238,.12)}
.icon-btn[aria-pressed="true"]{color:var(--cyan2);border-color:rgba(34,211,238,.45)}
.screen{display:none}.screen.active{display:block}
.panel{
  background:linear-gradient(145deg,rgba(11,22,41,.88),rgba(7,18,38,.7));
  border:1px solid var(--border);border-radius:var(--radius);box-shadow:var(--shadow);
  backdrop-filter:blur(18px);
}
.lobby{padding:clamp(24px,5vw,68px);min-height:calc(100vh - 110px);display:grid;align-content:center}
.hero{max-width:920px;margin:0 auto;text-align:center}
.eyebrow{color:var(--cyan2);font-size:11px;letter-spacing:.28em;font-weight:800;margin-bottom:13px}
.hero h2{
  margin:0;font-size:clamp(46px,9vw,108px);line-height:.92;letter-spacing:-.045em;
  background:linear-gradient(100deg,var(--text),var(--primary2) 48%,var(--cyan2));
  -webkit-background-clip:text;background-clip:text;color:transparent;
  text-shadow:0 0 40px rgba(139,92,246,.18)
}
.hero .tagline{margin:18px 0 8px;font-size:clamp(14px,2vw,19px);letter-spacing:.16em;font-weight:800}
.hero .sub{margin:0 auto 30px;color:var(--muted);max-width:600px;line-height:1.7}
.diff-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px auto;max-width:980px}
.diff{
  position:relative;text-align:left;padding:20px;border-radius:17px;border:1px solid var(--border);
  background:rgba(9,20,38,.74);color:var(--text);cursor:pointer;transition:.2s ease;overflow:hidden
}
.diff:after{content:"";position:absolute;inset:auto -30% -60% 30%;height:100px;background:radial-gradient(circle,rgba(34,211,238,.13),transparent 70%)}
.diff:hover{transform:translateY(-3px);border-color:rgba(167,139,250,.48)}
.diff.selected{border-color:var(--primary2);box-shadow:0 0 0 1px rgba(167,139,250,.15),0 0 30px rgba(139,92,246,.16)}
.diff .level{font-size:12px;letter-spacing:.18em;color:var(--primary2);font-weight:900}
.diff h3{margin:7px 0 4px;font-size:22px}
.diff p{margin:0 0 17px;color:var(--muted);font-size:13px}
.diff-meta{display:flex;gap:14px;font-size:11px;color:var(--cyan2);font-weight:800}
.primary{
  border:0;color:#fff;cursor:pointer;border-radius:13px;padding:14px 24px;font-weight:850;
  letter-spacing:.08em;background:linear-gradient(100deg,var(--primary),#6d5dfc,var(--cyan));
  box-shadow:0 12px 30px rgba(99,78,240,.28);transition:.2s ease
}
.primary:hover{transform:translateY(-2px);filter:brightness(1.08);box-shadow:0 16px 38px rgba(99,78,240,.35)}
.lobby-bottom{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:22px}
.mini-record{font-size:11px;color:var(--muted);border:1px solid var(--border);padding:9px 12px;border-radius:999px;background:rgba(8,18,36,.58)}
.game-layout{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:18px}
.game-main{min-width:0}
.hud{
  display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin-bottom:14px
}
.stat{padding:13px 14px;min-width:0}
.stat-label{font-size:9px;color:var(--muted);font-weight:900;letter-spacing:.16em}
.stat-value{font-size:22px;font-weight:850;margin-top:3px;white-space:nowrap}
.timer-value{color:var(--cyan2)}.timer-value.warning{color:var(--warning)}.timer-value.critical{color:var(--danger);text-shadow:0 0 16px rgba(251,113,133,.45)}
.progress-wrap{height:5px;border-radius:999px;background:rgba(148,163,184,.1);overflow:hidden;margin:0 1px 13px}
.progress{height:100%;width:100%;background:linear-gradient(90deg,var(--cyan),var(--primary));transition:width .25s linear}
.progress.warning{background:linear-gradient(90deg,var(--warning),#f97316)}.progress.critical{background:linear-gradient(90deg,var(--danger),#ef4444);box-shadow:0 0 15px rgba(251,113,133,.4)}
.board-panel{padding:clamp(12px,2vw,24px)}
.board-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;gap:12px}
.board-head strong{font-size:12px;letter-spacing:.16em}.board-head span{font-size:11px;color:var(--muted)}
.board{
  display:grid;gap:clamp(7px,1.1vw,13px);width:min(100%,900px);margin:0 auto;
  perspective:1200px
}
.memory-card{
  aspect-ratio:1;border:0;padding:0;background:transparent;cursor:pointer;min-width:0;
  perspective:900px;position:relative;border-radius:14px
}
.memory-card:disabled{cursor:default}.memory-card .inner{
  position:relative;width:100%;height:100%;transform-style:preserve-3d;
  transition:transform .42s cubic-bezier(.2,.75,.25,1)
}
.memory-card.flipped .inner,.memory-card.matched .inner{transform:rotateY(180deg)}
.face{
  position:absolute;inset:0;border-radius:14px;backface-visibility:hidden;-webkit-backface-visibility:hidden;
  overflow:hidden;border:1px solid rgba(103,232,249,.14);display:grid;place-items:center
}
.back{
  background:
    radial-gradient(circle at center,rgba(139,92,246,.25),transparent 45%),
    linear-gradient(145deg,#0b1730,#071022);
  box-shadow:inset 0 0 30px rgba(34,211,238,.035)
}
.back:before{content:"";position:absolute;inset:13%;border:1px dashed rgba(103,232,249,.18);border-radius:10px;transform:rotate(45deg)}
.back-symbol{font-size:clamp(18px,3vw,30px);color:var(--cyan2);text-shadow:0 0 18px rgba(34,211,238,.55)}
.front{
  transform:rotateY(180deg);padding:6px;text-align:center;
  background:linear-gradient(145deg,rgba(22,37,66,.96),rgba(9,20,38,.96));
  border-color:rgba(167,139,250,.35);box-shadow:0 0 18px rgba(139,92,246,.12),inset 0 0 25px rgba(139,92,246,.06)
}
.symbol{font-size:clamp(25px,5vw,52px);line-height:1;text-shadow:0 0 18px rgba(103,232,249,.22)}
.card-name{font-size:clamp(8px,1.2vw,11px);font-weight:800;letter-spacing:.1em;color:var(--muted);margin-top:5px}
.card-cat{font-size:8px;color:var(--cyan2);letter-spacing:.12em;text-transform:uppercase;margin-top:2px}
.memory-card:hover:not(:disabled) .back{border-color:rgba(103,232,249,.48);box-shadow:0 0 20px rgba(34,211,238,.14),inset 0 0 25px rgba(34,211,238,.07)}
.memory-card:hover:not(:disabled){transform:translateY(-2px)}
.memory-card.matched .front{border-color:rgba(52,211,153,.75);box-shadow:0 0 25px rgba(52,211,153,.2),inset 0 0 25px rgba(52,211,153,.08)}
.memory-card.matched .symbol{color:var(--success);text-shadow:0 0 20px rgba(52,211,153,.5)}
.memory-card.mismatch .front{animation:shake .36s ease;border-color:rgba(251,113,133,.85);box-shadow:0 0 24px rgba(251,113,133,.22)}
@keyframes shake{0%,100%{transform:translateX(0) rotateY(180deg)}25%{transform:translateX(-4px) rotateY(180deg)}75%{transform:translateX(4px) rotateY(180deg)}}
.board.locked .memory-card{cursor:default}
.side{display:flex;flex-direction:column;gap:12px}
.side-panel{padding:18px}
.side-title{font-size:11px;letter-spacing:.17em;font-weight:900;margin-bottom:13px}
.combo-box{padding:16px;border:1px solid rgba(139,92,246,.24);background:linear-gradient(145deg,rgba(139,92,246,.1),rgba(34,211,238,.04));border-radius:14px}
.combo-num{font-size:35px;font-weight:900;color:var(--primary2)}.combo-copy{font-size:10px;color:var(--muted);letter-spacing:.12em}
.controls{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.control-btn{padding:11px 9px;font-size:11px;font-weight:800}.control-btn.danger{color:var(--danger)}
.accuracy-ring{display:grid;place-items:center;width:104px;height:104px;border-radius:50%;margin:5px auto 12px;background:conic-gradient(var(--cyan) var(--accuracy),rgba(148,163,184,.12) 0);position:relative}
.accuracy-ring:after{content:"";position:absolute;inset:8px;border-radius:50%;background:#091426}
.accuracy-ring span{position:relative;z-index:1;font-weight:900;font-size:20px}
.recent{display:grid;gap:7px;max-height:205px;overflow:auto}
.recent-row{display:grid;grid-template-columns:1fr auto;gap:8px;padding:8px;border-radius:9px;background:rgba(148,163,184,.045);font-size:10px}
.recent-row small{color:var(--muted)}.win{color:var(--success)}.loss{color:var(--danger)}
.score-pop{position:fixed;z-index:50;pointer-events:none;font-size:18px;font-weight:950;color:var(--success);text-shadow:0 0 16px rgba(52,211,153,.65);animation:scoreFloat .8s ease forwards}
@keyframes scoreFloat{0%{opacity:0;transform:translateY(8px) scale(.8)}20%{opacity:1}100%{opacity:0;transform:translateY(-50px) scale(1.08)}}
.toast{
  position:fixed;right:20px;bottom:20px;z-index:100;padding:12px 15px;border-radius:12px;
  background:rgba(7,18,38,.94);border:1px solid rgba(103,232,249,.3);box-shadow:var(--shadow);
  color:var(--text);font-size:12px;transform:translateY(20px);opacity:0;pointer-events:none;transition:.2s
}
.toast.show{transform:none;opacity:1}.toast.warn{border-color:rgba(251,191,36,.42)}.toast.error{border-color:rgba(251,113,133,.48)}
.modal-backdrop{position:fixed;inset:0;z-index:80;background:rgba(1,5,15,.76);backdrop-filter:blur(9px);display:none;align-items:center;justify-content:center;padding:18px}
.modal-backdrop.open{display:flex}.modal{width:min(620px,100%);padding:25px;border-radius:20px;background:linear-gradient(145deg,#0d1a31,#071022);border:1px solid var(--border);box-shadow:0 30px 100px rgba(0,0,0,.58)}
.modal h2{margin:0 0 7px;font-size:31px}.modal-sub{color:var(--muted);font-size:12px;letter-spacing:.12em}
.modal-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:20px 0}
.result-stat{padding:12px;border-radius:11px;background:rgba(148,163,184,.06);border:1px solid var(--border)}
.result-stat b{display:block;font-size:18px}.result-stat span{font-size:9px;color:var(--muted);letter-spacing:.1em}
.modal-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:17px}.secondary{background:rgba(148,163,184,.08);box-shadow:none}
.dialog-content{line-height:1.7;color:var(--muted);font-size:13px}.dialog-content strong{color:var(--text)}
.settings-list{display:grid;gap:10px;margin:18px 0}.setting-row{display:flex;align-items:center;justify-content:space-between;gap:15px;padding:12px;border:1px solid var(--border);border-radius:11px}
.toggle{width:44px;height:24px;border-radius:999px;border:0;background:#334155;position:relative;cursor:pointer}.toggle:after{content:"";position:absolute;width:18px;height:18px;top:3px;left:3px;border-radius:50%;background:#fff;transition:.2s}.toggle.on{background:var(--primary)}.toggle.on:after{left:23px}
.countdown{position:fixed;inset:0;z-index:70;display:none;place-items:center;background:rgba(2,6,23,.54);backdrop-filter:blur(4px)}
.countdown.open{display:grid}.countdown-number{font-size:clamp(90px,20vw,190px);font-weight:950;color:#fff;text-shadow:0 0 45px rgba(139,92,246,.65);animation:countPop .8s ease both}
@keyframes countPop{0%{opacity:0;transform:scale(1.5)}25%{opacity:1}100%{opacity:.15;transform:scale(.92)}}
.live{display:inline-flex;align-items:center;gap:6px}.live i{width:7px;height:7px;border-radius:50%;background:var(--success);box-shadow:0 0 9px var(--success)}
.records-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:16px}.record-card{padding:15px}.record-card b{font-size:22px}.record-card span{display:block;color:var(--muted);font-size:9px;letter-spacing:.12em;margin-top:4px}
.table{width:100%;border-collapse:collapse;font-size:11px}.table th,.table td{text-align:left;padding:10px;border-bottom:1px solid var(--border)}.table th{color:var(--muted);font-size:9px;letter-spacing:.1em}
.hidden{display:none!important}
.footer{max-width:1450px;margin:14px auto 0;color:var(--muted);font-size:9px;text-align:center;letter-spacing:.08em}
@media(max-width:1050px){.game-layout{grid-template-columns:1fr}.side{display:grid;grid-template-columns:repeat(3,1fr)}.hud{grid-template-columns:repeat(5,1fr)}}
@media(max-width:760px){
  .app{padding:12px 10px 28px}.topbar{align-items:flex-start}.brand p{letter-spacing:.13em}
  .brand-mark{width:40px;height:40px}.top-actions{gap:5px}.icon-btn{width:38px;height:38px}
  .diff-grid{grid-template-columns:1fr}.lobby{padding:25px 14px;min-height:calc(100vh - 85px)}
  .hero h2{font-size:clamp(43px,15vw,74px)}.hud{grid-template-columns:repeat(3,1fr)}
  .hud .stat:nth-child(1){grid-column:span 2}.hud .stat-value{font-size:18px}
  .board-panel{padding:10px}.board{gap:6px}.face{border-radius:10px}.memory-card{border-radius:10px}
  .side{grid-template-columns:1fr}.side-panel{padding:14px}.accuracy-ring{width:90px;height:90px}
  .records-grid{grid-template-columns:repeat(2,1fr)}.modal-grid{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:420px){.topbar .brand h1{font-size:18px}.topbar .brand p{font-size:8px}.hud{gap:6px}.stat{padding:10px}.stat-value{font-size:16px}.card-name,.card-cat{display:none}.board{gap:4px}}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}
  .memory-card:hover:not(:disabled){transform:none}.countdown-number{animation:none}
}
</style>
</head>
<body>
<div class="app" id="app">
  <div class="shell">
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">✦</div>
        <div><h1>MEMORY MATRIX</h1><p>MATCH. REMEMBER. MASTER.</p></div>
      </div>
      <nav class="top-actions" aria-label="Game controls">
        <button class="icon-btn" id="soundBtn" aria-label="Toggle sound" aria-pressed="false" title="Sound (M)">🔇</button>
        <button class="icon-btn" id="themeBtn" aria-label="Toggle theme" title="Theme">◐</button>
        <button class="icon-btn" id="recordsBtn" aria-label="Open records" title="Records">◫</button>
        <button class="icon-btn" id="helpBtn" aria-label="How to play" title="How to play">?</button>
      </nav>
    </header>

    <main>
      <section class="screen active" id="lobbyScreen" aria-labelledby="gameTitle">
        <div class="panel lobby">
          <div class="hero">
            <div class="eyebrow">NEURAL MEMORY TRAINING / REAL-TIME PUZZLE</div>
            <h2 id="gameTitle">MEMORY MATRIX</h2>
            <div class="tagline">TRAIN YOUR MEMORY BEFORE THE CLOCK RUNS OUT.</div>
            <p class="sub">Match every pair before the timer reaches zero. Build combos, protect your accuracy, and push your personal record.</p>
            <div class="diff-grid" id="difficultyGrid" role="radiogroup" aria-label="Select difficulty"></div>
            <button class="primary" id="startBtn">START MISSION&nbsp; →</button>
            <div class="lobby-bottom" id="lobbyRecords"></div>
          </div>
        </div>
      </section>

      <section class="screen" id="gameScreen" aria-labelledby="boardHeading">
        <div class="game-layout">
          <div class="game-main">
            <div class="hud" aria-live="polite">
              <div class="panel stat"><div class="stat-label">TIME</div><div class="stat-value timer-value" id="timeValue">01:00</div></div>
              <div class="panel stat"><div class="stat-label">SCORE</div><div class="stat-value" id="scoreValue">0</div></div>
              <div class="panel stat"><div class="stat-label">MOVES</div><div class="stat-value" id="movesValue">0</div></div>
              <div class="panel stat"><div class="stat-label">MATCHES</div><div class="stat-value" id="matchesValue">0 / 8</div></div>
              <div class="panel stat"><div class="stat-label">ACCURACY</div><div class="stat-value" id="accuracyValue">100%</div></div>
            </div>
            <div class="progress-wrap" aria-hidden="true"><div class="progress" id="timeProgress"></div></div>
            <div class="panel board-panel">
              <div class="board-head">
                <strong id="boardHeading">MATRIX / INITIATE</strong>
                <span class="live"><i></i><span id="statusText">READY</span></span>
              </div>
              <div class="board" id="board" role="grid" aria-label="Memory card board"></div>
            </div>
          </div>
          <aside class="side" aria-label="Game information">
            <div class="panel side-panel combo-box">
              <div class="side-title">COMBO SIGNAL</div>
              <div class="combo-num" id="comboValue">×0</div>
              <div class="combo-copy">MAX <span id="maxComboValue">×0</span></div>
            </div>
            <div class="panel side-panel">
              <div class="side-title">MISSION</div>
              <div class="controls">
                <button class="control-btn" id="pauseBtn">Ⅱ PAUSE</button>
                <button class="control-btn danger" id="restartBtn">↻ RESTART</button>
                <button class="control-btn" id="lobbyBtn">⌂ LOBBY</button>
                <button class="control-btn" id="settingsBtn">⚙ SETTINGS</button>
              </div>
            </div>
            <div class="panel side-panel">
              <div class="side-title">ACCURACY MATRIX</div>
              <div class="accuracy-ring" id="accuracyRing" style="--accuracy:100%"><span id="ringValue">100%</span></div>
              <div class="side-title">RECENT RUNS</div>
              <div class="recent" id="recentRuns"></div>
            </div>
          </aside>
        </div>
      </section>

      <section class="screen" id="recordsScreen">
        <div class="panel" style="padding:clamp(18px,4vw,34px)">
          <div class="board-head"><strong>PERSONAL RECORDS</strong><button class="control-btn" id="recordsBack">← BACK</button></div>
          <div class="records-grid" id="recordsSummary"></div>
          <div style="overflow:auto"><table class="table"><thead><tr><th>RESULT</th><th>MODE</th><th>SCORE</th><th>TIME</th><th>MOVES</th><th>ACCURACY</th><th>DATE</th></tr></thead><tbody id="recordsTable"></tbody></table></div>
          <div class="modal-actions"><button class="control-btn danger" id="clearDataBtn">CLEAR LOCAL DATA</button></div>
        </div>
      </section>
    </main>
    <footer class="footer">NO ACCOUNTS • NO TRACKING • LOCAL PERSONAL RECORDS ONLY</footer>
  </div>
</div>

<div class="countdown" id="countdown" aria-live="assertive" aria-label="Game countdown"><div class="countdown-number" id="countdownNumber">3</div></div>
<div class="toast" id="toast" role="status"></div>

<div class="modal-backdrop" id="modalBackdrop" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <div class="modal">
    <h2 id="modalTitle"></h2><div class="modal-sub" id="modalSub"></div>
    <div id="modalBody"></div>
    <div class="modal-actions" id="modalActions"></div>
  </div>
</div>

<script>
(() => {
"use strict";

const DIFFICULTIES = Object.freeze({
  initiate:{id:"initiate",name:"INITIATE",description:"Learn the matrix.",rows:4,columns:4,pairs:8,timeLimit:60},
  pro:{id:"pro",name:"PRO",description:"Test your memory.",rows:4,columns:5,pairs:10,timeLimit:75},
  elite:{id:"elite",name:"ELITE",description:"Master the matrix.",rows:6,columns:6,pairs:18,timeLimit:120}
});

const CARD_CATALOG = Object.freeze([
  ["nova","✦","Nova","Astronomy"],["moon","☾","Moon","Astronomy"],["sun","☀","Sun","Astronomy"],
  ["comet","☄","Comet","Astronomy"],["orbit","◌","Orbit","Astronomy"],["star","★","Star","Astronomy"],
  ["nebula","✧","Nebula","Astronomy"],["eclipse","◐","Eclipse","Astronomy"],
  ["leaf","❧","Leaf","Nature"],["flower","✿","Flower","Nature"],["tree","♧","Tree","Nature"],
  ["water","≈","Water","Nature"],["mountain","⌁","Mountain","Nature"],["wind","〰","Wind","Nature"],
  ["flame","♨","Flame","Energy"],["bolt","ϟ","Bolt","Energy"],["atom","⚛","Atom","Science"],
  ["dna","⌬","DNA","Science"],["micro","⌕","Micro","Science"],["code","⌘","Code","Technology"],
  ["chip","▦","Chip","Technology"],["signal","⌁","Signal","Technology"],["robot","◈","Robot","Technology"],
  ["cloud","☁","Cloud","Weather"],["rain","♒","Rain","Weather"],["storm","ϟ","Storm","Weather"],
  ["snow","❄","Snow","Weather"],["crystal","◇","Crystal","Abstract"],["prism","◈","Prism","Abstract"],
  ["spiral","◎","Spiral","Abstract"],["wave","∿","Wave","Abstract"],["pulse","⌁","Pulse","Abstract"]
].map(([id,symbol,name,category]) => ({id,symbol,name,category})));

const KEYS = Object.freeze({
  settings:"memory-matrix.settings",
  statistics:"memory-matrix.statistics",
  results:"memory-matrix.results"
});

const SCORE = Object.freeze({
  MATCH_BASE:100, COMBO_BONUS:25, FAST_MATCH_BONUS:50,
  TIME_BONUS_MULTIPLIER:5, MISTAKE_PENALTY:15
});

const DEFAULT_SETTINGS = {soundEnabled:false,theme:"dark",reducedEffects:false,confirmRestart:true};
const DEFAULT_STATS = {gamesPlayed:0,gamesWon:0,bestScore:0,fastestTime:null,fewestMoves:null,bestCombo:0};

function clone(v){return JSON.parse(JSON.stringify(v));}
function safeParse(raw,fallback){
  try { return raw ? JSON.parse(raw) : clone(fallback); } catch { return clone(fallback); }
}
function storageAvailable(){
  try { const x="__mm_test__"; localStorage.setItem(x,x); localStorage.removeItem(x); return true; }
  catch { return false; }
}
const hasStorage=storageAvailable();
let memoryStore={};
function load(key,fallback){
  if(!hasStorage) return key in memoryStore ? clone(memoryStore[key]) : clone(fallback);
  return safeParse(localStorage.getItem(key),fallback);
}
function save(key,value){
  if(!hasStorage){memoryStore[key]=clone(value);return true;}
  try { localStorage.setItem(key,JSON.stringify(value)); return true; } catch { return false; }
}
function remove(key){
  if(!hasStorage){delete memoryStore[key];return;}
  try {localStorage.removeItem(key);} catch {}
}

function randomIndex(max){
  if(max<=1)return 0;
  try {const a=new Uint32Array(1);crypto.getRandomValues(a);return a[0] % max;}
  catch {return Math.floor(Math.random()*max);}
}
function shuffle(input){
  const a=[...input];
  for(let i=a.length-1;i>0;i--){const j=randomIndex(i+1);[a[i],a[j]]=[a[j],a[i]];}
  return a;
}
function formatTime(seconds){
  const s=Math.max(0,Math.ceil(seconds));
  return `${String(Math.floor(s/60)).padStart(2,"0")}:${String(s%60).padStart(2,"0")}`;
}
function formatNumber(n){return Math.max(0,Math.round(n)).toLocaleString();}
function clamp(n,min,max){return Math.min(max,Math.max(min,n));}

class AudioService{
  constructor(){this.enabled=false;this.ctx=null;this.master=null;}
  setEnabled(v){this.enabled=!!v;if(this.enabled)this.ensure();}
  ensure(){
    if(!this.enabled)return;
    if(!this.ctx){
      const C=window.AudioContext||window.webkitAudioContext;
      if(!C)return;
      this.ctx=new C();this.master=this.ctx.createGain();this.master.gain.value=.07;this.master.connect(this.ctx.destination);
    }
    if(this.ctx.state==="suspended")this.ctx.resume().catch(()=>{});
  }
  tone(freq,duration,type="sine",gain=.08,delay=0){
    if(!this.enabled)return;
    this.ensure();if(!this.ctx)return;
    const t=this.ctx.currentTime+delay,o=this.ctx.createOscillator(),g=this.ctx.createGain();
    o.type=type;o.frequency.setValueAtTime(freq,t);o.frequency.exponentialRampToValueAtTime(Math.max(50,freq*.72),t+duration);
    g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(gain,t+.008);g.gain.exponentialRampToValueAtTime(.0001,t+duration);
    o.connect(g);g.connect(this.master);o.start(t);o.stop(t+duration+.02);
  }
  click(){this.tone(420,.06,"sine",.07)}
  flip(){this.tone(620,.07,"triangle",.06)}
  match(){this.tone(660,.11,"sine",.09);this.tone(880,.16,"sine",.08,.07)}
  mismatch(){this.tone(180,.18,"sawtooth",.07)}
  combo(){this.tone(760,.08,"triangle",.08);this.tone(1100,.12,"triangle",.07,.07)}
  countdown(){this.tone(520,.12,"sine",.06)}
  go(){this.tone(760,.12,"sine",.07);this.tone(1040,.18,"sine",.07,.08)}
  warning(){this.tone(360,.09,"square",.035)}
  victory(){[660,784,988,1318].forEach((f,i)=>this.tone(f,.16,"sine",.075,i*.09))}
  defeat(){[420,330,250].forEach((f,i)=>this.tone(f,.18,"triangle",.06,i*.11))}
}

class Timer{
  constructor(duration,onTick,onEnd){this.duration=duration;this.onTick=onTick;this.onEnd=onEnd;this.running=false;this.startedAt=0;this.pausedAt=0;this.elapsedBeforePause=0;this.raf=0;this.lastSecond=null;}
  reset(duration=this.duration){this.stop();this.duration=duration;this.elapsedBeforePause=0;this.startedAt=0;this.pausedAt=0;this.lastSecond=null;this.emit(0);}
  start(){
    this.stop();this.running=true;this.startedAt=performance.now();this.elapsedBeforePause=0;this.lastSecond=null;this.loop();
  }
  pause(){if(!this.running)return;this.running=false;this.pausedAt=performance.now();this.elapsedBeforePause=this.getElapsed();cancelAnimationFrame(this.raf);}
  resume(){if(this.running)return;this.startedAt=performance.now()-this.elapsedBeforePause*1000;this.running=true;this.loop();}
  stop(){this.running=false;cancelAnimationFrame(this.raf);}
  getElapsed(){if(!this.startedAt)return this.elapsedBeforePause;return this.running?(performance.now()-this.startedAt)/1000:this.elapsedBeforePause;}
  getRemaining(){return Math.max(0,this.duration-this.getElapsed());}
  emit(remaining){if(this.onTick)this.onTick(remaining);}
  loop=()=>{
    if(!this.running)return;
    const elapsed=this.getElapsed(),remaining=Math.max(0,this.duration-elapsed);
    this.emit(remaining);
    if(remaining<=0){this.running=false;cancelAnimationFrame(this.raf);if(this.onEnd)this.onEnd();return;}
    this.raf=requestAnimationFrame(this.loop);
  }
}

class ScoreEngine{
  matchScore(combo,fast){return SCORE.MATCH_BASE+Math.max(0,combo-1)*SCORE.COMBO_BONUS+(fast?SCORE.FAST_MATCH_BONUS:0)}
  mistakePenalty(){return SCORE.MISTAKE_PENALTY}
  timeBonus(remaining){return Math.floor(Math.max(0,remaining)*SCORE.TIME_BONUS_MULTIPLIER)}
  finalScore(base,remaining){return Math.max(0,base+this.timeBonus(remaining))}
}

class Game{
  constructor(ui){
    this.ui=ui;this.audio=new AudioService();this.scoreEngine=new ScoreEngine();
    this.settings=load(KEYS.settings,DEFAULT_SETTINGS);this.stats=load(KEYS.statistics,DEFAULT_STATS);
    this.results=load(KEYS.results,[]);
    this.difficulty="initiate";this.status="READY";this.cards=[];this.first=null;this.second=null;
    this.moves=0;this.matches=0;this.mistakes=0;this.score=0;this.combo=0;this.maxCombo=0;this.startedAt=null;
    this.lastMatchAt=0;this.lockToken=0;this.countdownToken=0;
    this.timer=new Timer(60,(r)=>this.onTick(r),()=>this.lose());
    this.applySettings();
  }
  applySettings(){
    document.documentElement.classList.toggle("light",this.settings.theme==="light");
    this.audio.setEnabled(this.settings.soundEnabled);
    ui.soundBtn.textContent=this.settings.soundEnabled?"🔊":"🔇";
    ui.soundBtn.setAttribute("aria-pressed",String(this.settings.soundEnabled));
    renderLobbyRecords();
  }
  setDifficulty(id){if(DIFFICULTIES[id]){this.difficulty=id;this.ui.renderDifficulty();}}
  initialize(){
    this.resetData();
    const d=DIFFICULTIES[this.difficulty];
    const selected=shuffle(CARD_CATALOG).slice(0,d.pairs);
    const deck=[];
    selected.forEach(c=>{
      deck.push({id:`${c.id}-a-${randomIndex(1e9)}`,pairId:c.id,symbol:c.symbol,name:c.name,category:c.category,flipped:false,matched:false});
      deck.push({id:`${c.id}-b-${randomIndex(1e9)}`,pairId:c.id,symbol:c.symbol,name:c.name,category:c.category,flipped:false,matched:false});
    });
    this.cards=shuffle(deck);this.timer.reset(d.timeLimit);this.ui.renderBoard(this.cards,d);
    this.status="READY";this.ui.update(this);return this;
  }
  resetData(){
    this.timer.stop();this.lockToken++;this.first=null;this.second=null;this.moves=0;this.matches=0;this.mistakes=0;
    this.score=0;this.combo=0;this.maxCombo=0;this.startedAt=null;this.lastMatchAt=0;this.cards=[];this.status="READY";
  }
  async start(){
    this.initialize();showScreen("gameScreen");this.ui.update(this);
    await this.countdown();if(this.status!=="COUNTDOWN")return;
    this.status="PLAYING";this.startedAt=Date.now();this.timer.start();this.ui.update(this);this.audio.go();
  }
  countdown(){
    const token=++this.countdownToken;this.status="COUNTDOWN";ui.countdown.classList.add("open");
    return new Promise(resolve=>{
      let n=3;ui.countdownNumber.textContent=n;this.audio.countdown();
      const step=()=>{
        if(token!==this.countdownToken){ui.countdown.classList.remove("open");resolve();return;}
        n--;
        if(n>0){ui.countdownNumber.textContent=n;this.audio.countdown();setTimeout(step,700);}
        else{ui.countdownNumber.textContent="GO";this.audio.go();setTimeout(()=>{ui.countdown.classList.remove("open");resolve();},520);}
      };
      setTimeout(step,700);
    });
  }
  selectCard(id){
    if(this.status!=="PLAYING"||this.second)return;
    const card=this.cards.find(c=>c.id===id);if(!card||card.flipped||card.matched)return;
    card.flipped=true;this.ui.flipCard(card);this.audio.flip();
    if(!this.first){this.first=card;return;}
    this.second=card;this.moves++;this.status="CHECKING";this.ui.update(this);this.evaluateSelection();
  }
  evaluateSelection(){
    const a=this.first,b=this.second,token=++this.lockToken;
    if(a.pairId===b.pairId){
      a.matched=b.matched=true;this.matches++;this.combo++;this.maxCombo=Math.max(this.maxCombo,this.combo);
      const now=performance.now(),fast=this.lastMatchAt>0&&now-this.lastMatchAt<3500;
      this.lastMatchAt=now;const gained=this.scoreEngine.matchScore(this.combo,fast);this.score+=gained;
      this.ui.markMatched(a,b);this.ui.showScore(gained,b);this.audio.match();if(this.combo>=2)this.audio.combo();
      this.first=null;this.second=null;this.status="PLAYING";this.ui.update(this);
      if(this.matches===DIFFICULTIES[this.difficulty].pairs)this.win();
    }else{
      this.mistakes++;this.combo=0;this.score=Math.max(0,this.score-this.scoreEngine.mistakePenalty());
      this.ui.markMismatch(a,b);this.audio.mismatch();this.ui.update(this);
      setTimeout(()=>{
        if(token!==this.lockToken||this.status!=="CHECKING")return;
        a.flipped=false;b.flipped=false;this.first=null;this.second=null;this.status="PLAYING";this.ui.unflip(a,b);this.ui.update(this);
      },this.settings.reducedEffects?450:780);
    }
  }
  pause(){
    if(this.status!=="PLAYING")return;this.timer.pause();this.status="PAUSED";this.ui.update(this);this.ui.showPause();
  }
  resume(){
    if(this.status!=="PAUSED")return;this.status="PLAYING";this.timer.resume();this.ui.hidePause();this.ui.update(this);
  }
  restart(force=false){
    if(this.status==="WON"||this.status==="LOST"||force){this.start();return;}
    if(this.settings.confirmRestart){this.ui.confirm("RESTART MISSION?","Your current run will be discarded.",()=>this.start());}
    else this.start();
  }
  win(){
    if(this.status==="WON")return;this.timer.stop();this.status="WON";const d=DIFFICULTIES[this.difficulty];
    const remaining=this.timer.getRemaining(),timeUsed=Math.max(0,d.timeLimit-remaining);
    const final=this.scoreEngine.finalScore(this.score,remaining);this.score=final;
    const result=this.buildResult("WON",timeUsed,remaining);const isRecord=this.saveResult(result);
    this.audio.victory();this.ui.update(this);this.ui.showResult(result,isRecord,true);
  }
  lose(){
    if(this.status==="LOST"||this.status==="WON")return;
    this.timer.stop();this.status="LOST";const d=DIFFICULTIES[this.difficulty];
    const result=this.buildResult("LOST",d.timeLimit,0);this.saveResult(result);this.audio.defeat();this.ui.update(this);this.ui.showResult(result,false,false);
  }
  buildResult(result,timeUsed,timeRemaining){
    const accuracy=this.moves?Math.round((this.matches/this.moves)*100):100;
    return {id:`${Date.now()}-${randomIndex(1e9)}`,difficulty:this.difficulty,score:this.score,
      timeUsed:Math.round(timeUsed),timeRemaining:Math.round(timeRemaining),moves:this.moves,matches:this.matches,
      accuracy,maxCombo:this.maxCombo,result,completedAt:new Date().toISOString()};
  }
  saveResult(result){
    this.results=Array.isArray(this.results)?this.results:[];this.results.unshift(result);this.results=this.results.slice(0,20);save(KEYS.results,this.results);
    this.stats.gamesPlayed++;if(result.result==="WON")this.stats.gamesWon++;
    this.stats.bestScore=Math.max(this.stats.bestScore,result.score);
    if(result.result==="WON"&&(this.stats.fastestTime===null||result.timeUsed<this.stats.fastestTime))this.stats.fastestTime=result.timeUsed;
    if(this.stats.fewestMoves===null||result.moves<this.stats.fewestMoves)this.stats.fewestMoves=result.moves;
    this.stats.bestCombo=Math.max(this.stats.bestCombo,result.maxCombo);save(KEYS.statistics,this.stats);
    return result.result==="WON"&&(
      result.score===this.stats.bestScore ||
      result.timeUsed===this.stats.fastestTime ||
      result.moves===this.stats.fewestMoves ||
      result.maxCombo===this.stats.bestCombo
    );
  }
}

const ui={
  lobbyScreen:document.getElementById("lobbyScreen"),gameScreen:document.getElementById("gameScreen"),recordsScreen:document.getElementById("recordsScreen"),
  difficultyGrid:document.getElementById("difficultyGrid"),startBtn:document.getElementById("startBtn"),board:document.getElementById("board"),
  timeValue:document.getElementById("timeValue"),scoreValue:document.getElementById("scoreValue"),movesValue:document.getElementById("movesValue"),
  matchesValue:document.getElementById("matchesValue"),accuracyValue:document.getElementById("accuracyValue"),comboValue:document.getElementById("comboValue"),
  maxComboValue:document.getElementById("maxComboValue"),timeProgress:document.getElementById("timeProgress"),statusText:document.getElementById("statusText"),
  boardHeading:document.getElementById("boardHeading"),accuracyRing:document.getElementById("accuracyRing"),ringValue:document.getElementById("ringValue"),
  recentRuns:document.getElementById("recentRuns"),soundBtn:document.getElementById("soundBtn"),themeBtn:document.getElementById("themeBtn"),
  countdown:document.getElementById("countdown"),countdownNumber:document.getElementById("countdownNumber"),toast:document.getElementById("toast"),
  modalBackdrop:document.getElementById("modalBackdrop"),modalTitle:document.getElementById("modalTitle"),modalSub:document.getElementById("modalSub"),
  modalBody:document.getElementById("modalBody"),modalActions:document.getElementById("modalActions"),pauseBtn:document.getElementById("pauseBtn"),
  restartBtn:document.getElementById("restartBtn"),lobbyBtn:document.getElementById("lobbyBtn"),settingsBtn:document.getElementById("settingsBtn"),
  recordsBtn:document.getElementById("recordsBtn"),helpBtn:document.getElementById("helpBtn"),recordsBack:document.getElementById("recordsBack"),
  recordsSummary:document.getElementById("recordsSummary"),recordsTable:document.getElementById("recordsTable"),clearDataBtn:document.getElementById("clearDataBtn")
};

let game=new Game(ui);
let toastTimer=0;

function showScreen(id){
  [ui.lobbyScreen,ui.gameScreen,ui.recordsScreen].forEach(s=>s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}
function toast(message,type=""){
  clearTimeout(toastTimer);ui.toast.textContent=message;ui.toast.className=`toast show ${type}`;
  toastTimer=setTimeout(()=>ui.toast.className="toast",2600);
}
function showModal(title,sub,body,actions=[]){
  ui.modalTitle.textContent=title;ui.modalSub.textContent=sub||"";ui.modalBody.innerHTML=body;
  ui.modalActions.replaceChildren(...actions.map(({label,handler,primary=false,danger=false})=>{
    const b=document.createElement("button");b.className=`control-btn ${primary?"primary":""} ${danger?"danger":""}`;
    b.textContent=label;b.addEventListener("click",handler,{once:true});return b;
  }));
  ui.modalBackdrop.classList.add("open");
}
function closeModal(){ui.modalBackdrop.classList.remove("open");ui.modalActions.replaceChildren();}
ui.confirm=(title,sub,yes)=>{
  showModal(title,sub,"<div class='dialog-content'>This action cannot restore the current run.</div>",
    [{label:"CANCEL",handler:closeModal},{label:"CONFIRM",handler:()=>{closeModal();yes();},primary:true}]);
};
ui.showPause=()=>{showModal("MISSION PAUSED","TIMER SUSPENDED","<div class='dialog-content'>Your board is frozen and your remaining time is safe. Resume when ready.</div>",
  [{label:"RESUME",handler:()=>{closeModal();game.resume();},primary:true},{label:"RESTART",handler:()=>{closeModal();game.restart(true);}}]);};
ui.hidePause=closeModal;

ui.renderDifficulty=()=>{
  ui.difficultyGrid.replaceChildren(...Object.values(DIFFICULTIES).map(d=>{
    const b=document.createElement("button");b.type="button";b.className=`diff ${game.difficulty===d.id?"selected":""}`;
    b.setAttribute("role","radio");b.setAttribute("aria-checked",String(game.difficulty===d.id));
    b.innerHTML=`<div class="level">${d.id==="initiate"?"01":d.id==="pro"?"02":"03"} / ${d.name}</div><h3>${d.name}</h3><p>${d.description}</p><div class="diff-meta"><span>${d.pairs} PAIRS</span><span>${d.timeLimit} SEC</span><span>${d.rows}×${d.columns}</span></div>`;
    b.addEventListener("click",()=>game.setDifficulty(d.id));return b;
  }));
};
ui.renderBoard=(cards,d)=>{
  ui.board.style.gridTemplateColumns=`repeat(${d.columns},minmax(0,1fr))`;ui.board.replaceChildren();
  cards.forEach((card,index)=>{
    const b=document.createElement("button");b.className="memory-card";b.type="button";b.dataset.id=card.id;b.setAttribute("role","gridcell");
    b.setAttribute("aria-label",`Hidden memory card ${index+1}`);b.innerHTML=`<span class="inner"><span class="face back"><span class="back-symbol">✦</span></span><span class="face front"><span><span class="symbol">${card.symbol}</span><span class="card-name">${card.name}</span><span class="card-cat">${card.category}</span></span></span></span>`;
    b.addEventListener("click",()=>game.selectCard(card.id));ui.board.appendChild(b);
  });
};
function cardEl(card){return ui.board.querySelector(`[data-id="${CSS.escape(card.id)}"]`);}
ui.flipCard=(card)=>{const e=cardEl(card);if(!e)return;e.classList.add("flipped");e.setAttribute("aria-label",`${card.name}, ${card.category}`);};
ui.unflip=(a,b)=>[a,b].forEach(c=>{const e=cardEl(c);if(e){e.classList.remove("flipped","mismatch");e.setAttribute("aria-label","Hidden memory card");}});
ui.markMatched=(a,b)=>[a,b].forEach(c=>{const e=cardEl(c);if(e){e.classList.add("matched");e.disabled=true;e.setAttribute("aria-label",`${c.name}, matched`);}});
ui.markMismatch=(a,b)=>[a,b].forEach(c=>{const e=cardEl(c);if(e)e.classList.add("mismatch");});
ui.showScore=(amount,anchor)=>{
  const e=cardEl(anchor);if(!e)return;const r=e.getBoundingClientRect(),p=document.createElement("div");p.className="score-pop";p.textContent=`+${amount}`;
  p.style.left=`${r.left+r.width/2-18}px`;p.style.top=`${r.top+10}px`;document.body.appendChild(p);setTimeout(()=>p.remove(),850);
};
ui.onTick=()=>{};
ui.update=(g)=>{
  const d=DIFFICULTIES[g.difficulty],remaining=g.timer.getRemaining(),accuracy=g.moves?Math.round(g.matches/g.moves*100):100;
  ui.timeValue.textContent=formatTime(remaining);ui.timeValue.className=`stat-value timer-value ${remaining<=10?"critical":remaining<=20?"warning":""}`;
  ui.scoreValue.textContent=formatNumber(g.score);ui.movesValue.textContent=g.moves;ui.matchesValue.textContent=`${g.matches} / ${d.pairs}`;
  ui.accuracyValue.textContent=`${accuracy}%`;ui.comboValue.textContent=`×${g.combo}`;ui.maxComboValue.textContent=`×${g.maxCombo}`;
  ui.boardHeading.textContent=`MATRIX / ${d.name}`;ui.statusText.textContent=g.status;
  const pct=clamp(remaining/d.timeLimit*100,0,100);ui.timeProgress.style.width=`${pct}%`;ui.timeProgress.className=`progress ${remaining<=10?"critical":remaining<=20?"warning":""}`;
  ui.accuracyRing.style.setProperty("--accuracy",`${accuracy}%`);ui.ringValue.textContent=`${accuracy}%`;
  ui.pauseBtn.disabled=!["PLAYING","PAUSED"].includes(g.status);ui.pauseBtn.textContent=g.status==="PAUSED"?"▶ RESUME":"Ⅱ PAUSE";
  renderRecent();
};
function renderRecent(){
  const rs=Array.isArray(game.results)?game.results.slice(0,5):[];
  ui.recentRuns.replaceChildren(...(rs.length?rs.map(r=>{
    const row=document.createElement("div");row.className="recent-row";
    row.innerHTML=`<div><b class="${r.result==="WON"?"win":"loss"}">${r.result}</b><br><small>${DIFFICULTIES[r.difficulty].name} • ${r.moves} moves</small></div><strong>${formatNumber(r.score)}</strong>`;return row;
  }):[Object.assign(document.createElement("div"),{className:"recent-row",textContent:"No completed runs yet."})]));
}
function renderLobbyRecords(){
  const s=game.stats;
  document.getElementById("lobbyRecords").innerHTML=`<span class="mini-record">BEST SCORE <b>${formatNumber(s.bestScore)}</b></span><span class="mini-record">FASTEST <b>${s.fastestTime===null?"—":formatTime(s.fastestTime)}</b></span><span class="mini-record">WINS <b>${s.gamesWon}/${s.gamesPlayed}</b></span>`;
}
function renderRecords(){
  const s=game.stats,winRate=s.gamesPlayed?Math.round(s.gamesWon/s.gamesPlayed*100):0;
  ui.recordsSummary.innerHTML=`<div class="panel record-card"><b>${formatNumber(s.bestScore)}</b><span>BEST SCORE</span></div><div class="panel record-card"><b>${s.fastestTime===null?"—":formatTime(s.fastestTime)}</b><span>FASTEST WIN</span></div><div class="panel record-card"><b>${s.fewestMoves===null?"—":s.fewestMoves}</b><span>FEWEST MOVES</span></div><div class="panel record-card"><b>×${s.bestCombo}</b><span>BEST COMBO • ${winRate}% WIN RATE</span></div>`;
  ui.recordsTable.replaceChildren(...game.results.map(r=>{
    const tr=document.createElement("tr");const date=new Date(r.completedAt).toLocaleString();
    [r.result,DIFFICULTIES[r.difficulty].name,formatNumber(r.score),formatTime(r.timeUsed),r.moves,`${r.accuracy}%`,date].forEach((v,i)=>{const td=document.createElement("td");td.textContent=v;if(i===0)td.className=r.result==="WON"?"win":"loss";tr.appendChild(td);});return tr;
  }));
}
function openHelp(){
  showModal("HOW TO PLAY","MATCH. REMEMBER. MASTER.",
  `<div class="dialog-content"><p><strong>1.</strong> Choose a difficulty and start the mission.</p><p><strong>2.</strong> Flip two cards to reveal their symbols.</p><p><strong>3.</strong> Matching pairs stay open. Mismatches close again.</p><p><strong>4.</strong> Every move counts. Combos reward consecutive matches.</p><p><strong>5.</strong> Finish all pairs before the timer reaches zero.</p><p><strong>Keyboard:</strong> Tab to focus cards, Enter/Space to activate, P to pause, R to restart, M to toggle sound, Escape to close dialogs.</p></div>`,
  [{label:"CLOSE",handler:closeModal,primary:true}]);
}
function openSettings(){
  const s=game.settings;
  showModal("SETTINGS","PERSONALIZE YOUR MATRIX",
  `<div class="settings-list">
    <div class="setting-row"><span>Sound effects</span><button class="toggle ${s.soundEnabled?"on":""}" id="setSound" aria-label="Toggle sound"></button></div>
    <div class="setting-row"><span>Reduced visual effects</span><button class="toggle ${s.reducedEffects?"on":""}" id="setReduced" aria-label="Toggle reduced effects"></button></div>
    <div class="setting-row"><span>Confirm restart</span><button class="toggle ${s.confirmRestart?"on":""}" id="setConfirm" aria-label="Toggle restart confirmation"></button></div>
    <div class="setting-row"><span>Theme</span><button class="control-btn" id="setTheme">${s.theme==="dark"?"NEON NIGHT":"CYBER LIGHT"}</button></div>
  </div>
  <div class="dialog-content">Gameplay statistics are stored only in this browser. They are personal records and are not cryptographically verified.</div>`,
  [{label:"DONE",handler:closeModal,primary:true}]);
  document.getElementById("setSound").onclick=()=>{s.soundEnabled=!s.soundEnabled;save(KEYS.settings,s);game.applySettings();openSettings();};
  document.getElementById("setReduced").onclick=()=>{s.reducedEffects=!s.reducedEffects;save(KEYS.settings,s);openSettings();};
  document.getElementById("setConfirm").onclick=()=>{s.confirmRestart=!s.confirmRestart;save(KEYS.settings,s);openSettings();};
  document.getElementById("setTheme").onclick=()=>{s.theme=s.theme==="dark"?"light":"dark";save(KEYS.settings,s);game.applySettings();openSettings();};
}
ui.startBtn.onclick=()=>game.start();
ui.pauseBtn.onclick=()=>game.status==="PAUSED"?game.resume():game.pause();
ui.restartBtn.onclick=()=>game.restart();
ui.lobbyBtn.onclick=()=>{if(["PLAYING","PAUSED","COUNTDOWN","CHECKING"].includes(game.status)){game.confirmAndLobby=true;ui.confirm("RETURN TO LOBBY?","Your current run will be discarded.",()=>{game.resetData();showScreen("lobbyScreen");});}else showScreen("lobbyScreen");};
ui.settingsBtn.onclick=openSettings;
ui.soundBtn.onclick=()=>{game.settings.soundEnabled=!game.settings.soundEnabled;save(KEYS.settings,game.settings);game.applySettings();if(game.settings.soundEnabled)game.audio.click();};
ui.themeBtn.onclick=()=>{game.settings.theme=game.settings.theme==="dark"?"light":"dark";save(KEYS.settings,game.settings);game.applySettings();};
ui.recordsBtn.onclick=()=>{renderRecords();showScreen("recordsScreen");};
ui.recordsBack.onclick=()=>showScreen("lobbyScreen");
ui.helpBtn.onclick=openHelp;
ui.modalBackdrop.addEventListener("click",e=>{if(e.target===ui.modalBackdrop)closeModal();});
ui.clearDataBtn.onclick=()=>{
  showModal("CLEAR LOCAL DATA","THIS CANNOT BE UNDONE","<div class='dialog-content'>This removes Memory Matrix settings, statistics, and personal records from this browser.</div>",
    [{label:"CANCEL",handler:closeModal},{label:"CLEAR DATA",handler:()=>{remove(KEYS.settings);remove(KEYS.statistics);remove(KEYS.results);game.settings=clone(DEFAULT_SETTINGS);game.stats=clone(DEFAULT_STATS);game.results=[];game.applySettings();renderRecords();renderLobbyRecords();closeModal();toast("Local data cleared.");},danger:true}]);
};

document.addEventListener("keydown",e=>{
  if(e.key==="Escape"){if(ui.modalBackdrop.classList.contains("open"))closeModal();return;}
  const tag=(e.target?.tagName||"").toLowerCase();if(tag==="input"||tag==="textarea")return;
  if(e.key.toLowerCase()==="m"){e.preventDefault();ui.soundBtn.click();}
  if(e.key.toLowerCase()==="p"&&["PLAYING","PAUSED"].includes(game.status)){e.preventDefault();ui.pauseBtn.click();}
  if(e.key.toLowerCase()==="r"&&["PLAYING","PAUSED","WON","LOST"].includes(game.status)){e.preventDefault();game.restart();}
});

ui.renderDifficulty();renderRecent();renderLobbyRecords();
if(!hasStorage)toast("Local statistics are unavailable. Gameplay is still available.","warn");
window.addEventListener("pagehide",()=>{game.timer.stop();});
})();
</script>
</body>
</html>
"""

st.markdown(
    """
    <style>
    .stApp { background: #050b18; }
    header[data-testid="stHeader"] { background: transparent; }
    div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
    section.main > div { padding-top: 0; }
    iframe { border: 0 !important; width: 100% !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(GAME_HTML, height=1180, scrolling=False)
