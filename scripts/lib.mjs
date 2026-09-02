import { mkdirSync, existsSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

export const ROOT = new URL('../', import.meta.url).pathname;
export const DATA = join(ROOT, 'data');
export const CSV_HEADER = 'date,base,quote,type,value';

export function bankDir(code) {
  const d = join(DATA, code);
  mkdirSync(join(d, 'history'), { recursive: true });
  mkdirSync(join(d, 'daily'), { recursive: true });
  return d;
}

// Merge rows into data/<bank>/history/<year>.csv, keyed by (date,base,quote,type).
// Newer values win. Returns number of rows added or changed.
export function mergeHistory(code, rows) {
  const byYear = new Map();
  for (const r of rows) {
    const y = r.date.slice(0, 4);
    if (!byYear.has(y)) byYear.set(y, []);
    byYear.get(y).push(r);
  }
  let changed = 0;
  for (const [year, list] of byYear) {
    const file = join(bankDir(code), 'history', `${year}.csv`);
    const map = new Map();
    if (existsSync(file)) {
      for (const line of readFileSync(file, 'utf8').split('\n').slice(1)) {
        if (!line) continue;
        const [date, base, quote, type, value] = line.split(',');
        map.set(`${date},${base},${quote},${type}`, value);
      }
    }
    for (const r of list) {
      const k = `${r.date},${r.base},${r.quote},${r.type}`;
      const v = String(r.value);
      if (map.get(k) !== v) { map.set(k, v); changed++; }
    }
    const lines = [...map.entries()].sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)).map(([k, v]) => `${k},${v}`);
    writeFileSync(file, `${CSV_HEADER}\n${lines.join('\n')}\n`);
  }
  return changed;
}

export function writeJson(path, obj) {
  writeFileSync(path, JSON.stringify(obj, null, 1) + '\n');
}

export function readJson(path, fallback = null) {
  return existsSync(path) ? JSON.parse(readFileSync(path, 'utf8')) : fallback;
}

export function listBanks() {
  return readdirSync(DATA, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort();
}
