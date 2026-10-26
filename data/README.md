# Data

Raw data is not committed to this repository (the CSV exceeds GitHub's 100 MB limit).

## Source

CFPB Consumer Complaint Database (CCDB), monthly export for June 2026.

- Source URL: _TODO_
- Downloaded: _TODO_
- Save as: `data/raw/CCDB_Export_19_June_2026.zip`

## Integrity check

The notebook refuses to run unless the file matches this fingerprint:

| File | sha256 |
|---|---|
| `CCDB_Export_19_June_2026.zip` | `3021c8af9eeed4971a92f15be21c7ce08cf3c1337151de255e5b12bf782049df` |

Expected contents: 620,794 rows, 16 columns, unique `Complaint ID`.

## Folders

- `raw/`: original downloads, never modified
- `processed/`: files the notebook generates (samples, model outputs)
