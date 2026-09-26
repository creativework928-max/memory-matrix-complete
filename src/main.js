import "./styles/base.css";

import { DIFFICULTIES, DEFAULT_DIFFICULTY, GAME_STATES } from "./config/gameConfig.js";
import { DEFAULT_SETTINGS } from "./config/storageKeys.js";
import { Game } from "./core/Game.js";
import { AudioService } from "./services/AudioService.js";
import { StatisticsService } from "./services/StatisticsService.js";
import { StorageService } from "./services/StorageService.js";
import { BoardRenderer } from "./ui/BoardRenderer.js";
import { HUDRenderer } from "./ui/HUDRenderer.js";
import { ModalManager } from "./ui/ModalManager.js";
import { ThemeManager } from "./ui/ThemeManager.js";
import { ToastManager } from "./ui/ToastManager.js";
import { $, $all } from "./utils/dom.js";
import { formatNumber, formatSeconds } from "./utils/format.js";

const storage = new StorageService();
const settings = storage.getSettings();
const audio = new AudioService({ enabled: settings.soundEnabled });
const statistics = new StatisticsService(storage);
const themeManager = new ThemeManager();
const modalManager = new ModalManager();
const toastManager = new ToastManager($("#toast-region"));

const state = {
  difficulty: DEFAULT_DIFFICULTY,
  currentView: "lobby",
  settings: {
    ...DEFAULT_SETTINGS,
    ...settings,
  },
};

let game = null;
let boardRenderer;
let hudRenderer;
let resultRecorded = false;

const elements = {
  lobbyView: $("#lobby-view"),
  gameView: $("#game-view"),
  statisticsView: $("#statistics-view"),
  difficultyGrid: $("#difficulty-grid"),
  startButton: $("#start-button"),
  soundToggle: $("#sound-toggle"),
  themeToggle: $("#theme-toggle"),
  settingsButton: $("#settings-button"),
  howToPlayButton: $("#how-to-play-button"),
  statisticsButton: $("#statistics-button"),
  statisticsBack: $("#statistics-back"),
  pauseButton: $("#pause-button"),
  restartButton: $("#restart-button"),
  board: $("#memory-board"),
  gameStatus: $("#game-status"),
  difficultyLabel: $("#game-difficulty-label"),
  activeModeName: $("#active-mode-name"),
  activeModeDescription: $("#active-mode-description"),
  countdownOverlay: $("#countdown-overlay"),
  countdownValue: $("#countdown-value"),
  pauseModal: $("#pause-modal"),
  resumeButton: $("#resume-button"),
  pauseRestart: $("#pause-restart"),
  pauseExit: $("#pause-exit"),
  resultModal: $("#result-modal"),
  resultPlayAgain: $("#result-play-again"),
  resultStatistics: $("#result-statistics"),
  resultChangeDifficulty: $("#result-change-difficulty"),
  resultEyebrow: $("#result-eyebrow"),
  resultTitle: $("#result-title"),
  resultSubtitle: $("#result-subtitle"),
  resultScore: $("#result-score"),
  resultTime: $("#result-time"),
  resultMoves: $("#result-moves"),
  resultAccuracy: $("#result-accuracy"),
  resultCombo: $("#result-combo"),
  resultTimeBonus: $("#result-time-bonus"),
  newRecord: $("#new-record"),
  settingsSound: $("#settings-sound"),
  settingsReducedEffects: $("#settings-reduced-effects"),
  settingsTheme: $("#settings-theme"),
  settingsHowToPlay: $("#settings-how-to-play"),
  settingsClearData: $("#settings-clear-data"),
  clearRecordsButton: $("#clear-records-button"),
  confirmYes: $("#confirm-yes"),
  confirmNo: $("#confirm-no"),
  hud: {
    time: $("#time-value"),
    score: $("#score-value"),
    moves: $("#moves-value"),
    matches: $("#matches-value"),
    combo: $("#combo-value"),
    accuracy: $("#accuracy-value"),
    progress: $("#time-progress"),
    timerCard: $(".hud-card--timer"),
    timerStatus: $("#timer-status"),
  },
};

boardRenderer = new BoardRenderer(elements.board, {
  onCardSelect: (cardId) => game?.selectCard(cardId),
});

hudRenderer = new HUDRenderer(elements.hud);

themeManager.setTheme(state.settings.theme);
syncSettingsControls();
renderDifficultyCards();
renderLobbyStats();
bindEvents();

function createGame() {
  if (game) {
    game.stop();
  }

  const config = DIFFICULTIES[state.difficulty];

  game = new Game({
    difficulty: state.difficulty,
    audio,
    statistics,
    reducedMotion: state.settings.reducedEffects,
    onStateChange: renderGame,
    onEvent: handleGameEvent,
  });

  game.initialize();

  elements.difficultyLabel.textContent = config.name;
  elements.activeModeName.textContent = config.name;
  elements.activeModeDescription.textContent = config.description;
}

