# MEMORY MATRIX

### MATCH. REMEMBER. MASTER.

A futuristic real-time browser memory puzzle game.

> Train your memory before the clock runs out.

---

## Overview

Memory Matrix is a local-first memory matching game built with modern browser technologies.

The player selects a difficulty, enters a timed memory matrix, reveals cards two at a time, builds combos, earns points, and attempts to match every pair before the timer expires.

There is no backend, account system, analytics system, or external gameplay dataset.

---

## Features

- INITIATE, PRO, and ELITE difficulties
- 4 × 4, 4 × 5, and 6 × 6 matrices
- Timestamp-based countdown timer
- 3-second mission countdown
- Pair matching
- Mismatch delay
- Combo scoring
- Accuracy tracking
- Time bonus
- Personal records
- Last 20 mission results
- Pause/resume
- Restart
- Keyboard controls
- Touch support
- Web Audio sound effects
- Neon Night theme
- Cyber Light theme
- Reduced-effects setting
- `prefers-reduced-motion` support
- Storage failure recovery
- Corrupted-storage recovery
- Responsive desktop/tablet/mobile UI
- Vitest tests
- ESLint
- Prettier
- Vite production build

---

## Difficulty

| Mode | Grid | Pairs | Time |
|---|---:|---:|---:|
| Initiate | 4 × 4 | 8 | 60 sec |
| Pro | 4 × 5 | 10 | 75 sec |
| Elite | 6 × 6 | 18 | 120 sec |

---

## Gameplay

1. Select a difficulty.
2. Start the mission.
3. Wait for the countdown.
4. Reveal two cards.
5. Find matching pairs.
6. Keep matched cards visible.
7. Mismatches flip back automatically.
8. Build combos by finding consecutive matches.
9. Complete all pairs before time expires.
10. Review your local performance record.

---

## Scoring

A normal match starts at 100 points.

Combo bonus:

