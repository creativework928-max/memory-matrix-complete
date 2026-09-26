import { describe, expect, it } from "vitest";
import { StatisticsService } from "../src/services/StatisticsService.js";
import { StorageService } from "../src/services/StorageService.js";

function createStorage() {
  const data = new Map();

  return {
    getItem: (key) => data.get(key) ?? null,
    setItem: (key, value) => data.set(key, String(value)),
    removeItem: (key) => data.delete(key),
  };
}

describe("StatisticsService", () => {
  it("records a win and updates personal records", () => {
    const storage = new StorageService(createStorage());
    const service = new StatisticsService(storage);

    const state = {
      difficulty: "initiate",
      score: 1200,
      timeLimit: 60,
      timeRemaining: 18,
      moves: 15,
      matches: 8,
      accuracy: 53,
      maxCombo: 5,
      status: "WON",
    };

    const output = service.recordResult(state);

    expect(output.statistics.gamesPlayed).toBe(1);
    expect(output.statistics.gamesWon).toBe(1);
    expect(output.statistics.bestScore).toBe(1200);
    expect(output.statistics.fastestTime).toBe(42);
    expect(output.statistics.fewestMoves).toBe(15);
    expect(output.statistics.bestCombo).toBe(5);
  });

  it("calculates win rate", () => {
    const storage = new StorageService(createStorage());
    storage.saveStatistics({
      gamesPlayed: 4,
      gamesWon: 3,
      bestScore: 0,
      fastestTime: null,
      fewestMoves: null,
      bestCombo: 0,
    });

    const service = new StatisticsService(storage);

    expect(service.calculateWinRate()).toBe(75);
  });

  it("keeps fastest and fewest values only when appropriate", () => {
    const storage = new StorageService(createStorage());
    const service = new StatisticsService(storage);

    service.recordResult({
      difficulty: "initiate",
      score: 500,
      timeLimit: 60,
      timeRemaining: 10,
      moves: 20,
      matches: 8,
      accuracy: 40,
      maxCombo: 2,
      status: "WON",
    });

    service.recordResult({
      difficulty: "initiate",
      score: 400,
      timeLimit: 60,
      timeRemaining: 20,
      moves: 25,
      matches: 8,
      accuracy: 32,
      maxCombo: 1,
      status: "WON",
    });

    expect(service.getFastestTime()).toBe(50);
    expect(service.getFewestMoves()).toBe(20);
  });
});
