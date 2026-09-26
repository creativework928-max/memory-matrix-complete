import { describe, expect, it } from "vitest";
import { StorageService } from "../src/services/StorageService.js";

function createStorage() {
  const data = new Map();

  return {
    getItem: (key) => data.get(key) ?? null,
    setItem: (key, value) => data.set(key, String(value)),
    removeItem: (key) => data.delete(key),
  };
}

describe("StorageService", () => {
  it("saves and reads settings", () => {
    const service = new StorageService(createStorage());

    service.saveSettings({
      soundEnabled: true,
      theme: "light",
    });

    const settings = service.getSettings();

    expect(settings.soundEnabled).toBe(true);
    expect(settings.theme).toBe("light");
  });

  it("recovers from corrupted JSON", () => {
    const storage = createStorage();
    storage.setItem("memory-matrix.results", "{bad json");

    const service = new StorageService(storage);

    expect(service.getResults()).toEqual([]);
  });

  it("does not crash when storage is unavailable", () => {
    const service = new StorageService({
      getItem() {
        throw new Error("blocked");
      },
      setItem() {
        throw new Error("blocked");
      },
      removeItem() {
        throw new Error("blocked");
      },
    });

    expect(service.getResults()).toEqual([]);
    expect(service.saveResult({ score: 1 })).toBe(false);
  });

  it("limits records to 20", () => {
    const service = new StorageService(createStorage());

    for (let index = 0; index < 25; index += 1) {
      service.saveResult({ id: index });
    }

    expect(service.getResults()).toHaveLength(20);
  });
});
