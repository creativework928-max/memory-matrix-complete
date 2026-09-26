export function randomInt(max) {
  if (max <= 0) {
    return 0;
  }

  if (typeof crypto !== "undefined" && crypto.getRandomValues) {
    const values = new Uint32Array(1);
    crypto.getRandomValues(values);
    return Math.floor((values[0] / 4294967296) * max);
  }

  return Math.floor(Math.random() * max);
}

export function shuffle(array) {
  const result = [...array];

  for (let index = result.length - 1; index > 0; index -= 1) {
    const swapIndex = randomInt(index + 1);
    [result[index], result[swapIndex]] = [result[swapIndex], result[index]];
  }

  return result;
}
