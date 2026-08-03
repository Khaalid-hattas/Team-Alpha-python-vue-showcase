# Team Alpha — Test Case Documentation
Covers: **1. Frontend (`mypart`)** · **2. Backend (Flask app)** · **3. API Endpoints**
 
Based on the actual code in:
`mypart/src/App.vue`, `mypart/src/components/AddSiteForm.vue`, `MainControls.vue`, `WebsiteManager.vue`, `DataDisplay.vue`
`backend/app.py`, `backend/routes/*.py`, `backend/services/*.py`
 
---



## Execution Notes
- Backend base URL used above: `http://127.0.0.1:5000` (adjust to your `PORT` env value).
- Frontend dev server: `npm run dev` inside `mypart/`, default `http://localhost:5173`.
- `/api/history` is currently a stub (`TC-API-08`) — re-test once real history persistence is implemented.
- For automated versions of the API tests, `pytest` + Flask's test client (`app.test_client()`) or `requests` against a running server are both suitable; for the frontend, `vitest` + `@vue/test-utils` covers component-level cases (TC-FE-*).


 ## Team-Alpha Python-Vue Showcase — Test Cases
 
## This document covers three test suites for the project:
 
1. **Backend Test Cases** (Flask app in `backend/`)
2. **Frontend Test Cases — My Part** (Vue app in `mypart/`)
3. **API / Endpoint Test Cases** (all REST endpoints actually used between `mypart` and `backend`)
 `backend/app.py`, `backend/routes/*.py`, `backend/services/*.py`, and `mypart/src/**`.
 
---
 
## Table of Contents
- [1. Backend Test Cases](#1-backend-test-cases)
- [2. Frontend Test Cases (mypart)](#2-frontend-test-cases-mypart)
- [3. API / Endpoints Test Cases](#3-api--endpoints-test-cases)
- [4. All Endpoints Reference](#4-all-endpoints-reference)
- [Execution Guidelines](#execution-guidelines)


## Execution Guidelines
 
**Backend (manual/API testing):**
```bash
cd backend
pip install -r requirements.txt
python app.py
 
# In another terminal:
curl http://localhost:5000/
curl http://localhost:5000/api/health
curl http://localhost:5000/api/items
curl "http://localhost:5000/api/items?limit=5&source=EWN"
curl http://localhost:5000/api/statistics
curl http://localhost:5000/api/history
curl "http://localhost:5000/api/search?q=news"
curl http://localhost:5000/api/websites
curl http://localhost:5000/api/scrape
curl "http://localhost:5000/api/scrape?force_full=true"
```
 
**Frontend (mypart):**
```bash
cd mypart
npm install
npm run dev
# Then exercise routes manually: /, /websites, /global-map, /about
# Or wire up a test runner (Vitest + @vue/test-utils) for the component-level cases above
```
 
**Suggested tooling:**
- Backend: `pytest` + Flask's test client (`app.test_client()`) for TC-API-* and TC-BE-* cases.
- Frontend: `Vitest` + `@vue/test-utils` for TC-FE-* component cases; `msw` or manual `fetch`/`axios` mocks for API-dependent components (`GlobalMap.vue`, `services/api.js`).
---
 
### Known Issues Surfaced During Analysis
1. `services/api.js`'s `runScrape()` sends `POST /scrape`, but the backend route only accepts `GET`.
2. `services/api.js`'s `addWebsite()` sends `POST /websites`, but the backend route only accepts `GET` and has no create logic.
3. `services/api.js`'s `getItems(page, category)` sends `page`/`category` params, but the backend reads `limit`/`source`.
4. `/api/items?limit=<non-numeric>` throws an unhandled `int()` conversion error (surfaces as `500` instead of a clean `400`).
5. `/api/history` is a stub — always returns a "not yet implemented" message regardless of actual scrape history.
6. None of the `mypart` Vue components currently import `services/api.js`; `GlobalMap.vue` is the only place calling the backend directly (via native `fetch`).


## second testcases are pre-deployment testcases there will be additional testcases after the  deployement takes place (pre-submission) 


## pre test development 