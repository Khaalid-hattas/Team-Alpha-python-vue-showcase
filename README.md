# Team-Alpha-python-vue-showcase

## About The Project

Team Alpha is focused on implementing backend functionality into a modern Vue.js frontend framework. The project centers around building Flask API services and web scraping live data to power a dynamic, scalable website.

This project addresses key data integration challenges by delivering a responsive web application that scrapes, processes, and serves real-time data directly to a reactive frontend interface.

Built as a 2-week Agile Scrum capstone project, the platform automatically collects publicly available information from selected websites (news, jobs, e-commerce, or weather sources) and displays it in a clean, interactive dashboard — demonstrating the full lifecycle of data collection, processing, API delivery, and frontend rendering.

---

## Company Background

| Detail | Information |
| :--- | :--- |
| **Project** | Team-Alpha-python-vue-showcase |
| **Framework** | Vue.js & Flask (Python) |
| **Core Feature** | Web Scraping & Live Data Integration |
| **Architecture** | Scalable Full-Stack Application |
| **Focus** | Real-time Data Visualization & Processing |
| **Methodology** | Agile Scrum (2-week sprint cycle) |

---

## Current Pain Points

* Live data is fragmented across external web sources and difficult to aggregate
* Backend processing and scraping logic are disconnected from front-end interfaces
* Static data displays lack real-time updates and dynamic responsiveness
* Scaling backend data extraction requires unified API endpoints for frontend consumption

---

## Project Goal

To create a **user-friendly, responsive web-based system** that demonstrates how live scraped data and Flask backend services can be seamlessly integrated and automated using modern front-end technologies like Vue.js.

---

## Team Members & Roles

### Leadership & QA

| Name | Role |
| :--- | :--- |
| Nikita Muller | Team Leader |
| Sibongile Mapeta | Scrum Master |
| Khaalid Hattas | QA |

### Frontend Team

| Name | Role |
| :--- | :--- |
| Lisekho Smith | Frontend Dev 1 |
| Aphiwe Lukho Bija | Frontend Dev 2 |
| Matthew Neo Adriaanse | Frontend Dev 3 |
| Nithaam Julius | Frontend Dev 4 |

### Backend Team

| Name | Role |
| :--- | :--- |
| Krishendree Kistensamy | Backend Dev 1 |
| Siwaphiwe Siboto | Backend Dev 2 |
| Nhlakanipho Luthuli | Backend Dev 3 |

---

## Individual Contributions

### Frontend

**Person 1 - Aphiwe Lukho Bija**
* Designed the live globe's look and feel, including a double-click "galaxy view" easter egg
* Set the overall frontend layout and visual style, later extended by Nithaam's dedicated globe page
* Built the dashboard page components: navbar, app header, topic filter pills, search bar, run-scrape button
* Built the Website Manager page (`WebsiteManager.vue`, `AddSiteForm.vue`, `SitesTable.vue`) — form validation, listing, and removal of registered sources, tested against mock data
* Divided page ownership across the frontend team (Lukho, Matthew, Lisekho, Nithaam) and merged everyone's frontend code into one working build

**Person 2 - Lisekho Smith — Data Display Page**
* Connected to the REST API via Axios to fetch records on component mount
* Rendered data in a responsive, dynamic table with columns mapped from the API response
* Implemented loading and error states
* Added search and filtering functionality

**Person 3 - Matthew Neo Adriaanse**
* Fixed graph rendering issues
* Created the system metric panel
* Created the navbar
* Created the front page blocks
* Built the register pipeline feed system

**Person 4 - Nithaam Julius**
* Created the Three.js interactive globe

### Backend

**Person 1 - Krishendree Kistensamy — Data Layer & Backend API**
* Set up the virtual environment (Python, Flask, BeautifulSoup4) for the backend
* Verified database schema and models (SQLAlchemy `db` instance, `Item` table)
* Built statistics and history reporting (`get_statistics()`, `get_history()`, `create_scrape_log()`)
* Added global error handling for 404, 500, and unexpected exceptions
*  Divided backend task ownership across the team (Siwaphiwe, Nhlakanipho) and helped oversee that everyone's backend code was functional.

