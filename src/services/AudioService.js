export class AudioService {
  constructor({ enabled = false } = {}) {
    this.enabled = enabled;
    this.context = null;
    this.masterGain = null;
  }

  setEnabled(enabled) {
    this.enabled = Boolean(enabled);

    if (this.enabled) {
      this.ensureContext();
    }
  }

  toggle() {
    this.setEnabled(!this.enabled);
    return this.enabled;
  }

  ensureContext() {
    if (this.context) {
      if (this.context.state === "suspended") {
        this.context.resume().catch(() => {});
      }
      return this.context;
    }

    const Context = window.AudioContext || window.webkitAudioContext;

    if (!Context) {
      return null;
    }

    this.context = new Context();
    this.masterGain = this.context.createGain();
    this.masterGain.gain.value = 0.055;
    this.masterGain.connect(this.context.destination);

    return this.context;
  }

  play(type) {
    if (!this.enabled) {
      return;
    }

    const context = this.ensureContext();

    if (!context || !this.masterGain) {
      return;
    }

    const presets = {
      click: [220, 0.045, "square", 0.025],
      flip: [420, 0.07, "sine", 0.04],
      match: [660, 0.12, "triangle", 0.06],
      mismatch: [150, 0.13, "sawtooth", 0.035],
      combo: [880, 0.16, "triangle", 0.06],
      countdown: [520, 0.09, "square", 0.045],
      "countdown-go": [880, 0.18, "triangle", 0.065],
      warning: [120, 0.1, "square", 0.035],
      victory: [740, 0.4, "triangle", 0.08],
      defeat: [110, 0.45, "sawtooth", 0.045],
    };

    const [frequency, duration, typeName, volume] = presets[type] ?? presets.click;
    const oscillator = context.createOscillator();
    const gain = context.createGain();

    oscillator.type = typeName;
    oscillator.frequency.setValueAtTime(frequency, context.currentTime);

    gain.gain.setValueAtTime(volume, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + duration);

    oscillator.connect(gain);
    gain.connect(this.masterGain);

    oscillator.start();
    oscillator.stop(context.currentTime + duration);

    if (type === "victory") {
      setTimeout(() => this.playTone(990, 0.2), 110);
      setTimeout(() => this.playTone(1180, 0.25), 220);
    }
  }

  playTone(frequency, duration) {
    if (!this.enabled || !this.context || !this.masterGain) {
      return;
    }

    const oscillator = this.context.createOscillator();
    const gain = this.context.createGain();

    oscillator.type = "triangle";
    oscillator.frequency.value = frequency;

    gain.gain.setValueAtTime(0.045, this.context.currentTime);
    gain.gain.exponentialRampToValueAtTime(
      0.001,
      this.context.currentTime + duration,
    );

    oscillator.connect(gain);
    gain.connect(this.masterGain);
    oscillator.start();
    oscillator.stop(this.context.currentTime + duration);
  }
}
