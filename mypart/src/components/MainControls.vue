<script setup>
import { ref } from 'vue'

const query = ref('')
const activeCategory = ref('All')
const loading = ref(false)

const filters = ['All', 'Politics', 'World', 'Local', 'Sport', 'Business']

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
      
      <header class="console-header">
        <div class="brand-group">
          <h1>EWN Console</h1>
          <p class="subtitle">SCRAPING ANALYTICS PLATFORM</p>
        </div>
      </header>

      <div class="controls-toolbar">
        <div class="left-controls">
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
        
        <div class="right-controls">
          <div class="search-container">
            <input 
              v-model="query"
              type="text" 
              placeholder="Search headlines, authors, topics..." 
              class="figma-search"
            />
            <span class="status-indicator"></span>
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

.console-header {
  padding: 20px 0 10px 0;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 15px;
}

.brand-group h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.brand-group .subtitle {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: #757575;
  margin: 2px 0 0 0;
}

.controls-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  gap: 20px;
}

.right-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pills-row {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.pills-row button {
  background-color: #f1f3f4;
  color: #5f6368;
  border: 1px solid transparent;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.pills-row button:hover {
  background-color: #e8eaed;
}

.pills-row button.active-pill {
  background-color: #1a73e8;
  color: #ffffff;
  font-weight: 600;
}

.search-container {
  position: relative;
  display: inline-block;
}

.figma-search {
  width: 240px;
  padding: 8px 32px 8px 12px;
  font-size: 12px;
  border: 1px solid #dadce0;
  border-radius: 4px;
  color: #3c4043;
  background-color: #ffffff;
  box-sizing: border-box;
}

.figma-search:focus {
  outline: none;
  border-color: #1a73e8;
}

.status-indicator {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background-color: #00e676;
  border-radius: 50%;
}

.scrape-action-btn {
  background-color: #1b1464;
  color: #ffffff;
  border: none;
  padding: 8px 16px;
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

@media (max-width: 900px) {
  .controls-toolbar {
    flex-direction: column;
    align-items: flex-start;
  }
  .right-controls {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
