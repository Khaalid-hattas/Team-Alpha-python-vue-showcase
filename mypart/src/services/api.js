import axios from 'axios'

// Create Axios instance with production backend base URL
const api = axios.create({
  baseURL: 'https://team-alpha-python-vue-showcase-back.onrender.com/api',
  timeout: 10000, // 10s default timeout for standard requests
  headers: {
    'Content-Type': 'application/json',
  },
})

// ============================
// API Endpoints
// ============================

// Statistics -> GET /api/statistics
export const getStatistics = () => api.get('/statistics')

// Items -> GET /api/items?page=1&category=...
export const getItems = (page = 1, category = null) =>
  api.get('/items', {
    params: { page, category },
  })

// Search -> GET /api/search?q=...
export const searchItems = (q) =>
  api.get('/search', {
    params: { q },
  })

// Trigger Scraping -> POST /api/scrape
// Note: Handled asynchronously on backend to prevent Render 502 HTTP timeouts
export const runScrape = () =>
  api.post('/scrape', {}, { timeout: 30000 }) 

// History -> GET /api/history
export const getHistory = () => api.get('/history')

// Websites -> GET /api/websites & POST /api/websites
export const getWebsites = () => api.get('/websites')

export const addWebsite = (site) => api.post('/websites', site)

export default api