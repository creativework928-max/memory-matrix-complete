import { describe, expect, it } from "vitest";
import { ScoreEngine } from "../src/core/ScoreEngine.js";

describe("ScoreEngine", () => {
  const engine = new ScoreEngine();

  it("awards the base match score", () => {
    expect(engine.matchScore(1, 4).total).toBe(100);
  });

  it("awards combo bonus", () => {
    expect(engine.matchScore(3, 4).total).toBe(150);
  });

  it("awards fast match bonus", () => {
    expect(engine.matchScore(1, 1.5).total).toBe(150);
  });

  it("calculates mistake penalty", () => {
    expect(engine.mistakePenalty()).toBe(15);
  });

  it("calculates time bonus", () => {
    expect(engine.timeBonus(20)).toBe(100);
  });

  it("calculates final score", () => {
    expect(engine.finalScore(500, 20)).toEqual({
      bonus: 100,
      total: 600,
    });
  });
});
