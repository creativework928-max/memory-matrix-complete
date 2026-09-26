export class BoardRenderer {
  constructor(element, { onCardSelect }) {
    this.element = element;
    this.onCardSelect = onCardSelect;
    this.reducedMotion = false;

    this.element.addEventListener("click", (event) => {
      const card = event.target.closest(".memory-card");

      if (!card) {
        return;
      }

      this.onCardSelect(card.dataset.cardId);
    });

    this.element.addEventListener("keydown", (event) => {
      if (!["Enter", " "].includes(event.key)) {
        return;
      }

      const card = event.target.closest(".memory-card");

      if (!card) {
        return;
      }

      event.preventDefault();
      this.onCardSelect(card.dataset.cardId);
    });
  }

  setReducedMotion(value) {
    this.reducedMotion = Boolean(value);
  }

  render(state) {
    this.element.style.setProperty("--board-columns", state.config.columns);
    this.element.setAttribute(
      "aria-rowcount",
      String(state.config.rows),
    );

    const fragment = document.createDocumentFragment();

    state.cards.forEach((card, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "memory-card";
      button.dataset.cardId = card.id;
      button.dataset.category = card.category;
      button.setAttribute("role", "gridcell");
      button.setAttribute("aria-rowindex", String(Math.floor(index / state.config.columns) + 1));
      button.setAttribute(
        "aria-colindex",
        String((index % state.config.columns) + 1),
      );

      if (card.flipped || card.matched) {
        button.classList.add("is-flipped");
      }

      if (card.matched) {
        button.classList.add("is-matched");
        button.disabled = true;
      }

      const accessibleLabel = card.flipped || card.matched
        ? `${card.name}, ${card.category}${card.matched ? ", matched" : ""}`
        : "Hidden memory card";

      button.setAttribute("aria-label", accessibleLabel);

      button.innerHTML = `
        <span class="card-inner">
          <span class="card-face card-back" aria-hidden="true">
            <span class="card-back-symbol">✦</span>
          </span>
          <span class="card-face card-front" aria-hidden="true">
            <span class="card-symbol">${card.symbol}</span>
            <span class="card-name">${card.name}</span>
            <span class="card-category">${card.category}</span>
          </span>
        </span>
      `;

      fragment.append(button);
    });

    this.element.replaceChildren(fragment);
  }
}
