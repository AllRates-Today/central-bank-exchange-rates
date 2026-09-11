"""Push a new version of the Kaggle dataset allratestoday/central-bank-exchange-rates.

Flat layout (Kaggle browses top-level files best): <code>.csv per institution,
latest_<code>.json, index.json, sources.json. Needs KAGGLE_API_TOKEN. Run by
the daily Action after a data commit; each run is a new dataset version.
"""
import glob, json, os, shutil, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
ID = "allratestoday/central-bank-exchange-rates"

work = tempfile.mkdtemp()
sources = json.load(open(f"{DATA}/sources.json"))
total = 0
for code in sorted(sources):
    files = sorted(glob.glob(f"{DATA}/{code}/history/*.csv"))
    if not files:
        continue
    with open(f"{work}/{code}.csv", "w") as out:
        out.write("date,base,quote,type,value\n")
        for f in files:
            for line in open(f).read().split("\n")[1:]:
                if line:
                    out.write(line + "\n"); total += 1
    if os.path.exists(f"{DATA}/{code}/latest.json"):
        shutil.copy(f"{DATA}/{code}/latest.json", f"{work}/latest_{code}.json")
shutil.copy(f"{DATA}/index.json", work); shutil.copy(f"{DATA}/sources.json", work)
index = json.load(open(f"{DATA}/index.json"))
latest = max(v["latest"] for v in index["sources"].values())

# Kaggle shows dataset-metadata.json's description as the page's README, so it
# has to describe THIS flat layout (<code>.csv, latest_<code>.json), not the
# GitHub repo's data/<code>/history/ tree. Regenerated every version so the
# counts and the sources table never drift from the files beside it.
rows_by = {}
for code in sorted(sources):
    if os.path.exists(f"{work}/{code}.csv"):
        rows_by[code] = sum(1 for _ in open(f"{work}/{code}.csv")) - 1
banks = sum(1 for c in rows_by if sources[c].get("kind") != "tax_authority" and c != "composite")
taxes = len(rows_by) - banks
oldest = min((min(l.split(",")[0] for l in open(f"{work}/{c}.csv").read().split("\n")[1:] if l) for c in rows_by), default="")
# A source can be in the CSVs (history) but absent from index.json for a run
# (its live table failed to fetch that pass) — take the date from the file then.
def latest_of(c):
    if c in index["sources"]:
        return index["sources"][c]["latest"]
    return max(l.split(",")[0] for l in open(f"{work}/{c}.csv").read().split("\n")[1:] if l)
src_rows = "\n".join(
    f"| {sources[c]['name']} | {sources[c]['country']} | `{c}` | {sources[c]['home_currency']} | {latest_of(c)} | {rows_by[c]:,} |"
    for c in rows_by)
description = f"""# Central Bank Exchange Rates

Official exchange rates published by **{banks} central banks and {taxes} tax authorities**, one CSV per institution: {total:,} rows, the oldest series from {oldest[:4]}, latest table {latest}. Collected and published by [AllRatesToday](https://allratestoday.com/central-bank-rates-api/), refreshed daily from the GitHub source repository [AllRates-Today/central-bank-exchange-rates](https://github.com/AllRates-Today/central-bank-exchange-rates).

Every row is the figure the institution itself published for that date: the ECB euro reference rate, the Federal Reserve H.10 table, the Bank of England spot rates, RBI reference rates, PBoC central parity, HMRC monthly rates for VAT, US Treasury quarterly rates, and a hundred more. These are the rates that invoices, tax filings, customs declarations, transfer pricing and audits require, as opposed to market rates.

## Files

| File | What it is |
|---|---|
| `<code>.csv` | Full history for one institution, e.g. `ecb.csv`, `fed.csv`, `boe.csv`, `rbi.csv` |
| `latest_<code>.json` | That institution's current table, as published |
| `index.json` | Catalogue of every source: name, country, home currency, latest date, freshness, currencies published |
| `sources.json` | Institution metadata, including the official publication page each table comes from |

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

## About AllRatesToday

This dataset is maintained by [AllRatesToday](https://allratestoday.com/), a currency-data API for developers and finance teams. The website serves the same official tables live, with per-date lookups, time series, publication calendars and JSON/CSV/XML/XLSX output, plus real-time mid-market rates for 160+ currencies:

- Website: https://allratestoday.com/
- Central bank rates API: https://allratestoday.com/central-bank-rates-api/
- Per-institution pages (live table, cadence, FAQ): `https://allratestoday.com/central-bank-rates-api/<code>/`
- API documentation: https://allratestoday.com/docs/
- npm SDK per institution (e.g. `ecb-exchange-rate`): https://www.npmjs.com/org/allratestoday

## Also available

The same data as JSON/CSV over a CDN (no key): https://github.com/AllRates-Today/central-bank-exchange-rates. On Hugging Face: https://huggingface.co/datasets/AllRates/central-bank-exchange-rates.

License: CC BY 4.0. Attribution: "AllRatesToday, https://allratestoday.com". The underlying figures are public publications of the institutions named above.
"""
json.dump({
    "id": ID,
    "title": "Central Bank Exchange Rates, 1914 to today",
    "subtitle": f"Official rates from {banks} central banks and {taxes} tax authorities, daily",
    "description": description,
    "licenses": [{"name": "CC-BY-4.0"}],
    "keywords": ["finance", "currencies and foreign exchange", "economics", "time series analysis", "banking"],
}, open(f"{work}/dataset-metadata.json", "w"), indent=1)
subprocess.run(["kaggle", "datasets", "version", "-p", work, "-m", f"Daily refresh, latest table {latest}, {total:,} rows"], check=True)
print(f"pushed {total:,} rows to https://www.kaggle.com/datasets/{ID}")
