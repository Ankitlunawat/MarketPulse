# MarketPulse

MarketPulse is a product price comparison and history dashboard.

## What is this project used for?

MarketPulse helps a retailer or analyst compare product offers across sources, spot price changes, check availability and review historical prices in one place. Instead of comparing separate catalogue pages manually, users can search products, filter categories, inspect price history and download a CSV for further analysis.

The application demonstrates the complete path from extracting catalogue HTML to validated price observations, an API and an interactive dashboard. It is useful as a starting point for a permitted-source price monitoring system.

## Typical workflow

1. Import a catalogue snapshot with its capture timestamp.
2. Review the latest offers and availability in the dashboard.
3. Compare sources and inspect historical price movements.
4. Export results for reporting or further analysis.

## Quick start (Windows, macOS or Linux)

Requires Python 3.12+ and Node 20+.

1. Open a terminal in this folder. Run `python -m venv .venv`.
2. Activate: Windows `.venv\Scripts\activate`; macOS/Linux `source .venv/bin/activate`.
3. Run `pip install -r requirements.txt`.
4. Run `python backend/manage.py migrate`.
5. Run `python backend/manage.py import_snapshot fixtures/day1.html --at 2026-10-01T10:00:00+00:00`. Repeat for day2 / October 2 and day3 / October 3.
6. Run `python backend/manage.py runserver`.
7. In another terminal: `cd frontend`, `npm install`, `npm run dev`.
8. Open http://127.0.0.1:5173.

## Instant sample

Open sample-output/MarketPulse_Demo.html in your browser. It embeds the real API output from the synthetic fixtures and needs no server. Search, category filters, history and CSV download work offline.

## Features

Search, category filter, multi-source comparison, stock status, price changes, historical observations, CSV download, error/loading states and responsive layout. Importing the same snapshot twice does not duplicate records. API is read-only.

Default database is SQLite for easy local startup. Set PGDATABASE, PGUSER, PGPASSWORD and optionally PGHOST/PGPORT to use PostgreSQL; then migrate and import again.

## Data honesty

All bundled prices, products and retailers are synthetic. HTML fixtures are scraped by the real parser; these are not live retailer results. URLs use reserved example.com. Sample output was generated from those fixtures. No client engagement or business impact is claimed.

Refresh retrieves the database's latest data. To capture a new observation, import a new HTML file with its real timezone-aware timestamp. The scraper module includes an explicitly allowlisted HTTPS fetch function with a robots check, timeout and no redirects. Real websites need permission, source-specific selectors, rate limits and testing. No scheduler or live retail integration is enabled.

## API

GET /api/products/?q=headphones&category=Audio
GET /api/products/1/history/
GET /api/summary/
GET /api/export/

## Verification

`python backend/manage.py test tracker`
`cd frontend` then `npm run build`

## Deployment

Local demo only. Before public deployment configure a secret, DEBUG=0, exact allowed hosts, authentication where required, HTTPS, a production server, logging and backups. Never expose the default demo configuration publicly.
