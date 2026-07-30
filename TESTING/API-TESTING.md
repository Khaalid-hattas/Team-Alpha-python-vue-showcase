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
 
