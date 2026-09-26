import {
  GAME_STATES,
  GAME_TIMINGS,
  DIFFICULTIES,
} from "../config/gameConfig.js";
import { createInitialState } from "./GameState.js";
import { Deck } from "./Deck.js";
import { Timer } from "./Timer.js";
import { ScoreEngine } from "./ScoreEngine.js";

export class Game {
  constructor({
    difficulty = "initiate",
    onStateChange = () => {},
    onEvent = () => {},
    audio = null,
    statistics = null,
    reducedMotion = false,
    mismatchDelay = GAME_TIMINGS.MISMATCH_DELAY_MS,
  } = {}) {
    this.difficultyId = difficulty;
    this.config = DIFFICULTIES[difficulty] ?? DIFFICULTIES.initiate;
    this.onStateChange = onStateChange;
    this.onEvent = onEvent;
    this.audio = audio;
    this.statistics = statistics;
    this.reducedMotion = reducedMotion;
    this.mismatchDelay = mismatchDelay;

    this.deck = new Deck(this.config);
    this.scoreEngine = new ScoreEngine();

    this.state = createInitialState(this.config.id, this.config.timeLimit);
    this.timer = this.createTimer();
    this.pendingTimeout = null;
    this.selectionStartedAt = null;
  }

  createTimer() {
    return new Timer(this.config.timeLimit, {
      onTick: (remaining) => {
        this.state.timeRemaining = remaining;
        this.onStateChange(this.getState());
        this.onEvent("timer-tick", { remaining });
      },
      onExpire: () => this.lose(),
    });
  }

  initialize() {
    this.clearPendingTimeout();
    this.timer.reset(this.config.timeLimit);
    this.state = createInitialState(this.config.id, this.config.timeLimit);
    this.onStateChange(this.getState());
  }

  start({ skipCountdown = false } = {}) {
    this.reset();
    this.state.status = skipCountdown ? GAME_STATES.PLAYING : GAME_STATES.COUNTDOWN;
    this.state.startedAt = Date.now();
    this.onStateChange(this.getState());

    if (skipCountdown) {
      this.beginPlaying();
      return;
    }

    this.runCountdown();
  }

  runCountdown() {
    let count = 3;

    const tick = () => {
      if (this.state.status !== GAME_STATES.COUNTDOWN) {
        return;
      }

      this.onEvent("countdown", { value: count });

      if (count === 0) {
        this.beginPlaying();
        return;
      }

      count -= 1;
      this.pendingTimeout = setTimeout(tick, GAME_TIMINGS.COUNTDOWN_STEP_MS);
    };

    tick();
  }

  beginPlaying() {
    this.clearPendingTimeout();
    this.state.status = GAME_STATES.PLAYING;
    this.state.startedAt = Date.now();
    this.timer.start();
    this.audio?.play("countdown-go");
    this.onEvent("playing");
    this.onStateChange(this.getState());
  }

  pause() {
    if (
      ![GAME_STATES.PLAYING, GAME_STATES.CHECKING].includes(this.state.status)
    ) {
      return false;
    }

    this.timer.pause();
    this.state.pausedAt = Date.now();
    this.state.status = GAME_STATES.PAUSED;
    this.onEvent("paused");
    this.onStateChange(this.getState());
    return true;
  }

  resume() {
    if (this.state.status !== GAME_STATES.PAUSED) {
      return false;
    }

    this.timer.resume();
    this.state.pausedAt = null;
    this.state.status = GAME_STATES.PLAYING;
    this.onEvent("resumed");
    this.onStateChange(this.getState());
    return true;
  }

  restart() {
    this.stop();
    this.start();
  }

  reset() {
    this.clearPendingTimeout();
    this.timer.reset(this.config.timeLimit);
    this.deck.reset();
    this.deck.generate();

    this.state = createInitialState(this.config.id, this.config.timeLimit);
    this.state.cards = this.deck.getCards();
    this.selectionStartedAt = null;

    this.onStateChange(this.getState());
  }

  stop() {
    this.clearPendingTimeout();
    this.timer.stop();
  }

  selectCard(cardId) {
    if (this.state.status !== GAME_STATES.PLAYING) {
      return false;
    }

    const card = this.state.cards.find((item) => item.id === cardId);

    if (!card || card.flipped || card.matched) {
      return false;
    }

    if (this.state.firstCardId === cardId) {
      return false;
    }

    if (this.state.secondCardId !== null) {
      return false;
    }

    card.flipped = true;
    this.audio?.play("flip");

    if (this.state.firstCardId === null) {
      this.state.firstCardId = cardId;
      this.selectionStartedAt = Date.now();
      this.onEvent("first-selection", { card });
      this.onStateChange(this.getState());
      return true;
    }

    this.state.secondCardId = cardId;
    this.state.moves += 1;
    this.state.status = GAME_STATES.CHECKING;

    this.onStateChange(this.getState());
    this.evaluateSelection();

    return true;
  }

