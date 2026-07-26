<script setup>
import { ref } from 'vue'

const activeNav = ref('Websites')

// Registered sources — swap for real data from your API / store
const sources = ref([
  {
    id: 1,
    name: 'EWN',
    url: 'https://example.com/latest',
    category: 'News',
    lastScrape: '6 minutes ago',
    status: 'Active',
  },
])

function handleRemove(id) {
  sources.value = sources.value.filter((source) => source.id !== id)
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
          <router-link to="/" exact-active-class="nav-active">Dashboard</router-link>
          <router-link to="/websites" exact-active-class="nav-active">Websites</router-link>
        </nav>
      </header>

      <!-- Registered sources card -->
      <div class="sources-card">
        <div class="sources-card-header">
          <h2>Registered sources</h2>
        </div>

        <table class="sources-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>URL</th>
              <th>Category</th>
              <th>Last Scrape</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="source in sources" :key="source.id">
              <td class="cell-name">{{ source.name }}</td>
              <td class="cell-url">{{ source.url }}</td>
              <td>
                <span class="category-pill">{{ source.category }}</span>
              </td>
              <td class="cell-last-scrape">{{ source.lastScrape.toUpperCase() }}</td>
              <td>
                <div class="status-remove-group">
                  <span class="status-active">{{ source.status }}</span>
                  <button class="remove-btn" @click="handleRemove(source.id)">Remove</button>
                </div>
              </td>
            </tr>

            <tr v-if="!sources.length">
              <td colspan="5" class="empty-row">No registered sources yet.</td>
            </tr>
          </tbody>
        </table>
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
  text-decoration: none;
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

.nav-links a:hover,
.top-nav .nav-links a:hover {
  color: #362f78 !important;
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

/* Registered sources card */
.sources-card {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
}

.sources-card-header {
  background-color: #f4f5f6;
  padding: 20px 24px;
}

.sources-card-header h2 {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #1a1a1a;
}

/* Table */
.sources-table {
  width: 100%;
  border-collapse: collapse;
}

.sources-table thead tr {
  background-color: #7fc59c;
}

.sources-table thead th {
  text-align: left;
  padding: 14px 24px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  color: #14361f;
}

.sources-table tbody tr {
  background-color: #f4f5f6;
  border-top: 1px solid #e2e8f0;
}

.sources-table tbody td {
  padding: 18px 24px;
  font-size: 15px;
  color: #1a1a1a;
  vertical-align: middle;
}

.cell-name {
  font-weight: 700;
}

.cell-url {
  color: #4b5563;
  font-weight: 500;
}

.cell-last-scrape {
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.3px;
}

.category-pill {
  display: inline-block;
  background-color: #dbe6fb;
  color: #1d3f8f;
  font-weight: 700;
  font-size: 13px;
  padding: 6px 16px;
  border-radius: 20px;
}

.status-remove-group {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-active {
  color: #1e9e5a;
  font-weight: 700;
}

.remove-btn {
  background-color: #ffffff;
  color: #d64545;
  border: 1px solid #f0b8b8;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease;
}

.remove-btn:hover {
  background-color: #fdf0f0;
  border-color: #d64545;
}

.empty-row {
  text-align: center;
  padding: 32px 24px;
  color: #94a3b8;
  font-size: 14px;
}
</style>