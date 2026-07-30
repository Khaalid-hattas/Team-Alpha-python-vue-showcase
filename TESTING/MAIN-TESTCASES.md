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
