import { CARD_CATALOG } from "../config/cardCatalog.js";
import { shuffle } from "../utils/random.js";

export class Deck {
  constructor(config, catalog = CARD_CATALOG) {
    this.config = config;
    this.catalog = catalog;
    this.cards = [];
  }

  generate() {
    const selected = shuffle(this.catalog).slice(0, this.config.pairs);

    this.cards = selected.flatMap((definition, pairIndex) => [
      this.createCard(definition, pairIndex, 0),
      this.createCard(definition, pairIndex, 1),
    ]);

    this.shuffle();
    return this.getCards();
  }

  createCard(definition, pairIndex, copyIndex) {
    return {
      id: `card-${pairIndex + 1}-${copyIndex + 1}-${definition.id}`,
      pairId: definition.id,
      symbol: definition.symbol,
      name: definition.name,
      category: definition.category,
      flipped: false,
      matched: false,
    };
  }

  shuffle() {
    this.cards = shuffle(this.cards);
    return this.getCards();
  }

  reset() {
    this.cards = [];
  }

  getCards() {
    return this.cards.map((card) => ({ ...card }));
  }
}
