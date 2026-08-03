## 1. Frontend Test Cases (`mypart`)
 
| Test Case ID | Component | Test Case Description | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-FE-01** | `App.vue` — Navigation | Verify tab switching between Dashboard and Websites. | 1. Load the app.<br>2. Click **Websites** in the nav.<br>3. Click **Dashboard** again. | Only the selected tab's page (`MainControls` or `WebsiteManager`) is visible; the active nav button is highlighted (`.active` class applied). |
| **TC-FE-02** | `App.vue` — Shared state | Verify `globalSources` and `globalArticles` are shared correctly via `provide/inject`. | 1. Add a source on the Websites tab.<br>2. Switch to Dashboard tab. | The new source appears as an "Active Source" count on the Dashboard without a page reload. |
| **TC-FE-03** | `AddSiteForm.vue` — Valid submission | Add a new RSS source with valid name/URL. | 1. Go to Websites tab.<br>2. Enter Name = "BBC World", URL = "feeds.bbci.co.uk/news/rss.xml", Category = "World".<br>3. Click **Add Pipeline Stream**. | `site-added` event emits `{ name, url: 'https://feeds.bbci.co.uk/news/rss.xml', category: 'World' }`; URL gets `https://` auto-prefixed; new row appears in the Registered Target Pipelines table; form fields reset to defaults. |
| **TC-FE-04** | `AddSiteForm.vue` — Empty field validation | Attempt submission with empty name or URL. | 1. Leave "Stream Reference Name" blank.<br>2. Fill URL only.<br>3. Click submit. | `handleAdd()` returns early; no `site-added` event is emitted; no new row is added (guarded by `required` + trim check). |
| **TC-FE-05** | `AddSiteForm.vue` — URL normalization | Enter a URL without a protocol prefix. | 1. Type `ewn.co.za/rss` in the URL field.<br>2. Submit. | Emitted URL is normalized to `https://ewn.co.za/rss`. |
| **TC-FE-06** | `WebsiteManager.vue` — Remove source | Remove an existing pipeline. | 1. Click **Remove** on any row in the table. | Row is removed from `sources`; `globalArticles` is cleared (per `removeSource`), and the Dashboard article feed/stat counts reset to 0. |
| **TC-FE-07** | `WebsiteManager.vue` — Empty state | View table with no registered sources. | 1. Remove all sources. | Table shows the "No pipelines registered yet. Use the form above." message spanning all 6 columns. |
| **TC-FE-08** | `MainControls.vue` — Run Scrape Job | Trigger the client-side RSS fetch. | 1. Click **Run Scrape Job** on Dashboard. | Button text changes to "Running Extraction..." and is disabled while `loading = true`; on completion, `globalArticles` populates (max 15 items/source) and each source's `lastScrape` updates to `Success: <time>`. |
| **TC-FE-09** | `MainControls.vue` — Fallback proxy | Primary RSS proxy (`rss2json`) fails or returns non-`ok` status. | 1. Mock/force `rss2json` to fail (e.g., invalid feed).<br>2. Click **Run Scrape Job**. | `fetchRSS` catches the error, logs "rss2json failed, trying backup," and retries via the `allorigins` proxy, parsing the XML with `DOMParser`. |
| **TC-FE-10** | `MainControls.vue` — Both proxies fail | Simulate both RSS proxies failing (network error / bad URL). | 1. Add a source with an invalid/unreachable URL.<br>2. Run Scrape Job. | `console.error` logs the failure; that source's `lastScrape` is set to `'Failed'`; app does not crash; other valid sources still populate normally. |
| **TC-FE-11** | `MainControls.vue` — Category filter pills | Filter articles by category. | 1. Run a scrape.<br>2. Click a filter pill (e.g., "Sport"). | Only articles whose `category` (case-insensitive) matches the selected pill are shown; "Showing" stat count updates accordingly; pill gets the `.active` style. |
| **TC-FE-12** | `MainControls.vue` — Search box | Search articles by keyword. | 1. Type a keyword into the search input that matches a title, description, or source name. | Article list filters live to only matching entries (case-insensitive substring match across title/description/sourceName). |
| **TC-FE-13** | `MainControls.vue` — Empty results state | Search/filter combination yields zero matches. | 1. Enter a nonsense search term. | "No articles match your filters. Click 'Run Scrape Job'." message is shown (only when not loading). |
| **TC-FE-14** | `DataDisplay.vue` — Chart rendering | Verify bar chart renders category counts. | 1. Run a scrape that returns articles across 2+ categories. | Bar chart (`vue-chartjs`) renders one bar per category with correct labels/counts; "Top Categories Metrics" table lists matching rows. |
| **TC-FE-15** | `DataDisplay.vue` — No data state | View chart/table before any scrape has run. | 1. Load Dashboard tab fresh (no scrape yet). | Chart renders with empty dataset (no bars); table shows "No analytics summary data discovered." |
| **TC-FE-16** | Responsiveness | Verify layout adapts on narrow viewports. | 1. Resize browser to <1100px (form) and <992px (charts row). | `AddSiteForm` grid collapses to a single column with full-width button; `DataDisplay` charts stack vertically instead of side-by-side. |