**Person 2 - Siwaphiwe Siboto — Flask API Setup & Integration**
* Set up the Flask backend environment (virtual env, dependencies, `requirements.txt`)
* Structured the backend project (`app.py`, `routes/`, `.env`, `.gitignore`)
* Configured the main Flask app, enabled CORS, and registered API blueprints
* Added global error handling for 404, 500, and unexpected exceptions
* Managed backend Git workflow and merge integration into the `develop` branch

**Person 3 - Nhlakanipho Luthuli — Scraper Development**
* Scoped and confirmed the EWN (Eyewitness News) scraping source
* Built `ewn_scraper.py`, including metadata parsing and the main `scrape()` entry point
* Registered EWN topics into the scraper service and normalized items before saving
* Assisted with Three.js integration on the frontend

---

## images of what the frontend and backend work looks like

### Frontend

![Frontend screenshot 1](https://i.ibb.co/GvMtQgrH/2-B19-DC05-EF11-4-CC2-9947-5-AB8-A383-CF18.png)

![Frontend screenshot 2](https://i.ibb.co/G4GZ4FYQ/812084-A6-77-DF-4-DE9-A097-02-CF8-BB28836.png)

![Frontend screenshot 3](https://i.ibb.co/6cXMvFH9/F50-EBDCD-0951-41-AB-B697-0290-DA1-F3-B42.png)

### Backend

![Backend screenshot 1](https://i.ibb.co/7Jgh8Cnc/nhlaksscrap2.png)

![Backend screenshot 2](https://i.ibb.co/rJW6HZD/Nhlaksscrap1.png)

---

## Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Vue.js** | Frontend framework & reactive components |
| **Vue Router** | Frontend page navigation |
| **Pinia** | Frontend state management |
| **Axios** | HTTP client for API requests |
| **Python & Flask** | Backend REST API framework |
| **BeautifulSoup4** | HTML parsing for web scraping |
| **Requests** | HTTP requests for scraping targets |
| **HTML5** | Structure |
| **CSS3** | Styling |
| **JavaScript (ES6)** | Interactivity & API requests |
| **Git & GitHub** | Version control |

---

## Getting Started

### Backend (Flask)

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with any required environment variables (e.g. `FLASK_ENV=development`).

```bash
python app.py
```

The API will run at `http://localhost:5000`. Confirm it's working by visiting `/api/health`.

### Frontend (Vue.js)

```bash
cd frontend
npm install
npm run dev
```

The dashboard will run at `http://localhost:5173` (or the port shown in your terminal) and will connect to the Flask API automatically via Axios.

> Make sure the backend is running first, since the frontend depends on it for all live data.

---

## Project Structure

```
project/
├── backend/
│   ├── app.py              # Application entry point
│   ├── routes/              # Flask Blueprints & endpoints
│   ├── services/            # Scraping logic & orchestration
│   ├── scrapers/             # Site-specific BeautifulSoup scrapers
│   ├── models/               # Data schemas / persistence layer
│   ├── utils/                # Helper functions & data cleaners
│   └── requirements.txt      # Flask, BeautifulSoup4, Requests, pandas
└── frontend/
    ├── src/
    │   ├── components/       # Reusable UI widgets (Navbar, StatCards)
    │   ├── views/             # Page views (Dashboard, Websites, Search)
    │   ├── services/          # Axios API HTTP service modules
    │   ├── router/            # Vue Router navigation maps
    │   └── assets/            # CSS stylesheets and media images
    └── public/
```

---

## Core API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/items` | Retrieves all scraped items with pagination support |
| `POST` | `/api/scrape` | Triggers an on-demand scraping job for selected targets |
| `GET` | `/api/statistics` | Returns summary stats (total items, success rate, target count) |
| `GET` | `/api/history` | Lists historical scraping logs and execution timestamps |
| `GET` | `/api/search?q={query}` | Filters scraped items matching the search query parameter |
| `GET` / `POST` | `/api/websites` | Fetches or registers websites available for scraping |

---

## Git Workflow

| Branch | Purpose |
| :--- | :--- |
| `main` | Production-ready release code |
| `develop` | Integration branch for features |
| `feature/frontend` | UI developments |
| `feature/api` | REST endpoint implementations |
| `feature/scraper` | Web scraping scripts |

All code passes Pull Request (PR) review before merging.
