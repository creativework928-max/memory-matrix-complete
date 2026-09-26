export class Timer {
  constructor(duration, { onTick = () => {}, onExpire = () => {}, now = () => Date.now() } = {}) {
    this.duration = Math.max(0, duration);
    this.remaining = this.duration;
    this.onTick = onTick;
    this.onExpire = onExpire;
    this.now = now;

    this.running = false;
    this.startedAt = null;
    this.pausedAt = null;
    this.intervalId = null;
    this.deadline = null;
  }

  start() {
    this.stopInterval();
    this.remaining = this.duration;
    this.startedAt = this.now();
    this.pausedAt = null;
    this.deadline = this.startedAt + this.duration * 1000;
    this.running = true;
    this.emitTick();
    this.startInterval();
  }

  pause() {
    if (!this.running) {
      return;
    }

    this.updateRemaining();
    this.running = false;
    this.pausedAt = this.now();
    this.stopInterval();
  }

  resume() {
    if (this.running || this.remaining <= 0) {
      return;
    }

    const now = this.now();
    this.startedAt = now - (this.duration - this.remaining) * 1000;
    this.deadline = now + this.remaining * 1000;
    this.pausedAt = null;
    this.running = true;
    this.startInterval();
  }

  stop() {
    if (this.running) {
      this.updateRemaining();
    }

    this.running = false;
    this.stopInterval();
  }

  reset(duration = this.duration) {
    this.stopInterval();
    this.duration = Math.max(0, duration);
    this.remaining = this.duration;
    this.startedAt = null;
    this.pausedAt = null;
    this.deadline = null;
    this.running = false;
    this.emitTick();
  }

  getRemaining() {
    if (this.running) {
      this.updateRemaining();
    }

    return this.remaining;
  }

  getElapsed() {
    return Math.max(0, this.duration - this.getRemaining());
  }

  isRunning() {
    return this.running;
  }

  updateRemaining() {
    if (!this.running || this.deadline === null) {
      return;
    }

    const milliseconds = Math.max(0, this.deadline - this.now());
    this.remaining = Math.ceil(milliseconds / 1000);

    if (milliseconds <= 0) {
      this.remaining = 0;
      this.running = false;
      this.stopInterval();
      this.emitTick();
      this.onExpire();
      return;
    }

    this.emitTick();
  }

  startInterval() {
    this.intervalId = setInterval(() => this.updateRemaining(), 100);
  }

  stopInterval() {
    if (this.intervalId !== null) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }

  emitTick() {
    this.onTick(this.remaining, this.duration);
  }
}
