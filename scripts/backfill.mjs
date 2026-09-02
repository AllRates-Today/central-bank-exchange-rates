// One-time (and re-runnable) history backfill straight from the ingest D1
// database via wrangler, bank by bank and year by year — every query is a
// primary-key range seek, so rows_read equals rows returned. Maintainer-only:
// needs the cbr-ingest checkout and Cloudflare credentials.
//   node scripts/backfill.mjs [--from 2016] [--banks ecb,boc]
import { execFileSync } from 'node:child_process';
import { join } from 'node:path';
import { DATA, mergeHistory, readJson } from './lib.mjs';

const INGEST = process.env.CBR_INGEST_DIR ?? join(DATA, '../../cbr-ingest');
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const fromYear = Number(opt('--from', '1900'));
const only = opt('--banks', '')?.split(',').filter(Boolean);
const sources = readJson(join(DATA, 'sources.json'), {});
const banks = (only.length ? only : Object.keys(sources)).sort();
const thisYear = new Date().getUTCFullYear();

function q(sql) {
  const out = execFileSync('npx', ['wrangler', 'd1', 'execute', 'cb-rates', '--remote', '--json', '--command', sql],
    { cwd: INGEST, encoding: 'utf8', maxBuffer: 1 << 28, stdio: ['ignore', 'pipe', 'ignore'] });
  return JSON.parse(out)[0].results;
}

for (const code of banks) {
  const [{ mn }] = q(`SELECT MIN(rate_date) mn FROM rates WHERE bank_code='${code}'`);
  if (!mn) { console.log(`${code}: no rows`); continue; }
  const start = Math.max(Number(mn.slice(0, 4)), fromYear);
  let total = 0;
  for (let y = start; y <= thisYear; y++) {
    let rows;
    for (let attempt = 0; ; attempt++) {
      try {
        rows = q(`SELECT rate_date d,base_ccy b,quote_ccy q,rate_type t,value v FROM rates WHERE bank_code='${code}' AND rate_date>='${y}-01-01' AND rate_date<'${y + 1}-01-01'`);
        break;
      } catch (e) {
        if (attempt >= 3) throw e;
        await new Promise((r) => setTimeout(r, 5000));
      }
    }
    if (!rows.length) continue;
    mergeHistory(code, rows.map((r) => ({ date: r.d, base: r.b, quote: r.q, type: r.t, value: r.v })));
    total += rows.length;
  }
  console.log(`${code}: ${total} rows from ${mn}`);
}
