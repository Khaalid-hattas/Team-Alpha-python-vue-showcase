<script setup>
import { ref, provide } from 'vue'
<<<<<<< HEAD
import MainControls from './components/MainControls.vue'
import WebsiteManager from './components/WebsiteManager.vue'
import Globe from './components/Globe.vue'

const activeTab = ref('Dashboard')
=======
>>>>>>> 79f50824fc0d7876796b89d0944b4fcdee71c365

const globalStats = ref({
  top_categories: []
})

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
<<<<<<< HEAD
    name: 'BBC',
    url: 'https://bbci.co.uk',
    category: 'World',
=======
    name: 'SABC News',
    url: 'https://www.sabcnews.com/sabcnews/feed/',
    category: 'Local',
>>>>>>> 79f50824fc0d7876796b89d0944b4fcdee71c365
    lastScrape: 'Never Scraped',
    isActive: true
  }
])

const globalArticles = ref([])
const selectedSourceName = ref('')

function setSelectedSourceName(sourceName) {
  selectedSourceName.value = sourceName || ''
}

function clearSelectedSourceName() {
  selectedSourceName.value = ''
}

provide('globalSources', sourcesList)
provide('globalArticles', globalArticles)
provide('globalStats', globalStats)
provide('selectedSourceName', selectedSourceName)
provide('setSelectedSourceName', setSelectedSourceName)
provide('clearSelectedSourceName', clearSelectedSourceName)
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
          <RouterLink to="/" class="nav-link" active-class="active" exact-active-class="active">
            <span class="nav-icon" aria-hidden="true"></span>
            Dashboard
          </RouterLink>

          <RouterLink to="/websites" class="nav-link" active-class="active">
            <span class="nav-icon" aria-hidden="true"></span>
            Websites
<<<<<<< HEAD
          </button>

          <button
            :class="{ active: activeTab === 'TargetGlobe' }"
            @click="activeTab = 'TargetGlobe'"
          >
            Target Globe
          </button>
=======
          </RouterLink>

          <RouterLink to="/global-map" class="nav-link" active-class="active">
            <span class="nav-icon" aria-hidden="true"></span>
            Global Map
          </RouterLink>
>>>>>>> 79f50824fc0d7876796b89d0944b4fcdee71c365
        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <div class="page">
          <RouterView />
        </div>
<<<<<<< HEAD

        <div class="page" v-show="activeTab === 'Websites'">
          <WebsiteManager />
        </div>

        <!-- Correctly bounds state variables onto the standalone view layer components -->
        <div class="page" v-show="activeTab === 'TargetGlobe'">
          <div class="fullscreen-globe-wrapper">
            <Globe />
          </div>
        </div>

=======
>>>>>>> 79f50824fc0d7876796b89d0944b4fcdee71c365
      </div>
    </main>
  </div>
</template>

<style>
@import url('https://googleapis.com');

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
<<<<<<< HEAD
  width: 380px; 
=======
  width: 480px;
>>>>>>> 79f50824fc0d7876796b89d0944b4fcdee71c365
  flex-shrink: 0;
  gap: 20px;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-muted);
  padding: 8px 0;
  font-family: 'Inter';
  transition: .2s;
}

.nav-link.active {
  color: var(--primary);
  font-weight: 600;
  border-bottom: 2px solid var(--primary);
}

.nav-icon {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  opacity: 0.65;
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

.fullscreen-globe-wrapper :deep(.canvas-viewport) {
  height: 650px !important; 
  background: radial-gradient(circle at center, #111126 0%, #050512 100%) !important;
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
