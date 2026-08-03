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