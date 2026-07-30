# Backend Test Suite Documentation

This repository contains the backend test cases for validating the **Flask application** (`app.py`), **SQLite database** (`articles.db`), and **web scraper modules** (`ewn_scraper.py`, `news24_scraper.py`, `sabc_scraper.py`).

---

# Table of Contents
- [1. Database Setup & Management](#1-database-setup--management-articlesdb--apppy)
- [2. Web Scraper Modules](#2-web-scraper-modules-scrapers)
- [3. Flask REST API Endpoints](#3-flask-rest-api-endpoints-apppy)
- [Execution & Verification Guidelines](#execution--verification-guidelines)

---

# 1. Database Setup & Management (`articles.db` & `app.py`)

| Test Case ID | Feature / Area | Test Case Description | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-DB-01** | Table Schema | Verify initialization of the database and `articles` table structure. | Run backend start command or DB init script. Inspect SQLite schema. | Database `articles.db` is created with columns: `id`, `title`, `source`, `url`, `content`, `category`, and `timestamp`. |
| **TC-DB-02** | Unique Constraints | Ensure duplicate articles (by URL or title) are prevented. | Insert an article entry twice into the SQLite database. | Database handles/ignores duplicates gracefully without corrupting existing records or crashing. |
| **TC-DB-03** | Data Persistence | Validate that stored articles persist across server restarts. | 1. Insert test records.<br>2. Restart Flask server.<br>3. Query articles table. | All previously scraped/inserted records remain intact in the database. |

---

# 2. Web Scraper Modules (`scrapers/`)

| Test Case ID | Feature / Area | Test Case Description | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-SCRAP-01** | EWN Scraper | Validate fetching and parsing of EWN news articles (`ewn_scraper.py`). | Execute `ewn_scraper.py` directly or trigger via scrape task. | Successfully fetches live articles, returning title, URL, publication timestamp, and content body. |
| **TC-SCRAP-02** | News24 Scraper | Validate fetching and parsing of News24 articles (`news24_scraper.py`). | Execute `news24_scraper.py` directly or trigger via scrape task. | Parses target selectors correctly; extracts non-empty article titles and valid article links. |
| **TC-SCRAP-03** | SABC Scraper | Validate fetching and parsing of SABC News articles (`sabc_scraper.py`). | Execute `sabc_scraper.py` directly or trigger via scrape task. | Successfully extracts headlines and article data from the SABC RSS/web feed. |
| **TC-SCRAP-04** | Error Handling | Verify scraper resilience to HTTP timeouts or broken HTML selectors. | Simulate target site outage or invalid selector parsing. | Scraper catches the exception, logs appropriate errors, and does not crash the entire application. |
| **TC-SCRAP-05** | Data Sanitation | Ensure scraped HTML content is sanitized before DB insert. | Pass raw scraped HTML strings containing tags or scripts into parser. | HTML tags are stripped/cleaned, leaving safe, formatted plain text content. |

---

# 3. Flask REST API Endpoints (`app.py`)

| Test Case ID | Endpoint | Test Case Description | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-API-01** | `GET /` | Health Check / Index endpoint validation. | Send `GET` request to `http://localhost:5000/`. | Returns `200 OK` status with API status/welcome message. |
| **TC-API-02** | `GET /api/articles` | Retrieve all articles from database. | Send `GET` request to `/api/articles`. | Returns `200 OK` with JSON array containing list of all stored articles. |
| **TC-API-03** | `GET /api/articles?source=<source>` | Filter articles by source (e.g., `EWN`, `News24`, `SABC`). | Send `GET` request to `/api/articles?source=EWN`. | Returns `200 OK` containing only articles where source matches `EWN`. |
| **TC-API-04** | `GET /api/articles/<id>` | Fetch single article details by ID. | Send `GET` request to `/api/articles/1`. | Returns `200 OK` with JSON payload for article ID 1. |
| **TC-API-05** | `GET /api/articles/<id>` | Request non-existent article ID. | Send `GET` request to `/api/articles/999999`. | Returns `404 Not Found` with a structured error JSON message (e.g., `{"error": "Article not found"}`). |
| **TC-API-06** | `POST /api/scrape` | Trigger manual scraping process. | Send `POST` request to `/api/scrape`. | Triggers scrapers, populates DB, and returns `200 OK` with job status summary (e.g., `{"status": "success", "added": X}`). |
| **TC-API-07** | Middleware / CORS | Validate CORS header handling for frontend communication. | Send `OPTIONS` request with `Origin: http://localhost:5173`. | Response includes `Access-Control-Allow-Origin` headers allowing request processing. |

---

## Execution & Verification Guidelines

To run these manual tests locally:

1. **Database Checks:**
   ```bash
   sqlite3 articles.db ".schema"


   #INDIVIDUAL SCRAPER INFO
   python scrapers/ewn_scraper.py
   python scrapers/news24_scraper.py
   python scrapers/sabc_scraper.py

   #API ENDPOINT VERIFICATION
   curl -X GET [http://127.0.0.1:5000/api/articles]//(http://127.0.0.1:5000/api/articles)




   ##CASE TEST TWO FROM BACKEND

   # 2. Backend Test Cases (Flask app, services, scrapers, storage)
 
| Test Case ID | Feature / Area | Test Case Description | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-BE-01** | App bootstrap | Verify `bootstrap()` initializes storage and starts the scheduler on import. | Run `python app.py` (or import `app`). | `init_storage()` creates/opens `data/articles.db` without error; `start_scheduler()` starts without raising; log line "Application bootstrap complete" is emitted. |
| **TC-BE-02** | Blueprint registration | Verify all blueprints are registered and routable. | Start the app and hit each of `/`, `/api/health`, `/api/items`, `/api/statistics`, `/api/history`, `/api/search`, `/api/websites`, `/api/scrape`. | All routes respond (no 404 due to missing blueprint registration). |
| **TC-BE-03** | CORS | Verify CORS is enabled for cross-origin frontend requests. | Send a request with `Origin: http://localhost:5173` header to any `/api/*` route. | Response includes `Access-Control-Allow-Origin` header (via `flask_cors.CORS(app)`), allowing the Vue frontend to consume the API. |
| **TC-BE-04** | 404 handler | Request an undefined route. | `GET /api/does-not-exist`. | Returns HTTP `404` with JSON body `{"error": "Resource not found"}`. |
| **TC-BE-05** | 500 / generic exception handler | Force an unhandled exception (e.g., malformed query param causing a server-side error). | Trigger an internal error, e.g., pass a non-numeric `limit` to `/api/items` (`?limit=abc`). | `int(request.args.get("limit", 100))` raises `ValueError`; the global `Exception` handler catches it and returns HTTP `500` with `{"error": "<message>"}` instead of crashing the server. |
| **TC-BE-06** | `SECRET_KEY` / env config | Verify environment variables load via `.env`/`dotenv`. | Set `SECRET_KEY` and `PORT` in `.env`; start app. | `app.config["SECRET_KEY"]` matches `.env` value; server binds to the configured `PORT` (defaults to 5000 if unset). |
| **TC-BE-07** | Storage — `init_storage()` | Verify database/table is created if not present. | Delete `data/articles.db` (or point to a fresh path), then start the app. | `articles.db` and its schema are (re)created automatically without errors. |
| **TC-BE-08** | Storage — `get_articles()` filtering | Verify article retrieval honors `limit` and `source` filters. | Call `get_articles(limit=5)` and `get_articles(source="ewn")` directly (unit test) with seeded rows. | Returns at most `limit` rows; `source` filter returns only rows matching that source (case handling as implemented). |
| **TC-BE-09** | Storage — duplicate handling | Insert the same article (same URL/title) twice. | Seed the DB with a duplicate scraped item. | Duplicate is not inserted twice / does not corrupt the DB (no unhandled `IntegrityError` bubbling to a 500). |
| **TC-BE-10** | Scraper service — `scrape_all_sources()` | Verify orchestration across all registered scrapers. | Call `scrape_all_sources(force_full=False)` directly. | Returns a summary result (e.g., counts per source); calls each scraper in `SCRAPER_REGISTRY` and persists new articles via `services.storage`. |
| **TC-BE-11** | Scraper service — `force_full` flag | Verify `force_full=true` behaves differently from an incremental scrape. | Call scrape once normally, then again with `force_full=True`. | Full scrape re-fetches/re-processes sources rather than only new/incremental items (per implementation logic). |
| **TC-BE-12** | Scraper service — scheduler | Verify `start_scheduler()` and `get_scheduler_status()` reflect running state. | Start the app; call `get_scheduler_status()`. | Returns a dict describing scheduler state (e.g., running, last run time, next run time) — no placeholder/stub values. |
| **TC-BE-13** | `SCRAPER_REGISTRY` | Verify all expected scrapers are registered. | Inspect `SCRAPER_REGISTRY.keys()`. | Contains entries for EWN, News24, and SABC (matching `scrapers/ewn_scraper.py`, `news24_scraper.py`, `sabc_scraper.py`). |
| **TC-BE-14** | `ewn_scraper.py` | Verify EWN scraper parses live/mock HTML correctly. | Run scraper against a live or mocked EWN page/RSS. | Returns non-empty list of articles with title, url, and timestamp populated; no unhandled exception on malformed markup. |
| **TC-BE-15** | `news24_scraper.py` | Verify News24 scraper parses target selectors. | Run scraper against a live or mocked News24 page/RSS. | Extracts non-empty titles and valid article links; gracefully skips malformed entries. |
| **TC-BE-16** | `sabc_scraper.py` | Verify SABC scraper parses target selectors. | Run scraper against a live or mocked SABC page/RSS. | Extracts non-empty headlines/article data. |
| **TC-BE-17** | Scraper error resilience | Simulate a timeout or broken selector for any scraper. | Point a scraper at an unreachable URL or altered HTML structure. | Exception is caught internally, logged, and does not propagate to crash `scrape_all_sources()` or the Flask process. |
| **TC-BE-18** | `scraper_helpers.py` | Verify shared helper utilities (e.g., text cleaning/date parsing) behave correctly on edge-case input. | Pass empty strings, `None`, and HTML-laden strings into helper functions. | Functions handle `None`/empty gracefully (no `AttributeError`) and strip HTML/whitespace as intended. |
 
---
