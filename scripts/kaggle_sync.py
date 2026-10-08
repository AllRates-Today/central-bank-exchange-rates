"""Push a new version of the Kaggle dataset allratestoday/central-bank-exchange-rates.

Flat layout (Kaggle browses top-level files best): <code>.csv per institution,
latest_<code>.json, index.json, sources.json. Lag and attribution rules in mirror_lib.py. Needs KAGGLE_API_TOKEN. Run by
the daily Action after a data commit; each run is a new dataset version.
"""
import sys, json, os, subprocess, tempfile
import mirror_lib as M

ID = "allratestoday/central-bank-exchange-rates"
UTM = "kaggle"

work = tempfile.mkdtemp()
st = M.build(work, UTM, lambda c: f"{c}.csv", lambda c: f"latest_{c}.json")
total, banks, taxes, oldest, latest = st["total"], st["banks"], st["taxes"], st["oldest"], st["latest"]
src_rows = M.source_rows(st, UTM)

# Kaggle shows dataset-metadata.json's description as the page's README, so it
# has to describe THIS flat layout (<code>.csv, latest_<code>.json), not the
# GitHub repo's data/<code>/history/ tree. Regenerated every version so the
# counts and the sources table never drift from the files beside it.
description = f"""# Central Bank Exchange Rates

Official exchange rates published by **{banks} central banks and {taxes} tax authorities**, one CSV per institution: {total:,} rows, the oldest series from {oldest[:4]}, latest table in this mirror {latest} (the mirror lags the live data by {M.LAG_DAYS} days). Collected and published by [AllRatesToday]({M.link("/central-bank-rates-api/", UTM)}), refreshed daily from the GitHub source repository [AllRates-Today/central-bank-exchange-rates](https://github.com/AllRates-Today/central-bank-exchange-rates).

Every row is the figure the institution itself published for that date: the ECB euro reference rate, the Federal Reserve H.10 table, the Bank of England spot rates, RBI reference rates, PBoC central parity, HMRC monthly rates for VAT, US Treasury quarterly rates, and a hundred more. These are the rates that invoices, tax filings, customs declarations, transfer pricing and audits require, as opposed to market rates.

## Files

| File | What it is |
|---|---|
| `<code>.csv` | Full history for one institution, e.g. `ecb.csv`, `fed.csv`, `boe.csv`, `rbi.csv` |
| `latest_<code>.json` | That institution's most recent table inside the mirror window, with its page and API links |
| `index.json` | Catalogue of every source: name, country, home currency, latest date, currencies published |
| `sources.json` | Institution metadata, including the official publication page each table comes from |
| `ATTRIBUTION.txt` | How to credit the data and where the live tables are |

## Schema (every `<code>.csv`)

| Column | Meaning |
|---|---|
| `date` | Publication date (ISO 8601). Weekends and holidays are absent, as in the source. |
| `base` | Currency being priced (ISO 4217) |
| `quote` | Currency it is priced in |
| `type` | The institution's own label: `reference`, `middle`, `buy`, `sell`, `spot`, `monthly`, `monthly_average`, ... |
| `value` | One unit of `base` costs `value` units of `quote` |

Direction follows the publisher: the ECB quotes `EUR -> USD`, the Reserve Bank of India quotes `USD -> INR`. Nothing is cross-computed; if a bank did not print a pair, it is not in the file.

## Load

```python
import pandas as pd
ecb = pd.read_csv("/kaggle/input/central-bank-exchange-rates/ecb.csv", parse_dates=["date"])
usd = ecb[(ecb.quote == "USD") & (ecb.type == "reference")].set_index("date")["value"]
```

## Sources

| Institution | Country | Code | Home | Latest | Rows |
|---|---|---|---|---|---|
{src_rows}

{M.about(UTM)}
Also on Hugging Face: {M.HF}
"""
json.dump({
    "id": ID,
    "title": "Central Bank Exchange Rates, 1914 to today",
    "subtitle": f"Official rates from {banks} central banks and {taxes} tax authorities, daily",
    "description": description,
    "licenses": [{"name": "CC-BY-4.0"}],
    "keywords": ["finance", "currencies and foreign exchange", "economics", "time series analysis", "banking"],
}, open(f"{work}/dataset-metadata.json", "w"), indent=1)
if "--dry-run" in sys.argv:
    print("dry run, built in", work); sys.exit(0)
subprocess.run(["kaggle", "datasets", "version", "-p", work, "-m", f"Daily refresh to {latest}, {total:,} rows"], check=True)
print(f"pushed {total:,} rows to https://www.kaggle.com/datasets/{ID}")
