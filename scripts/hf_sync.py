"""Mirror the data to the Hugging Face dataset AllRatesToday/central-bank-exchange-rates.

One CSV per institution under rates/ (what the dataset viewer and pandas users
want), the catalogue, ATTRIBUTION.txt
and a generated README.md dataset card. See mirror_lib.py for the lag and the
attribution rules. Needs HF_TOKEN with write access. Run by the daily Action
after a data commit; safe to re-run.
"""
import sys, os, tempfile
from huggingface_hub import HfApi
import mirror_lib as M

REPO = "AllRates/central-bank-exchange-rates"  # upload id: token scope follows the old owner; HF redirects to the org
UTM = "huggingface"

work = tempfile.mkdtemp()
st = M.build(work, UTM, lambda c: f"rates/{c}.csv")

card = f"""---
license: cc-by-nc-4.0
extra_gated_heading: "Access needs a free AllRatesToday API key"
extra_gated_prompt: "This dataset is published by AllRatesToday under CC BY-NC 4.0 (free for research, teaching, personal projects and journalism; commercial use needs the Official Rates plan at https://allratestoday.com/pricing#official). To download it, register for a free AllRatesToday account at https://allratestoday.com/register and paste your API key (it starts with art_live_) below. Requests are checked automatically every 5 minutes: a valid key is approved within about 5 minutes, an invalid one is rejected. If you were rejected by mistake, email support@allratestoday.com with your Hugging Face username and your key."
extra_gated_fields:
  AllRatesToday API key (register free on the AllRatesToday site, key starts with art_live_): text
  I will credit AllRatesToday with a link where the data is shown: checkbox
  Intended use:
    type: select
    options:
      - Research or teaching
      - Personal project
      - Journalism
      - Internal reporting at a company (commercial)
      - Other
extra_gated_button_content: "Get access"
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

> **Need today's rates, not a {M.LAG_DAYS}-day-old mirror?** [Register for a free API key]({M.link('/register/', UTM)}) and query the same data live from the [central bank rates API]({M.link('/central-bank-rates-api/', UTM)}).

## Access

Downloading needs two free accounts: a Hugging Face login, and an AllRatesToday account whose API key you paste into the **Get access** form above ([register here]({M.link('/register/', UTM)}), the key is on your dashboard). Requests are checked every 5 minutes: a valid key is approved within about 5 minutes, an invalid key is rejected. Rejected by mistake? Email support@allratestoday.com with your Hugging Face username and key. In code, run `huggingface-cli login` once (or set `HF_TOKEN`) and `load_dataset`, `pd.read_csv("hf://...")`, Polars and DuckDB all work. The same tables are on the [GitHub source repository]({M.GITHUB}) and the [API]({M.link('/central-bank-rates-api/', UTM)}) as well.

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
| `index.json` | Catalogue of every source: name, country, home currency, latest date, currencies published |
| `sources.json` | Institution metadata, including the official publication page each table comes from |
| `ATTRIBUTION.txt` | How to credit the data and where the live tables are |

## Load

```python
from datasets import load_dataset
ds = load_dataset("AllRatesToday/central-bank-exchange-rates", "rates")
```

```python
import pandas as pd
ecb = pd.read_csv("hf://datasets/AllRatesToday/central-bank-exchange-rates/rates/ecb.csv", parse_dates=["date"])
usd = ecb[(ecb.quote == "USD") & (ecb.type == "reference")].set_index("date")["value"]
```

Need the rate for one date in code rather than the whole file? The API does the holiday fallback for you, no key needed for the latest table:

```bash
curl "{M.SITE}/api/central-bank/ecb/latest"
```

## Sources

| Institution | Country | Code | Home | Latest | Rows | SDK |
|---|---|---|---|---|---|---|
{M.source_rows(st, UTM)}

{M.about(UTM)}
Also on Kaggle: {M.KAGGLE}
"""
open(f"{work}/README.md", "w").write(card)

if "--dry-run" in sys.argv:
    print("dry run, built in", work); sys.exit(0)
api = HfApi()
api.upload_folder(folder_path=work, repo_id=REPO, repo_type="dataset",
                  delete_patterns=["latest/*"],  # history only since 2026-10-26; current tables live on the API
                  commit_message=f"Daily sync: {st['total']:,} rows to {st['cutoff']}")
print(f"synced {st['total']:,} rows (to {st['cutoff']}) to https://huggingface.co/datasets/{REPO}")
