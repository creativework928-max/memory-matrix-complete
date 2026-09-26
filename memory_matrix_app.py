"""
MEMORY MATRIX
A polished, responsive, accessible browser memory game served by Flask.

Run:
    pip install flask
    python app.py

Then open:
    http://127.0.0.1:5000

The browser owns the game state. Flask provides the shell, configuration,
health endpoint, and a small API surface so the game remains fast and
real-time without round trips for every card click.
"""

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

GAME_CONFIG = {
    "name": "Memory Matrix",
    "version": "1.0.0",
    "levels": {
        "easy": {"label": "Easy", "size": 4, "pairs": 8, "time": 75},
        "medium": {"label": "Medium", "size": 5, "pairs": 12, "time": 105},
        "hard": {"label": "Hard", "size": 6, "pairs": 18, "time": 150},
    },
    "theme": {
        "accent": "#7c5cff",
        "cyan": "#22d3ee",
        "green": "#34d399",
        "gold": "#fbbf24",
        "danger": "#fb7185",
    },
}

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#070a16">
<meta name="description" content="Memory Matrix — a fast, polished memory matching game.">
<title>Memory Matrix</title>
<style>
:root{
  --bg:#070a16;--surface:#0e1427;--surface2:#141c34;--surface3:#1a2441;
  --text:#f8fafc;--muted:#94a3b8;--line:rgba(148,163,184,.17);
  --accent:#7c5cff;--cyan:#22d3ee;--green:#34d399;--gold:#fbbf24;--danger:#fb7185;
  --shadow:0 24px 70px rgba(0,0,0,.38);--radius:22px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;min-height:100vh;color:var(--text);
  font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:
    radial-gradient(circle at 15% 0%,rgba(124,92,255,.20),transparent 34rem),
    radial-gradient(circle at 90% 10%,rgba(34,211,238,.12),transparent 30rem),
    linear-gradient(145deg,#050713,#0a0e1d 48%,#080b18);
  overflow-x:hidden;
}
button{font:inherit}
button:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--cyan);outline-offset:3px}
.app{width:min(1240px,calc(100% - 28px));margin:auto;padding:24px 0 42px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:22px}
.brand{display:flex;align-items:center;gap:13px}
.logo{
  width:46px;height:46px;border-radius:15px;display:grid;place-items:center;
  background:linear-gradient(135deg,var(--accent),var(--cyan));box-shadow:0 10px 32px rgba(124,92,255,.32);
  font-size:23px;font-weight:900;
}
.brand h1{font-size:18px;letter-spacing:.14em;margin:0}
.brand p{margin:2px 0 0;color:var(--muted);font-size:11px;letter-spacing:.16em;text-transform:uppercase}
.actions{display:flex;gap:9px}
.icon-btn,.control-btn{
  border:1px solid var(--line);background:rgba(20,28,52,.8);color:var(--text);
  border-radius:13px;padding:10px 13px;cursor:pointer;transition:.2s ease;
}
.icon-btn:hover,.control-btn:hover{transform:translateY(-1px);border-color:rgba(124,92,255,.55);background:var(--surface3)}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:18px}
.panel{
  background:linear-gradient(180deg,rgba(20,28,52,.84),rgba(10,14,29,.92));
  border:1px solid var(--line);box-shadow:var(--shadow);border-radius:var(--radius);
}
.game-panel{padding:20px}
.hero{display:flex;align-items:flex-end;justify-content:space-between;gap:15px;margin-bottom:17px}
.kicker{color:var(--cyan);font-size:11px;font-weight:800;letter-spacing:.18em;text-transform:uppercase}
.hero h2{font-size:clamp(25px,4vw,42px);line-height:1.02;margin:7px 0 0;letter-spacing:-.04em}
.hero p{color:var(--muted);margin:8px 0 0;font-size:14px}
.levels{display:flex;gap:7px;flex-wrap:wrap}
.level{
  border:1px solid var(--line);background:var(--surface);color:var(--muted);
  border-radius:999px;padding:8px 12px;font-size:12px;font-weight:800;cursor:pointer;
}
.level.active{color:white;border-color:rgba(124,92,255,.7);background:rgba(124,92,255,.16);box-shadow:0 0 0 3px rgba(124,92,255,.07)}
.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px}
.stat{padding:12px 14px;border:1px solid var(--line);border-radius:16px;background:rgba(8,12,26,.55)}
.stat span{display:block;color:var(--muted);font-size:10px;letter-spacing:.14em;text-transform:uppercase}
.stat strong{display:block;margin-top:3px;font-size:21px}
#timer.warn{color:var(--gold)}#timer.danger{color:var(--danger)}
.progress{height:5px;background:#202941;border-radius:999px;overflow:hidden;margin-bottom:16px}
.progress i{display:block;height:100%;width:100%;background:linear-gradient(90deg,var(--accent),var(--cyan));transition:width .25s linear}
.board-wrap{display:grid;place-items:center;min-height:400px;padding:6px}
.board{
  width:min(100%,680px);display:grid;gap:9px;perspective:1000px;
}
.card{aspect-ratio:1;border:0;background:transparent;padding:0;cursor:pointer;position:relative;min-width:0}
.card:disabled{cursor:default}
.card-inner{position:absolute;inset:0;transform-style:preserve-3d;transition:transform .42s cubic-bezier(.2,.75,.2,1)}
.card.flipped .card-inner,.card.matched .card-inner{transform:rotateY(180deg)}
.face{
  position:absolute;inset:0;border-radius:15px;backface-visibility:hidden;
  display:grid;place-items:center;border:1px solid rgba(255,255,255,.09);
}
.back{
  background:
    linear-gradient(135deg,rgba(124,92,255,.19),rgba(34,211,238,.08)),
    repeating-linear-gradient(45deg,transparent 0 8px,rgba(255,255,255,.025) 8px 9px),
    #11182d;
  box-shadow:inset 0 0 24px rgba(124,92,255,.08);
}
.back::after{content:"";width:34%;aspect-ratio:1;border:2px solid rgba(148,163,184,.25);border-radius:9px;transform:rotate(45deg)}
.front{transform:rotateY(180deg);font-size:clamp(22px,5vw,40px);background:linear-gradient(145deg,#1b2746,#10172b);box-shadow:inset 0 0 25px rgba(255,255,255,.035)}
.card:hover:not(.flipped):not(.matched) .back{border-color:rgba(34,211,238,.5);transform:translateY(-2px)}
.card.matched .front{border-color:rgba(52,211,153,.55);box-shadow:0 0 24px rgba(52,211,153,.14),inset 0 0 25px rgba(52,211,153,.06)}
.card.matched{animation:matchPop .45s ease}
@keyframes matchPop{45%{transform:scale(1.06)}}
.controls{display:flex;justify-content:center;gap:9px;margin-top:16px;flex-wrap:wrap}
.primary{border:0;border-radius:13px;padding:11px 17px;color:white;background:linear-gradient(135deg,var(--accent),#5c7cff);font-weight:800;cursor:pointer;box-shadow:0 9px 25px rgba(124,92,255,.25)}
.secondary{border:1px solid var(--line);border-radius:13px;padding:10px 16px;color:var(--text);background:var(--surface);font-weight:700;cursor:pointer}
.side{padding:18px;display:flex;flex-direction:column;gap:13px}
.side h3{margin:0;font-size:14px;letter-spacing:.08em;text-transform:uppercase}
.side-section{padding:15px;border:1px solid var(--line);border-radius:17px;background:rgba(7,10,22,.5)}
.mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:11px}
.mini{padding:11px;border-radius:12px;background:rgba(255,255,255,.035)}
.mini span{display:block;color:var(--muted);font-size:10px}.mini b{font-size:18px}
.tips{padding-left:17px;color:var(--muted);font-size:12px;line-height:1.7;margin:10px 0 0}
.badges{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.badge{padding:6px 8px;border-radius:999px;background:rgba(124,92,255,.1);border:1px solid rgba(124,92,255,.2);font-size:10px;color:#c4b5fd}
.toast{
  position:fixed;left:50%;bottom:24px;transform:translate(-50%,20px);opacity:0;pointer-events:none;
  padding:11px 16px;border-radius:12px;background:#121a31;border:1px solid var(--line);box-shadow:var(--shadow);
  transition:.25s ease;font-size:13px;z-index:20
}
.toast.show{opacity:1;transform:translate(-50%,0)}
.modal-backdrop{position:fixed;inset:0;background:rgba(2,4,12,.72);backdrop-filter:blur(9px);display:none;place-items:center;padding:20px;z-index:10}
.modal-backdrop.open{display:grid}
.modal{width:min(480px,100%);padding:25px;border-radius:24px;background:#0e1529;border:1px solid var(--line);box-shadow:var(--shadow)}
.modal h2{margin:0 0 8px;font-size:28px}.modal p{color:var(--muted);line-height:1.6}
.result-score{font-size:64px;font-weight:900;letter-spacing:-.06em;background:linear-gradient(90deg,var(--cyan),#a78bfa);color:transparent;background-clip:text}
.result-meta{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:15px 0}
.result-meta div{padding:12px;background:rgba(255,255,255,.035);border-radius:13px;text-align:center}
.result-meta span{display:block;color:var(--muted);font-size:10px}.result-meta b{font-size:18px}
.modal-actions{display:flex;gap:8px;margin-top:18px}.modal-actions>*{flex:1}
.visually-hidden{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media(max-width:900px){.layout{grid-template-columns:1fr}.side{display:grid;grid-template-columns:1fr 1fr}.side-section:last-child{grid-column:1/-1}}
@media(max-width:620px){
  .app{width:min(100% - 16px,600px);padding-top:12px}.game-panel{padding:12px}.topbar{margin-bottom:13px}
  .hero{align-items:flex-start;flex-direction:column}.hero h2{font-size:31px}.hud{grid-template-columns:repeat(2,1fr)}
  .board{gap:5px}.front,.back{border-radius:9px}.board-wrap{min-height:0;padding:2px}
  .side{display:flex;padding:12px}.actions .secondary-label{display:none}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{scroll-behavior:auto!important;animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}
}
</style>
</head>
<body>
<main class="app">
  <header class="topbar">
    <div class="brand">
      <div class="logo" aria-hidden="true">M</div>
      <div><h1>MEMORY MATRIX</h1><p>Focus · Recall · Master</p></div>
    </div>
    <div class="actions">
      <button class="icon-btn" id="soundBtn" aria-label="Toggle sound">🔊</button>
      <button class="icon-btn" id="themeBtn" aria-label="Toggle visual theme">◐</button>
    </div>
  </header>

  <section class="layout">
    <section class="panel game-panel" aria-label="Memory Matrix game">
      <div class="hero">
        <div>
          <div class="kicker">ANALYZE YOUR MEMORY</div>
          <h2>Find every matching pair.</h2>
          <p>Flip two cards, remember their positions, and clear the matrix before time runs out.</p>
        </div>
        <div class="levels" role="group" aria-label="Difficulty">
          <button class="level active" data-level="easy">Easy</button>
          <button class="level" data-level="medium">Medium</button>
          <button class="level" data-level="hard">Hard</button>
        </div>
      </div>

      <div class="hud" aria-live="polite">
        <div class="stat"><span>Time</span><strong id="timer">01:15</strong></div>
        <div class="stat"><span>Moves</span><strong id="moves">0</strong></div>
        <div class="stat"><span>Pairs</span><strong id="pairs">0 / 8</strong></div>
        <div class="stat"><span>Score</span><strong id="score">0</strong></div>
      </div>
      <div class="progress" aria-label="Remaining time"><i id="timeProgress"></i></div>

      <div class="board-wrap">
        <div class="board" id="board" role="grid" aria-label="Memory card grid"></div>
      </div>

      <div class="controls">
        <button class="primary" id="newGame">New Game</button>
        <button class="secondary" id="pauseGame">Pause</button>
        <button class="secondary" id="resetStats">Reset Stats</button>
      </div>
    </section>

    <aside class="panel side" aria-label="Game information">
      <section class="side-section">
        <h3>Session</h3>
        <div class="mini-grid">
          <div class="mini"><span>Best Score</span><b id="bestScore">0</b></div>
          <div class="mini"><span>Best Time</span><b id="bestTime">—</b></div>
          <div class="mini"><span>Games</span><b id="gamesPlayed">0</b></div>
          <div class="mini"><span>Win Rate</span><b id="winRate">0%</b></div>
        </div>
      </section>
      <section class="side-section">
        <h3>Memory Lab</h3>
        <ul class="tips">
          <li>Group cards mentally by position.</li>
          <li>Use the first few turns to map the grid.</li>
          <li>Avoid random clicks once you know a location.</li>
          <li>Accuracy is worth more than speed.</li>
        </ul>
        <div class="badges">
          <span class="badge">NO ADS</span><span class="badge">LOCAL SAVE</span><span class="badge">KEYBOARD</span>
        </div>
      </section>
      <section class="side-section">
        <h3>Keyboard</h3>
        <p style="color:var(--muted);font-size:12px;line-height:1.6;margin:10px 0 0">
          Use <b>Tab</b> to navigate cards. Press <b>Enter</b> or <b>Space</b> to flip.
          <br>Press <b>P</b> to pause and <b>R</b> to restart.
        </p>
      </section>
    </aside>
  </section>
</main>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<div class="modal-backdrop" id="modalBackdrop" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <div class="modal">
    <div class="kicker" id="modalKicker">MATRIX COMPLETE</div>
    <h2 id="modalTitle">Excellent recall.</h2>
    <div class="result-score" id="resultScore">0</div>
    <p id="resultText">You cleared the matrix.</p>
    <div class="result-meta">
      <div><span>Moves</span><b id="resultMoves">0</b></div>
      <div><span>Time Left</span><b id="resultTime">0s</b></div>
      <div><span>Accuracy</span><b id="resultAccuracy">0%</b></div>
    </div>
    <div class="modal-actions">
      <button class="secondary" id="closeModal">Close</button>
      <button class="primary" id="playAgain">Play Again</button>
    </div>
  </div>
</div>

<script>
"use strict";

const CONFIG = __CONFIG__;

const SYMBOLS = [
  "◆","●","▲","■","★","✦","✚","⬟","⬢","☀","☾","♥",
  "♣","♠","♦","☘","⚡","✿","❖","◎","◉","⬡","✧","✪"
];

const STORAGE = {
  stats: "memory-matrix.stats.v1",
  sound: "memory-matrix.sound.v1",
  theme: "memory-matrix.theme.v1",
  difficulty: "memory-matrix.difficulty.v1"
};

const $ = (s) => document.querySelector(s);

const state = {
  level: localStorage.getItem(STORAGE.difficulty) || "easy",
  cards: [],
  first: null,
  second: null,
  lock: false,
  paused: false,
  running: false,
  moves: 0,
  matches: 0,
  score: 0,
  startedAt: 0,
  elapsed: 0,
  remaining: 0,
  interval: null,
  sound: localStorage.getItem(STORAGE.sound) !== "off",
  theme: localStorage.getItem(STORAGE.theme) || "dark",
};

let stats = loadStats();
let audioCtx = null;

function loadStats(){
  try {
    return Object.assign({games:0,wins:0,bestScore:0,bestTime:null}, JSON.parse(localStorage.getItem(STORAGE.stats) || "{}"));
  } catch { return {games:0,wins:0,bestScore:0,bestTime:null}; }
}
function saveStats(){ localStorage.setItem(STORAGE.stats, JSON.stringify(stats)); }
function shuffle(a){
  const x = [...a];
  for(let i=x.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [x[i],x[j]]=[x[j],x[i]]; }
  return x;
}
function formatTime(s){
  s=Math.max(0,Math.ceil(s)); return `${String(Math.floor(s/60)).padStart(2,"0")}:${String(s%60).padStart(2,"0")}`;
}
function levelCfg(){ return CONFIG.levels[state.level]; }

function updateStatsPanel(){
  $("#bestScore").textContent = stats.bestScore.toLocaleString();
  $("#bestTime").textContent = stats.bestTime == null ? "—" : formatTime(stats.bestTime);
  $("#gamesPlayed").textContent = stats.games;
  $("#winRate").textContent = stats.games ? Math.round(stats.wins/stats.games*100)+"%" : "0%";
}

function toast(message){
  const el=$("#toast"); el.textContent=message; el.classList.add("show");
  clearTimeout(toast.timer); toast.timer=setTimeout(()=>el.classList.remove("show"),1800);
}

function beep(freq=440,duration=.07,type="sine"){
  if(!state.sound) return;
  try{
    audioCtx ||= new (window.AudioContext||window.webkitAudioContext)();
    const o=audioCtx.createOscillator(), g=audioCtx.createGain();
    o.type=type;o.frequency.value=freq;g.gain.setValueAtTime(.045,audioCtx.currentTime);
    g.gain.exponentialRampToValueAtTime(.001,audioCtx.currentTime+duration);
    o.connect(g);g.connect(audioCtx.destination);o.start();o.stop(audioCtx.currentTime+duration);
  }catch{}
}

function buildDeck(){
  const pairs=levelCfg().pairs;
  const values=shuffle(SYMBOLS).slice(0,pairs);
  return shuffle(values.flatMap((value,id)=>[
    {id:`${id}-a`,pair:id,value,flipped:false,matched:false},
    {id:`${id}-b`,pair:id,value,flipped:false,matched:false}
  ]));
}

function startGame(){
  clearInterval(state.interval);
  const cfg=levelCfg();
  state.cards=buildDeck(); state.first=null;state.second=null;state.lock=false;
  state.paused=false;state.running=true;state.moves=0;state.matches=0;state.score=0;
  state.elapsed=0;state.remaining=cfg.time;state.startedAt=Date.now();
  stats.games++; saveStats(); updateStatsPanel();
  renderBoard(); updateHUD(); startClock();
  $("#pauseGame").textContent="Pause";
  toast(`${cfg.label} matrix ready`);
}

function startClock(){
  state.interval=setInterval(()=>{
    if(!state.running || state.paused) return;
    state.elapsed=(Date.now()-state.startedAt)/1000;
    state.remaining=Math.max(0,levelCfg().time-state.elapsed);
    updateHUD();
    if(state.remaining<=0) endGame(false,"Time expired");
  },250);
}

function updateHUD(){
  const cfg=levelCfg();
  $("#timer").textContent=formatTime(state.remaining);
  $("#timer").classList.toggle("warn",state.remaining<=20 && state.remaining>8);
  $("#timer").classList.toggle("danger",state.remaining<=8);
  $("#moves").textContent=state.moves;
  $("#pairs").textContent=`${state.matches} / ${cfg.pairs}`;
  $("#score").textContent=Math.max(0,state.score).toLocaleString();
  $("#timeProgress").style.width=`${Math.max(0,state.remaining/cfg.time*100)}%`;
}

function renderBoard(){
  const board=$("#board"); board.innerHTML="";
  const n=levelCfg().size;
  board.style.gridTemplateColumns=`repeat(${n},1fr)`;
  state.cards.forEach((card,index)=>{
    const btn=document.createElement("button");
    btn.className="card"; btn.type="button"; btn.dataset.index=index;
    btn.setAttribute("role","gridcell"); btn.setAttribute("aria-label",`Hidden card ${index+1}`);
    btn.innerHTML=`<span class="card-inner">
      <span class="face back" aria-hidden="true"></span>
      <span class="face front" aria-hidden="true">${card.value}</span>
    </span>`;
    btn.addEventListener("click",()=>flipCard(index));
    board.appendChild(btn);
  });
}

function setCardVisual(index){
  const card=state.cards[index], el=$("#board").children[index];
  if(!el)return;
  el.classList.toggle("flipped",card.flipped||card.matched);
  el.classList.toggle("matched",card.matched);
  el.setAttribute("aria-label",card.matched?`Matched ${card.value}`:(card.flipped?`Revealed ${card.value}`:`Hidden card ${index+1}`));
}

function flipCard(index){
  if(!state.running || state.paused || state.lock) return;
  const card=state.cards[index];
  if(!card || card.flipped || card.matched) return;
  if(state.first===index) return;
  card.flipped=true; setCardVisual(index); beep(520,.045,"triangle");
  if(state.first===null){ state.first=index; return; }
  state.second=index; state.lock=true; state.moves++;
  const a=state.cards[state.first],b=state.cards[state.second];
  if(a.pair===b.pair){
    a.matched=b.matched=true; state.matches++;
    const timeBonus=Math.round(state.remaining*2);
    const moveBonus=Math.max(10,90-state.moves*2);
    state.score += 100+timeBonus+moveBonus;
    setTimeout(()=>{setCardVisual(state.first);setCardVisual(state.second);beep(780,.12,"sine");resetTurn(); if(state.matches===levelCfg().pairs) endGame(true,"Every pair found.");},180);
  }else{
    state.score=Math.max(0,state.score-4);
    setTimeout(()=>{
      a.flipped=b.flipped=false;setCardVisual(state.first);setCardVisual(state.second);
      beep(180,.10,"sawtooth");resetTurn();
    },650);
  }
  updateHUD();
}
function resetTurn(){state.first=null;state.second=null;state.lock=false;updateHUD()}

function togglePause(){
  if(!state.running)return;
  state.paused=!state.paused;
  $("#pauseGame").textContent=state.paused?"Resume":"Pause";
  toast(state.paused?"Game paused":"Game resumed");
}
function endGame(won,message){
  if(!state.running)return;
  state.running=false;clearInterval(state.interval);
  if(won){
    stats.wins++;
    if(state.score>stats.bestScore)stats.bestScore=state.score;
    const elapsed=Math.max(0,levelCfg().time-state.remaining);
    if(stats.bestTime==null || elapsed<stats.bestTime)stats.bestTime=Math.round(elapsed);
  }
  saveStats();updateStatsPanel();
  $("#modalKicker").textContent=won?"MATRIX COMPLETE":"TIME OUT";
  $("#modalTitle").textContent=won?"Excellent recall.":"The matrix won this round.";
  $("#resultScore").textContent=Math.max(0,state.score).toLocaleString();
  $("#resultText").textContent=message;
  $("#resultMoves").textContent=state.moves;
  $("#resultTime").textContent=formatTime(state.remaining);
  const accuracy=state.moves?Math.round(state.matches/state.moves*100):0;
  $("#resultAccuracy").textContent=accuracy+"%";
  $("#modalBackdrop").classList.add("open");
  $("#playAgain").focus();
  beep(won?880:130,.18,won?"sine":"sawtooth");
}
function closeModal(){$("#modalBackdrop").classList.remove("open");}
function selectLevel(level){
  if(!CONFIG.levels[level])return;
  state.level=level;localStorage.setItem(STORAGE.difficulty,level);
  document.querySelectorAll(".level").forEach(b=>b.classList.toggle("active",b.dataset.level===level));
  startGame();
}
function toggleTheme(){
  state.theme=state.theme==="dark"?"midnight":"dark";
  localStorage.setItem(STORAGE.theme,state.theme);
  document.documentElement.style.filter=state.theme==="midnight"?"saturate(.82) brightness(.92)":"none";
}
function toggleSound(){
  state.sound=!state.sound;localStorage.setItem(STORAGE.sound,state.sound?"on":"off");
  $("#soundBtn").textContent=state.sound?"🔊":"🔇";toast(state.sound?"Sound enabled":"Sound muted");
}
function resetStatistics(){
  if(!confirm("Reset all locally saved statistics?"))return;
  stats={games:0,wins:0,bestScore:0,bestTime:null};saveStats();updateStatsPanel();toast("Statistics reset");
}

$("#newGame").addEventListener("click",startGame);
$("#pauseGame").addEventListener("click",togglePause);
$("#resetStats").addEventListener("click",resetStatistics);
$("#soundBtn").addEventListener("click",toggleSound);
$("#themeBtn").addEventListener("click",toggleTheme);
$("#closeModal").addEventListener("click",closeModal);
$("#playAgain").addEventListener("click",()=>{closeModal();startGame()});
$("#modalBackdrop").addEventListener("click",e=>{if(e.target.id==="modalBackdrop")closeModal()});
document.querySelectorAll(".level").forEach(b=>b.addEventListener("click",()=>selectLevel(b.dataset.level)));
document.addEventListener("keydown",e=>{
  if(e.key.toLowerCase()==="p"){e.preventDefault();togglePause()}
  if(e.key.toLowerCase()==="r"){e.preventDefault();startGame()}
  if(e.key==="Escape" && $("#modalBackdrop").classList.contains("open"))closeModal();
});
document.querySelectorAll(".level").forEach(b=>b.classList.toggle("active",b.dataset.level===state.level));
$("#soundBtn").textContent=state.sound?"🔊":"🔇";
updateStatsPanel();
startGame();
</script>
</body>
</html>"""

PAGE = HTML.replace("__CONFIG__", __import__("json").dumps(GAME_CONFIG))

@app.get("/")
def index():
    return render_template_string(PAGE)

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "app": GAME_CONFIG["name"], "version": GAME_CONFIG["version"]})

@app.get("/api/config")
def config():
    return jsonify(GAME_CONFIG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
