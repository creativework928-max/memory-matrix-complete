import { describe, expect, it, vi } from "vitest";
import { Timer } from "../src/core/Timer.js";

describe("Timer", () => {
  it("starts and expires using elapsed timestamps", () => {
    vi.useFakeTimers();
    vi.setSystemTime(0);

    const onExpire = vi.fn();
    const timer = new Timer(10, { onExpire });

    timer.start();

    vi.advanceTimersByTime(3000);

    expect(timer.getRemaining()).toBe(7);
    expect(onExpire).not.toHaveBeenCalled();

    vi.advanceTimersByTime(7000);

    expect(timer.getRemaining()).toBe(0);
    expect(onExpire).toHaveBeenCalledTimes(1);

    timer.stop();
    vi.useRealTimers();
  });

  it("pauses and resumes", () => {
    vi.useFakeTimers();
    vi.setSystemTime(0);

    const timer = new Timer(20);
    timer.start();

    vi.advanceTimersByTime(5000);
    timer.pause();

    expect(timer.getRemaining()).toBe(15);

    vi.advanceTimersByTime(5000);
    expect(timer.getRemaining()).toBe(15);

    timer.resume();
    vi.advanceTimersByTime(3000);

    expect(timer.getRemaining()).toBe(12);

    timer.stop();
    vi.useRealTimers();
  });

  it("resets", () => {
    vi.useFakeTimers();
    vi.setSystemTime(0);

    const timer = new Timer(10);
    timer.start();

    vi.advanceTimersByTime(4000);
    timer.reset();

    expect(timer.getRemaining()).toBe(10);
    expect(timer.isRunning()).toBe(false);

    vi.useRealTimers();
  });
});