function bindEvents() {
  elements.difficultyGrid.addEventListener("click", (event) => {
    const button = event.target.closest("[data-difficulty]");

    if (!button) {
      return;
    }

    selectDifficulty(button.dataset.difficulty);
  });

  elements.startButton.addEventListener("click", () => startMission());

  elements.soundToggle.addEventListener("click", () => {
    const enabled = audio.toggle();

    state.settings.soundEnabled = enabled;
    persistSettings();

    syncSettingsControls();
    toastManager.show(enabled ? "Sound enabled." : "Sound muted.");
  });

  elements.themeToggle.addEventListener("click", () => {
    state.settings.theme = themeManager.toggle(state.settings.theme);
    persistSettings();
    syncSettingsControls();
  });

  elements.settingsButton.addEventListener("click", () => {
    syncSettingsControls();
    modalManager.open("settings-modal");
  });

  elements.howToPlayButton.addEventListener("click", () => {
    modalManager.open("how-to-play-modal");
  });

  elements.statisticsButton.addEventListener("click", () => {
    showStatistics();
  });

  elements.statisticsBack.addEventListener("click", () => {
    showLobby();
  });

  elements.pauseButton.addEventListener("click", () => togglePause());

  elements.restartButton.addEventListener("click", () => requestRestart());

  elements.resumeButton.addEventListener("click", () => {
    game?.resume();
    modalManager.close("pause-modal");
  });

  elements.pauseRestart.addEventListener("click", () => {
    modalManager.close("pause-modal");
    requestRestart();
  });

  elements.pauseExit.addEventListener("click", () => {
    modalManager.close("pause-modal");
    game?.stop();
    showLobby();
  });

  elements.resultPlayAgain.addEventListener("click", () => {
    modalManager.close("result-modal");
    startMission();
  });

  elements.resultStatistics.addEventListener("click", () => {
    modalManager.close("result-modal");
    showStatistics();
  });

  elements.resultChangeDifficulty.addEventListener("click", () => {
    modalManager.close("result-modal");
    showLobby();
  });

  elements.settingsSound.addEventListener("change", (event) => {
    state.settings.soundEnabled = event.target.checked;
    audio.setEnabled(state.settings.soundEnabled);
    persistSettings();
    syncSettingsControls();
  });

  elements.settingsReducedEffects.addEventListener("change", (event) => {
    state.settings.reducedEffects = event.target.checked;
    persistSettings();
    boardRenderer.setReducedMotion(state.settings.reducedEffects);
  });

  elements.settingsTheme.addEventListener("change", (event) => {
    state.settings.theme = event.target.value;
    themeManager.setTheme(state.settings.theme);
    persistSettings();
  });

  elements.settingsHowToPlay.addEventListener("click", () => {
    modalManager.close("settings-modal");
    modalManager.open("how-to-play-modal");
  });

  elements.settingsClearData.addEventListener("click", () => {
    modalManager.confirm({
      title: "Clear local data?",
      message: "All personal records and preferences owned by Memory Matrix will be removed.",
      confirmText: "CLEAR DATA",
      onConfirm: () => {
        statistics.clearAll();
        Object.assign(state.settings, DEFAULT_SETTINGS);
        audio.setEnabled(false);
        themeManager.setTheme("neon");
        persistSettings();
        syncSettingsControls();
        renderLobbyStats();
        renderStatistics();
        toastManager.show("Local data cleared.", { type: "success" });
      },
    });
  });

  elements.clearRecordsButton.addEventListener("click", () => {
    modalManager.confirm({
      title: "Clear records?",
      message: "Your local mission history will be deleted.",
      confirmText: "CLEAR RECORDS",
      onConfirm: () => {
        statistics.clearRecords();
        renderStatistics();
        toastManager.show("Mission history cleared.", { type: "success" });
      },
    });
  });

  elements.confirmYes.addEventListener("click", () => modalManager.resolveConfirm());
  elements.confirmNo.addEventListener("click", () => modalManager.cancelConfirm());

  document.addEventListener("keydown", handleKeyboard);
}

function handleKeyboard(event) {
  const target = event.target;

  if (
    target instanceof HTMLInputElement ||
    target instanceof HTMLTextAreaElement ||
    target instanceof HTMLSelectElement
  ) {
    return;
  }

  if (event.key === "Escape") {
    modalManager.closeAll();
    return;
  }

  if (!game) {
    return;
  }

  if (event.key.toLowerCase() === "p") {
    event.preventDefault();
    togglePause();
  }

  if (event.key.toLowerCase() === "r") {
    event.preventDefault();
    requestRestart();
  }

  if (event.key.toLowerCase() === "m") {
    event.preventDefault();
    const enabled = audio.toggle();
    state.settings.soundEnabled = enabled;
    persistSettings();
    syncSettingsControls();
  }
}

