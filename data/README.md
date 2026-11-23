# These files have moved

Since 23 November 2026 the rate tables are no longer stored in this repository. Each `data/<code>/latest.json` here is a short notice saying where the data went, so existing scripts get an explanation instead of a bare 404.

**To keep getting the data:**

1. Register for a free AllRatesToday account: https://allratestoday.com/register/?utm_source=github&utm_medium=moved_notice&utm_campaign=central-bank-exchange-rates (one minute, no card).
2. Copy your API key from your dashboard.
3. Call `https://allratestoday.com/api/v1/central-bank/<code>/latest` with the header `Authorization: Bearer YOUR_KEY`. Same rates list as before (base, quote, type, value), with the date in `rate_date`, refreshed four times a day.

**Full history** (back to 1914, one CSV per institution): https://huggingface.co/datasets/AllRatesToday/central-bank-exchange-rates. Log in to Hugging Face and paste your free key into the **Get access** form; it is approved within about 5 minutes.

Questions or a broken integration: support@allratestoday.com
