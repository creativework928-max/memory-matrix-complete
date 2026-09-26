import { defineConfig } from "vite";

export default defineConfig({
  server: {
    host: true,
    port: 5173,
  },
  preview: {
    host: true,
    port: 4173,
  },
  build: {
    target: "es2022",
    sourcemap: true,
    emptyOutDir: true,
  },
  test: {
    environment: "node",
    globals: true,
    coverage: {
      reporter: ["text", "html"],
      exclude: ["src/main.js"],
    },
  },
});
