"""Shared builder for the Hugging Face and Kaggle mirrors.

Both mirrors get the same treatment:

* LAG_DAYS: rows newer than (today UTC - LAG_DAYS) are left out, and each
  institution's "latest" table is rebuilt at its last date inside the window.
  The mirrors are for research and training; the current day's tables are the
  product and stay on allratestoday.com and the GitHub/jsDelivr files.
* Attribution travels with the data, not only on the card: index.json,
  sources.json and every latest JSON carry `attribution`/`api`/`page` fields,
  and an ATTRIBUTION.txt sits beside the files. Users who load with pandas or
  `datasets` never see the Hub README, so the hook has to be in the files.
* Every allratestoday.com link carries utm_source=<mirror> so GA can tell
  whether anyone follows them.
"""
import datetime as dt, glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LAG_DAYS = 2
SITE = "https://allratestoday.com"
GITHUB = "https://github.com/AllRates-Today/central-bank-exchange-rates"
HF = "https://huggingface.co/datasets/AllRates/central-bank-exchange-rates"
KAGGLE = "https://www.kaggle.com/datasets/allratestoday/central-bank-exchange-rates"


def link(path, utm_source):
    """allratestoday.com URL tagged for GA (source = huggingface | kaggle)."""
    return f"{SITE}{path}?utm_source={utm_source}&utm_medium=dataset&utm_campaign=central-bank-exchange-rates"


def cutoff():
    return (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=LAG_DAYS)).isoformat()


def build(work, utm_source, csv_path, latest_path):
    """Write the lagged mirror into `work`.

    csv_path(code) / latest_path(code) give the per-institution file names
    (HF wants rates/<code>.csv + latest/<code>.json, Kaggle a flat layout).
    Returns a stats dict used by the card/description generators.
    """
    sources = json.load(open(f"{DATA}/sources.json"))
    index = json.load(open(f"{DATA}/index.json"))
    cut = cutoff()
    attribution = {
        "attribution": f"AllRatesToday, {SITE}",
        "license": "CC-BY-4.0",
        "api": link("/central-bank-rates-api/", utm_source),
        "live_data": GITHUB,
        "lag_days": LAG_DAYS,
        "note": f"Mirror ends {cut}. Current tables, per-date lookups and publication calendars are on the API.",
    }
    stats = {"total": 0, "rows_by": {}, "latest_by": {}, "oldest": None, "cutoff": cut}
    for code in sorted(sources):
        files = sorted(glob.glob(f"{DATA}/{code}/history/*.csv"))
        if not files:
            continue
        rows, n, last = [], 0, None
        for path in files:
            out_dir = os.path.dirname(f"{work}/{csv_path(code)}")
            os.makedirs(out_dir, exist_ok=True)
            with open(f"{work}/{csv_path(code)}", "a") as out:
                if n == 0 and out.tell() == 0:
                    out.write("date,base,quote,type,value\n")
                for line in open(path).read().split("\n")[1:]:
                    if not line:
                        continue
                    date = line[:10]
                    if date > cut:
                        continue
                    out.write(line + "\n"); n += 1
                    if stats["oldest"] is None or date < stats["oldest"]:
                        stats["oldest"] = date
                    if last is None or date > last:
                        last, rows = date, [line]
                    elif date == last:
                        rows.append(line)
        if n == 0:
            os.remove(f"{work}/{csv_path(code)}")
            continue
        stats["total"] += n; stats["rows_by"][code] = n; stats["latest_by"][code] = last
        # latest table rebuilt at the lagged date, metadata from the live file
        meta = {}
        if os.path.exists(f"{DATA}/{code}/latest.json"):
            meta = json.load(open(f"{DATA}/{code}/latest.json"))
        latest = {k: meta.get(k) for k in ("source", "name", "country", "home_currency", "kind", "cadence", "official_source", "page", "license") if k in meta}
        latest.setdefault("source", code)
        latest["date"] = last
        latest["rates"] = []
        for line in rows:
            _, base, quote, typ, value = line.split(",", 4)
            latest["rates"].append({"base": base, "quote": quote, "type": typ, "value": float(value)})
        latest["page"] = link(f"/central-bank-rates-api/{code}/", utm_source)
        latest["api"] = attribution["api"]
        latest["attribution"] = attribution["attribution"]
        latest["lag_days"] = LAG_DAYS
        os.makedirs(os.path.dirname(f"{work}/{latest_path(code)}"), exist_ok=True)
        json.dump(latest, open(f"{work}/{latest_path(code)}", "w"), separators=(",", ":"))

    # index.json: same catalogue, dates clamped to the mirror window, tagged pages
    idx = {"generated_at": index["generated_at"], "source_count": len(stats["rows_by"]), **attribution, "sources": {}}
    for code in stats["rows_by"]:
        s = dict(index["sources"].get(code) or {k: sources[code][k] for k in ("name", "country", "home_currency", "kind")})
        s["latest"] = stats["latest_by"][code]
        s.pop("latest_url", None); s.pop("stale", None)
        s["page"] = link(f"/central-bank-rates-api/{code}/", utm_source)
        s["currencies"] = s.get("currencies")
        idx["sources"][code] = s
    json.dump(idx, open(f"{work}/index.json", "w"), indent=1)
    src = {code: {**sources[code], "page": link(f"/central-bank-rates-api/{code}/", utm_source)} for code in sorted(sources)}
    json.dump(src, open(f"{work}/sources.json", "w"), indent=1)

    banks = sum(1 for c in stats["rows_by"] if sources[c].get("kind") != "tax_authority" and c != "composite")
    stats.update(banks=banks, taxes=sum(1 for c in stats["rows_by"] if sources[c].get("kind") == "tax_authority"),
                 latest=max(stats["latest_by"].values()), sources=sources)
    with open(f"{work}/ATTRIBUTION.txt", "w") as f:
        f.write(f"""Central Bank Exchange Rates - official rates from {banks} central banks and {stats['taxes']} tax authorities
Collected and published by AllRatesToday, {SITE}
License: CC BY 4.0. Credit "AllRatesToday" with a link to {SITE} in anything you build or publish from this data.

This mirror ends {cut} (it lags the live source by {LAG_DAYS} days).
Today's tables, per-date lookups, publication calendars and JSON/CSV/XML/XLSX output:
  {attribution['api']}
Live files, refreshed four times a day, with per-day snapshots (no key):
  {GITHUB}
Underlying figures are public publications of the institutions named in sources.json.
""")
    return stats


