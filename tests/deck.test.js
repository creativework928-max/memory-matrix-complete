import { describe, expect, it } from "vitest";
import { DIFFICULTIES } from "../src/config/gameConfig.js";
import { Deck } from "../src/core/Deck.js";
import { CARD_CATALOG } from "../src/config/cardCatalog.js";

describe("Deck", () => {
  it("creates exactly two cards per pair", () => {
    const deck = new Deck(DIFFICULTIES.initiate, CARD_CATALOG);
    const cards = deck.generate();

    expect(cards).toHaveLength(16);

    const counts = new Map();

    cards.forEach((card) => {
      counts.set(card.pairId, (counts.get(card.pairId) ?? 0) + 1);
    });

    expect(counts.size).toBe(8);
    expect([...counts.values()].every((count) => count === 2)).toBe(true);
  });

  it("creates unique card ids", () => {
    const deck = new Deck(DIFFICULTIES.elite, CARD_CATALOG);
    const cards = deck.generate();

    expect(cards).toHaveLength(36);

    const ids = new Set(cards.map((card) => card.id));
    expect(ids.size).toBe(36);
  });

  it("can shuffle without changing card count", () => {
    const deck = new Deck(DIFFICULTIES.pro, CARD_CATALOG);
    const first = deck.generate();
    const firstIds = first.map((card) => card.id);

    deck.shuffle();

    const secondIds = deck.getCards().map((card) => card.id);

    expect(secondIds).toHaveLength(firstIds.length);
    expect(new Set(secondIds)).toEqual(new Set(firstIds));
  });
});
