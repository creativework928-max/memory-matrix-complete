# Architecture

Memory Matrix is a client-only modular browser game.

## Layers

### Core

The core layer owns gameplay rules.

- `Game.js`
- `GameState.js`
- `Deck.js`
- `Timer.js`
- `ScoreEngine.js`

The core layer does not depend on DOM rendering.

### Services

Services provide side effects and persistence.

- `StorageService.js`
- `StatisticsService.js`
- `AudioService.js`

Storage is local to the browser. No server is required.

### UI

UI modules translate game state into visual output.

- `BoardRenderer`
- `HUDRenderer`
- `ModalManager`
- `ToastManager`
- `ThemeManager`

### Configuration

All difficulty and score constants live in `src/config`.

### Data flow

1. User starts a mission.
2. `Game` generates a `Deck`.
3. `Game` starts `Timer`.
4. UI renders immutable snapshots of game state.
5. Card actions return to `Game.selectCard()`.
6. `Game` evaluates matches.
7. `ScoreEngine` calculates points.
8. `StatisticsService` persists completed results.
9. UI displays the result.

## Timer design

The timer uses a timestamp/deadline rather than decrementing a counter once per second. This reduces visible drift caused by delayed browser timers.

## Security model

The game does not execute dynamic code and does not use `eval()`.

DOM content that represents user or stored data is inserted with `textContent`.

Local records are personal records only. They are not cryptographically trustworthy competitive scores.
