import { describe, expect, it, vi } from "vitest";
import { Game } from "../src/core/Game.js";
import { DIFFICULTIES, GAME_STATES } from "../src/config/gameConfig.js";

describe("Game", () => {
  it("initializes with the correct deck", () => {
    const game = new Game({
      difficulty: "initiate",
    });

    game.initialize();

    const state = game.getState();

    expect(state.cards).toHaveLength(16);
    expect(state.totalPairs).toBe(8);
    expect(state.timeRemaining).toBe(60);
    expect(state.status).toBe(GAME_STATES.READY);
  });

  it("selects two cards and resolves a match", () => {
    const game = new Game({
      difficulty: "initiate",
    });

    game.initialize();
    game.start({ skipCountdown: true });

    const state = game.getState();
    const first = state.cards[0];
    const second = state.cards.find((card) => card.pairId === first.pairId && card.id !== first.id);

    expect(game.selectCard(first.id)).toBe(true);
    expect(game.selectCard(second.id)).toBe(true);

    const after = game.getState();

    expect(after.moves).toBe(1);
    expect(after.matches).toBe(1);
    expect(after.combo).toBe(1);
    expect(after.score).toBeGreaterThan(0);
  });

  it("prevents selecting the same card twice", () => {
    const game = new Game({
      difficulty: "initiate",
    });

    game.initialize();
    game.start({ skipCountdown: true });

    const card = game.getState().cards[0];

    expect(game.selectCard(card.id)).toBe(true);
    expect(game.selectCard(card.id)).toBe(false);
  });

  it("prevents a third card during checking", () => {
    vi.useFakeTimers();

    const game = new Game({
      difficulty: "initiate",
      mismatchDelay: 800,
    });

    game.initialize();
    game.start({ skipCountdown: true });

    const cards = game.getState().cards;
    const first = cards[0];
    const second = cards.find((card) => card.pairId !== first.pairId);
    const third = cards.find(
      (card) => card.id !== first.id && card.id !== second.id,
    );

    game.selectCard(first.id);
    game.selectCard(second.id);

    expect(game.getState().status).toBe(GAME_STATES.CHECKING);
    expect(game.selectCard(third.id)).toBe(false);

    vi.advanceTimersByTime(800);

    expect(game.getState().status).toBe(GAME_STATES.PLAYING);

    vi.useRealTimers();
  });

  it("breaks combo on mismatch", () => {
    vi.useFakeTimers();

    const game = new Game({
      difficulty: "initiate",
    });

    game.initialize();
    game.start({ skipCountdown: true });

    const cards = game.getState().cards;
    const first = cards[0];
    const second = cards.find((card) => card.pairId !== first.pairId);

    game.selectCard(first.id);
    game.selectCard(second.id);

    vi.advanceTimersByTime(800);

    expect(game.getState().mistakes).toBe(1);
    expect(game.getState().combo).toBe(0);
    expect(game.getState().score).toBe(0);

    vi.useRealTimers();
  });

  it("pauses and resumes", () => {
    const game = new Game({
      difficulty: "pro",
    });

    game.initialize();
    game.start({ skipCountdown: true });

    expect(game.pause()).toBe(true);
    expect(game.getState().status).toBe(GAME_STATES.PAUSED);

    expect(game.resume()).toBe(true);
    expect(game.getState().status).toBe(GAME_STATES.PLAYING);
  });

  it("loses when timer expires", () => {
    vi.useFakeTimers();
    vi.setSystemTime(0);

    const game = new Game({
      difficulty: "initiate",
    });

    game.initialize();
    game.start({ skipCountdown: true });

    vi.advanceTimersByTime(60000);

    expect(game.getState().status).toBe(GAME_STATES.LOST);
    expect(game.getState().timeRemaining).toBe(0);

    vi.useRealTimers();
  });

  it("supports restart", () => {
    const game = new Game({
      difficulty: "pro",
    });

    game.initialize();
    game.start({ skipCountdown: true });

    const firstDeck = game.getState().cards.map((card) => card.id);

    game.restart();

    const secondState = game.getState();

    expect(secondState.status).toBe(GAME_STATES.COUNTDOWN);
    expect(secondState.cards).toHaveLength(20);
    expect(new Set(secondState.cards.map((card) => card.id)).size).toBe(20);
    expect(firstDeck).toHaveLength(20);
  });

  it("uses the configured difficulty", () => {
    const game = new Game({
      difficulty: "elite",
    });

    expect(game.getState().difficulty).toBe("elite");
    expect(game.config).toEqual(DIFFICULTIES.elite);
  });
});
