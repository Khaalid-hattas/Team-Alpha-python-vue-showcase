# Team Alpha Showcase – Global News Dashboard

This branch contains the combined work of three team members on the Global News Dashboard project.

## Team Contributions

### Person 1 - Nhlakanipho Luthuli
- Developed the backend scraper system.
- Integrated APScheduler for automated scraping.
- Created and maintained news scrapers.
- Implemented article storage and scheduler services.

### Person 2 - Aphiwe Lukho Bija
- Developed the dashboard interface.
- Built the article tables and filtering system.
- Integrated the backend API with the frontend.
- Improved the overall dashboard layout and navigation.

### Person 3 - Nithaam Julius
- Developed the interactive 3D Global Map using Three.js.
- Connected the globe to the live `/api/statistics` endpoint.
- Added live source health monitoring.
- Created the Statistics Cards component.
- Added automatic refresh of live statistics.
- Improved responsiveness for the Global Map page.
- Implemented source selection from globe markers to filter dashboard data.
- Improved globe marker interaction by enlarging click areas and separating overlapping Johannesburg markers.
- Added status indicators, progress bars, and formatted refresh timestamps.
- Optimised cleanup of Three.js resources when leaving the page.

---

# Technologies Used

- Vue 3
- Vite
- Three.js
- Flask
- APScheduler
- Python
- JavaScript
- HTML5
- CSS3

---

# Project Structure


frontend/
    src/
        components/
        views/
        router/

backend/
    routes/
    services/
    scrapers/
    storage/
```

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd Team-Alpha-showcase-project


---

## 2. Install Backend

```bash
cd backend
pip install -r requirements.txt
```

---

## 3. Run Backend

```bash
python app.py
```

The backend will start on:

```
http://127.0.0.1:5000
```

---

## 4. Install Frontend

Open another terminal.

```bash
cd frontend
npm install
```

---

## 5. Run Frontend

```bash
npm run dev
```

The frontend will normally be available at:

```
http://localhost:5173
```

---

# Features

- Live news dashboard
- Interactive 3D globe
- Live source health monitoring
- Automatic statistics refresh
- Dashboard filtering by clicking globe markers
- Responsive design
- Scheduled scraping
- REST API endpoints

---

# API Endpoint Used


GET /api/statistics


Returns:

- Scheduler status
- Source health
- Success rates
- Last refresh
- Articles scraped
- Registered sources

---

# Notes

- Start the Flask backend before running the Vue frontend.
- APScheduler automatically refreshes scraper statistics.
- The frontend communicates with the backend through the `/api/statistics` endpoint.
- Globe markers can be selected to filter dashboard information.
