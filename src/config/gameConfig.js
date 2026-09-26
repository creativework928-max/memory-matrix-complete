export const DIFFICULTIES = {
  initiate: {
    id: "initiate",
    name: "INITIATE",
    description: "Learn the matrix.",
    label: "BEGINNER",
    rows: 4,
    columns: 4,
    pairs: 8,
    timeLimit: 60,
  },

  pro: {
    id: "pro",
    name: "PRO",
    description: "Test your memory.",
    label: "INTERMEDIATE",
    rows: 4,
    columns: 5,
    pairs: 10,
    timeLimit: 75,
  },

  elite: {
    id: "elite",
    name: "ELITE",
    description: "Master the matrix.",
    label: "EXPERT",
    rows: 6,
    columns: 6,
    pairs: 18,
    timeLimit: 120,
  },
};

export const DEFAULT_DIFFICULTY = "initiate";

export const GAME_STATES = Object.freeze({
  READY: "READY",
  COUNTDOWN: "COUNTDOWN",
  PLAYING: "PLAYING",
  CHECKING: "CHECKING",
  PAUSED: "PAUSED",
  WON: "WON",
  LOST: "LOST",
});

export const GAME_TIMINGS = Object.freeze({
  COUNTDOWN_STEP_MS: 750,
  MISMATCH_DELAY_MS: 800,
});

export const SCORE_CONFIG = Object.freeze({
  MATCH_BASE: 100,
  COMBO_BONUS: 25,
  FAST_MATCH_BONUS: 50,
  TIME_BONUS_MULTIPLIER: 5,
  MISTAKE_PENALTY: 15,
});
