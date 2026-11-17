[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/bongekanjing/tiny-chess-01-quiet-walrus-47/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# Tiny Chess — a 4 KB Python chess engine

A complete chess engine that fits in one 4,096-byte `main.py`, written for
the [make.fun tiny-chess bounty](https://make.fun/bounty/tiny-chess-01).

`main.py` is the compressed entrypoint: it unpacks (`lzma`) and runs the
readable source in `engine.py`. The rules count the packed payload and the
unpacker together against the 4,096-byte cap, and the kit's own
`makefun compress` produces it from `engine.py`.

## How it plays

- **Board** — 0x88 layout (128 squares) so off-board tests are a mask.
  Piece codes 1–6; white positive, black negative.
- **Search** — iterative deepening alpha-beta with a principal-variation
  split, a transposition table keyed on Zobrist hashes, null-move pruning,
  late-move reductions, and killers for move ordering.
- **Quiescence** — captures are resolved before an evaluation is returned,
  with a delta prune so clearly losing captures are skipped.
- **Evaluation** — material plus piece-square tables, kept incrementally:
  `make` and `unmake` adjust the score and the hash instead of recomputing
  them, which is what makes the node rate high enough to search deeply.
- **Determinism** — the search stops on a fixed node budget, never a clock,
  so a replay plays exactly the same moves.

The engine speaks the kit's environment protocol: it asks for the position,
replies with its best move, and falls back down its ordered candidate list
if the environment refuses one.

## Size

| file | bytes |
| --- | --- |
| `main.py` (packed entrypoint, committed) | 4,013 |
| `engine.py` (readable source) | 15,229 |
| `README.md` + `LICENSE` | under the 8,192-byte tree cap |

`main.py` is regenerated with the kit's packer, never hand-edited:

    node cli/makefun.mjs compress engine.py --out main.py

## Licence

MIT — see `LICENSE`.
