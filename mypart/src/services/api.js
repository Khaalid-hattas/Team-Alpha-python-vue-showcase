import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 8000,
})

// Statistics
export const getStatistics = () => api.get('/statistics')

// Items
export const getItems = (page = 1, category = null) =>
  api.get('/items', {
    params: { page, category }
  })

// Search
export const searchItems = (q) =>
  api.get('/search', {
    params: { q }
  })

// Scraping
export const runScrape = () => api.post('/scrape')

// History
export const getHistory = () => api.get('/history')

// Websites
export const getWebsites = () => api.get('/websites')

export const addWebsite = (site) =>
  api.post('/websites', site)

export default api