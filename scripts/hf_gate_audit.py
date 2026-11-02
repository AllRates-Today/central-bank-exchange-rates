"""Backstop for the Hugging Face gate (the live approver is the site worker cron,
astro-blog-starter-template/src/lib/hf-gate.ts, which accepts/rejects pending
requests every 5 minutes against the API_KEYS KV). This script re-checks already
accepted users once a day in case a key was deleted since.

Enforce the Hugging Face gate: every approved user must have given a valid
AllRatesToday API key in the access form. Approval is automatic on HF; this
script runs afterwards, validates the key each user typed, and cancels access
where it is missing or invalid (the user can request again after registering).

Usage:
  python hf_gate_audit.py              # check requests from the last 30 hours
  python hf_gate_audit.py --all        # re-check everyone
  python hf_gate_audit.py --dry-run    # report only
  python hf_gate_audit.py --accept USER   # restore a revoked user (they emailed a valid key)
  python hf_gate_audit.py --reject USER   # refuse a pending user for good

Revoked users land in HF's "pending" list and cannot resubmit the form, so the
gate text tells them to email support@ with their HF username and key; restore
with --accept.

Needs HF_TOKEN (or ~/.cache/huggingface/token) with write access to the dataset.
A key is validated with one request to /api/v1/rates: 401 = invalid, anything
else (200, 429 quota) = the key exists.
"""
import argparse, datetime as dt, json, os, re, sys, urllib.request

REPO = "AllRatesToday/central-bank-exchange-rates"
FIELD_RE = re.compile(r"api key", re.I)
KEY_RE = re.compile(r"art_live_[A-Za-z0-9_-]{8,}")
SITE = "https://allratestoday.com"
ALLOWLIST = {"Chathurangac8"}  # owner test account; never revoked


def key_from_fields(fields):
    """The form answer whose label mentions 'API key'; falls back to any art_live_ value."""
    if not fields:
        return None
    if isinstance(fields, dict):
        items = fields.items()
    else:
        items = [(f.get("name") or f.get("label") or "", f.get("value")) for f in fields]
    for label, value in items:
        if FIELD_RE.search(str(label)) and value:
            m = KEY_RE.search(str(value))
            return m.group(0) if m else str(value).strip()
    for _, value in items:
        m = KEY_RE.search(str(value or ""))
        if m:
            return m.group(0)
    return None


def key_is_valid(key):
    if not key or not KEY_RE.fullmatch(key):
        return False
    req = urllib.request.Request(
        f"{SITE}/api/v1/rates?base=EUR&symbols=USD",
        headers={"Authorization": f"Bearer {key}", "User-Agent": "hf-gate-audit/1"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status != 401
    except urllib.error.HTTPError as e:
        return e.code != 401
    except Exception as e:  # network trouble: never revoke on a transient error
        print(f"  ! could not validate ({e}); treating as valid for now", file=sys.stderr)
        return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--since-hours", type=float, default=30)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--accept", metavar="USER")
    ap.add_argument("--reject", metavar="USER")
    a = ap.parse_args()

    from huggingface_hub import HfApi
    api = HfApi()
    if a.accept:
        api.accept_access_request(REPO, a.accept, repo_type="dataset")
        print(f"accepted {a.accept}")
        return
    if a.reject:
        api.reject_access_request(REPO, a.reject, repo_type="dataset")
        print(f"rejected {a.reject}")
        return
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=a.since_hours)
    checked = revoked = 0
    report = []
    for r in api.list_accepted_access_requests(REPO, repo_type="dataset"):
        ts = r.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=dt.timezone.utc)
        if not a.all and ts < cutoff:
            continue
        checked += 1
        key = key_from_fields(r.fields)
        ok = r.username in ALLOWLIST or key_is_valid(key)
        report.append({"user": r.username, "email": r.email, "when": ts.isoformat(), "key_tail": (key or "")[-4:], "valid": ok, "fields": r.fields})
        print(f"{'ok    ' if ok else 'REVOKE'} {r.username:<24} {r.email or '':<32} {ts:%Y-%m-%d %H:%M} key=…{(key or '')[-4:]}")
        if not ok and not a.dry_run:
            api.cancel_access_request(REPO, r.username, repo_type="dataset")
            revoked += 1
    print(f"\nchecked {checked}, revoked {revoked}{' (dry run)' if a.dry_run else ''}")
    pending = list(api.list_pending_access_requests(REPO, repo_type="dataset"))
    if pending:
        print(f"pending (revoked earlier, restore with --accept once they send a valid key): {', '.join(r.username for r in pending)}")
    out = os.environ.get("GATE_AUDIT_JSON")
    if out:
        json.dump(report, open(out, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
