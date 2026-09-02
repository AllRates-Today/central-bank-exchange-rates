# Central Bank Exchange Rates

Official exchange rates from **102 central banks and 4 tax authorities**, updated every day, as plain JSON and CSV files. No API key, no rate limit, no sign-up. Served free by jsDelivr's global CDN.

Examples of what is here: the ECB euro reference rates, the Federal Reserve H.10 table, the Bank of England spot rates, RBI reference rates, PBoC central parity, the HMRC monthly rates for VAT, and the US Treasury quarterly rates. Every table is the number the institution itself published, not a market or interbank rate, so it is what you need for invoices, VAT returns, customs, transfer pricing, and audit evidence.

## Use it

Latest ECB table:

```
https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ecb/latest.json
```

```json
{
 "source": "ecb",
 "name": "European Central Bank",
 "home_currency": "EUR",
 "date": "2026-09-02",
 "rates": [
  { "base": "EUR", "quote": "USD", "type": "reference", "value": 1.1712 },
  ...
 ]
}
```

**JavaScript**

```js
const r = await fetch('https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ecb/latest.json').then(r => r.json());
const usd = r.rates.find(x => x.quote === 'USD').value;
```

**Python**

```python
import requests
r = requests.get('https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ecb/latest.json').json()
usd = next(x['value'] for x in r['rates'] if x['quote'] == 'USD')
```

**Google Sheets**

```
=IMPORTDATA("https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ecb/history/2026.csv")
```

**curl**

```sh
curl -s https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/hmrc/latest.json | jq '.rates[] | select(.quote=="USD")'
```

## Files

| Path | What it is |
|---|---|
| `data/index.json` | Catalogue of every source: name, country, home currency, latest date, freshness, currencies published |
| `data/latest.json` | Every source's latest table in one file |
| `data/<source>/latest.json` | The latest published table for one source |
| `data/<source>/daily/<YYYY-MM-DD>.json` | One snapshot per publication date (from September 2026) |
| `data/<source>/history/<YYYY>.csv` | Long-form history, one row per date, pair and rate type. Columns: `date,base,quote,type,value` |
| `data/sources.json` | Static metadata, including each institution's official publication page |

A rate row means: one unit of `base` costs `value` units of `quote`, as published by the institution on `date`. `type` is the institution's own label: `reference`, `middle`, `buy`, `sell`, `spot`, `monthly_average`, and so on. Publication direction follows the source, so the ECB is `EUR → USD` and the Reserve Bank of India is `USD → INR`.

Files change at most once per publication date. Use `@main` for the live files. jsDelivr caches `@main` for up to 12 hours; use raw.githubusercontent.com if you need the very latest commit.

## Sources

