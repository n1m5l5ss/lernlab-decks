"""Checks index.json and every deck in it. Run: python3 scripts/check.py"""
import hashlib, json, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LICENCES = {"CC-BY-4.0", "CC-BY-SA-4.0", "CC0-1.0"}
MAX_SIZE = 200 * 1024 * 1024
errors = []

def fail(msg):
    errors.append(msg)

index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
if index.get("format") != "lernlab-gallery" or index.get("version") != 1:
    fail('index.json: "format" must be "lernlab-gallery" and "version" must be 1')
seen = set()
listed = set()
for n, d in enumerate(index.get("decks", [])):
    where = f"decks[{n}] ({d.get('id', '?')})"
    for key in ("id", "title", "cards", "licence", "author", "url", "sha256", "size"):
        if key not in d:
            fail(f"{where}: missing {key}")
    did = d.get("id", "")
    if not re.fullmatch(r"[a-z0-9-]{1,80}", did):
        fail(f"{where}: id must be lower-case letters, digits and -, up to 80 characters")
    if did in seen:
        fail(f"{where}: id is used twice")
    seen.add(did)
    if d.get("licence") not in LICENCES:
        fail(f"{where}: licence must be one of {sorted(LICENCES)}")
    url = d.get("url", "")
    if url != f"decks/{did}.lernpack":
        fail(f"{where}: url must be decks/{did}.lernpack")
        continue
    path = ROOT / url
    listed.add(path.name)
    if not path.is_file():
        fail(f"{where}: {url} does not exist")
        continue
    data = path.read_bytes()
    if len(data) > MAX_SIZE:
        fail(f"{where}: file is over 200 MB")
    if d.get("size") != len(data):
        fail(f"{where}: size should be {len(data)}")
    if d.get("sha256") != hashlib.sha256(data).hexdigest():
        fail(f"{where}: sha256 should be {hashlib.sha256(data).hexdigest()}")
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            for name in names:
                if name.startswith("/") or ".." in name.split("/") or "\\" in name:
                    fail(f"{where}: unsafe path in zip: {name}")
            manifest = next((x for x in names if x.split("/")[-1] == "manifest.json" and x.count("/") <= 1), None)
            if not manifest:
                fail(f"{where}: no manifest.json in the package")
                continue
            m = json.loads(z.read(manifest))
            if m.get("format") != "lernpack" or m.get("version") != 1:
                fail(f"{where}: not a .lernpack version 1")
            if m.get("cards") != d.get("cards"):
                fail(f"{where}: cards should be {m.get('cards')} (from manifest.json)")
    except zipfile.BadZipFile:
        fail(f"{where}: not a zip file")

for f in (ROOT / "decks").glob("*"):
    if f.name not in listed:
        fail(f"decks/{f.name} is not listed in index.json")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(seen)} decks")