function selectDifficulty(difficulty) {
  if (!DIFFICULTIES[difficulty]) {
    return;
  }

  state.difficulty = difficulty;
  renderDifficultyCards();

  const config = DIFFICULTIES[difficulty];
  toastManager.show(`${config.name} selected.`);
}

function startMission() {
  modalManager.closeAll();
  showGame();

  createGame();
  resultRecorded = false;
  boardRenderer.setReducedMotion(state.settings.reducedEffects);
  game.start();
}

function requestRestart() {
  if (!game) {
    return;
  }

  const shouldConfirm =
    state.settings.confirmRestart &&
    [GAME_STATES.PLAYING, GAME_STATES.CHECKING, GAME_STATES.PAUSED].includes(
      game.getState().status,
    );

  if (!shouldConfirm) {
    game.restart();
    return;
  }

  modalManager.confirm({
    title: "Restart mission?",
    message: "Current progress will be discarded and a new matrix will be generated.",
    confirmText: "RESTART",
    onConfirm: () => {
      modalManager.close("pause-modal");
      game.restart();
    },
  });
}

function togglePause() {
  if (!game) {
    return;
  }

  const currentState = game.getState();

  if (currentState.status === GAME_STATES.PAUSED) {
    game.resume();
    modalManager.close("pause-modal");
  } else if (
    currentState.status === GAME_STATES.PLAYING ||
    currentState.status === GAME_STATES.CHECKING
  ) {
    game.pause();
    modalManager.open("pause-modal");
  }
}

function handleGameEvent(eventName, payload) {
  if (eventName === "countdown") {
    elements.countdownOverlay.hidden = false;
    elements.countdownValue.textContent = payload.value === 0 ? "GO" : String(payload.value);
    audio.play(payload.value === 0 ? "countdown-go" : "countdown");
  }

  if (eventName === "playing") {
    setTimeout(() => {
      elements.countdownOverlay.hidden = true;
    }, 180);
  }

  if (eventName === "first-selection") {
    elements.gameStatus.textContent = "Signal acquired. Select another card.";
  }

  if (eventName === "match") {
    elements.gameStatus.textContent = "MATCH CONFIRMED. Keep the combo alive.";
    toastManager.show(`+${payload.scoring.total}  /  COMBO ×${payload.combo}`, {
      type: "success",
      duration: 1000,
    });
  }

  if (eventName === "mismatch") {
    elements.gameStatus.textContent = "SIGNAL MISMATCH. Recalibrating…";
    toastManager.show("Combo broken.", { type: "warning", duration: 900 });
  }

  if (eventName === "paused") {
    elements.gameStatus.textContent = "Mission paused.";
  }

  if (eventName === "resumed") {
    elements.gameStatus.textContent = "Mission resumed. Stay focused.";
  }

  if (eventName === "won" || eventName === "lost") {
    recordResult(payload);
  }

  if (eventName === "timer-tick" && payload.remaining <= 10 && payload.remaining > 0) {
    if (payload.remaining === 10) {
      audio.play("warning");
      toastManager.show("Critical time remaining.", { type: "warning" });
    }
  }
}

function renderGame(currentState) {
  if (!currentState || !game) {
    return;
  }

  boardRenderer.render(currentState);
  hudRenderer.render(currentState);

  if (currentState.status === GAME_STATES.PAUSED) {
    elements.pauseButton.textContent = "RESUME";
  } else {
    elements.pauseButton.textContent = "PAUSE";
  }

  if (currentState.status === GAME_STATES.WON) {
    elements.gameStatus.textContent = "MATRIX COMPLETE.";
  }

  if (currentState.status === GAME_STATES.LOST) {
    elements.gameStatus.textContent = "TIME EXPIRED.";
  }

  if (currentState.status === GAME_STATES.COUNTDOWN) {
    elements.gameStatus.textContent = "Synchronizing matrix…";
  }
}

function recordResult(gameState) {
  if (resultRecorded) {
    return;
  }

  resultRecorded = true;

  const previousBest = statistics.getBestScore();
  const { result } = statistics.recordResult(gameState);
  const isNewRecord = gameState.score > previousBest;

  showResult(gameState, result, isNewRecord);
  renderLobbyStats();
}

function showResult(gameState, result, isNewRecord) {
  const won = gameState.status === GAME_STATES.WON;

  elements.resultEyebrow.textContent = won ? "MISSION COMPLETE" : "MISSION FAILED";
  elements.resultTitle.textContent = won ? "MEMORY MASTER" : "TIME EXPIRED";
  elements.resultSubtitle.textContent = won
    ? "ALL PAIRS MATCHED"
    : `${gameState.matches} / ${gameState.totalPairs} PAIRS FOUND`;

  elements.resultScore.textContent = formatNumber(result.score);
  elements.resultTime.textContent = formatSeconds(result.timeUsed);
  elements.resultMoves.textContent = String(result.moves);
  elements.resultAccuracy.textContent = `${result.accuracy}%`;
  elements.resultCombo.textContent = `×${result.maxCombo}`;
  elements.resultTimeBonus.textContent = formatNumber(gameState.timeBonus);

  elements.newRecord.hidden = !isNewRecord;

  modalManager.open("result-modal");
}

