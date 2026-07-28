# Team Alpha Backend News Aggregator

Production-ready Flask backend that scrapes EWN, News24, and SABC News, normalizes article metadata, stores unique articles, and auto-refreshes every 15 minutes.

## Features

- Multi-source scraping:
  - EWN: latest, local, politics, world
  - News24: latest, business, sport, investigations
  - SABC News: top, opinion, sport
- Safety controls:
  - Custom User-Agent
  - robots.txt checks
  - Request timeout and retry with backoff
  - 0.5 second delay between requests
- Data quality:
  - Shared metadata extraction helpers (Open Graph + fallback)
  - Normalized article schema
  - URL-based duplicate prevention
- Refresh automation:
  - APScheduler refresh job every 15 minutes (configurable)
- REST API:
  - `GET /api/scrape`
  - `GET /api/refresh`
  - `GET /api/articles`
  - `GET /api/status`

## Project Structure

```
backend/
|-- app.py
|-- requirements.txt
|-- scrapers/
|   |-- ewn_scraper.py
|   |-- news24_scraper.py
|   `-- sabc_scraper.py
|-- services/
|   |-- scraper_service.py
|   `-- storage.py
`-- utils/
    `-- scraper_helpers.py
```

## Setup

From the repository root:

```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python app.py
```

App runs on `http://127.0.0.1:5000` by default.

## Environment Variables

- `PORT` (default: `5000`)
- `LOG_LEVEL` (default: `INFO`)
- `SCRAPER_REFRESH_MINUTES` (default: `15`)

Example:

```powershell
$env:SCRAPER_REFRESH_MINUTES="15"
$env:LOG_LEVEL="INFO"
python app.py
```

## API Examples

Manual all-source scrape:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/scrape
```

Force immediate incremental refresh:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/refresh
```

Get latest articles:

```powershell
Invoke-RestMethod "http://127.0.0.1:5000/api/articles?limit=50"
```

Get scheduler/status:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/status
```

## Notes

- Storage uses SQLite at `backend/data/articles.db`.
- Duplicate URLs are skipped at insert time.
- Scheduler errors are isolated so one source failure does not stop refresh operations.
