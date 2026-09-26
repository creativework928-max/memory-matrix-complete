export class StatisticsService {
  constructor(storage) {
    this.storage = storage;
  }

  createResult(state) {
    const timeUsed = Math.max(0, state.timeLimit - state.timeRemaining);

    return {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      difficulty: state.difficulty,
      score: state.score,
      timeUsed,
      timeRemaining: state.timeRemaining,
      moves: state.moves,
      matches: state.matches,
      accuracy: state.accuracy,
      maxCombo: state.maxCombo,
      result: state.status === "WON" ? "won" : "lost",
      completedAt: new Date().toISOString(),
    };
  }

  recordResult(state) {
    const result = this.createResult(state);
    const statistics = this.storage.getStatistics();

    statistics.gamesPlayed += 1;

    if (result.result === "won") {
      statistics.gamesWon += 1;
    }

    statistics.bestScore = Math.max(statistics.bestScore, result.score);
    statistics.bestCombo = Math.max(statistics.bestCombo, result.maxCombo);

    if (
      result.result === "won" &&
      (statistics.fastestTime === null || result.timeUsed < statistics.fastestTime)
    ) {
      statistics.fastestTime = result.timeUsed;
    }

    if (
      result.result === "won" &&
      (statistics.fewestMoves === null || result.moves < statistics.fewestMoves)
    ) {
      statistics.fewestMoves = result.moves;
    }

    this.storage.saveStatistics(statistics);
    this.storage.saveResult(result);

    return {
      result,
      statistics,
      records: this.getRecords(),
    };
  }

  calculateWinRate(statistics = this.storage.getStatistics()) {
    if (!statistics.gamesPlayed) {
      return 0;
    }

    return Math.round((statistics.gamesWon / statistics.gamesPlayed) * 100);
  }

  getBestScore() {
    return this.storage.getStatistics().bestScore;
  }

  getFastestTime() {
    return this.storage.getStatistics().fastestTime;
  }

  getFewestMoves() {
    return this.storage.getStatistics().fewestMoves;
  }

  getBestCombo() {
    return this.storage.getStatistics().bestCombo;
  }

  getRecords() {
    return this.storage.getResults();
  }

  clearRecords() {
    return this.storage.clearResults();
  }

  clearAll() {
    this.storage.clearAll();
  }
}
