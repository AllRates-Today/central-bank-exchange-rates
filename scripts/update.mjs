// Daily refresh. Pulls every source's latest published table from the keyless
// AllRatesToday endpoints (edge-cached, no key, no quota) and writes:
//   data/<bank>/latest.json           the latest table
//   data/<bank>/daily/<date>.json     one snapshot per publication date
//   data/<bank>/history/<year>.csv    long-form history, appended
//   data/latest.json                  every source's latest table in one file
//   data/index.json                   catalogue: names, currencies, freshness
import { join } from 'node:path';
import { DATA, bankDir, mergeHistory, writeJson, readJson } from './lib.mjs';

const API = 'https://allratestoday.com/api/open';
const sources = readJson(join(DATA, 'sources.json'), {});

async function get(url, tries = 3) {
  for (let i = 0; i < tries; i++) {
    try {
      const res = await fetch(url, { headers: { 'User-Agent': 'central-bank-exchange-rates (github.com/AllRates-Today)' } });
      if (res.status === 404) return null;
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      if (i === tries - 1) throw e;
      await new Promise((r) => setTimeout(r, 2000 * (i + 1)));
    }
  }
}

const feed = await get(`${API}/central-banks`);
if (!feed?.sources?.length) throw new Error('freshness feed unavailable');

const index = {};
const all = {};
let updated = 0, failed = [];

for (const s of feed.sources) {
  const code = s.code;
  const meta = sources[code] ?? { name: s.name };
  try {
    const t = await get(`${API}/central-bank/${code}`);
    if (!t?.rates?.length) { failed.push(code); continue; }
    const rows = t.rates.map((r) => ({ date: t.rate_date, base: r.base, quote: r.quote, type: r.type, value: r.value }));
    const table = {
      source: code,
      name: meta.name,
      country: meta.country,
      home_currency: meta.home_currency,
      kind: meta.kind,
      date: t.rate_date,
      cadence: s.cadence,
      rates: t.rates,
      official_source: meta.official_source,
      page: meta.page,
      license: 'CC BY 4.0 — attribution: AllRatesToday, https://allratestoday.com',
    };
    const dir = bankDir(code);
    writeJson(join(dir, 'latest.json'), table);
    writeJson(join(dir, 'daily', `${t.rate_date}.json`), table);
    updated += mergeHistory(code, rows) ? 1 : 0;
    all[code] = table;
    index[code] = {
      name: meta.name, country: meta.country, home_currency: meta.home_currency, kind: meta.kind,
      latest: t.rate_date, cadence: s.cadence, stale: !!s.stale, currencies: t.rates.length,
      latest_url: `https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/${code}/latest.json`,
      page: meta.page,
    };
  } catch (e) {
    failed.push(`${code}:${e.message}`);
  }
}

writeJson(join(DATA, 'latest.json'), { generated_at: new Date().toISOString(), sources: all });
writeJson(join(DATA, 'index.json'), { generated_at: new Date().toISOString(), source_count: Object.keys(index).length, sources: index });
console.log(`sources: ${feed.sources.length}, tables written: ${Object.keys(all).length}, with new rows: ${updated}, failed: ${failed.length}`);
if (failed.length) console.log('failed:', failed.join(' '));
if (Object.keys(all).length < feed.sources.length * 0.8) { console.error('too many failures, aborting'); process.exit(1); }
