export class ThemeManager {
  constructor(root = document.documentElement) {
    this.root = root;
  }

  setTheme(theme) {
    const value = theme === "light" ? "light" : "neon";
    this.root.dataset.theme = value;
  }

  toggle(currentTheme) {
    const next = currentTheme === "neon" ? "light" : "neon";
    this.setTheme(next);
    return next;
  }
}