function showLobby() {
  modalManager.closeAll();
  switchView("lobby");
  renderLobbyStats();
}

function showGame() {
  switchView("game");
}

function showStatistics() {
  modalManager.closeAll();
  switchView("statistics");
  renderStatistics();
}

function switchView(view) {
  state.currentView = view;

  elements.lobbyView.hidden = view !== "lobby";
  elements.gameView.hidden = view !== "game";
  elements.statisticsView.hidden = view !== "statistics";

  elements.lobbyView.classList.toggle("view--active", view === "lobby");
  elements.gameView.classList.toggle("view--active", view === "game");
  elements.statisticsView.classList.toggle("view--active", view === "statistics");
}

function renderDifficultyCards() {
  elements.difficultyGrid.replaceChildren();

  Object.values(DIFFICULTIES).forEach((config) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "difficulty-card";
    button.dataset.difficulty = config.id;
    button.classList.toggle("is-selected", state.difficulty === config.id);

    button.innerHTML = `
      <span class="difficulty-number">${String(Object.keys(DIFFICULTIES).indexOf(config.id) + 1).padStart(2, "0")}</span>
      <strong>${config.name}</strong>
      <span class="difficulty-description">${config.description}</span>
      <span class="difficulty-stats">
        <span>${config.pairs} PAIRS</span>
        <span>${config.timeLimit} SEC</span>
      </span>
      <span class="difficulty-label">${config.label}</span>
    `;

    button.setAttribute("aria-pressed", String(state.difficulty === config.id));
    elements.difficultyGrid.append(button);
  });
}

function renderLobbyStats() {
  const stats = storage.getStatistics();

  $("#lobby-best-score").textContent = formatNumber(stats.bestScore);
  $("#lobby-fastest").textContent =
    stats.fastestTime === null ? "—" : formatSeconds(stats.fastestTime);
  $("#lobby-combo").textContent = `×${stats.bestCombo}`;
  $("#lobby-win-rate").textContent = `${statistics.calculateWinRate(stats)}%`;
  $("#lobby-games").textContent = String(stats.gamesPlayed);
}

function renderStatistics() {
  const stats = storage.getStatistics();
  const records = statistics.getRecords();

  $("#stat-best-score").textContent = formatNumber(stats.bestScore);
  $("#stat-fastest").textContent =
    stats.fastestTime === null ? "—" : formatSeconds(stats.fastestTime);
  $("#stat-fewest").textContent =
    stats.fewestMoves === null ? "—" : String(stats.fewestMoves);
  $("#stat-best-combo").textContent = `×${stats.bestCombo}`;
  $("#stat-games").textContent = String(stats.gamesPlayed);
  $("#stat-wins").textContent = String(stats.gamesWon);
  $("#stat-win-rate").textContent = `${statistics.calculateWinRate(stats)}%`;

  const body = $("#records-body");
  body.replaceChildren();

  if (!records.length) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    cell.colSpan = 6;
    cell.textContent = "No mission records yet.";
    cell.className = "empty-records";
    row.append(cell);
    body.append(row);
    return;
  }

  records.forEach((record) => {
    const row = document.createElement("tr");

    const values = [
      record.difficulty.toUpperCase(),
      record.result.toUpperCase(),
      formatNumber(record.score),
      formatSeconds(record.timeUsed),
      String(record.moves),
      `${record.accuracy}%`,
    ];

    values.forEach((value, index) => {
      const cell = document.createElement("td");
      cell.textContent = value;

      if (index === 1) {
        cell.className = record.result === "won" ? "result-won" : "result-lost";
      }

      row.append(cell);
    });

    body.append(row);
  });
}

function syncSettingsControls() {
  elements.settingsSound.checked = state.settings.soundEnabled;
  elements.settingsReducedEffects.checked = state.settings.reducedEffects;
  elements.settingsTheme.value = state.settings.theme;

  elements.soundToggle.classList.toggle("is-active", state.settings.soundEnabled);
  elements.soundToggle.setAttribute(
    "aria-label",
    state.settings.soundEnabled ? "Disable sound" : "Enable sound",
  );

  elements.themeToggle.classList.toggle("is-active", state.settings.theme === "light");
}

function persistSettings() {
  storage.saveSettings(state.settings);
}

boardRenderer.setReducedMotion(state.settings.reducedEffects);
renderDifficultyCards();
