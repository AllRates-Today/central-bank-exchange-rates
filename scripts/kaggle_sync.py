"""Push a new version of the Kaggle dataset allratestoday/central-bank-exchange-rates.

Flat layout (Kaggle browses top-level files best): <code>.csv per institution,
latest_<code>.json, index.json, sources.json. Lag and attribution rules in mirror_lib.py. Needs KAGGLE_API_TOKEN. Run by
the daily Action after a data commit; each run is a new dataset version.
"""
import sys, json, os, subprocess, tempfile
import mirror_lib as M

ID = "allratestoday/central-bank-exchange-rates"
UTM = "kaggle"

CSV_FIELDS = [
    {"name": "date", "type": "datetime", "description": "Publication date (ISO 8601, YYYY-MM-DD). Weekends and holidays are absent, exactly as in the institution's own table."},
    {"name": "base", "type": "string", "description": "Currency being priced (ISO 4217 code). Direction follows the publisher: the ECB prices EUR, the Reserve Bank of India prices USD."},
    {"name": "quote", "type": "string", "description": "Currency the base is priced in (ISO 4217 code), usually the institution's home currency."},
    {"name": "type", "type": "string", "description": "The institution's own label for the figure: reference, middle, buy, sell, spot, monthly, monthly_average, etc. Filter on it before building a series."},
    {"name": "value", "type": "numeric", "description": "One unit of base costs this many units of quote, as printed by the institution. Nothing is cross-computed or rounded."},
]


def resources(stats):
    """Per-file descriptions and column schemas (Kaggle 'file information' and
    'column descriptors'); the sources' own publication pages double as provenance."""
    src, out = stats["sources"], []
    for code in stats["rows_by"]:
        s = src[code]
        who = f"{s['name']} ({s['country']}, home currency {s['home_currency']})"
        out.append({"path": f"{code}.csv",
                    "description": f"Full history of official exchange rates published by {who}: {stats['rows_by'][code]:,} rows up to {stats['latest_by'][code]}, one row per date, currency pair and rate type. Source: {s.get('official_source') or s['page']}",
                    "schema": {"fields": CSV_FIELDS}})
        out.append({"path": f"latest_{code}.json",
                    "description": f"Most recent table from {s['name']} inside the mirror window ({stats['latest_by'][code]}): institution metadata, cadence, the list of rates (base, quote, type, value), and links to the live page and API."})
    out += [
        {"path": "index.json", "description": "Catalogue of every institution in the dataset: code, name, country, home currency, kind (central_bank or tax_authority), cadence, latest date in the mirror, number of currencies published, and page link."},
        {"path": "sources.json", "description": "Institution metadata keyed by code, including official_source, the URL of the publication page or feed each table is collected from. This is the provenance of every row."},
        {"path": "ATTRIBUTION.txt", "description": "How to credit the data (CC BY-NC 4.0, credit AllRatesToday with a link), the mirror's end date, and where the live tables are."},
    ]
    return out

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
    "licenses": [{"name": "CC-BY-NC-4.0"}],
    "keywords": ["finance", "currencies and foreign exchange", "economics", "time series analysis", "banking"],
    "resources": resources(st),
    # Provenance ("Sources" in the metadata tab) and update frequency are
    # dataset settings, not version fields: pushed by `datasets metadata --update`.
    "userSpecifiedSources": (
        f"Official publications of {banks} central banks and {taxes} tax authorities, each fetched from the institution's own page or feed "
        f"(exact URL per institution in sources.json, field official_source), e.g. ECB {st['sources']['ecb']['official_source']}, "
        f"Federal Reserve H.10 {st['sources']['fed']['official_source']}, Bank of England {st['sources']['boe']['official_source']}. "
        f"Collected daily by the AllRatesToday ingest pipeline, cross-checked across banks for unit and direction errors, "
        f"and published with per-day snapshots at {M.GITHUB}; this mirror lags that source by {M.LAG_DAYS} days."
    ),
    "expectedUpdateFrequency": "daily",
}, open(f"{work}/dataset-metadata.json", "w"), indent=1)
meta = json.load(open(f"{work}/dataset-metadata.json"))
if "--dry-run" in sys.argv:
    print("dry run, built in", work); sys.exit(0)
if "--settings-only" not in sys.argv:
    subprocess.run(["kaggle", "datasets", "version", "-p", work, "-m", f"Daily refresh to {latest}, {total:,} rows"], check=True)
    print(f"pushed {total:,} rows to https://www.kaggle.com/datasets/{ID}")
# File descriptions and columns travel with the version; provenance sources,
# update frequency and licence need the settings call. Two Kaggle quirks
# (verified 2026-10-12): the settings endpoint rejects the documented licence
# id "CC-BY-NC-4.0" ("You've specified an invalid license"), so the licence
# is "other" and the description states CC BY-NC 4.0; and it answers
# HTTP 200 with an empty body, which the client crashes decoding, so the
# empty success reply is handled here. Non-fatal so it never fails the mirror.
meta["licenses"] = [{"name": "other"}]
json.dump(meta, open(f"{work}/dataset-metadata.json", "w"), indent=1)
code = f"""
from kagglesdk import kaggle_http_client as H
orig = H.KaggleHttpClient._prepare_response
def patched(self, rt, resp):
    if resp.status_code == 200 and not resp.text.strip():
        return rt() if rt is not None else None
    return orig(self, rt, resp)
H.KaggleHttpClient._prepare_response = patched
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi(); api.authenticate()
api.dataset_metadata_update({ID!r}, {work!r})
"""
r = subprocess.run([sys.executable, "-c", code])
print("settings update", "ok" if r.returncode == 0 else f"failed (exit {r.returncode})", flush=True)
back = tempfile.mkdtemp()
if subprocess.run(["kaggle", "datasets", "metadata", "-p", back, ID], capture_output=True).returncode == 0:
    m = json.load(open(f"{back}/dataset-metadata.json")).get("info", {})
    print("Kaggle now holds:", {k: m.get(k) for k in ("licenses", "expectedUpdateFrequency", "usabilityRating")},
          "sources:", (m.get("userSpecifiedSources") or "")[:80] + "...")
