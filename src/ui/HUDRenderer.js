import { formatNumber, formatSeconds } from "../utils/format.js";

export class HUDRenderer {
  constructor(elements) {
    this.elements = elements;
    this.lastScore = 0;
  }

  render(state) {
    const {
      timeRemaining,
      timeLimit,
      score,
      moves,
      matches,
      totalPairs,
      combo,
      accuracy,
      lastScoreDelta,
    } = state;

    this.elements.time.textContent = formatSeconds(timeRemaining);
    this.elements.score.textContent = formatNumber(score);
    this.elements.moves.textContent = String(moves);
    this.elements.matches.textContent = `${matches} / ${totalPairs}`;
    this.elements.combo.textContent = `×${combo}`;
    this.elements.accuracy.textContent = `${accuracy}%`;

    const percentage = timeLimit > 0 ? (timeRemaining / timeLimit) * 100 : 0;
    this.elements.progress.style.width = `${percentage}%`;

    this.elements.timerCard.classList.toggle("is-warning", timeRemaining <= 20);
    this.elements.timerCard.classList.toggle("is-critical", timeRemaining <= 10);
    this.elements.timerStatus.textContent = timeRemaining <= 10 ? "!" : "●";

    if (lastScoreDelta !== 0 && lastScoreDelta !== this.lastScore) {
      this.showScoreDelta(lastScoreDelta);
    }

    this.lastScore = score;
  }

  showScoreDelta(delta) {
    const node = document.createElement("span");
    node.className = `score-pop ${delta < 0 ? "score-pop--negative" : ""}`;
    node.textContent = `${delta > 0 ? "+" : ""}${formatNumber(delta)}`;

    this.elements.score.parentElement.append(node);

    setTimeout(() => node.remove(), 900);
  }

  reset() {
    this.lastScore = 0;
  }
}
