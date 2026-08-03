test code:

## 3. API Endpoint Test Cases (all routes, with method + path)
 
| Test Case ID | Endpoint | Test Case Description | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-API-01** | `GET /` | Root/welcome route. | `curl http://127.0.0.1:5000/` | HTTP `200`; JSON `{"message": "Welcome to Team Alpha Backend API"}`. |
| **TC-API-02** | `GET /api/health` | Health check. | `curl http://127.0.0.1:5000/api/health` | HTTP `200`; JSON `{"status": "healthy", "message": "Backend is running"}`. |
| **TC-API-03** | `GET /api/items` | Retrieve items with default parameters. | `curl http://127.0.0.1:5000/api/items` | HTTP `200`; JSON `{"status": "success", "count": <n>, "items": [...]}` with `limit` defaulted to 100. |
| **TC-API-04** | `GET /api/items?limit=5` | Retrieve items with a custom limit. | `curl "http://127.0.0.1:5000/api/items?limit=5"` | HTTP `200`; `items` array length ≤ 5; `count` matches `len(items)`. |
| **TC-API-05** | `GET /api/items?source=ewn` | Filter items by source. | `curl "http://127.0.0.1:5000/api/items?source=ewn"` | HTTP `200`; all returned items belong to the `ewn` source. |
| **TC-API-06** | `GET /api/items?limit=abc` | Invalid (non-numeric) `limit` parameter. | `curl "http://127.0.0.1:5000/api/items?limit=abc"` | Raises `ValueError` internally → caught by the global exception handler → HTTP `500` with `{"error": "<message>"}` (not a silent crash). |
| **TC-API-07** | `GET /api/statistics` | Retrieve dashboard/scheduler statistics. | `curl http://127.0.0.1:5000/api/statistics` | HTTP `200`; JSON body reflects `get_scheduler_status()` (not the old placeholder). |
| **TC-API-08** | `GET /api/history` | Retrieve scrape history. | `curl http://127.0.0.1:5000/api/history` | HTTP `200`; JSON `{"message": "Scrape history is not yet implemented."}` (documents current stub state — flag for follow-up once implemented). |
| **TC-API-09** | `GET /api/search?q=<term>` | Search articles with a valid query. | `curl "http://127.0.0.1:5000/api/search?q=election"` | HTTP `200`; JSON `{"query": "election", "count": <n>, "results": [...]}`; results only include articles where `q` (lower-cased) appears in title, summary, or description. |
| **TC-API-10** | `GET /api/search` (no `q`) | Search without a query parameter. | `curl http://127.0.0.1:5000/api/search` | HTTP `400`; JSON `{"error": "Search query is required."}`. |
| **TC-API-11** | `GET /api/search?q=` (empty) | Search with an empty query string. | `curl "http://127.0.0.1:5000/api/search?q="` | Treated as falsy by `if not query` → HTTP `400` with the same required-query error. |
| **TC-API-12** | `GET /api/search` — server error path | Force an internal error during search (e.g., corrupted DB row). | Seed a malformed record, then search. | Caught by the route's own `try/except` → HTTP `500`; JSON `{"error": "An unexpected error occurred.", "details": "<str(e)>"}`. |
| **TC-API-13** | `GET /api/websites` | List supported scraper sources. | `curl http://127.0.0.1:5000/api/websites` | HTTP `200`; JSON `{"sources": [...]}` — alphabetically sorted list of `SCRAPER_REGISTRY` keys. |
| **TC-API-14** | `GET /api/scrape` | Trigger a scrape with default (incremental) mode. | `curl http://127.0.0.1:5000/api/scrape` | HTTP `200`; JSON `{"status": "success", "result": {...}}`; `force_full` defaults to `False`. |
| **TC-API-15** | `GET /api/scrape?force_full=true` | Trigger a full re-scrape. | `curl "http://127.0.0.1:5000/api/scrape?force_full=true"` | HTTP `200`; `force_full` is parsed as boolean `True` and passed to `scrape_all_sources`. |
| **TC-API-16** | `GET /api/scrape?force_full=<invalid>` | Pass a non-boolean-like value for `force_full`. | `curl "http://127.0.0.1:5000/api/scrape?force_full=maybe"` | `"maybe".lower() == "true"` evaluates to `False` → treated as a normal (non-full) scrape; no error thrown. |
| **TC-API-17** | Unknown route | Request a path with no matching blueprint. | `curl http://127.0.0.1:5000/api/unknown` | HTTP `404`; JSON `{"error": "Resource not found"}` (global 404 handler). |
| **TC-API-18** | CORS preflight | Verify `OPTIONS` preflight for any `/api/*` route from the Vue dev server origin. | `curl -X OPTIONS -H "Origin: http://localhost:5173" http://127.0.0.1:5000/api/items` | Response includes `Access-Control-Allow-Origin` (and related CORS headers) permitting the frontend to call the API. |
| **TC-API-19** | Wrong HTTP method | Call a GET-only endpoint with an unsupported method. | `curl -X POST http://127.0.0.1:5000/api/health` | HTTP `405 Method Not Allowed` (Flask default, since no `POST` handler is registered on that route). |
 


## latest API & ENDPOINT testcases
##  API / Endpoints Test Cases
 
Functional tests against the live Flask API (`http://localhost:5000`), covering every endpoint actually defined in `backend/routes/`.
 
