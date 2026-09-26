export function isValidDifficulty(value, difficulties) {
  return typeof value === "string" && Object.hasOwn(difficulties, value);
}

export function clamp(value, minimum, maximum) {
  return Math.min(maximum, Math.max(minimum, value));
}

export function safePercentage(value) {
  return clamp(Math.round(value), 0, 100);
}