  evaluateSelection() {
    const first = this.state.cards.find((card) => card.id === this.state.firstCardId);
    const second = this.state.cards.find((card) => card.id === this.state.secondCardId);

    if (!first || !second) {
      this.resetSelection();
      return;
    }

    if (first.pairId === second.pairId) {
      this.handleMatch(first, second);
    } else {
      this.handleMismatch(first, second);
    }
  }

  handleMatch(first, second) {
    first.matched = true;
    second.matched = true;

    this.state.matches += 1;
    this.state.combo += 1;
    this.state.maxCombo = Math.max(this.state.maxCombo, this.state.combo);

    const elapsed = Math.max(0, (Date.now() - (this.selectionStartedAt ?? Date.now())) / 1000);
    const scoring = this.scoreEngine.matchScore(this.state.combo, elapsed);

    this.state.score += scoring.total;
    this.state.lastScoreDelta = scoring.total;
    this.state.lastEvent = "match";

    this.audio?.play("match");

    if (this.state.combo >= 2) {
      this.audio?.play("combo");
    }

    this.onEvent("match", {
      first,
      second,
      scoring,
      combo: this.state.combo,
    });

    this.resetSelection();

    if (this.state.matches === this.config.pairs) {
      this.win();
      return;
    }

    this.state.status = GAME_STATES.PLAYING;
    this.onStateChange(this.getState());
  }

  handleMismatch(first, second) {
    this.state.mistakes += 1;
    this.state.combo = 0;
    this.state.lastScoreDelta = -this.scoreEngine.mistakePenalty();
    this.state.score = Math.max(0, this.state.score + this.state.lastScoreDelta);
    this.state.lastEvent = "mismatch";

    this.audio?.play("mismatch");

    this.onEvent("mismatch", {
      first,
      second,
      penalty: this.scoreEngine.mistakePenalty(),
    });

    this.clearPendingTimeout();

    const delay = this.reducedMotion ? 450 : this.mismatchDelay;

    this.pendingTimeout = setTimeout(() => {
      first.flipped = false;
      second.flipped = false;
      this.resetSelection();
      this.state.status = GAME_STATES.PLAYING;
      this.onStateChange(this.getState());
    }, delay);
  }

  win() {
    if ([GAME_STATES.WON, GAME_STATES.LOST].includes(this.state.status)) {
      return;
    }

    this.clearPendingTimeout();
    this.timer.stop();

    const final = this.scoreEngine.finalScore(
      this.state.score,
      this.state.timeRemaining,
    );

    this.state.timeBonus = final.bonus;
    this.state.score = final.total;
    this.state.status = GAME_STATES.WON;
    this.state.completedAt = Date.now();
    this.resetSelection();

    this.audio?.play("victory");
    this.onEvent("won", this.getState());
    this.onStateChange(this.getState());
  }

  lose() {
    if ([GAME_STATES.WON, GAME_STATES.LOST].includes(this.state.status)) {
      return;
    }

    this.clearPendingTimeout();
    this.timer.stop();

    this.state.timeRemaining = 0;
    this.state.status = GAME_STATES.LOST;
    this.state.completedAt = Date.now();
    this.resetSelection();

    this.audio?.play("defeat");
    this.onEvent("lost", this.getState());
    this.onStateChange(this.getState());
  }

  setDifficulty(difficulty) {
    if (!DIFFICULTIES[difficulty]) {
      return false;
    }

    this.stop();
    this.difficultyId = difficulty;
    this.config = DIFFICULTIES[difficulty];
    this.deck = new Deck(this.config);
    this.timer = this.createTimer();
    this.initialize();
    return true;
  }

  getAccuracy() {
    if (this.state.moves === 0) {
      return 100;
    }

    return Math.round((this.state.matches / this.state.moves) * 100);
  }

  getState() {
    return {
      ...this.state,
      cards: this.state.cards.map((card) => ({ ...card })),
      accuracy: this.getAccuracy(),
      totalPairs: this.config.pairs,
      config: { ...this.config },
    };
  }

  clearPendingTimeout() {
    if (this.pendingTimeout !== null) {
      clearTimeout(this.pendingTimeout);
      this.pendingTimeout = null;
    }
  }

  resetSelection() {
    this.state.firstCardId = null;
    this.state.secondCardId = null;
    this.selectionStartedAt = null;
  }
}
