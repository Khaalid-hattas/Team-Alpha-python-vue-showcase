import axios from 'axios'

const api = axios.create({
  baseURL: 'https://team-alpha-python-vue-showcase-back.onrender.com/api',
  timeout: 8000,
})

// Statistics
export const getStatistics = () => api.get('/statistics')

// Items
export const getItems = (page = 1, category = null) =>
  api.get('/items', {
    page,
    category
  })

// Search
export const searchItems = (q) =>
  api.get('/search', {
    params: { q }
  })

// Scraping
export const runScrape = () => api.post('/scrape', { timeout: 180000 }) // up to 3 min — real scraping is slow

// History
export const getHistory = () => api.get('/history')

// Websites
export const getWebsites = () => api.post('/websites')

export const addWebsite = (site) =>
  api.post('/websites', site)

export default api