def source_rows(stats, utm_source):
    """Markdown rows for the Sources table, institution name linked to its page."""
    return "\n".join(
        f"| [{stats['sources'][c]['name']}]({link(f'/central-bank-rates-api/{c}/', utm_source)}) | {stats['sources'][c]['country']} | `{c}` | {stats['sources'][c]['home_currency']} | {stats['latest_by'][c]} | {stats['rows_by'][c]:,} |"
        for c in stats["rows_by"])


def about(utm_source):
    """The AllRatesToday section shared by both cards."""
    L = lambda p: link(p, utm_source)
    return f"""## About AllRatesToday

This dataset is collected and maintained by [AllRatesToday]({L('/')}), a currency-data API built for developers, finance teams and AI agents. It is the same ingest pipeline that powers the live service: it fetches each institution's own publication, checks every table against the other banks for unit and direction errors, and quarantines anything more than ten percent off, so what you load here is what the bank printed.

**This mirror lags the live data by {LAG_DAYS} days.** It is meant for research, backtesting and model training. If you need today's table, a rate for a specific invoice date, or the next publication time, use the live service:

| Need | Where |
|---|---|
| Today's tables, four refreshes a day, JSON/CSV over a CDN, no key | [GitHub source repository]({GITHUB}) |
| Rate on a given date with holiday fallback, time series, pair resolution, publication calendars, CSV/XML/XLSX | [Central bank rates API]({L('/central-bank-rates-api/')}) |
| Real-time mid-market rates for 160+ currencies alongside the official ones | [Exchange rate API]({L('/exchange-rate-api/')}) |
| Per-institution page with the live table, cadence and FAQ | `{SITE}/central-bank-rates-api/<code>/` |
| Month-end close, VAT and customs, transfer pricing, audit evidence | [For finance teams]({L('/for-finance-teams/')}) |
| ERP and spreadsheet guides (SAP, Oracle, NetSuite, Dynamics, Sheets, Excel) | [Integrations]({L('/docs/integrations/')}) |
| Use the rates from Claude, Cursor or any MCP client | [Hosted MCP endpoint]({L('/mcp/')}) and the `@allratestoday/mcp-server` package |
| SDKs: `@allratestoday/sdk` (JS), `allratestoday` (Python), Go, PHP, Rust, plus one npm package per institution (e.g. `ecb-exchange-rate`) | [Documentation]({L('/docs/')}) |

The API is free to start, with paid plans for volume and an official-rates plan for finance teams: [pricing]({L('/pricing/')}).

## Cite

> AllRatesToday (2026). *Central Bank Exchange Rates: official rates from central banks and tax authorities, 1914 to today.* {GITHUB} (data via {SITE}/central-bank-rates-api/). CC BY 4.0.

## License

CC BY 4.0. Free for any use, including commercial, with a visible credit to AllRatesToday linking to {SITE}. The underlying figures are public information published by each institution. Verify against the institution before relying on a figure for a legal or tax filing.
"""
