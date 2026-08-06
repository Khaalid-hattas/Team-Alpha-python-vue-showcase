<script setup>
import { ref, provide } from 'vue'
import { SUPPORTED_SOURCES } from './constants/sources'

const mobileMenuOpen = ref(false)
const globalStats = ref({
  top_categories: []
})

// Sources start empty — the user picks from the dropdown in AddSiteForm
// to add the supported source. Once added, it's marked active and locked
// (non-removable) since it's the app's only supported source.
const sourcesList = ref([])

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

        <button
          class="nav-toggle"
          @click="mobileMenuOpen = !mobileMenuOpen"
          :aria-expanded="mobileMenuOpen"
          aria-label="Toggle navigation"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <nav class="nav" :class="{ open: mobileMenuOpen }">
          <RouterLink
            to="/"
            class="nav-link"
            active-class="active"
            exact-active-class="active"
            @click="mobileMenuOpen = false"
          >
            <span class="nav-icon" aria-hidden="true"></span>
            Dashboard
          </RouterLink>

          <RouterLink
            to="/websites"
            class="nav-link"
            active-class="active"
            @click="mobileMenuOpen = false"
          >
            <span class="nav-icon" aria-hidden="true"></span>
            Websites
          </RouterLink>

          <RouterLink
            to="/global-map"
            class="nav-link"
            active-class="active"
            @click="mobileMenuOpen = false"
          >
            <span class="nav-icon" aria-hidden="true"></span>
            Global Map
          </RouterLink>

        </nav>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <div class="page">
          <RouterView />
        </div>
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
  width: 480px;
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

.nav-toggle {
  display: none;
  width: 38px;
  height: 38px;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: transparent;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 6px;
}

.nav-toggle span {
  display: block;
  width: 20px;
  height: 2px;
  border-radius: 2px;
  background: var(--text);
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.nav.open {
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--bg);
  padding: 18px 32px 22px;
  border-bottom: 1px solid var(--border);
}

.main {
  width: 100%;
  padding: 28px 0;
}

@media (max-width: 960px) {
  .header-inner {
    padding: 0 18px;
    flex-wrap: wrap;
    gap: 14px;
  }

  .brand {
    width: auto;
  }

  .nav-toggle {
    display: flex;
  }

  .nav {
    display: none;
    width: 100%;
  }

  .nav.open {
    display: flex;
  }

  .nav-link {
    width: 100%;
    padding: 10px 0;
  }

  .nav-link.active {
    border-bottom: none;
    background: rgba(27, 20, 100, 0.05);
    border-radius: 8px;
    padding-left: 10px;
  }
}

@media (max-width: 640px) {
  .header-inner {
    padding: 0 14px;
  }

  .nav.open {
    padding: 16px;
  }

  .nav-link {
    font-size: 13px;
  }
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