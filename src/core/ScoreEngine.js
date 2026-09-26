import { SCORE_CONFIG } from "../config/gameConfig.js";

export class ScoreEngine {
  constructor(config = SCORE_CONFIG) {
    this.config = config;
  }

  matchScore(combo, elapsedSinceSelection = 0) {
    const comboBonus = this.comboBonus(combo);
    const speedBonus = this.speedBonus(elapsedSinceSelection);

    return {
      base: this.config.MATCH_BASE,
      comboBonus,
      speedBonus,
      total: this.config.MATCH_BASE + comboBonus + speedBonus,
    };
  }

  comboBonus(combo) {
    return Math.max(0, combo - 1) * this.config.COMBO_BONUS;
  }

  speedBonus(elapsedSeconds) {
    return elapsedSeconds <= 2 ? this.config.FAST_MATCH_BONUS : 0;
  }

  mistakePenalty() {
    return this.config.MISTAKE_PENALTY;
  }

  timeBonus(remainingSeconds) {
    return Math.max(0, Math.floor(remainingSeconds) * this.config.TIME_BONUS_MULTIPLIER);
  }

  finalScore(currentScore, remainingSeconds) {
    const bonus = this.timeBonus(remainingSeconds);
    return {
      bonus,
      total: Math.max(0, currentScore + bonus),
    };
  }
}
