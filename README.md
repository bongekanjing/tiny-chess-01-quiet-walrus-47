[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard)
[![reward](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/reward.svg)](https://make.fun/bounty/tiny-chess-01)

# Tiny Chess - a 4 KB Python chess engine

A full chess engine that fits in a single `main.py` under the 4,096-byte cap,
written for the [make.fun bounty](https://make.fun/bounty/tiny-chess-01).

`main.py` unpacks an LZMA stream of `tiny_chess.py` and speaks the
environment protocol: no clock, no randomness, a fixed node budget per move.

## How it works

- **Board:** 0x88 layout, piece codes 1-6, Zobrist hashing, incremental
  piece-square lists and an undo stack.
- **Search:** iterative deepening negamax with alpha-beta, PVS null-window
  re-search, principal-variation move ordering from a transposition table,
  MVV-LVA captures, killer moves, a history heuristic, late-move reductions
  and a quiescence search over captures, promotions and all evasions in check.
- **Evaluation:** material (P100 N320 B330 R500 Q900) plus a full set of
  piece-square tables, a king table that blends into a centralising endgame
  table as material drops, and a bishop pair bonus for holding castling rights.
- **Rules:** castling, en passant, promotions, repetition and stalemate are
  all handled; the search is deterministic and never reads a clock.
  A node budget of 80,000 caps every move well under the 10 second limit.

## Validation

- Move generation matches published perft counts on all five standard suites:
  start position 20/400/8,902/197,281; Kiwipete 48/2,039/97,862;
  position 3 14/191/2,812/43,238; position 4 6/264/9,467; position 5 44/1,486/62,379.
- Finds mate in one (Scholar, back rank) and takes free material.
- Practice trial: 3 wins, 2 draws, 1 loss against the house gauntlet,
  Elo 1451 on the practice set, two games unbeaten (floor 1154).
- `main.py` is 3,990 bytes; the whole snapshot is under 8,192 bytes.

## License

MIT - see [LICENSE](LICENSE).
