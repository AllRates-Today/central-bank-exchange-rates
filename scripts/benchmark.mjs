// Hourly probe of the keyless exchange rate APIs: latency, availability and
// freshness, measured from a GitHub Actions runner. Writes benchmark/latest.json
// (current run + rolling 7-day and 30-day summary) and appends benchmark/history.csv.
import { readFileSync, writeFileSync, existsSync, appendFileSync } from 'node:fs';

const PROVIDERS = [
  { id: 'allratestoday', name: 'AllRatesToday (open central-bank endpoint)', site: 'https://allratestoday.com/central-bank-rates-api/',
    url: 'https://allratestoday.com/api/open/central-bank/ecb', kind: 'official',
    parse: (j) => ({ date: j.rate_date ?? j.date, currencies: Array.isArray(j.rates) ? j.rates.length : Object.keys(j.rates ?? {}).length }) },
  { id: 'frankfurter', name: 'Frankfurter', site: 'https://frankfurter.dev/',
    url: 'https://api.frankfurter.dev/v1/latest?base=EUR', kind: 'official',
    parse: (j) => ({ date: j.date, currencies: Object.keys(j.rates ?? {}).length }) },
  { id: 'exchangerate-api-open', name: 'ExchangeRate-API (open endpoint)', site: 'https://www.exchangerate-api.com/',
    url: 'https://open.er-api.com/v6/latest/EUR', kind: 'market',
    parse: (j) => ({ date: j.time_last_update_utc ? new Date(j.time_last_update_utc).toISOString().slice(0, 10) : null, currencies: Object.keys(j.rates ?? {}).length }) },
  { id: 'fawazahmed0', name: 'fawazahmed0/currency-api (jsDelivr)', site: 'https://github.com/fawazahmed0/exchange-api',
    url: 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.min.json', kind: 'market',
    parse: (j) => ({ date: j.date, currencies: Object.keys(j.eur ?? {}).length }) },
  { id: 'floatrates', name: 'FloatRates', site: 'https://www.floatrates.com/',
    url: 'https://www.floatrates.com/daily/eur.json', kind: 'market',
    parse: (j) => { const first = Object.values(j)[0]; return { date: first?.date ? new Date(first.date).toISOString().slice(0, 10) : null, currencies: Object.keys(j).length }; } },
  { id: 'ecb-xml', name: 'ECB eurofxref-daily.xml (the source itself)', site: 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html',
    url: 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml', kind: 'official', xml: true,
    parse: (t) => ({ date: t.match(/time=['"](\d{4}-\d{2}-\d{2})['"]/)?.[1] ?? null, currencies: (t.match(/currency=['"]/g) ?? []).length }) },
];

const ATTEMPTS = 3;
const TIMEOUT_MS = 15000;

async function probe(p) {
  const ms = []; let last = null; let body = null; let status = 0;
  for (let i = 0; i < ATTEMPTS; i++) {
    const t0 = performance.now();
    try {
      const r = await fetch(p.url + (p.url.includes('?') ? '&' : '?') + '_bench=' + Date.now(), {
        signal: AbortSignal.timeout(TIMEOUT_MS), headers: { 'user-agent': 'allratestoday-benchmark/1.0 (+https://allratestoday.com/benchmarks/exchange-rate-api/)', 'cache-control': 'no-cache' } });
      const text = await r.text();
      ms.push(Math.round(performance.now() - t0));
      status = r.status;
      if (r.ok) body = text; else last = `HTTP ${r.status}`;
    } catch (e) { ms.push(Math.round(performance.now() - t0)); last = e.name === 'TimeoutError' ? 'timeout' : (e.message || String(e)); }
  }
  let parsed = { date: null, currencies: null };
  let ok = !!body;
  if (body) { try { parsed = p.parse(p.xml ? body : JSON.parse(body)); } catch (e) { ok = false; last = 'unparseable body'; } }
  const sorted = [...ms].sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)];
  const today = new Date().toISOString().slice(0, 10);
  const ageDays = parsed.date ? Math.round((Date.parse(today) - Date.parse(parsed.date)) / 86400000) : null;
  return { id: p.id, name: p.name, site: p.site, url: p.url, kind: p.kind, ok, status, ms, median_ms: median, min_ms: sorted[0], date: parsed.date, age_days: ageDays, currencies: parsed.currencies, error: ok ? null : last };
}

const ts = new Date().toISOString();
const results = [];
for (const p of PROVIDERS) results.push(await probe(p));

const HIST = 'benchmark/history.csv';
if (!existsSync(HIST)) writeFileSync(HIST, 'ts,id,ok,median_ms,date,currencies\n');
appendFileSync(HIST, results.map((r) => `${ts},${r.id},${r.ok ? 1 : 0},${r.median_ms},${r.date ?? ''},${r.currencies ?? ''}`).join('\n') + '\n');

// rolling summary
const rows = readFileSync(HIST, 'utf8').trim().split('\n').slice(1).map((l) => { const [t, id, ok, m] = l.split(','); return { t: Date.parse(t), id, ok: ok === '1', m: Number(m) }; });
const now = Date.now();
function summary(id, days) {
  const rs = rows.filter((r) => r.id === id && now - r.t <= days * 86400000);
  if (!rs.length) return null;
  const okRows = rs.filter((r) => r.ok);
  const lat = okRows.map((r) => r.m).sort((a, b) => a - b);
  return { runs: rs.length, uptime_pct: +(100 * okRows.length / rs.length).toFixed(2), median_ms: lat.length ? lat[Math.floor(lat.length / 2)] : null, p90_ms: lat.length ? lat[Math.floor(lat.length * 0.9)] : null };
}
for (const r of results) { r.last_7d = summary(r.id, 7); r.last_30d = summary(r.id, 30); }

const firstRun = rows.length ? new Date(Math.min(...rows.map((r) => r.t))).toISOString() : ts;
writeFileSync('benchmark/latest.json', JSON.stringify({
  generated: ts, since: firstRun, vantage: 'GitHub Actions hosted runner (ubuntu-latest, US East)',
  method: `${ATTEMPTS} sequential GETs per provider per run, cache-busting query string, ${TIMEOUT_MS / 1000}s timeout; median reported. Freshness = publication date in the response vs the run date (UTC). Uptime = share of hourly runs with an HTTP 2xx and a parseable body.`,
  providers: results,
}, null, 1) + '\n');
console.table(results.map((r) => ({ id: r.id, ok: r.ok, median_ms: r.median_ms, date: r.date, currencies: r.currencies, error: r.error })));