## latest frontend testcases
##  Frontend Test Cases (mypart)
 
Covers the `mypart/` Vue 3 + Vite app: `App.vue`, `router/index.js`, `services/api.js`, and views/components (`HomeView`, `WebsitesView`, `GlobalMap`, `MainControls`, `AddSiteForm`, `WebsiteManager`, `DataDisplay`, `global-map/*`).
 
### 2.1 App Shell & Routing (`App.vue`, `router/index.js`)
 
| ID | Area | Description | Steps | Expected Result |
|---|---|---|---|---|
| TC-FE-01 | Route: Dashboard | `/` renders `HomeView` → `MainControls` | Navigate to `/` | `MainControls` component (dashboard UI) is rendered |
| TC-FE-02 | Route: Websites | `/websites` renders `WebsitesView` → `WebsiteManager` | Navigate to `/websites` | `WebsiteManager` table + `AddSiteForm` rendered |
| TC-FE-03 | Route: Global Map | `/global-map` renders `GlobalMap` view (lazy-loaded) | Navigate to `/global-map` | Globe, Legend, and StatisticsCards render; route chunk loads on demand |
| TC-FE-04 | Route: About | `/about` renders `AboutView` (lazy-loaded) | Navigate to `/about` | "This is an about page" text is shown |
| TC-FE-05 | Active nav link | Nav link highlights the active route | Visit each route | Corresponding `.nav-link` gets `.active` class |
| TC-FE-06 | Provide/inject wiring | Shared state (`globalSources`, `globalArticles`, `selectedSourceName`, etc.) is provided at the root | Mount `App.vue`, inspect injected values in a child | Children receive the same reactive refs; mutating in one place reflects in another |
 
### 2.2 Dashboard — `MainControls.vue`
 
| ID | Area | Description | Steps | Expected Result |
|---|---|---|---|---|
| TC-FE-07 | RSS fetch (happy path) | `fetchRSS(url)` parses an RSS/XML feed via the CORS proxy | Call `fetchRSS('https://ewn.co.za/rss')` with proxy reachable | Returns array of `{title, link, description}`; length > 0 |
| TC-FE-08 | RSS fetch (proxy/network failure) | Fails gracefully when proxy or network is unavailable | Mock `fetch` to reject or return empty XML | Function catches the error, logs a warning, returns `null` (does not throw to caller) |
| TC-FE-09 | Search filter | Typing in the search box filters `filteredArticles` by title/description/source | Set `query.value = "cape town"` with matching + non-matching articles present | Only articles whose title/description/sourceName include the query remain |
| TC-FE-10 | Category filter | Selecting a filter chip (`Politics`, `World`, etc.) filters articles by category | Set `activeFilter.value = "Sport"` | Only `Sport` category articles remain; `"All"` restores the full list |
| TC-FE-11 | Source filter via Global Map selection | `selectedSourceName` (injected) narrows the article list | Set `selectedSourceName.value = "EWN"` | Only articles where `article.sourceName === "EWN"` remain |
| TC-FE-12 | Combined filters | Search + category + source filters can be applied together | Apply all three simultaneously | Resulting list satisfies all three predicates (AND logic) |
| TC-FE-13 | Empty state | No articles match the current filters | Apply a filter combo with zero matches | UI shows an empty/no-results state instead of erroring |
| TC-FE-14 | `globalStats` computed | Category counts are derived correctly from `globalArticles` | Seed `globalArticles` with known category distribution | `globalStats.value.top_categories` matches expected `{name, count}` pairs |
 
### 2.3 Website Manager — `WebsiteManager.vue` / `AddSiteForm.vue`
 
| ID | Area | Description | Steps | Expected Result |
|---|---|---|---|---|
| TC-FE-15 | Add site — valid input | Submitting the form with name + URL adds a new source | Fill "Stream Reference Name" + "Remote Target RSS URL", submit | `site-added` event emitted; new row appears in the pipelines table with `Never Scraped` status |
| TC-FE-16 | Add site — auto-prefix URL | URL without `http(s)://` is auto-prefixed | Enter `bbci.co.uk` as the URL | Emitted payload's `url` is `https://bbci.co.uk` |
| TC-FE-17 | Add site — required fields | Empty name or URL blocks submission | Submit with name or URL left blank | `handleAdd()` returns early; no `site-added` event fired; form does not clear |
| TC-FE-18 | Add site — default category | Category defaults to `Local` if unchanged | Submit without touching the category dropdown | New source's `category` is `"Local"` |
| TC-FE-19 | Form reset after add | Fields clear after a successful submit | Submit a valid entry | `siteName`, `siteUrl` reset to `""`; `category` resets to `"Local"` |
| TC-FE-20 | Remove source | Clicking "Remove" deletes a pipeline and clears cached articles | Click "Remove" on an existing row | Row disappears from `sources`; `globalArticles` is reset to `[]` |
| TC-FE-21 | Empty pipeline table | No sources registered | Remove all sources | Table shows "No pipelines registered yet. Use the form above." |
 
