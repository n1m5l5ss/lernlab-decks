# Share a deck

Anyone can suggest a deck for the gallery. The maintainer reviews every deck before it appears in LernLab, so nothing goes live without a check.

## What a deck needs

- A `.lernpack` file exported from LernLab (Decks → your deck → Export).
- An open licence: CC BY 4.0, CC BY-SA 4.0 or CC0. Only share cards and pictures you made yourself or are allowed to share under that licence.
- A clear title and a one- or two-sentence description.
- No real exam questions, nothing copied from paid courses, nothing hateful or adult.

## Two ways to send it

**1. The form (no GitHub skills needed).** Fill in the [deck submission form](https://github.com/n1m5l5ss/lernlab/issues/new?template=deck_submission.yml) and attach your `.lernpack`. The maintainer adds it for you.

**2. A pull request.**

1. Fork this repository.
2. Add your file as `decks/<id>.lernpack`. The `<id>` uses lower-case letters, digits and `-` (for example `french-food-words`).
3. Add an entry for it to the `decks` list in `index.json`. Copy an existing entry and change it. Get `sha256` and `size` with:
   ```
   sha256sum decks/<id>.lernpack
   stat -c %s decks/<id>.lernpack      # on a Mac: stat -f %z decks/<id>.lernpack
   ```
4. Run `python3 scripts/check.py`. It must say `OK`.
5. Open a pull request. The same check runs on it automatically.

## What happens next

The maintainer imports your deck into LernLab, checks the cards and the licence, and merges the pull request (or adds the deck from the form). Everyone who opens the gallery sees it from then on. To fix a deck later, send a new file with the same `id`. People who installed it get the fixes when they install it again, and they keep their progress.
