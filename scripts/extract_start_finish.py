#!/usr/bin/env python3
"""Extract track id, name, and start-finish GPS coordinates for every track.

Reads the per-track JSON files in the data directory and writes a single CSV
with one row per track.

Conventions (matching this repo's existing generate_manifest.py and README):
  * id        -> md5 hex digest of the JSON *filename* (e.g. md5("abc--foo.json"))
                 This is the same id used in the repo's tracks.csv.
  * lat/lon   -> stored as integers for precision; multiply by 1e-7 for degrees.
  * elevation -> stored in millimeters; divided by 1000 for meters here.

Output columns:
  id, name, start_finish_lat, start_finish_lon, start_finish_elev_m, dataset_id

Rows are emitted for every track. If a track has no usable start_finish block,
the coordinate columns are left blank rather than dropping the row.

Usage:
  python extract_start_finish.py [--data-dir ./data] [--out start_finish.csv]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from glob import glob

COORD_SCALE = 1.0e-7   # integer -> decimal degrees
ELEV_SCALE = 1.0e-3    # millimeters -> meters


def decode_coord(value):
    """Return decimal degrees from the integer encoding, or None if missing."""
    if value is None:
        return None
    return round(value * COORD_SCALE, 7)


def decode_elev(value):
    """Return meters from the millimeter encoding, or None if missing."""
    if value is None:
        return None
    return round(value * ELEV_SCALE, 3)


def extract_rows(data_dir):
    files = sorted(glob("*.json", root_dir=data_dir))
    rows = []
    skipped = 0
    for fname in files:
        path = os.path.join(data_dir, fname)
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARNING: could not read {fname}: {exc}")
            skipped += 1
            continue

        sf = data.get("start_finish") or {}
        rows.append(
            {
                "id": hashlib.md5(fname.encode()).hexdigest(),
                "name": data.get("name", ""),
                "start_finish_lat": decode_coord(sf.get("lat")),
                "start_finish_lon": decode_coord(sf.get("lon")),
                "start_finish_elev_m": decode_elev(sf.get("elev")),
                "dataset_id": os.path.splitext(fname)[0],
            }
        )

    rows.sort(key=lambda r: (r["name"].lower(), r["id"]))
    return rows, skipped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="./data", help="directory of track JSON files")
    parser.add_argument("--out", default="start_finish.csv", help="output CSV path")
    args = parser.parse_args()

    rows, skipped = extract_rows(args.data_dir)

    fieldnames = [
        "id",
        "name",
        "start_finish_lat",
        "start_finish_lon",
        "start_finish_elev_m",
        "dataset_id",
    ]
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    missing_coords = sum(1 for r in rows if r["start_finish_lat"] is None)
    print(f"Wrote {len(rows)} tracks to {args.out}")
    if missing_coords:
        print(f"  ({missing_coords} had no start_finish coordinates - left blank)")
    if skipped:
        print(f"  ({skipped} files skipped due to read/parse errors)")


if __name__ == "__main__":
    main()
