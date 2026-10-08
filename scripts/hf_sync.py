"""Mirror the data to the Hugging Face dataset AllRates/central-bank-exchange-rates.

One CSV per institution under rates/ (what the dataset viewer and pandas users
want), the lagged latest tables under latest/, the catalogue, ATTRIBUTION.txt
and a generated README.md dataset card. See mirror_lib.py for the lag and the
attribution rules. Needs HF_TOKEN with write access. Run by the daily Action
after a data commit; safe to re-run.
"""
import sys, os, tempfile
from huggingface_hub import HfApi
import mirror_lib as M

REPO = "AllRates/central-bank-exchange-rates"
UTM = "huggingface"

work = tempfile.mkdtemp()
st = M.build(work, UTM, lambda c: f"rates/{c}.csv", lambda c: f"latest/{c}.json")

card = f"""---
license: cc-by-4.0
language:
- en
pretty_name: Central Bank Exchange Rates
tags:
- finance
- exchange-rates
- currency
- forex
- central-bank
- economics
- time-series
- official-rates
- tax
size_categories:
- 10M<n<100M
task_categories:
- time-series-forecasting
configs:
- config_name: rates
  data_files: "rates/*.csv"
  default: true
---

# Central Bank Exchange Rates

Official exchange rates published by **{st['banks']} central banks and {st['taxes']} tax authorities**, as one CSV per institution: {st['total']:,} rows, the oldest series from {st['oldest'][:4]}, latest table in this mirror {st['latest']}. Collected and published by [AllRatesToday]({M.link('/central-bank-rates-api/', UTM)}) and refreshed daily from the GitHub source repository [AllRates-Today/central-bank-exchange-rates]({M.GITHUB}).

Every row is the figure the institution itself published for that date: the ECB euro reference rate, the Federal Reserve H.10 table, the Bank of England spot rates, RBI reference rates, PBoC central parity, HMRC monthly rates for VAT, US Treasury quarterly rates, and a hundred more. These are the rates that invoices, tax filings, customs declarations, transfer pricing and audits require, as opposed to market rates.

## Schema

| Column | Meaning |
|---|---|
| `date` | Publication date (ISO 8601). Weekends and holidays are absent, as in the source. |
| `base` | Currency being priced (ISO 4217) |
| `quote` | Currency it is priced in |
| `type` | The institution's own label: `reference`, `middle`, `buy`, `sell`, `spot`, `monthly`, `monthly_average`, ... |
| `value` | One unit of `base` costs `value` units of `quote` |

Direction follows the publisher: the ECB quotes `EUR → USD`, the Reserve Bank of India quotes `USD → INR`. Nothing is cross-computed; if a bank did not print a pair, it is not in the file.

## Files

| File | What it is |
|---|---|
| `rates/<code>.csv` | Full history for one institution, e.g. `rates/ecb.csv`, `rates/fed.csv`, `rates/boe.csv`, `rates/rbi.csv` |
| `latest/<code>.json` | That institution's most recent table inside the mirror window, with its page and API links |
| `index.json` | Catalogue of every source: name, country, home currency, latest date, currencies published |
| `sources.json` | Institution metadata, including the official publication page each table comes from |
| `ATTRIBUTION.txt` | How to credit the data and where the live tables are |

## Load

```python
from datasets import load_dataset
ds = load_dataset("AllRates/central-bank-exchange-rates", "rates")
```

```python
import pandas as pd
ecb = pd.read_csv("hf://datasets/AllRates/central-bank-exchange-rates/rates/ecb.csv", parse_dates=["date"])
usd = ecb[(ecb.quote == "USD") & (ecb.type == "reference")].set_index("date")["value"]
```

Need the rate for one date in code rather than the whole file? The API does the holiday fallback for you, no key needed for the latest table:

```bash
curl "{M.SITE}/api/central-bank/ecb/latest"
```

## Sources

| Institution | Country | Code | Home | Latest | Rows |
|---|---|---|---|---|---|
{M.source_rows(st, UTM)}

{M.about(UTM)}
Also on Kaggle: {M.KAGGLE}
"""
open(f"{work}/README.md", "w").write(card)

if "--dry-run" in sys.argv:
    print("dry run, built in", work); sys.exit(0)
api = HfApi()
api.upload_folder(folder_path=work, repo_id=REPO, repo_type="dataset",
                  commit_message=f"Daily sync: {st['total']:,} rows to {st['cutoff']}")
print(f"synced {st['total']:,} rows (to {st['cutoff']}) to https://huggingface.co/datasets/{REPO}")
