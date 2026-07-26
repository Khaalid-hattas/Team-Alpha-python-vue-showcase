<script setup>
import { ref } from 'vue'

const query = ref('')
const activeCategory = ref('All')
const activeNav = ref('Websites')
const loading = ref(false)

const filters = ['All', 'Politics', 'World', 'Local', 'Sport', 'Business']

// Analytics stats — swap these values for real data from your scrape job results
const stats = ref([
  { label: 'Total Items', value: '142', badge: '98%' },
  { label: 'Succes rate', value: '98.6%', badge: '0.4%' },
  { label: 'Active sources', value: '1', badge: '20' },
  { label: 'Total Items', value: '142', badge: null },
])

function handleScrape() {
  if (loading.value) return
  loading.value = true

  console.log('Initiating scrape job targeting:', {
    filter: activeCategory.value,
    search: query.value
  })

  // live web scraping API latency
  setTimeout(() => {
    loading.value = false
    alert(`Data aggregation complete for section: ${activeCategory.value}`)
  }, 2500)
}
</script>

<template>
  <div class="dashboard-canvas">
    <div class="dashboard-frame">

      <!-- Top nav bar -->
      <header class="top-nav">
        <div class="brand-group">
          <h1>SCRAPING ANALYTICS<br />PLATFORM</h1>
        </div>

        <nav class="nav-links">
          <a
            :class="{ 'nav-active': activeNav === 'Dashboard' }"
            @click="activeNav = 'Dashboard'"
          >Dashboard</a>
          <a
            :class="{ 'nav-active': activeNav === 'Websites' }"
            @click="activeNav = 'Websites'"
          >Websites</a>
        </nav>
      </header>

      <!-- Page heading + search/action row -->
      <div class="page-heading-row">
        <div class="page-heading">
          <h2>Dashboard</h2>
          <p class="page-subtitle">Source: ewn.co.za &middot; sitemap indexed &middot; Nuxt SSR</p>
        </div>

        <div class="right-controls">
          <div class="search-container">
            <input
              v-model="query"
              type="text"
              placeholder="Search headlines, authors, topics..."
              class="figma-search"
            />
            <button class="search-btn" type="button" aria-label="Search">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="11" cy="11" r="7" stroke="white" stroke-width="2" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" stroke="white" stroke-width="2" stroke-linecap="round" />
              </svg>
            </button>
          </div>

          <button
            :disabled="loading"
            @click="handleScrape"
            class="scrape-action-btn"
          >
            {{ loading ? 'Running...' : 'Run Scrape Job' }}
          </button>
        </div>
      </div>

      <!-- Filter pills -->
      <div class="controls-toolbar">
        <div class="pills-row">
          <button
            v-for="item in filters"
            :key="item"
            :class="{ 'active-pill': activeCategory === item }"
            @click="activeCategory = item"
          >
            {{ item }}
          </button>
        </div>
      </div>

      <!-- Analytics stats grid -->
      <div class="stats-grid">
        <div v-for="(stat, index) in stats" :key="index" class="stat-card">
          <div class="stat-top">
            <span class="stat-label">{{ stat.label }}</span>
            <span v-if="stat.badge" class="stat-badge">{{ stat.badge }}</span>
          </div>
          <div class="stat-value">{{ stat.value }}</div>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.dashboard-canvas {
  background-color: #f8f9fa;
  min-height: 100vh;
  padding: 24px;
  font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
}

.dashboard-frame {
  max-width: 1200px;
  margin: 0 auto;
  background-color: #ffffff;
  padding: 0 24px 24px 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* Top nav bar */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 0 16px 0;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 24px;
}

.brand-group h1 {
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.3px;
  color: #1a1a1a;
  line-height: 1.3;
  margin: 0;
  text-transform: uppercase;
}

.nav-links {
  display: flex;
  gap: 28px;
  align-items: center;
  padding-top: 6px;
}

.nav-links a {
  position: relative;
  font-size: 16px;
  font-weight: 500;
  color: #9aa0a6;
  cursor: pointer;
  padding-bottom: 6px;
  transition: color 0.2s ease;
}

.nav-links a::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 100%;
  height: 2px;
  background-color: #362f78;
  border-radius: 2px;
  transform: translateX(-50%) scaleX(0);
  transform-origin: center;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-links a:hover {
  color: #362f78;
}

.nav-links a:hover::after {
  transform: translateX(-50%) scaleX(1);
}

.nav-links a.nav-active {
  color: #362f78;
  font-weight: 700;
}

.nav-links a.nav-active::after {
  transform: translateX(-50%) scaleX(1);
  height: 2.5px;
}

/* Page heading row */
.page-heading-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 20px;
}

.page-heading h2 {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.page-subtitle {
  font-size: 13px;
  color: #9aa0a6;
  margin: 4px 0 0 0;
}

.right-controls {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 4px;
}

.search-container {
  position: relative;
  display: flex;
  align-items: stretch;
}

.figma-search {
  width: 240px;
  padding: 8px 12px;
  font-size: 12px;
  border: 1px solid #dadce0;
  border-right: none;
  border-radius: 4px 0 0 4px;
  color: #3c4043;
  background-color: #ffffff;
  box-sizing: border-box;
}

.figma-search:focus {
  outline: none;
  border-color: #5fae82;
}

.search-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  border: 1px solid #5fae82;
  background-color: #5fae82;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.search-btn:hover {
  background-color: #519671;
}

.scrape-action-btn {
  background-color: #1b1464;
  color: #ffffff;
  border: none;
  padding: 10px 18px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.2s;
}

.scrape-action-btn:hover {
  background-color: #130d43;
}

.scrape-action-btn:disabled {
  background-color: #757575;
  cursor: not-allowed;
}

/* Filter pills */
.controls-toolbar {
  margin-bottom: 8px;
}

.pills-row {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.pills-row button {
  background-color: #ffffff;
  color: #5f6368;
  border: 1px solid #dadce0;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.pills-row button:hover {
  background-color: #f1f3f4;
}

.pills-row button.active-pill {
  background-color: #1b1464;
  color: #ffffff;
  border-color: #1b1464;
  font-weight: 600;
}

/* Analytics stats grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 24px;
}

.stat-card {
  background-color: #f1f3f4;
  border-radius: 8px;
  padding: 16px 18px;
}

.stat-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
}

.stat-badge {
  font-size: 13px;
  font-weight: 600;
  color: #1e8e3e;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a1a;
}

@media (max-width: 900px) {
  .page-heading-row {
    flex-direction: column;
    align-items: flex-start;
  }
  .right-controls {
    width: 100%;
    justify-content: space-between;
  }
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .top-nav {
    flex-direction: column;
    gap: 12px;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>