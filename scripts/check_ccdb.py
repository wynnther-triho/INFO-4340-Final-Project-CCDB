"""
Quick profile of a CFPB CCDB archive export.
Usage:  python scripts/check_ccdb.py data/raw/CCDB_Export_19_June_2026.zip
Prints a summary only (no raw narratives), so the output is safe to paste back.
"""
import sys, zipfile, hashlib
import pandas as pd

path = sys.argv[1]

# --- 1. What's in the file -------------------------------------------------
print("=== FILE ===")
print("sha256:", hashlib.sha256(open(path, "rb").read()).hexdigest())
if path.lower().endswith(".zip"):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        print("files inside zip:", names)
        csvs = [n for n in names if n.lower().endswith(".csv")]
        assert csvs, "No CSV inside the zip; tell Claude what files are there."
        with z.open(csvs[0]) as f:
            df = pd.read_csv(f, dtype=str, low_memory=False)
else:
    df = pd.read_csv(path, dtype=str, low_memory=False)

print(f"rows: {len(df):,}   columns: {df.shape[1]}")

# --- 2. Columns and missingness --------------------------------------------
print("\n=== COLUMNS (non-null count, % null) ===")
for c in df.columns:
    nn = df[c].notna().sum()
    print(f"  {c!r:45} {nn:>9,}  {100*(1-nn/len(df)):5.1f}% null")

def find(*keys):
    """Find a column whose name contains all keywords (case-insensitive)."""
    for c in df.columns:
        if all(k in c.lower() for k in keys):
            return c
    return None

col_resp = find("response", "consumer")
col_narr = find("narrative")
col_date = find("date", "received")
col_sent = find("date", "sent")
col_id = find("complaint", "id")
col_prod = find("product")
col_timely = find("timely")

def counts(col, label, n=15):
    print(f"\n=== {label} [{col}] ===")
    if col is None:
        print("  (column not found)")
        return
    vc = df[col].value_counts(dropna=False)
    for k, v in vc.head(n).items():
        print(f"  {str(k):60} {v:>9,}  {100*v/len(df):5.1f}%")
    if len(vc) > n:
        print(f"  ... {len(vc)-n} more values")

# --- 3. Outcome field (the prediction target) -------------------------------
counts(col_resp, "COMPANY RESPONSE TO CONSUMER")

# --- 4. Narratives -----------------------------------------------------------
print(f"\n=== NARRATIVES [{col_narr}] ===")
if col_narr is None:
    print("  (no narrative column found)")
else:
    s = df[col_narr].dropna()
    s = s[s.str.strip() != ""]
    print(f"  rows with narrative: {len(s):,} ({100*len(s)/len(df):.1f}%)")
    if len(s):
        L = s.str.len()
        print(f"  length chars: min {L.min()}, median {int(L.median())}, "
              f"mean {int(L.mean())}, p95 {int(L.quantile(.95))}, max {L.max()}")
        x_share = s.str.contains("XXXX").mean()
        print(f"  share containing 'XXXX' redaction: {100*x_share:.1f}%")
        if col_resp:
            print("  outcome distribution among rows WITH narrative:")
            vc = df.loc[s.index, col_resp].value_counts(dropna=False)
            for k, v in vc.items():
                print(f"    {str(k):58} {v:>9,}  {100*v/len(s):5.1f}%")

# --- 5. Dates -----------------------------------------------------------------
for col, label in [(col_date, "DATE RECEIVED"), (col_sent, "DATE SENT TO COMPANY")]:
    print(f"\n=== {label} [{col}] ===")
    if col:
        d = pd.to_datetime(df[col], errors="coerce")
        print(f"  min {d.min()}   max {d.max()}   unparseable {d.isna().sum():,}")

# --- 6. Other checks -----------------------------------------------------------
counts(col_prod, "PRODUCT", n=20)
counts(col_timely, "TIMELY RESPONSE")
if col_id:
    print(f"\n=== DUPLICATE COMPLAINT IDs [{col_id}] ===")
    print(f"  duplicates: {df[col_id].duplicated().sum():,}")
