# Testing

Vitest is used for automated unit tests.

## Test suites

### Deck

Tests:

- pair count
- card count
- exactly two cards per pair
- unique IDs
- shuffle preservation

### Game

Tests:

- initialization
- card selection
- matching
- mismatch
- combo
- score
- third-card prevention
- pause/resume
- timeout
- restart

### Timer

Tests:

- start
- timestamp-based expiry
- pause
- resume
- reset

### Score

Tests:

- base score
- combo bonus
- speed bonus
- mistake penalty
- time bonus
- final score

### Storage

Tests:

- save/read
- corrupted JSON
- unavailable storage
- record limit

### Statistics

Tests:

- wins
- games played
- win rate
- best score
- fastest time
- fewest moves
- best combo

## Commands

