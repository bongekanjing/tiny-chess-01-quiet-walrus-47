[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# Tiny Chess — a 4 KB Python chess engine

A chess engine in one `main.py` (4,054 bytes), written from scratch for
the [make.fun bounty](https://make.fun/bounty/tiny-chess-01). It plays
the house gauntlet through the environment protocol: Python 3.13
standard library only, no clock of its own, no randomness.

`main.py` is packed with the kit's own `node cli/makefun.mjs compress`.
The readable source is what the transcript bundle carries beside the
sessions; it is not committed, because the competition caps every file
at 4,096 bytes and the source, spelling out the tables, is larger.

## How it works

- **Board:** 0x88 (128 squares), piece codes 1-6, incremental Zobrist
  hashing, incremental evaluation.
- **Move generation:** pseudo-legal with a king-safety filter; castling,
  en passant and all four promotions.
- **Search:** principal variation search over iterative deepening, a
  transposition table with bound flags, late-move reductions, a null-move
  probe, killer moves and least-valuable-attacker ordering. A wall clock
  guards the node budget: a finished iteration is trusted, and a new one
  starts only while there is time, so a long position cannot lose on time
  (the environment allows 10 s a move; the engine stops at 3 s).
  Quiescence takes no stand-pat while in check and searches every
  evasion, so a mate is scored as a mate.
- **Draws:** repetition scores 0 inside the search, matching the rule
  the house applies to the game.
- **Evaluation:** material (P100 N320 B330 R500 Q900) plus a piece-square
  table per piece, with separate middlegame and endgame king tables.

## Validation

- Move generation by perft: start 20 / 400 / 8,902 / 197,281; Kiwipete
  48 / 2,039.
- Incremental evaluation, hash, castling rights, en-passant square and
  the king squares restore exactly after make/unmake.
- Finds mate in one, a back-rank mate and a hanging queen.
- Practice trial: Elo 1451, 4.0 of 6, against the house gauntlet.
- `main.py` is 4,054 bytes (cap 4,096); the tree is five files, 8,155
  bytes (cap 8,192). Only `main.py` is read at run time.

## License

MIT — see [LICENSE](LICENSE).
