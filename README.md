# LernLab deck gallery

Free community decks for [LernLab](https://github.com/n1m5l5ss/lernlab), the open-source flashcard app. In LernLab, open **Decks → Deck gallery** to browse them and install one with a click.

- `index.json` lists every deck. Its format is described in [GALLERY.md](https://github.com/n1m5l5ss/lernlab/blob/dev/docs/GALLERY.md).
- `decks/` holds the `.lernpack` files ([format](https://github.com/n1m5l5ss/lernlab/blob/dev/docs/FORMAT.md)).

## Share your deck

Anyone can suggest a deck, with the [deck submission form](https://github.com/n1m5l5ss/lernlab/issues/new?template=deck_submission.yml) or a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md). Every deck is reviewed before it goes live, and needs an open licence (CC BY 4.0, CC BY-SA 4.0 or CC0), which is shown next to it in the gallery. `python3 scripts/check.py` checks the index and every deck file, and runs on every pull request.

## The team

Decks are reviewed by volunteers. Anyone can join as a reviewer, and anyone can take over running the project: see [GOVERNANCE.md](GOVERNANCE.md) and [MAINTAINERS.md](MAINTAINERS.md), or use the [Join the team form](https://github.com/n1m5l5ss/lernlab/issues/new?template=join_team.yml).

## Licences

Each deck's licence is in `index.json`. The starter decks made by LernLab are CC0 (public domain).