| Institution | Country | Code | Home | Currencies | Latest |
|---|---|---|---|---|---|
| [AllRatesToday Composite (official sources)](https://allratestoday.com/central-bank-rates-api/composite/) | Global | `composite` | USD | 153 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/composite/latest.json) |
| [Banca d'Italia](https://allratestoday.com/central-bank-rates-api/bdi/) | Italy | `bdi` | EUR | 150 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bdi/latest.json) |
| [Banco Central de Bolivia](https://allratestoday.com/central-bank-rates-api/bcbol/) | Bolivia | `bcbol` | BOB | 21 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcbol/latest.json) |
| [Banco Central de Costa Rica](https://allratestoday.com/central-bank-rates-api/bccr/) | Costa Rica | `bccr` | CRC | 3 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bccr/latest.json) |
| [Banco Central de Honduras](https://allratestoday.com/central-bank-rates-api/bch/) | Honduras | `bch` | HNL | 1 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bch/latest.json) |
| [Banco Central de Nicaragua](https://allratestoday.com/central-bank-rates-api/bcn/) | Nicaragua | `bcn` | NIO | 1 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcn/latest.json) |
| [Banco Central de la República Dominicana](https://allratestoday.com/central-bank-rates-api/bcrd/) | Dominican Republic | `bcrd` | DOP | 2 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcrd/latest.json) |
| [Banco Central del Paraguay](https://allratestoday.com/central-bank-rates-api/bcp/) | Paraguay | `bcp` | PYG | 26 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcp/latest.json) |
| [Banco Central do Brasil (PTAX)](https://allratestoday.com/central-bank-rates-api/bcb/) | Brazil | `bcb` | BRL | 312 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcb/latest.json) |
| [Banco de Guatemala](https://allratestoday.com/central-bank-rates-api/banguat/) | Guatemala | `banguat` | GTQ | 1 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/banguat/latest.json) |
| [Banco de Moçambique](https://allratestoday.com/central-bank-rates-api/bdm/) | Mozambique | `bdm` | MZN | 40 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bdm/latest.json) |
| [Banco de México](https://allratestoday.com/central-bank-rates-api/banxico/) | Mexico | `banxico` | MXN | 5 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/banxico/latest.json) |
| [Bangko Sentral ng Pilipinas](https://allratestoday.com/central-bank-rates-api/bsp/) | Philippines | `bsp` | PHP | 31 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bsp/latest.json) |
| [Bangladesh Bank](https://allratestoday.com/central-bank-rates-api/bb/) | Bangladesh | `bb` | BDT | 23 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bb/latest.json) |
| [Bank Al-Maghrib](https://allratestoday.com/central-bank-rates-api/bam/) | Morocco | `bam` | MAD | 30 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bam/latest.json) |
| [Bank Indonesia](https://allratestoday.com/central-bank-rates-api/bi/) | Indonesia | `bi` | IDR | 50 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bi/latest.json) |
| [Bank Negara Malaysia](https://allratestoday.com/central-bank-rates-api/bnm/) | Malaysia | `bnm` | MYR | 27 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bnm/latest.json) |
| [Bank of Albania](https://allratestoday.com/central-bank-rates-api/boa/) | Albania | `boa` | ALL | 20 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/boa/latest.json) |
| [Bank of Algeria](https://allratestoday.com/central-bank-rates-api/bda/) | Algeria | `bda` | DZD | 18 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bda/latest.json) |
| [Bank of Botswana](https://allratestoday.com/central-bank-rates-api/bob/) | Botswana | `bob` | BWP | 7 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bob/latest.json) |
| [Bank of Canada](https://allratestoday.com/central-bank-rates-api/boc/) | Canada | `boc` | CAD | 24 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/boc/latest.json) |
| [Bank of Central African States (BEAC)](https://allratestoday.com/central-bank-rates-api/beac/) | Central Africa (CEMAC) | `beac` | XAF | 26 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/beac/latest.json) |
| [Bank of England](https://allratestoday.com/central-bank-rates-api/boe/) | United Kingdom | `boe` | GBP | 23 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/boe/latest.json) |
| [Bank of Ghana](https://allratestoday.com/central-bank-rates-api/bog/) | Ghana | `bog` | GHS | 42 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bog/latest.json) |
| [Bank of Guyana](https://allratestoday.com/central-bank-rates-api/bogy/) | Guyana | `bogy` | GYD | 3 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bogy/latest.json) |
| [Bank of Israel](https://allratestoday.com/central-bank-rates-api/boi/) | Israel | `boi` | ILS | 14 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/boi/latest.json) |
| [Bank of Jamaica](https://allratestoday.com/central-bank-rates-api/bojm/) | Jamaica | `bojm` | JMD | 246 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bojm/latest.json) |
| [Bank of Japan](https://allratestoday.com/central-bank-rates-api/boj/) | Japan | `boj` | JPY | 2 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/boj/latest.json) |
| [Bank of Korea](https://allratestoday.com/central-bank-rates-api/bok/) | South Korea | `bok` | KRW | 43 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bok/latest.json) |
| [Bank of Mauritius](https://allratestoday.com/central-bank-rates-api/bmu/) | Mauritius | `bmu` | MUR | 24 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bmu/latest.json) |
| [Bank of Mongolia](https://allratestoday.com/central-bank-rates-api/bom/) | Mongolia | `bom` | MNT | 38 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bom/latest.json) |
| [Bank of Russia](https://allratestoday.com/central-bank-rates-api/cbr/) | Russia | `cbr` | RUB | 53 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbr/latest.json) |
| [Bank of Tanzania](https://allratestoday.com/central-bank-rates-api/botz/) | Tanzania | `botz` | TZS | 114 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/botz/latest.json) |
| [Bank of Thailand](https://allratestoday.com/central-bank-rates-api/bot/) | Thailand | `bot` | THB | 97 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bot/latest.json) |
| [Bank of Uganda](https://allratestoday.com/central-bank-rates-api/bou/) | Uganda | `bou` | UGX | 99 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bou/latest.json) |
| [Bank of Zambia](https://allratestoday.com/central-bank-rates-api/boz/) | Zambia | `boz` | ZMW | 6 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/boz/latest.json) |
| [Bank of the Lao PDR](https://allratestoday.com/central-bank-rates-api/bol/) | Laos | `bol` | LAK | 28 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bol/latest.json) |
| [Bulgarian National Bank](https://allratestoday.com/central-bank-rates-api/bnb/) | Bulgaria | `bnb` | EUR | 29 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bnb/latest.json) |
| [Central Bank of Argentina](https://allratestoday.com/central-bank-rates-api/bcra/) | Argentina | `bcra` | ARS | 36 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcra/latest.json) |
| [Central Bank of Armenia](https://allratestoday.com/central-bank-rates-api/cba/) | Armenia | `cba` | AMD | 30 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cba/latest.json) |
| [Central Bank of Azerbaijan](https://allratestoday.com/central-bank-rates-api/cbar/) | Azerbaijan | `cbar` | AZN | 38 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbar/latest.json) |
| [Central Bank of Bahrain](https://allratestoday.com/central-bank-rates-api/cbb/) | Bahrain | `cbb` | BHD | 33 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbb/latest.json) |
| [Central Bank of Bosnia and Herzegovina](https://allratestoday.com/central-bank-rates-api/cbbh/) | Bosnia and Herzegovina | `cbbh` | BAM | 49 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbbh/latest.json) |
| [Central Bank of Chile](https://allratestoday.com/central-bank-rates-api/bcch/) | Chile | `bcch` | CLP | 59 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcch/latest.json) |
| [Central Bank of Egypt](https://allratestoday.com/central-bank-rates-api/cbe/) | Egypt | `cbe` | EGP | 36 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbe/latest.json) |
| [Central Bank of Iceland](https://allratestoday.com/central-bank-rates-api/cbi/) | Iceland | `cbi` | ISK | 10 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbi/latest.json) |
| [Central Bank of Iraq](https://allratestoday.com/central-bank-rates-api/cbiq/) | Iraq | `cbiq` | IQD | 57 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbiq/latest.json) |
| [Central Bank of Jordan](https://allratestoday.com/central-bank-rates-api/cbj/) | Jordan | `cbj` | JOD | 10 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbj/latest.json) |
| [Central Bank of Kenya](https://allratestoday.com/central-bank-rates-api/cbke/) | Kenya | `cbke` | KES | 21 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbke/latest.json) |
| [Central Bank of Kuwait](https://allratestoday.com/central-bank-rates-api/cbk/) | Kuwait | `cbk` | KWD | 134 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbk/latest.json) |
| [Central Bank of Myanmar](https://allratestoday.com/central-bank-rates-api/cbm/) | Myanmar | `cbm` | MMK | 38 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbm/latest.json) |
| [Central Bank of Nigeria](https://allratestoday.com/central-bank-rates-api/cbn/) | Nigeria | `cbn` | NGN | 39 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbn/latest.json) |
| [Central Bank of Oman](https://allratestoday.com/central-bank-rates-api/cbo/) | Oman | `cbo` | OMR | 96 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbo/latest.json) |
| [Central Bank of Sri Lanka](https://allratestoday.com/central-bank-rates-api/cbsl/) | Sri Lanka | `cbsl` | LKR | 54 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbsl/latest.json) |
| [Central Bank of Suriname](https://allratestoday.com/central-bank-rates-api/cbvs/) | Suriname | `cbvs` | SRD | 22 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbvs/latest.json) |
| [Central Bank of Trinidad and Tobago](https://allratestoday.com/central-bank-rates-api/cbtt/) | Trinidad and Tobago | `cbtt` | TTD | 20 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbtt/latest.json) |
| [Central Bank of Tunisia](https://allratestoday.com/central-bank-rates-api/bct/) | Tunisia | `bct` | TND | 20 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bct/latest.json) |
| [Central Bank of Türkiye](https://allratestoday.com/central-bank-rates-api/tcmb/) | Türkiye | `tcmb` | TRY | 43 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/tcmb/latest.json) |
| [Central Bank of Uruguay](https://allratestoday.com/central-bank-rates-api/bcu/) | Uruguay | `bcu` | UYU | 60 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcu/latest.json) |
| [Central Bank of Uzbekistan](https://allratestoday.com/central-bank-rates-api/cbu/) | Uzbekistan | `cbu` | UZS | 74 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbu/latest.json) |
| [Central Bank of Venezuela](https://allratestoday.com/central-bank-rates-api/bcv/) | Venezuela | `bcv` | VES | 42 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcv/latest.json) |
| [Central Bank of West African States (BCEAO)](https://allratestoday.com/central-bank-rates-api/bceao/) | West Africa (WAEMU) | `bceao` | XOF | 27 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bceao/latest.json) |
| [Central Bank of the Republic of China (Taiwan)](https://allratestoday.com/central-bank-rates-api/cbc/) | Taiwan | `cbc` | TWD | 1 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbc/latest.json) |
| [Central Bank of the UAE](https://allratestoday.com/central-bank-rates-api/cbuae/) | United Arab Emirates | `cbuae` | AED | 75 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cbuae/latest.json) |
| [Central Reserve Bank of Peru](https://allratestoday.com/central-bank-rates-api/bcrp/) | Peru | `bcrp` | PEN | 4 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bcrp/latest.json) |
| [Czech National Bank](https://allratestoday.com/central-bank-rates-api/cnb/) | Czech Republic | `cnb` | CZK | 30 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/cnb/latest.json) |
| [Danmarks Nationalbank](https://allratestoday.com/central-bank-rates-api/dnb/) | Denmark | `dnb` | DKK | 30 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/dnb/latest.json) |
| [European Central Bank](https://allratestoday.com/central-bank-rates-api/ecb/) | Eurozone | `ecb` | EUR | 29 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ecb/latest.json) |
| [HM Revenue & Customs](https://allratestoday.com/central-bank-rates-api/hmrc/) | United Kingdom | `hmrc` | GBP | 141 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/hmrc/latest.json) |
| [Hong Kong Monetary Authority](https://allratestoday.com/central-bank-rates-api/hkma/) | Hong Kong | `hkma` | HKD | 17 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/hkma/latest.json) |
| [Magyar Nemzeti Bank](https://allratestoday.com/central-bank-rates-api/mnb/) | Hungary | `mnb` | HUF | 32 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/mnb/latest.json) |
| [Monetary Authority of Macao](https://allratestoday.com/central-bank-rates-api/amcm/) | Macao | `amcm` | MOP | 17 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/amcm/latest.json) |
| [Monetary Authority of Singapore](https://allratestoday.com/central-bank-rates-api/mas/) | Singapore | `mas` | SGD | 21 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/mas/latest.json) |
| [Narodowy Bank Polski](https://allratestoday.com/central-bank-rates-api/nbp/) | Poland | `nbp` | PLN | 32 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbp/latest.json) |
| [National Bank of Angola](https://allratestoday.com/central-bank-rates-api/bna/) | Angola | `bna` | AOA | 210 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bna/latest.json) |
| [National Bank of Cambodia](https://allratestoday.com/central-bank-rates-api/nbc/) | Cambodia | `nbc` | KHR | 85 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbc/latest.json) |
| [National Bank of Ethiopia](https://allratestoday.com/central-bank-rates-api/nbe/) | Ethiopia | `nbe` | ETB | 57 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbe/latest.json) |
| [National Bank of Georgia](https://allratestoday.com/central-bank-rates-api/nbg/) | Georgia | `nbg` | GEL | 42 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbg/latest.json) |
| [National Bank of Kazakhstan](https://allratestoday.com/central-bank-rates-api/nbk/) | Kazakhstan | `nbk` | KZT | 48 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbk/latest.json) |
| [National Bank of Moldova](https://allratestoday.com/central-bank-rates-api/nbm/) | Moldova | `nbm` | MDL | 40 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbm/latest.json) |
| [National Bank of North Macedonia](https://allratestoday.com/central-bank-rates-api/nbrm/) | North Macedonia | `nbrm` | MKD | 51 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbrm/latest.json) |
| [National Bank of Romania](https://allratestoday.com/central-bank-rates-api/bnr/) | Romania | `bnr` | RON | 37 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bnr/latest.json) |
| [National Bank of Rwanda](https://allratestoday.com/central-bank-rates-api/bnrw/) | Rwanda | `bnrw` | RWF | 60 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bnrw/latest.json) |
| [National Bank of Serbia](https://allratestoday.com/central-bank-rates-api/nbs/) | Serbia | `nbs` | RSD | 35 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbs/latest.json) |
| [National Bank of Ukraine](https://allratestoday.com/central-bank-rates-api/nbu/) | Ukraine | `nbu` | UAH | 45 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbu/latest.json) |
| [National Bank of the Kyrgyz Republic](https://allratestoday.com/central-bank-rates-api/nbkr/) | Kyrgyzstan | `nbkr` | KGS | 5 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbkr/latest.json) |
| [National Bank of the Republic of Belarus](https://allratestoday.com/central-bank-rates-api/nbrb/) | Belarus | `nbrb` | BYN | 30 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nbrb/latest.json) |
| [Nepal Rastra Bank](https://allratestoday.com/central-bank-rates-api/nrb/) | Nepal | `nrb` | NPR | 44 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/nrb/latest.json) |
| [Norges Bank](https://allratestoday.com/central-bank-rates-api/norges/) | Norway | `norges` | NOK | 37 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/norges/latest.json) |
| [Palestine Monetary Authority](https://allratestoday.com/central-bank-rates-api/pma/) | Palestine | `pma` | ILS | 8 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/pma/latest.json) |
| [People's Bank of China (CFETS)](https://allratestoday.com/central-bank-rates-api/pboc/) | China | `pboc` | CNY | 25 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/pboc/latest.json) |
| [Qatar Central Bank](https://allratestoday.com/central-bank-rates-api/qcb/) | Qatar | `qcb` | QAR | 7 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/qcb/latest.json) |
| [Reserve Bank of Australia](https://allratestoday.com/central-bank-rates-api/rba/) | Australia | `rba` | AUD | 20 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/rba/latest.json) |
| [Reserve Bank of India](https://allratestoday.com/central-bank-rates-api/rbi/) | India | `rbi` | INR | 6 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/rbi/latest.json) |
| [Reserve Bank of Malawi](https://allratestoday.com/central-bank-rates-api/rbm/) | Malawi | `rbm` | MWK | 114 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/rbm/latest.json) |
| [Reserve Bank of New Zealand](https://allratestoday.com/central-bank-rates-api/rbnz/) | New Zealand | `rbnz` | NZD | 17 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/rbnz/latest.json) |
| [Saudi Central Bank (SAMA)](https://allratestoday.com/central-bank-rates-api/sama/) | Saudi Arabia | `sama` | SAR | 24 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/sama/latest.json) |
| [South African Reserve Bank](https://allratestoday.com/central-bank-rates-api/sarb/) | South Africa | `sarb` | ZAR | 23 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/sarb/latest.json) |
| [State Bank of Pakistan](https://allratestoday.com/central-bank-rates-api/sbp/) | Pakistan | `sbp` | PKR | 35 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/sbp/latest.json) |
| [State Bank of Vietnam](https://allratestoday.com/central-bank-rates-api/sbv/) | Vietnam | `sbv` | VND | 42 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/sbv/latest.json) |
| [Superintendencia Financiera de Colombia](https://allratestoday.com/central-bank-rates-api/sfc/) | Colombia | `sfc` | COP | 1 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/sfc/latest.json) |
| [Sveriges Riksbank](https://allratestoday.com/central-bank-rates-api/riksbank/) | Sweden | `riksbank` | SEK | 29 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/riksbank/latest.json) |
| [Swiss Federal Office for Customs and Border Security](https://allratestoday.com/central-bank-rates-api/bazg/) | Switzerland | `bazg` | CHF | 145 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/bazg/latest.json) |
| [Swiss National Bank](https://allratestoday.com/central-bank-rates-api/snb/) | Switzerland | `snb` | CHF | 26 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/snb/latest.json) |
| [U.S. Department of the Treasury](https://allratestoday.com/central-bank-rates-api/ustreasury/) | United States | `ustreasury` | USD | 145 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/ustreasury/latest.json) |
| [US Federal Reserve (H.10)](https://allratestoday.com/central-bank-rates-api/fed/) | United States | `fed` | USD | 22 | [latest.json](https://cdn.jsdelivr.net/gh/AllRates-Today/central-bank-exchange-rates@main/data/fed/latest.json) |

## How it is built

A GitHub Action runs four times a day, reads each institution's latest table from the keyless [AllRatesToday](https://allratestoday.com/central-bank-rates-api/) open endpoints, and commits only when something changed. The upstream collector fetches each institution's own publication, checks every table against the other banks for unit and direction errors, and quarantines anything more than ten percent off. History before September 2026 was loaded from the same collector's database.

If you need more than daily files, the [AllRatesToday API](https://allratestoday.com/central-bank-rates-api/) adds rate-on-a-date lookups with weekend and holiday fallback, pair and cross-rate resolution, publication calendars, CSV, XML and XLSX output, real-time market rates, and support. There are also per-bank npm and PyPI SDKs and an [MCP server](https://github.com/AllRates-Today/central-bank-mcp) for AI agents.

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it for anything, including commercially, with a visible credit to AllRatesToday linking to https://allratestoday.com. The underlying figures are public information published by each institution.

Code in `scripts/`: MIT.

Rates are provided as published. Verify against the institution before relying on a figure for a legal or tax filing.
