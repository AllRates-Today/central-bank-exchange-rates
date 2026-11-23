# Central Bank Exchange Rates

Official exchange rates from **[123 central banks and 59 tax and customs authorities](https://allratestoday.com/central-bank-rates-api/institutions/)**, refreshed four times a day, with history back to 1914.

Examples: the ECB euro reference rates, the Federal Reserve H.10 table, the Bank of England spot rates, RBI reference rates, PBoC central parity, the HMRC monthly rates for VAT, the US Treasury quarterly rates, and customs rates from Australia to Switzerland. Every table is the institution's own official figure, not a market or interbank rate, so it is what you need for invoices, VAT returns, customs, transfer pricing, and audit evidence.

> **The data files have moved behind a free account (23 November 2026).** This repository no longer hosts the JSON and CSV files. [Register for a free API key](https://allratestoday.com/register/?utm_source=github&utm_medium=readme&utm_campaign=central-bank-exchange-rates) (one minute, no card) and get the same tables, and the full history, from the API or the Hugging Face dataset below.

## Get the data

1. **Register** at [allratestoday.com/register](https://allratestoday.com/register/?utm_source=github&utm_medium=readme&utm_campaign=central-bank-exchange-rates). Your API key is on your [dashboard](https://allratestoday.com/profile).
2. **Call the API** with the key:

```sh
curl -H "Authorization: Bearer $ALLRATES_API_KEY" \
  "https://allratestoday.com/api/v1/central-bank/ecb/latest"
```

**JavaScript**

```js
const r = await fetch('https://allratestoday.com/api/v1/central-bank/ecb/latest', {
  headers: { Authorization: `Bearer ${process.env.ALLRATES_API_KEY}` },
}).then((r) => r.json());
```

**Python**

```python
import os, requests
r = requests.get('https://allratestoday.com/api/v1/central-bank/ecb/latest',
                 headers={'Authorization': f"Bearer {os.environ['ALLRATES_API_KEY']}"}).json()
```

History, rate-on-a-date lookups with weekend and holiday fallback, and CSV, XML and XLSX output are in the [API documentation](https://allratestoday.com/docs/?utm_source=github&utm_medium=readme&utm_campaign=central-bank-exchange-rates). Replace `ecb` with any code from the table below.

## Bulk download: Hugging Face

The whole history, one CSV per institution, is on [Hugging Face](https://huggingface.co/datasets/AllRatesToday/central-bank-exchange-rates). Log in to Hugging Face, paste your AllRatesToday API key into the **Get access** form, and a valid key is approved within about 5 minutes. Then:

```python
from datasets import load_dataset
ds = load_dataset("AllRatesToday/central-bank-exchange-rates", "rates")
```

## Replacing exchangeratesapi.io, Fixer or exchangerate.host

Those free APIs served this same ECB table before they went behind paid keys. AllRatesToday serves their exact JSON shapes, keyless for latest rates:

```
https://allratestoday.com/api/compat/exchangeratesapi/latest?base=USD&symbols=GBP
https://allratestoday.com/api/compat/fixer/latest?base=EUR&symbols=USD
https://allratestoday.com/api/compat/exchangerate-host/latest?base=USD
https://allratestoday.com/api/compat/frankfurter/latest?from=USD&to=GBP
```

One-line migration guides: https://allratestoday.com/migrate/

## Sources

| Institution | Country | Type | Code | Home | Currencies |
|---|---|---|---|---|---|
| [AllRatesToday Composite (official sources)](https://allratestoday.com/central-bank-rates-api/composite/) | Global | Composite | `composite` | USD | 135 |
| [ARCA Customs (Argentina)](https://allratestoday.com/tax-authority-rates-api/arcamaria/) | Argentina | Tax / customs | `arcamaria` | ARS | 50 |
| [Australian Border Force](https://allratestoday.com/tax-authority-rates-api/abf/) | Australia | Tax / customs | `abf` | AUD | 28 |
| [Austrian Ministry of Finance (BMF)](https://allratestoday.com/tax-authority-rates-api/bmfat/) | Austria | Tax / customs | `bmfat` | EUR | 159 |
| [Banca d'Italia](https://allratestoday.com/central-bank-rates-api/bdi/) | Italy | Central bank | `bdi` | EUR | 150 |
| [Banco Central de Bolivia](https://allratestoday.com/central-bank-rates-api/bcbol/) | Bolivia | Central bank | `bcbol` | BOB | 21 |
| [Banco Central de Costa Rica](https://allratestoday.com/central-bank-rates-api/bccr/) | Costa Rica | Central bank | `bccr` | CRC | 2 |
| [Banco Central de Cuba](https://allratestoday.com/central-bank-rates-api/bccu/) | Cuba | Central bank | `bccu` | CUP | 39 |
| [Banco Central de Honduras](https://allratestoday.com/central-bank-rates-api/bch/) | Honduras | Central bank | `bch` | HNL | 1 |
| [Banco Central de la República Dominicana](https://allratestoday.com/central-bank-rates-api/bcrd/) | Dominican Republic | Central bank | `bcrd` | DOP | 2 |
| [Banco Central de Nicaragua](https://allratestoday.com/central-bank-rates-api/bcn/) | Nicaragua | Central bank | `bcn` | NIO | 1 |
| [Banco Central de São Tomé e Príncipe](https://allratestoday.com/central-bank-rates-api/bcstp/) | São Tomé and Príncipe | Central bank | `bcstp` | STN | 42 |
| [Banco Central del Paraguay](https://allratestoday.com/central-bank-rates-api/bcp/) | Paraguay | Central bank | `bcp` | PYG | 26 |
| [Banco Central do Brasil (PTAX)](https://allratestoday.com/central-bank-rates-api/bcb/) | Brazil | Central bank | `bcb` | BRL | 312 |
| [Banco de Guatemala](https://allratestoday.com/central-bank-rates-api/banguat/) | Guatemala | Central bank | `banguat` | GTQ | 1 |
| [Banco de la Nación Argentina (divisa rate for tax)](https://allratestoday.com/tax-authority-rates-api/bnadivisa/) | Argentina | Tax / customs | `bnadivisa` | ARS | 22 |
| [Banco de Moçambique](https://allratestoday.com/central-bank-rates-api/bdm/) | Mozambique | Central bank | `bdm` | MZN | 40 |
| [Banco de México](https://allratestoday.com/central-bank-rates-api/banxico/) | Mexico | Central bank | `banxico` | MXN | 4 |
| [Bangko Sentral ng Pilipinas](https://allratestoday.com/central-bank-rates-api/bsp/) | Philippines | Central bank | `bsp` | PHP | 31 |
| [Bangladesh Bank](https://allratestoday.com/central-bank-rates-api/bb/) | Bangladesh | Central bank | `bb` | BDT | 23 |
| [Bangladesh National Board of Revenue (customs rates)](https://allratestoday.com/tax-authority-rates-api/nbrbd/) | Bangladesh | Tax / customs | `nbrbd` | BDT | 26 |
| [Bank Al-Maghrib](https://allratestoday.com/central-bank-rates-api/bam/) | Morocco | Central bank | `bam` | MAD | 30 |
| [Bank Indonesia](https://allratestoday.com/central-bank-rates-api/bi/) | Indonesia | Central bank | `bi` | IDR | 50 |
| [Bank Negara Malaysia](https://allratestoday.com/central-bank-rates-api/bnm/) | Malaysia | Central bank | `bnm` | MYR | 27 |
| [Bank of Albania](https://allratestoday.com/central-bank-rates-api/boa/) | Albania | Central bank | `boa` | ALL | 20 |
| [Bank of Algeria](https://allratestoday.com/central-bank-rates-api/bda/) | Algeria | Central bank | `bda` | DZD | 18 |
| [Bank of Botswana](https://allratestoday.com/central-bank-rates-api/bob/) | Botswana | Central bank | `bob` | BWP | 7 |
| [Bank of Canada](https://allratestoday.com/central-bank-rates-api/boc/) | Canada | Central bank | `boc` | CAD | 24 |
| [Bank of Central African States (BEAC)](https://allratestoday.com/central-bank-rates-api/beac/) | Central Africa (CEMAC) | Central bank | `beac` | XAF | 26 |
| [Bank of England](https://allratestoday.com/central-bank-rates-api/boe/) | United Kingdom | Central bank | `boe` | GBP | 23 |
| [Bank of Ghana](https://allratestoday.com/central-bank-rates-api/bog/) | Ghana | Central bank | `bog` | GHS | 42 |
| [Bank of Guyana](https://allratestoday.com/central-bank-rates-api/bogy/) | Guyana | Central bank | `bogy` | GYD | 13 |
| [Bank of Israel](https://allratestoday.com/central-bank-rates-api/boi/) | Israel | Central bank | `boi` | ILS | 14 |
| [Bank of Jamaica](https://allratestoday.com/central-bank-rates-api/bojm/) | Jamaica | Central bank | `bojm` | JMD | 246 |
| [Bank of Japan](https://allratestoday.com/central-bank-rates-api/boj/) | Japan | Central bank | `boj` | JPY | 2 |
| [Bank of Korea](https://allratestoday.com/central-bank-rates-api/bok/) | South Korea | Central bank | `bok` | KRW | 43 |
| [Bank of Lithuania](https://allratestoday.com/central-bank-rates-api/lb/) | Lithuania | Central bank | `lb` | EUR | 87 |
| [Bank of Mauritius](https://allratestoday.com/central-bank-rates-api/bmu/) | Mauritius | Central bank | `bmu` | MUR | 24 |
| [Bank of Mongolia](https://allratestoday.com/central-bank-rates-api/bom/) | Mongolia | Central bank | `bom` | MNT | 38 |
| [Bank of Namibia](https://allratestoday.com/central-bank-rates-api/bon/) | Namibia | Central bank | `bon` | NAD | 4 |
| [Bank of Russia](https://allratestoday.com/central-bank-rates-api/cbr/) | Russia | Central bank | `cbr` | RUB | 54 |
| [Bank of Sierra Leone](https://allratestoday.com/central-bank-rates-api/bsl/) | Sierra Leone | Central bank | `bsl` | SLE | 23 |
| [Bank of Tanzania](https://allratestoday.com/central-bank-rates-api/botz/) | Tanzania | Central bank | `botz` | TZS | 114 |
| [Bank of Thailand](https://allratestoday.com/central-bank-rates-api/bot/) | Thailand | Central bank | `bot` | THB | 97 |
| [Bank of the Lao PDR](https://allratestoday.com/central-bank-rates-api/bol/) | Laos | Central bank | `bol` | LAK | 28 |
| [Bank of Uganda](https://allratestoday.com/central-bank-rates-api/bou/) | Uganda | Central bank | `bou` | UGX | 54 |
| [Bank of Zambia](https://allratestoday.com/central-bank-rates-api/boz/) | Zambia | Central bank | `boz` | ZMW | 6 |
| [Banque Centrale de Mauritanie](https://allratestoday.com/central-bank-rates-api/bcm/) | Mauritania | Central bank | `bcm` | MRU | 19 |
| [Banque Centrale du Congo](https://allratestoday.com/central-bank-rates-api/bcc/) | DR Congo | Central bank | `bcc` | CDF | 63 |
| [Banque de la République d'Haïti](https://allratestoday.com/central-bank-rates-api/brh/) | Haiti | Central bank | `brh` | HTG | 3 |
| [Belgian Customs (FPS Finance)](https://allratestoday.com/tax-authority-rates-api/tarbel/) | Belgium | Tax / customs | `tarbel` | EUR | 81 |
| [Belize Customs and Excise](https://allratestoday.com/tax-authority-rates-api/customsbz/) | Belize | Tax / customs | `customsbz` | BZD | 15 |
| [Bermuda Customs](https://allratestoday.com/tax-authority-rates-api/bermudacustoms/) | Bermuda | Tax / customs | `bermudacustoms` | BMD | 14 |
| [Bulgarian National Bank](https://allratestoday.com/central-bank-rates-api/bnb/) | Bulgaria | Central bank | `bnb` | EUR | 29 |
| [Cambodia General Department of Customs and Excise](https://allratestoday.com/tax-authority-rates-api/gdce/) | Cambodia | Tax / customs | `gdce` | KHR | 29 |
| [Canada Border Services Agency](https://allratestoday.com/tax-authority-rates-api/cbsa/) | Canada | Tax / customs | `cbsa` | CAD | 137 |
| [Central Bank of Argentina](https://allratestoday.com/central-bank-rates-api/bcra/) | Argentina | Central bank | `bcra` | ARS | 36 |
| [Central Bank of Armenia](https://allratestoday.com/central-bank-rates-api/cba/) | Armenia | Central bank | `cba` | AMD | 30 |
| [Central Bank of Azerbaijan](https://allratestoday.com/central-bank-rates-api/cbar/) | Azerbaijan | Central bank | `cbar` | AZN | 38 |
| [Central Bank of Bahrain](https://allratestoday.com/central-bank-rates-api/cbb/) | Bahrain | Central bank | `cbb` | BHD | 33 |
| [Central Bank of Barbados](https://allratestoday.com/central-bank-rates-api/cbbd/) | Barbados | Central bank | `cbbd` | BBD | 14 |
| [Central Bank of Belize](https://allratestoday.com/central-bank-rates-api/cbbz/) | Belize | Central bank | `cbbz` | BZD | 8 |
| [Central Bank of Bosnia and Herzegovina](https://allratestoday.com/central-bank-rates-api/cbbh/) | Bosnia and Herzegovina | Central bank | `cbbh` | BAM | 49 |
| [Central Bank of Chile](https://allratestoday.com/central-bank-rates-api/bcch/) | Chile | Central bank | `bcch` | CLP | 60 |
| [Central Bank of Egypt](https://allratestoday.com/central-bank-rates-api/cbe/) | Egypt | Central bank | `cbe` | EGP | 36 |
| [Central Bank of Iceland](https://allratestoday.com/central-bank-rates-api/cbi/) | Iceland | Central bank | `cbi` | ISK | 10 |
| [Central Bank of Iran](https://allratestoday.com/central-bank-rates-api/cbir/) | Iran | Central bank | `cbir` | IRR | 47 |
| [Central Bank of Iraq](https://allratestoday.com/central-bank-rates-api/cbiq/) | Iraq | Central bank | `cbiq` | IQD | 57 |
| [Central Bank of Jordan](https://allratestoday.com/central-bank-rates-api/cbj/) | Jordan | Central bank | `cbj` | JOD | 10 |
| [Central Bank of Kenya](https://allratestoday.com/central-bank-rates-api/cbke/) | Kenya | Central bank | `cbke` | KES | 21 |
| [Central Bank of Kuwait](https://allratestoday.com/central-bank-rates-api/cbk/) | Kuwait | Central bank | `cbk` | KWD | 133 |
| [Central Bank of Libya](https://allratestoday.com/central-bank-rates-api/cbl/) | Libya | Central bank | `cbl` | LYD | 60 |
| [Central Bank of Madagascar (BFM)](https://allratestoday.com/central-bank-rates-api/bfm/) | Madagascar | Central bank | `bfm` | MGA | 19 |
| [Central Bank of Myanmar](https://allratestoday.com/central-bank-rates-api/cbm/) | Myanmar | Central bank | `cbm` | MMK | 38 |
| [Central Bank of Nigeria](https://allratestoday.com/central-bank-rates-api/cbn/) | Nigeria | Central bank | `cbn` | NGN | 39 |
| [Central Bank of Oman](https://allratestoday.com/central-bank-rates-api/cbo/) | Oman | Central bank | `cbo` | OMR | 96 |
| [Central Bank of Sri Lanka](https://allratestoday.com/central-bank-rates-api/cbsl/) | Sri Lanka | Central bank | `cbsl` | LKR | 54 |
| [Central Bank of Suriname](https://allratestoday.com/central-bank-rates-api/cbvs/) | Suriname | Central bank | `cbvs` | SRD | 22 |
| [Central Bank of The Gambia](https://allratestoday.com/central-bank-rates-api/cbg/) | Gambia | Central bank | `cbg` | GMD | 32 |
| [Central Bank of the Republic of China (Taiwan)](https://allratestoday.com/central-bank-rates-api/cbc/) | Taiwan | Central bank | `cbc` | TWD | 1 |
| [Central Bank of the UAE](https://allratestoday.com/central-bank-rates-api/cbuae/) | United Arab Emirates | Central bank | `cbuae` | AED | 75 |
| [Central Bank of Trinidad and Tobago](https://allratestoday.com/central-bank-rates-api/cbtt/) | Trinidad and Tobago | Central bank | `cbtt` | TTD | 18 |
| [Central Bank of Tunisia](https://allratestoday.com/central-bank-rates-api/bct/) | Tunisia | Central bank | `bct` | TND | 20 |
| [Central Bank of Turkmenistan](https://allratestoday.com/central-bank-rates-api/cbt/) | Turkmenistan | Central bank | `cbt` | TMT | 48 |
| [Central Bank of Türkiye](https://allratestoday.com/central-bank-rates-api/tcmb/) | Türkiye | Central bank | `tcmb` | TRY | 43 |
| [Central Bank of Uruguay](https://allratestoday.com/central-bank-rates-api/bcu/) | Uruguay | Central bank | `bcu` | UYU | 60 |
| [Central Bank of Uzbekistan](https://allratestoday.com/central-bank-rates-api/cbu/) | Uzbekistan | Central bank | `cbu` | UZS | 74 |
| [Central Bank of Venezuela](https://allratestoday.com/central-bank-rates-api/bcv/) | Venezuela | Central bank | `bcv` | VES | 42 |
| [Central Bank of West African States (BCEAO)](https://allratestoday.com/central-bank-rates-api/bceao/) | West Africa (WAEMU) | Central bank | `bceao` | XOF | 24 |
| [Central Board of Indirect Taxes and Customs (CBIC)](https://allratestoday.com/tax-authority-rates-api/cbic/) | India | Tax / customs | `cbic` | INR | 44 |
| [Central Reserve Bank of Peru](https://allratestoday.com/central-bank-rates-api/bcrp/) | Peru | Central bank | `bcrp` | PEN | 2 |
| [Cyprus Department of Customs and Excise](https://allratestoday.com/tax-authority-rates-api/cycustoms/) | Cyprus | Tax / customs | `cycustoms` | EUR | 43 |
| [Czech Customs Administration](https://allratestoday.com/tax-authority-rates-api/celnisprava/) | Czech Republic | Tax / customs | `celnisprava` | CZK | 152 |
| [Czech National Bank](https://allratestoday.com/central-bank-rates-api/cnb/) | Czech Republic | Central bank | `cnb` | CZK | 30 |
| [Czech Tax Administration (yearly uniform rate)](https://allratestoday.com/tax-authority-rates-api/gfrcz/) | Czech Republic | Tax / customs | `gfrcz` | CZK | 31 |
| [Danmarks Nationalbank](https://allratestoday.com/central-bank-rates-api/dnb/) | Denmark | Central bank | `dnb` | DKK | 30 |
| [DGA (Dominican Republic customs)](https://allratestoday.com/tax-authority-rates-api/dgado/) | Dominican Republic | Tax / customs | `dgado` | DOP | 1 |
| [DGII (Dominican Republic tax authority)](https://allratestoday.com/tax-authority-rates-api/dgii/) | Dominican Republic | Tax / customs | `dgii` | DOP | 2 |
| [DNIT (Paraguay tax and customs authority)](https://allratestoday.com/tax-authority-rates-api/dnit/) | Paraguay | Tax / customs | `dnit` | PYG | 30 |
| [Douane (Netherlands Customs)](https://allratestoday.com/tax-authority-rates-api/douanenl/) | Netherlands | Tax / customs | `douanenl` | EUR | 73 |
| [European Central Bank](https://allratestoday.com/central-bank-rates-api/ecb/) | Eurozone | Central bank | `ecb` | EUR | 29 |
| [European Commission (InforEuro)](https://allratestoday.com/tax-authority-rates-api/inforeuro/) | European Union | Tax / customs | `inforeuro` | EUR | 151 |
| [French Customs (DGDDI)](https://allratestoday.com/tax-authority-rates-api/douanefr/) | France | Tax / customs | `douanefr` | EUR | 154 |
| [German Customs (Zoll)](https://allratestoday.com/tax-authority-rates-api/zollde/) | Germany | Tax / customs | `zollde` | EUR | 118 |
| [German Federal Ministry of Finance (VAT rates)](https://allratestoday.com/tax-authority-rates-api/bmfust/) | Germany | Tax / customs | `bmfust` | EUR | 29 |
| [Ghana Revenue Authority Customs (ICUMS)](https://allratestoday.com/tax-authority-rates-api/icumsgh/) | Ghana | Tax / customs | `icumsgh` | GHS | 30 |
| [Guyana Revenue Authority (customs rates)](https://allratestoday.com/tax-authority-rates-api/gracustoms/) | Guyana | Tax / customs | `gracustoms` | GYD | 33 |
| [HM Revenue & Customs](https://allratestoday.com/tax-authority-rates-api/hmrc/) | United Kingdom | Tax / customs | `hmrc` | GBP | 141 |
| [Hong Kong Association of Banks (HKAB)](https://allratestoday.com/central-bank-rates-api/hkab/) | Hong Kong | Bank association | `hkab` | HKD | 66 |
| [Hong Kong Inland Revenue Department (average rates)](https://allratestoday.com/tax-authority-rates-api/hkird/) | Hong Kong | Tax / customs | `hkird` | HKD | 8 |
| [Hong Kong Monetary Authority](https://allratestoday.com/central-bank-rates-api/hkma/) | Hong Kong | Central bank | `hkma` | HKD | 17 |
| [Iceland Revenue and Customs (Skatturinn)](https://allratestoday.com/tax-authority-rates-api/tollgengi/) | Iceland | Tax / customs | `tollgengi` | ISK | 50 |
| [Indonesia Ministry of Finance (Kurs Pajak)](https://allratestoday.com/tax-authority-rates-api/kurspajak/) | Indonesia | Tax / customs | `kurspajak` | IDR | 25 |
| [Inland Revenue (New Zealand)](https://allratestoday.com/tax-authority-rates-api/nzird/) | New Zealand | Tax / customs | `nzird` | NZD | 51 |
| [Internal Revenue Service (yearly average rates)](https://allratestoday.com/tax-authority-rates-api/irs/) | United States | Tax / customs | `irs` | USD | 38 |
| [International Monetary Fund](https://allratestoday.com/central-bank-rates-api/imf/) | International | Central bank | `imf` | USD | 35 |
| [Italy Revenue Agency (Agenzia delle Entrate)](https://allratestoday.com/tax-authority-rates-api/adecambi/) | Italy | Tax / customs | `adecambi` | EUR | 151 |
| [Japan Customs](https://allratestoday.com/tax-authority-rates-api/jpcustoms/) | Japan | Tax / customs | `jpcustoms` | JPY | 85 |
| [Jordan Customs Department](https://allratestoday.com/tax-authority-rates-api/jocustoms/) | Jordan | Tax / customs | `jocustoms` | JOD |  |
| [Kenya Revenue Authority (customs rates)](https://allratestoday.com/tax-authority-rates-api/kra/) | Kenya | Tax / customs | `kra` | KES | 21 |
| [Korea Customs Service](https://allratestoday.com/tax-authority-rates-api/kcs/) | South Korea | Tax / customs | `kcs` | KRW | 114 |
| [Luxembourg Customs and Excise](https://allratestoday.com/tax-authority-rates-api/douaneslu/) | Luxembourg | Tax / customs | `douaneslu` | EUR | 151 |
| [Madagascar Customs (Douanes)](https://allratestoday.com/tax-authority-rates-api/douanesmg/) | Madagascar | Tax / customs | `douanesmg` | MGA | 18 |
| [Magyar Nemzeti Bank](https://allratestoday.com/central-bank-rates-api/mnb/) | Hungary | Central bank | `mnb` | HUF | 32 |
| [Maldives Monetary Authority](https://allratestoday.com/central-bank-rates-api/mma/) | Maldives | Central bank | `mma` | MVR | 1 |
| [Mauritius Revenue Authority (Customs)](https://allratestoday.com/tax-authority-rates-api/mramu/) | Mauritius | Tax / customs | `mramu` | MUR | 54 |
| [Mexico DOF tax equivalence table (Banxico)](https://allratestoday.com/tax-authority-rates-api/dofequiv/) | Mexico | Tax / customs | `dofequiv` | MXN | 65 |
| [Monetary Authority of Macao](https://allratestoday.com/central-bank-rates-api/amcm/) | Macao | Central bank | `amcm` | MOP | 17 |
| [Monetary Authority of Singapore](https://allratestoday.com/central-bank-rates-api/mas/) | Singapore | Central bank | `mas` | SGD | 21 |
| [Narodowy Bank Polski](https://allratestoday.com/central-bank-rates-api/nbp/) | Poland | Central bank | `nbp` | PLN | 32 |
| [National Bank of Angola](https://allratestoday.com/central-bank-rates-api/bna/) | Angola | Central bank | `bna` | AOA | 210 |
| [National Bank of Cambodia](https://allratestoday.com/central-bank-rates-api/nbc/) | Cambodia | Central bank | `nbc` | KHR | 88 |
| [National Bank of Ethiopia](https://allratestoday.com/central-bank-rates-api/nbe/) | Ethiopia | Central bank | `nbe` | ETB | 57 |
| [National Bank of Georgia](https://allratestoday.com/central-bank-rates-api/nbg/) | Georgia | Central bank | `nbg` | GEL | 42 |
| [National Bank of Kazakhstan](https://allratestoday.com/central-bank-rates-api/nbk/) | Kazakhstan | Central bank | `nbk` | KZT | 48 |
| [National Bank of Moldova](https://allratestoday.com/central-bank-rates-api/nbm/) | Moldova | Central bank | `nbm` | MDL | 40 |
| [National Bank of North Macedonia](https://allratestoday.com/central-bank-rates-api/nbrm/) | North Macedonia | Central bank | `nbrm` | MKD | 51 |
| [National Bank of Romania](https://allratestoday.com/central-bank-rates-api/bnr/) | Romania | Central bank | `bnr` | RON | 37 |
| [National Bank of Rwanda](https://allratestoday.com/central-bank-rates-api/bnrw/) | Rwanda | Central bank | `bnrw` | RWF | 60 |
| [National Bank of Serbia](https://allratestoday.com/central-bank-rates-api/nbs/) | Serbia | Central bank | `nbs` | RSD | 35 |
| [National Bank of Tajikistan](https://allratestoday.com/central-bank-rates-api/nbt/) | Tajikistan | Central bank | `nbt` | TJS | 36 |
| [National Bank of the Kyrgyz Republic](https://allratestoday.com/central-bank-rates-api/nbkr/) | Kyrgyzstan | Central bank | `nbkr` | KGS | 48 |
| [National Bank of the Republic of Belarus](https://allratestoday.com/central-bank-rates-api/nbrb/) | Belarus | Central bank | `nbrb` | BYN | 30 |
| [National Bank of Ukraine](https://allratestoday.com/central-bank-rates-api/nbu/) | Ukraine | Central bank | `nbu` | UAH | 45 |
| [Nepal Rastra Bank](https://allratestoday.com/central-bank-rates-api/nrb/) | Nepal | Central bank | `nrb` | NPR | 44 |
| [New Zealand Customs Service](https://allratestoday.com/tax-authority-rates-api/nzcustoms/) | New Zealand | Tax / customs | `nzcustoms` | NZD | 28 |
| [Norges Bank](https://allratestoday.com/central-bank-rates-api/norges/) | Norway | Central bank | `norges` | NOK | 37 |
| [North Macedonia Customs Administration](https://allratestoday.com/tax-authority-rates-api/customsmk/) | North Macedonia | Tax / customs | `customsmk` | MKD | 10 |
| [Norwegian Customs (Tolletaten)](https://allratestoday.com/tax-authority-rates-api/tolletaten/) | Norway | Tax / customs | `tolletaten` | NOK | 22 |
| [Palestine Monetary Authority](https://allratestoday.com/central-bank-rates-api/pma/) | Palestine | Central bank | `pma` | ILS | 8 |
| [People's Bank of China (CFETS)](https://allratestoday.com/central-bank-rates-api/pboc/) | China | Central bank | `pboc` | CNY | 25 |
| [Poland Ministry of Finance customs rates](https://allratestoday.com/tax-authority-rates-api/kaspl/) | Poland | Tax / customs | `kaspl` | PLN | 32 |
| [Portugal Tax and Customs Authority (AT)](https://allratestoday.com/tax-authority-rates-api/atpt/) | Portugal | Tax / customs | `atpt` | EUR | 41 |
| [Qatar Central Bank](https://allratestoday.com/central-bank-rates-api/qcb/) | Qatar | Central bank | `qcb` | QAR | 7 |
| [Receita Federal do Brasil (rates for tax)](https://allratestoday.com/tax-authority-rates-api/receitabr/) | Brazil | Tax / customs | `receitabr` | BRL | 10 |
| [Reserve Bank of Australia](https://allratestoday.com/central-bank-rates-api/rba/) | Australia | Central bank | `rba` | AUD | 20 |
| [Reserve Bank of Fiji](https://allratestoday.com/central-bank-rates-api/rbf/) | Fiji | Central bank | `rbf` | FJD | 8 |
| [Reserve Bank of India](https://allratestoday.com/central-bank-rates-api/rbi/) | India | Central bank | `rbi` | INR | 6 |
| [Reserve Bank of Malawi](https://allratestoday.com/central-bank-rates-api/rbm/) | Malawi | Central bank | `rbm` | MWK | 114 |
| [Reserve Bank of New Zealand](https://allratestoday.com/central-bank-rates-api/rbnz/) | New Zealand | Central bank | `rbnz` | NZD | 17 |
| [Reserve Bank of Zimbabwe](https://allratestoday.com/central-bank-rates-api/rbz/) | Zimbabwe | Central bank | `rbz` | ZWG | 102 |
| [Revenue Commissioners (Ireland customs rates)](https://allratestoday.com/tax-authority-rates-api/revenueie/) | Ireland | Tax / customs | `revenueie` | EUR | 89 |
| [Royal Monetary Authority of Bhutan](https://allratestoday.com/central-bank-rates-api/rma/) | Bhutan | Central bank | `rma` | BTN | 24 |
| [SARS average exchange rates (income tax)](https://allratestoday.com/tax-authority-rates-api/sarsavg/) | South Africa | Tax / customs | `sarsavg` | ZAR | 18 |
| [SARS customs rates of exchange](https://allratestoday.com/tax-authority-rates-api/sarsrex/) | South Africa | Tax / customs | `sarsrex` | ZAR | 20 |
| [Saudi Central Bank (SAMA)](https://allratestoday.com/central-bank-rates-api/sama/) | Saudi Arabia | Central bank | `sama` | SAR | 66 |
| [Serbia Customs Administration](https://allratestoday.com/tax-authority-rates-api/carinars/) | Serbia | Tax / customs | `carinars` | RSD | 23 |
| [Servicio Nacional de Aduanas (Chile customs)](https://allratestoday.com/tax-authority-rates-api/aduanacl/) | Chile | Tax / customs | `aduanacl` | CLP | 60 |
| [SII (Chile tax authority) dólar observado](https://allratestoday.com/tax-authority-rates-api/siicl/) | Chile | Tax / customs | `siicl` | CLP | 1 |
| [South African Reserve Bank](https://allratestoday.com/central-bank-rates-api/sarb/) | South Africa | Central bank | `sarb` | ZAR | 23 |
| [Sri Lanka Customs](https://allratestoday.com/tax-authority-rates-api/lkcustoms/) | Sri Lanka | Tax / customs | `lkcustoms` | LKR | 48 |
| [State Bank of Pakistan](https://allratestoday.com/central-bank-rates-api/sbp/) | Pakistan | Central bank | `sbp` | PKR | 35 |
| [State Bank of Vietnam](https://allratestoday.com/central-bank-rates-api/sbv/) | Vietnam | Central bank | `sbv` | VND | 42 |
| [SUNAT (Peru tax and customs authority)](https://allratestoday.com/tax-authority-rates-api/sunat/) | Peru | Tax / customs | `sunat` | PEN | 2 |
| [Superintendencia Financiera de Colombia](https://allratestoday.com/central-bank-rates-api/sfc/) | Colombia | Central bank | `sfc` | COP | 1 |
| [Sveriges Riksbank](https://allratestoday.com/central-bank-rates-api/riksbank/) | Sweden | Central bank | `riksbank` | SEK | 29 |
| [Swedish Customs (Tullverket)](https://allratestoday.com/tax-authority-rates-api/tullverket/) | Sweden | Tax / customs | `tullverket` | SEK | 148 |
| [Swiss Federal Office for Customs and Border Security](https://allratestoday.com/tax-authority-rates-api/bazg/) | Switzerland | Tax / customs | `bazg` | CHF | 144 |
| [Swiss Federal Tax Administration (ESTV Kursliste)](https://allratestoday.com/tax-authority-rates-api/estvkursliste/) | Switzerland | Tax / customs | `estvkursliste` | CHF | 130 |
| [Swiss National Bank](https://allratestoday.com/central-bank-rates-api/snb/) | Switzerland | Central bank | `snb` | CHF | 30 |
| [Thai Customs Department](https://allratestoday.com/tax-authority-rates-api/thcustoms/) | Thailand | Tax / customs | `thcustoms` | THB | 96 |
| [U.S. Department of the Treasury](https://allratestoday.com/tax-authority-rates-api/ustreasury/) | United States | Tax / customs | `ustreasury` | USD | 145 |
| [Uganda Revenue Authority](https://allratestoday.com/tax-authority-rates-api/ura/) | Uganda | Tax / customs | `ura` | UGX | 285 |
| [US Federal Reserve (H.10)](https://allratestoday.com/central-bank-rates-api/fed/) | United States | Central bank | `fed` | USD | 22 |

## How it is built

The upstream collector fetches each institution's own official table, checks it against the other banks for unit and direction errors, and quarantines anything more than ten percent off. The scripts in `scripts/` refresh the mirrors four times a day.

## Cite this dataset

If you use these files in a paper, notebook, article or product, please cite the dataset and link to it. A visible credit and non-commercial use are the conditions of the CC BY-NC 4.0 licence.

Ready to paste:

```html
<a href="https://allratestoday.com">Exchange rates by AllRatesToday</a>
```

```markdown
Exchange rates by [AllRatesToday](https://allratestoday.com)
```

The link should be a normal, followable link on the page or README where the data is shown.

Plain text:

> AllRatesToday (2026). *Central Bank Exchange Rates: official rates from 180+ central banks, tax and customs authorities.* https://github.com/AllRates-Today/central-bank-exchange-rates (data via https://allratestoday.com/central-bank-rates-api/).

BibTeX:

```bibtex
@misc{allratestoday_central_bank_exchange_rates,
  author       = {AllRatesToday},
  title        = {Central Bank Exchange Rates: official rates from 180+ central banks, tax and customs authorities},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/AllRates-Today/central-bank-exchange-rates}},
  note         = {Daily mirror of the AllRatesToday central bank exchange rate API, https://allratestoday.com/central-bank-rates-api/}
}
```

In a README or blog post, one line is enough:

```md
Exchange rates: [Central Bank Exchange Rates](https://github.com/AllRates-Today/central-bank-exchange-rates) by [AllRatesToday](https://allratestoday.com/central-bank-rates-api/), CC BY-NC 4.0.
```

## License

Data: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Free for non-commercial use (research, education, personal projects, journalism) with a visible credit to AllRatesToday linking to https://allratestoday.com. Commercial use needs a licence: the [Official Rates plan](https://allratestoday.com/pricing#official) covers it, or contact support@allratestoday.com. The underlying figures are public information published by each institution.

Code in `scripts/`: MIT.

Rates are provided as issued by each institution. Verify against the institution before relying on a figure for a legal or tax filing.

## 🔗 Links

- **Download central bank rates:** [allratestoday.com/download-central-bank-rates](https://allratestoday.com/download-central-bank-rates/) — every bank's tables as Excel, CSV or JSON
- [Bank Exchange Rate API](https://allratestoday.com/bank-exchange-rate-api/) — live buy and sell rates from 1,200+ commercial banks in 120+ countries · [npm](https://www.npmjs.com/package/bank-exchange-rates) · [GitHub](https://github.com/AllRates-Today/bank-exchange-rates)
- **All keyless endpoints in one page:** [free-exchange-rate-api](https://github.com/AllRates-Today/free-exchange-rate-api) (open central-bank tables, Frankfurter/Fixer/exchangeratesapi/exchangerate.host drop-ins, MCP)
- **AI agents:** Claude Code plugin `/plugin marketplace add AllRates-Today/claude-code-plugin` · hosted MCP endpoint `https://allratestoday.com/api/mcp` (keyless)
- **New in Oct 2026:** agents can self-issue a trial key — `POST https://allratestoday.com/api/agent/keys` (JSON) → 100 calls / 7 days — and read the keyless [Daily Reference Rate](https://allratestoday.com/reference-rate/) (16:00 London fix) at `https://allratestoday.com/api/open/reference-rate`
- **API Documentation:** [allratestoday.com/developers](https://allratestoday.com/developers)
- **Register (Free):** [allratestoday.com/register](https://allratestoday.com/register)
- **Dashboard:** [allratestoday.com/profile](https://allratestoday.com/profile)
- **Status:** [allratestoday.com/status](https://allratestoday.com/status)
- **Postman:** [allratestoday.com/postman](https://allratestoday.com/postman/)
- [ChatGPT app](https://chatgpt.com/plugins/plugin_asdk_app_6ae1e76098f48191a285ac3f5ab7a83b) — ask ChatGPT for live and official central bank rates
- [OpenAPI reference on Bump.sh](https://bump.sh/allratestoday/doc/allratestoday-api) — also on [SwaggerHub](https://app.swaggerhub.com/apis-docs/allratestoday/allratestoday-exchange-rate-central-bank-rates-api/2.2.0)
