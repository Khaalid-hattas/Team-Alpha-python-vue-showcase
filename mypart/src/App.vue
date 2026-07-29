<script setup>
import { ref, provide } from 'vue'
import MainControls from './components/MainControls.vue'
import WebsiteManager from './components/WebsiteManager.vue'

const activeTab = ref('Dashboard')

const globalStats = ref({
  top_categories: []
})

// RSS feed sources
const sourcesList = ref([
  {
    id: 1,
    name: 'EWN',
    url: 'https://ewn.co.za/rss',
    category: 'Local',
    lastScrape: 'Never Scraped',
    isActive: true
  },
  {
    id: 2,
    name: 'News24',
    url: 'https://www.news24.com/rss/news24/topstories',
    category: 'Politics',
    lastScrape: 'Never Scraped',
    isActive: true
  },
  {
    id: 3,
    name: 'BBC',
    url: 'https://feeds.bbci.co.uk/news/rss.xml',
    category: 'World',
    lastScrape: 'Never Scraped',
    isActive: true
  }
])

const globalArticles = ref([])

provide('globalSources', sourcesList)
provide('globalArticles', globalArticles)
provide('activeTab', activeTab)
provide('globalStats', globalStats)
</script>

<template>
  <div class="app">
    <header class="header">
      <div class="header-inner">
        <div class="brand">
          <div class="brand-bar"></div>
          <h1>SCRAPING ANALYTICS PLATFORM</h1>
        </div>

        <nav class="nav">
          <button
            :class="{ active: activeTab === 'Dashboard' }"
            @click="activeTab = 'Dashboard'"
          >
            Dashboard
          </button>

          <button
            :class="{ active: activeTab === 'Websites' }"
            @click="activeTab = 'Websites'"
          >
            Websites
          </button>
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">

        <div class="page" v-show="activeTab === 'Dashboard'">
          <MainControls />
        </div>

        <div class="page" v-show="activeTab === 'Websites'">
          <WebsiteManager />
        </div>

      </div>
    </main>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --navy: #212161;
  --primary: #1b1464;
  --text: #202124;
  --text-muted: #5f6368;
  --border: #dadce0;
  --bg: #ffffff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body,
#app {
  width: 100%;
  min-height: 100%;
  background: #f8f9fa;
}

body {
  font-family: 'Inter', sans-serif;
  color: var(--text);
  font-size: 14px;
}

.app {
  width: 100%;
  min-height: 100vh;
}

.header {
  position: sticky;
  top: 0;
  z-index: 100;
  width: 100%;
  height: 64px;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
}

.header-inner {
  max-width: 1600px;
  height: 100%;
  margin: auto;
  padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 340px;
  flex-shrink: 0;
}

.brand-bar {
  width: 4px;
  height: 24px;
  background: var(--primary);
}

.brand h1 {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: .3px;
  white-space: nowrap;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  width: 220px;
  flex-shrink: 0;
  gap: 32px;
}

.nav button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-muted);
  padding: 8px 0;
  font-family: 'Inter';
  transition: .2s;
}

.nav button.active {
  color: var(--primary);
  font-weight: 600;
  border-bottom: 2px solid var(--primary);
}

.main {
  width: 100%;
  padding: 28px 0;
}

.container {
  max-width: 1600px;
  margin: auto;
  padding: 0 32px;
}

.page {
  width: 100%;
  animation: fade .25s ease;
}

.card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
}

@keyframes fade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>