"""Mirror the data to the Hugging Face dataset AllRates/central-bank-exchange-rates.

Consolidates the per-year CSVs into one CSV per institution (what the dataset
viewer and pandas users want), copies the latest tables and catalogue, and
uploads the changed files. Needs HF_TOKEN with write access. Run by the daily
Action after a data commit; safe to re-run.
"""
import glob, json, os, shutil, sys, tempfile
from huggingface_hub import HfApi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPO = "AllRates/central-bank-exchange-rates"

work = tempfile.mkdtemp()
os.makedirs(f"{work}/rates"); os.makedirs(f"{work}/latest")
sources = json.load(open(f"{DATA}/sources.json"))
total = 0
for code in sorted(sources):
    files = sorted(glob.glob(f"{DATA}/{code}/history/*.csv"))
    if not files:
        continue
    with open(f"{work}/rates/{code}.csv", "w") as out:
        out.write("date,base,quote,type,value\n")
        for f in files:
            for line in open(f).read().split("\n")[1:]:
                if line:
                    out.write(line + "\n"); total += 1
    if os.path.exists(f"{DATA}/{code}/latest.json"):
        shutil.copy(f"{DATA}/{code}/latest.json", f"{work}/latest/{code}.json")
shutil.copy(f"{DATA}/index.json", work); shutil.copy(f"{DATA}/sources.json", work)

api = HfApi()
# keep the dataset card that lives on the Hub; only data files are synced
api.upload_folder(folder_path=work, repo_id=REPO, repo_type="dataset",
                  commit_message=f"Daily sync: {total:,} rows")
print(f"synced {total:,} rows to https://huggingface.co/datasets/{REPO}")
