"""Sync the S&S Machinery stock feed from Modern DMS into the ss-stock branch.

Reads the private MDMS feed address from the MDMS_FEED_URL secret, keeps only
public listing fields, stores sale photos under stable file names (by
photo_key, so unchanged photos are never re-downloaded) and writes stock.json
for sandsmachinery.com.au/stock.html to read.

Usage: python ss_stock_feed.py <output_dir>
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

OUT = sys.argv[1]
FEED = os.environ.get("MDMS_FEED_URL", "").strip()
if not FEED:
    sys.exit("MDMS_FEED_URL secret is not set")

KEEP = ["stock_number", "make", "model", "series", "year", "category", "condition",
        "machine_condition", "status", "description", "price", "branch",
        "location_suburb", "location_state", "location_postcode", "hours",
        "meter_type", "engine_hours", "has_books", "updated_at"]


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "ss-stock-sync/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


try:
    data = json.loads(get(FEED))
except urllib.error.HTTPError as err:
    # 401 = token wrong or feed switched off. Keep the last good stock.json
    # rather than emptying the website, and fail so the run shows red.
    sys.exit(f"Feed returned HTTP {err.code}; leaving the published stock unchanged")

os.makedirs(f"{OUT}/photos", exist_ok=True)
os.makedirs(f"{OUT}/thumbs", exist_ok=True)

units, wanted = [], set()
for u in data.get("units", []):
    item = {k: u.get(k) for k in KEEP}
    photos = []
    for i, key in enumerate(u.get("photo_keys") or []):
        name = hashlib.sha1(key.encode()).hexdigest()[:20] + ".jpg"
        wanted.add(name)
        for folder, src in (("photos", (u.get("photos") or [])), ("thumbs", (u.get("thumbnails") or []))):
            path = f"{OUT}/{folder}/{name}"
            if not os.path.exists(path) and i < len(src) and src[i]:
                with open(path, "wb") as f:
                    f.write(get(src[i]))
        photos.append(name)
    item["photos"] = photos
    units.append(item)

# Drop images no longer used by any published machine.
for folder in ("photos", "thumbs"):
    for name in os.listdir(f"{OUT}/{folder}"):
        if name not in wanted:
            os.remove(f"{OUT}/{folder}/{name}")

payload = {"dealer": data.get("dealer"), "count": len(units), "units": units}
path = f"{OUT}/stock.json"
old = None
if os.path.exists(path):
    with open(path) as f:
        old = json.load(f)
    old.pop("synced_at", None)
if old != payload:
    payload["synced_at"] = data.get("generated_at")
    with open(path, "w") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    print(f"stock.json updated: {len(units)} machines")
else:
    print(f"No change: {len(units)} machines")
