#!/usr/bin/env node
// Serve this repository's data/ folder as a tiny local exchange-rate API.
// Zero dependencies. For laptops behind firewalls, CI jobs, and anyone who
// would rather not depend on a hosted service.
//
//   node scripts/serve.mjs            # http://localhost:8787
//   PORT=9000 node scripts/serve.mjs
//
// Routes (all JSON, CORS *):
//   /                                   index of sources
//   /:code/latest                       a source's latest table, as stored in data/<code>/latest.json
//   /latest?base=USD&symbols=GBP,JPY    ECB table re-based, in the exchangeratesapi.io / Frankfurter shape
//   /:date?base=USD                     ECB table for a date (YYYY-MM-DD) from data/ecb/daily/<date>.json
//
// The /latest and /:date shapes match https://allratestoday.com/api/compat/exchangeratesapi/
// so code can switch between the hosted endpoint and this one with a hostname change.
import { createServer } from 'node:http';
import { readFile, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', 'data');
const PORT = Number(process.env.PORT || 8787);
const CCY = /^[A-Z]{3}$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;

const json = (res, body, status = 200) => {
  res.writeHead(status, { 'content-type': 'application/json', 'access-control-allow-origin': '*' });
  res.end(JSON.stringify(body));
};

async function readJson(path) {
  return JSON.parse(await readFile(path, 'utf8'));
}

// { EUR: 1, USD: 1.17, ... } from an ECB table file
function perEur(table) {
  const out = { EUR: 1 };
  for (const r of table.rates) if (r.base === 'EUR' && r.value > 0) out[r.quote] = r.value;
  return out;
}

function rebase(map, base, symbols) {
  const b = map[base];
  if (!b) return null;
  const rates = {};
  for (const k of symbols ?? Object.keys(map)) {
    if (k === base || map[k] === undefined) continue;
    rates[k] = Number((map[k] / b).toPrecision(8));
  }
  return rates;
}

async function ecbTable(date) {
  const file = date ? join(ROOT, 'ecb', 'daily', `${date}.json`) : join(ROOT, 'ecb', 'latest.json');
  if (!existsSync(file)) return null;
  const t = await readJson(file);
  return { date: t.date, map: perEur(t) };
}

createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    const seg = url.pathname.replace(/^\/+|\/+$/g, '').split('/');
    if (seg[0] === '') {
      const codes = (await readdir(ROOT, { withFileTypes: true })).filter((d) => d.isDirectory()).map((d) => d.name).sort();
      return json(res, { sources: codes, routes: ['/:code/latest', '/latest?base=USD&symbols=GBP,JPY', '/YYYY-MM-DD?base=USD'] });
    }
    if (seg.length === 2 && seg[1] === 'latest') {
      const file = join(ROOT, seg[0], 'latest.json');
      if (!existsSync(file)) return json(res, { error: `Unknown source ${seg[0]}` }, 404);
      return json(res, await readJson(file));
    }
    if (seg.length === 1 && (seg[0] === 'latest' || DATE.test(seg[0]))) {
      const base = (url.searchParams.get('base') ?? url.searchParams.get('from') ?? 'EUR').toUpperCase();
      const raw = url.searchParams.get('symbols') ?? url.searchParams.get('to');
      const symbols = raw ? raw.split(',').map((s) => s.trim().toUpperCase()) : null;
      if (!CCY.test(base) || (symbols && symbols.some((s) => !CCY.test(s)))) return json(res, { error: 'Invalid currency code' }, 400);
      const t = await ecbTable(seg[0] === 'latest' ? null : seg[0]);
      if (!t) return json(res, { error: 'No ECB table for that date in data/' }, 404);
      const rates = rebase(t.map, base, symbols);
      if (!rates) return json(res, { error: `Base currency ${base} is not in the ECB table` }, 400);
      return json(res, { base, date: t.date, rates, source: 'European Central Bank reference rates (local copy)' });
    }
    return json(res, { error: 'Not found' }, 404);
  } catch (err) {
    return json(res, { error: String(err?.message ?? err) }, 500);
  }
}).listen(PORT, () => console.log(`central-bank-exchange-rates: serving ${ROOT} on http://localhost:${PORT}`));
