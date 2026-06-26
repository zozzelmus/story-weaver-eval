# results/ — outputs land here

Two kinds of file, written by the skills:

- `<CASE-ID>.<variant>.tickets.md` — generated tickets (from gen-v0..v3)
- `<CASE-ID>.<variant>.json` — judge scores (from invest-judge)

`scripts/aggregate.py` reads the `*.json` files. The `.md` and `.json` outputs are gitignored
by default so runs don't clutter your history — see `.gitignore` if you want to keep them.
