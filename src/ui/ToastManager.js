export class ToastManager {
  constructor(region) {
    this.region = region;
  }

  show(message, { type = "info", duration = 1800 } = {}) {
    const toast = document.createElement("div");
    toast.className = `toast toast--${type}`;
    toast.textContent = message;
    this.region.append(toast);

    requestAnimationFrame(() => {
      toast.classList.add("is-visible");
    });

    setTimeout(() => {
      toast.classList.remove("is-visible");
      setTimeout(() => toast.remove(), 250);
    }, duration);
  }
}
