import { DEFAULT_SETTINGS, STORAGE_KEYS } from "../config/storageKeys.js";

export class StorageService {
  constructor(storage = typeof localStorage !== "undefined" ? localStorage : null) {
    this.storage = storage;
    this.available = this.checkAvailability();
  }

  checkAvailability() {
    if (!this.storage) {
      return false;
    }

    try {
      const key = "__memory_matrix_test__";
      this.storage.setItem(key, "1");
      this.storage.removeItem(key);
      return true;
    } catch {
      return false;
    }
  }

  readJson(key, fallback) {
    if (!this.available) {
      return fallback;
    }

    try {
      const raw = this.storage.getItem(key);

      if (!raw) {
        return fallback;
      }

      return JSON.parse(raw);
    } catch {
      this.remove(key);
      return fallback;
    }
  }

  writeJson(key, value) {
    if (!this.available) {
      return false;
    }

    try {
      this.storage.setItem(key, JSON.stringify(value));
      return true;
    } catch {
      return false;
    }
  }

  remove(key) {
    if (!this.available) {
      return false;
    }

    try {
      this.storage.removeItem(key);
      return true;
    } catch {
      return false;
    }
  }

  getSettings() {
    const settings = this.readJson(STORAGE_KEYS.SETTINGS, {});
    return {
      ...DEFAULT_SETTINGS,
      ...(settings && typeof settings === "object" ? settings : {}),
    };
  }

  saveSettings(settings) {
    return this.writeJson(STORAGE_KEYS.SETTINGS, {
      ...DEFAULT_SETTINGS,
      ...settings,
    });
  }

  getStatistics() {
    return this.readJson(STORAGE_KEYS.STATISTICS, {
      gamesPlayed: 0,
      gamesWon: 0,
      bestScore: 0,
      fastestTime: null,
      fewestMoves: null,
      bestCombo: 0,
    });
  }

  saveStatistics(statistics) {
    return this.writeJson(STORAGE_KEYS.STATISTICS, statistics);
  }

  getResults() {
    const results = this.readJson(STORAGE_KEYS.RESULTS, []);
    return Array.isArray(results) ? results : [];
  }

  saveResult(result) {
    const results = this.getResults();
    results.unshift(result);
    return this.writeJson(STORAGE_KEYS.RESULTS, results.slice(0, 20));
  }

  clearResults() {
    return this.remove(STORAGE_KEYS.RESULTS);
  }

  clearAll() {
    this.remove(STORAGE_KEYS.SETTINGS);
    this.remove(STORAGE_KEYS.STATISTICS);
    this.remove(STORAGE_KEYS.RESULTS);
  }
}
