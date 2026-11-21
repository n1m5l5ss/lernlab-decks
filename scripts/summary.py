"""Writes a plain-language summary of the decks a pull request adds or changes.

Run: python3 scripts/summary.py <base folder> <pull request folder> <check output file>
It only reads files (index.json, and manifest.json and cards.jsonl inside each .lernpack).
It never runs anything from the pull request.
"""
import json, re, sys, zipfile
from pathlib import Path

base, head, check_file = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
SAMPLE = 5


def safe(text, limit=120):
    """Deck text is untrusted: keep it on one line, short, with no HTML, links or @mentions."""
    text = re.sub(r"<[^>]*>", " ", str(text or ""))
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("@", "@​").replace("|", "\\|").replace("`", "'")
    text = re.sub(r"[\[\]]", "", text).replace("://", ":​//")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def decks(root):
    try:
        return {d.get("id"): d for d in json.loads((root / "index.json").read_text("utf-8")).get("decks", [])}
    except Exception:
        return {}


before, after = decks(base), decks(head)
changed = [d for i, d in after.items() if i not in before or before[i] != d]
removed = [d for i, d in before.items() if i not in after]
check = check_file.read_text("utf-8").strip()
ok = check.startswith("OK")

out = ["<!-- deck-summary -->", "### Deck submission summary", ""]
out.append(
    "✅ **The automatic check passed**: the file, its listing and its licence are valid."
    if ok
    else "❌ **The automatic check found problems.** The person who sent this needs to fix them:\n\n```\n" + check[:3000].replace("`", "'") + "\n```"
)
out.append("")
for d in changed:
    new = d.get("id") not in before
    out.append(f"#### {'New deck' if new else 'Updated deck'}: {safe(d.get('title'))}")
    out.append("")
    out.append("| | |\n|---|---|")
    out.append(f"| Description | {safe(d.get('description'), 300)} |")
    out.append(f"| Cards | {safe(d.get('cards'))} |")
    out.append(f"| Language | {safe(d.get('language') or 'any subject')} |")
    out.append(f"| Licence | {safe(d.get('licence'))} |")
    out.append(f"| Author | {safe(d.get('author'))} |")
    out.append(f"| File size | {round((d.get('size') or 0) / 1024)} KB |")
    out.append("")
    try:
        path = head / f"decks/{d.get('id')}.lernpack"
        if d.get("url") != f"decks/{d.get('id')}.lernpack" or path.is_symlink():
            raise ValueError("not a deck file")
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.split("/")[-1] == "cards.jsonl" and n.count("/") <= 1)
            rows = []
            with z.open(name) as f:
                for _ in range(50):
                    line = f.readline(100_000).decode("utf-8", "replace")
                    if not line or len(rows) == SAMPLE:
                        break
                    if line.strip():
                        rows.append(json.loads(line))
        out.append(f"First {len(rows)} cards:")
        out.append("")
        out.append("| Front | Back |\n|---|---|")
        for c in rows:
            out.append(f"| {safe(c.get('front'))} | {safe(c.get('back'))} |")
        out.append("")
    except Exception:
        out.append("_The cards could not be read for a preview._\n")
for d in removed:
    out.append(f"⚠️ **Removes the deck** {safe(d.get('title'))}.\n")
if not changed and not removed:
    out.append("This pull request doesn't add or change a deck in `index.json`.\n")
out.append("**To review:** read the sample cards, check that the licence fits (the person must own the cards or be allowed to share them), then approve and merge. To refuse, close it with a short, friendly reason.")
out.append("")
out.append("_Written automatically by the deck check. Nothing is published until a maintainer approves and merges._")
print("\n".join(out))
