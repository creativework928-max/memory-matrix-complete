import { GAME_STATES } from "../config/gameConfig.js";

export function createInitialState(difficulty, timeLimit) {
  return {
    status: GAME_STATES.READY,
    difficulty,
    cards: [],
    firstCardId: null,
    secondCardId: null,
    moves: 0,
    matches: 0,
    mistakes: 0,
    score: 0,
    combo: 0,
    maxCombo: 0,
    timeLimit,
    timeRemaining: timeLimit,
    startedAt: null,
    pausedAt: null,
    completedAt: null,
    timeBonus: 0,
    lastScoreDelta: 0,
    lastEvent: null,
  };
}