| ID | Method & Endpoint | Description | Steps | Expected Result |
|---|---|---|---|---|
| TC-API-01 | `GET /` | Root welcome/health message | `curl http://localhost:5000/` | `200`, `{"message": "Welcome to Team Alpha Backend API"}` |
| TC-API-02 | `GET /api/health` | Health check endpoint | `curl http://localhost:5000/api/health` | `200`, `{"status": "healthy", "message": "Backend is running"}` |
| TC-API-03 | `GET /api/items` | List stored articles (default limit) | `curl http://localhost:5000/api/items` | `200`, `{"status": "success", "count": N, "items": [...]}`, `count == len(items)`, `len(items) <= 100` |
| TC-API-04 | `GET /api/items?limit=5` | Limit result count | `curl "http://localhost:5000/api/items?limit=5"` | Returns at most 5 items |
| TC-API-05 | `GET /api/items?source=EWN` | Filter items by source | `curl "http://localhost:5000/api/items?source=EWN"` | All returned items have `source == "EWN"` |
| TC-API-06 | `GET /api/items?limit=abc` | Invalid non-numeric limit | `curl "http://localhost:5000/api/items?limit=abc"` | `500` with generic error JSON (int conversion fails) — flag as a bug: should validate and return `400` instead |
| TC-API-07 | `GET /api/statistics` | Dashboard/scheduler statistics | `curl http://localhost:5000/api/statistics` | `200`, JSON includes `running`, `interval_minutes`, `last_refresh`, `last_duration_seconds`, `stored_articles`, `sources_registered`, `source_health` (array of 3 objects) |
| TC-API-08 | `GET /api/history` | Scrape history | `curl http://localhost:5000/api/history` | `200`, `{"message": "Scrape history is not yet implemented."}` (placeholder, not yet functional) |
| TC-API-09 | `GET /api/search?q=<term>` | Search articles by keyword | `curl "http://localhost:5000/api/search?q=weather"` | `200`, `{"query": "weather", "count": N, "results": [...]}`; every result's title/summary/description contains `"weather"` (case-insensitive) |
| TC-API-10 | `GET /api/search` (no `q`) | Missing required query param | `curl http://localhost:5000/api/search` | `400`, `{"error": "Search query is required."}` |
| TC-API-11 | `GET /api/search?q=` | Empty query string | `curl "http://localhost:5000/api/search?q="` | `400` (empty string is falsy) with same error as TC-API-10 |
| TC-API-12 | `GET /api/websites` | List supported scraper sources | `curl http://localhost:5000/api/websites` | `200`, `{"sources": [...]}` — sorted list of `SCRAPER_REGISTRY` keys (11 topic scrapers) |
| TC-API-13 | `GET /api/scrape` | Trigger incremental scrape (default) | `curl http://localhost:5000/api/scrape` | `200`, `{"status": "success", "result": {"found", "saved", "duplicates", "errors", "duration_seconds", "last_refresh"}}` |
| TC-API-14 | `GET /api/scrape?force_full=true` | Trigger full re-scrape ignoring dedupe cache | `curl "http://localhost:5000/api/scrape?force_full=true"` | `200`, `result.found` reflects all fetched items (not just new ones) |
| TC-API-15 | `POST /api/scrape` | Frontend's `runScrape()` expects POST support | `curl -X POST http://localhost:5000/api/scrape` | Currently `405 Method Not Allowed` — **known bug**, route only registers `GET` |
| TC-API-16 | `POST /api/websites` | Frontend's `addWebsite()` expects POST support | `curl -X POST http://localhost:5000/api/websites -d '{...}'` | Currently `405 Method Not Allowed` — **known bug**, route only registers `GET` (no request body handling implemented) |
| TC-API-17 | `GET /api/does-not-exist` | Unregistered route | `curl http://localhost:5000/api/does-not-exist` | `404`, `{"error": "Resource not found"}` (global 404 handler) |
| TC-API-18 | CORS preflight | Frontend origin allowed for cross-origin calls | Send `OPTIONS` request with `Origin: http://localhost:5173` | Response includes `Access-Control-Allow-Origin` header |
| TC-API-19 | Response content type | All endpoints return JSON | Inspect `Content-Type` header on any successful response | `application/json` |
| TC-API-20 | Idempotency of `/api/scrape` | Running scrape twice in a row doesn't duplicate stored articles | Call `GET /api/scrape` twice consecutively (without `force_full`) | Second call's `saved` is low/0 and `duplicates` reflects previously-seen URLs; `stored_articles` count in `/api/statistics` doesn't double |
 
---
 
## 4. All Endpoints Reference
 
Quick reference of every backend endpoint and where (if anywhere) it's consumed on the frontend.
 
| Endpoint | Method | Blueprint File | Consumed By (Frontend) |
|---|---|---|---|
| `/` | GET | `app.py` | — (manual/health check only) |
| `/api/health` | GET | `routes/health.py` | Not currently called from `mypart` |
| `/api/items` | GET | `routes/items.py` | `services/api.js → getItems()` (param mismatch — see TC-FE-34) |
| `/api/statistics` | GET | `routes/statistics.py` | `views/GlobalMap.vue` (direct `fetch`) and `services/api.js → getStatistics()` |
| `/api/history` | GET | `routes/history.py` | `services/api.js → getHistory()` (backend not yet implemented) |
| `/api/search` | GET | `routes/search.py` | `services/api.js → searchItems()` |
| `/api/websites` | GET | `routes/websites.py` | `services/api.js → getWebsites()`; `addWebsite()` expects POST (not implemented backend-side) |
| `/api/scrape` | GET | `routes/scrape.py` | `services/api.js → runScrape()` expects POST (backend is GET-only) |
 
