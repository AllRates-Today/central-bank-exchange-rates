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
json.dump({"id": ID}, open(f"{work}/dataset-metadata.json", "w"))
latest = max(v["latest"] for v in json.load(open(f"{DATA}/index.json"))["sources"].values())
subprocess.run(["kaggle", "datasets", "version", "-p", work, "-m", f"Daily refresh, latest table {latest}, {total:,} rows"], check=True)
print(f"pushed {total:,} rows to https://www.kaggle.com/datasets/{ID}")
