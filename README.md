[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# Tiny Chess — a 4 KB Python chess engine

A compact chess engine in a single `main.py` (3,934 bytes), written
from scratch for the [make.fun bounty](https://make.fun/bounty/tiny-chess-01).
It plays the house gauntlet through the environment protocol: no clock,
no randomness, a fixed node budget per move.

## How it works

`main.py` unpacks (lzma) and runs a 0x88-board engine, Python 3.13
standard library only:

- **Board:** 0x88 representation (128 squares), piece codes 1–6.
- **Move generation:** pseudo-legal generation with a king-safety
  filter; castling, en passant and promotions handled.
- **Search:** negamax with alpha-beta, quiescence on captures and
  promotions (all evasions when in check), MVV-LVA move ordering,
  iterative deepening to a fixed budget of 20,000 nodes per move
  (typically depth 3–5, ~2 s per move, well under the 10 s limit).
- **Evaluation:** material (P100 N320 B330 R500 Q900) plus a centre
  table, pawn advance and central-pawn bonuses, and a development
  bonus for knights and bishops off the back rank.

## Validation

- Move generation verified by perft: start position 20 / 400 / 8,902
  (depths 1–3); Kiwipete position 48 / 2,039 / 97,862.
- Finds mate-in-1 (Scholar's mate Qxf7#) and plays sensible
  developing moves from the start position (Nc3).
- `main.py` is 3,934 bytes (under the 4,096 cap); the whole snapshot
  is under 8,192 bytes. No file other than `main.py` is read.

## License

MIT — see [LICENSE](LICENSE).