### 2.4 Global Map — `GlobalMap.vue`, `Globe.vue`, `Legend.vue`, `StatisticsCards.vue`
 
| ID | Area | Description | Steps | Expected Result |
|---|---|---|---|---|
| TC-FE-22 | Statistics load (happy path) | `loadStatistics()` fetches `/api/statistics` on mount | Mount `GlobalMap.vue` with backend reachable | `statistics.value` populated from response; `loading` toggles true→false; no `errorMessage` |
| TC-FE-23 | Statistics load (failure) | Backend unreachable / non-200 response | Mock `fetch('/api/statistics')` to reject or return `!ok` | `errorMessage` is set to the fallback-notice text; `nodes` computed falls back to `fallbackNodes` |
| TC-FE-24 | Auto-refresh | Statistics refresh automatically every 30s | Mount component, advance fake timers by 30000ms | `loadStatistics()` is called again; `refreshTimer` cleared on unmount (`onBeforeUnmount`) |
| TC-FE-25 | Node merge logic | Live `source_health` data overrides fallback node coordinates/status | Return `source_health` for `"EWN"` only | Resulting `nodes` array: EWN uses live data, News24/SABC use fallback values |
| TC-FE-26 | `averageSuccessRate` computed | Correctly averages `success_rate` across sources | Provide `source_health` with known success rates (e.g. 100, 50, 0) | Computed value equals `round((100+50+0)/3)` = `50` |
| TC-FE-27 | Select node on globe | Clicking a globe node sets `selectedSourceName` and filters dashboard | Emit `select` from `Globe` with a node | `setSelectedSourceName(node.source_name)` called; selection banner appears with that source name |
| TC-FE-28 | Clear filter | "Clear filter" button resets the selection | Click "Clear filter" while a source is selected | `clearSelectedSourceName()` called; banner disappears; dashboard shows all sources again |
| TC-FE-29 | Scheduler status badge | Header badge reflects running/offline/loading state | Toggle `loading` and `statistics.running` | Badge text/class switches between "Refreshing...", "Scheduler Running", "Scheduler Offline" |
| TC-FE-30 | StatisticsCards rendering | Cards display last refresh, duration, stored articles, active/total sources | Pass known props into `StatisticsCards` | Displayed values match the props exactly; `lastRefresh` formatted via `toLocaleString("en-ZA", ...)` |
| TC-FE-31 | Legend rendering | Legend lists all mapped sources with correct color coding | Pass `nodes` prop with mixed `status` values | Green/red indicators match each node's `status`; all node names listed |
 
### 2.5 API Service Layer — `services/api.js`
 
| ID | Area | Description | Steps | Expected Result |
|---|---|---|---|---|
| TC-FE-32 | Base URL / timeout config | Axios instance is configured correctly | Inspect `api` instance | `baseURL: 'http://localhost:5000/api'`, `timeout: 8000` |
| TC-FE-33 | `getStatistics()` | Calls `GET /statistics` | Invoke and mock axios | Request made to `/statistics` with no params |
| TC-FE-34 | `getItems(page, category)` | Calls `GET /items` with query params | Invoke `getItems(2, "Sport")` | Request includes `params: {page: 2, category: "Sport"}` — **Note:** backend's `items` route currently reads `limit`/`source`, not `page`/`category`; flag as a mismatch to fix |
| TC-FE-35 | `searchItems(q)` | Calls `GET /search` with query param `q` | Invoke `searchItems("weather")` | Request includes `params: {q: "weather"}` |
| TC-FE-36 | `runScrape()` | Calls `POST /scrape` | Invoke `runScrape()` | Request is a `POST` to `/scrape` — **Note:** backend route `scrape.py` only defines `methods=["GET"]`; a `POST` from the frontend will currently return `405 Method Not Allowed` |
| TC-FE-37 | `getHistory()` | Calls `GET /history` | Invoke `getHistory()` | Request made to `/history` |
| TC-FE-38 | `getWebsites()` | Calls `GET /websites` | Invoke `getWebsites()` | Request made to `/websites` |
| TC-FE-39 | `addWebsite(site)` | Calls `POST /websites` with a site payload | Invoke `addWebsite({name, url, category})` | Request is a `POST` to `/websites` — **Note:** no `POST` handler currently exists in `routes/websites.py` (GET only); will 405 until implemented |
| TC-FE-40 | Timeout handling | Request exceeding 8s timeout is rejected | Mock a slow response (>8000ms) | Promise rejects with axios timeout error; caller can catch and show an error state |
 
> ⚠️ **Integration gap found:** `services/api.js` currently calls endpoints/params (`getItems` page+category, `runScrape` POST, `addWebsite` POST) that don't match the current backend implementation, and none of the `mypart` components import from `services/api.js` yet — only `GlobalMap.vue` talks to the backend directly via `fetch('/api/statistics')`. Test cases TC-FE-33–39 should be treated as **pending/integration tests** to run once wiring is completed.
