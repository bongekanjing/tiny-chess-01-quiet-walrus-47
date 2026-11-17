[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# Tiny Chess — a 4 KB Python chess engine

A compact chess engine in a single `main.py` (3,508 bytes), written
from scratch for the [make.fun bounty](https://make.fun/bounty/tiny-chess-01).
It plays the house gauntlet through the environment protocol: no clock,
no randomness, a fixed node budget per move.

`main.py` is the readable source packed with the kit's own
`node cli/makefun.mjs compress`. The readable source is what the
transcript bundle carries beside the sessions; it is not committed,
because the competition caps every file at 4,096 bytes and a source
spelling out the tables is larger than that.

## How it works

`main.py` unpacks (lzma) and runs a 0x88-board engine, Python 3.13
standard library only:

- **Board:** 0x88 representation (128 squares), piece codes 1-6,
  incremental Zobrist hashing.
- **Move generation:** pseudo-legal generation with a king-safety
  filter; castling, en passant and promotions handled.
- **Search:** negamax with alpha-beta, iterative deepening to a fixed
  node budget per move (25,000 nodes, typically depth 4-5), a
  transposition table with bound flags, principal-variation and
  least-valuable-attacker move ordering, and killer moves. Quiescence
  searches captures and promotions, takes no stand-pat while in check,
  and searches every evasion when checked, so a mate is seen as a mate.
- **Draws:** repetition and the fifty-move rule score 0 inside the
  search, matching the rules the house applies to the game.
- **Evaluation:** material (P100 N320 B330 R500 Q900) plus a
  piece-square table for each piece, with separate middlegame and
  endgame king tables. Taking the endgame king table in the middlegame
  is what walked the king into the centre and lost games; the two are
  kept apart now.

## Validation

- Move generation verified by perft: start position 20 / 400 / 8,902 /
  197,281 (depths 1-4); Kiwipete 48 / 2,039.
- Incremental evaluation, Zobrist hash, castling rights, en-passant
  square and the king squares are checked to restore exactly after
  make/unmake.
- Finds mate in one, back-rank mate, and a hanging queen.
- `main.py` is 3,508 bytes (under the 4,096 cap) and the tree is four
  files, 7,337 bytes (under the 8,192 cap). No file other than `main.py`
  is read at run time.

## License

MIT — see [LICENSE](LICENSE).
