<script setup>
import { ref } from 'vue'

const query = ref('')
const activeCategory = ref('All')
const loading = ref(false)
const filters = ['All', 'Politics', 'World', 'Local', 'Sport', 'Business']

function handleScrape() {
  if (loading.value) return
  loading.value = true
  setTimeout(() => { loading.value = false }, 2500)
}
</script>

<template>
  <div class="dashboard-controls-wrapper">
    <!-- Main Command Card Module -->
    <div class="dashboard-card">
      
      <!-- Top Row: Structured Search Box and Trigger Action Button -->
      <div class="search-action-row">
        <div class="search-field-box">
          <svg class="search-lens-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input v-model="query" type="text" placeholder="Search global data feeds..." class="figma-search" />
        </div>
        
        <button :disabled="loading" @click="handleScrape" class="scrape-action-btn">
          {{ loading ? 'Running Pipeline...' : 'Run Scrape Job' }}
        </button>
      </div>

      <!-- Bottom Row: Sleek Segmented Category Navigation Underline Tabs -->
      <div class="filter-navigation-tabs">
        <button 
          v-for="item in filters" 
          :key="item"
          :class="{ 'active-tab-pill': activeCategory === item }"
          @click="activeCategory = item"
        >
          {{ item }}
        </button>
      </div>

    </div>

    <!-- 
      TEAMMATE RESERVED WORKSPACE BUFFER
      This dedicated section remains open. Your teammate can drop their data tables, 
      analytics components, or graphs here, and they will stack cleanly.
    -->
    <div class="teammate-workspace-zone">
      <!-- Your teammate's code will automatically sit right here -->
    </div>
  </div>
</template>

<style scoped>
.dashboard-controls-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 32px; /* Leaves a professional spatial gap above your teammate's upcoming component entries */
}

.dashboard-card {
  background-color: #ffffff;
  color: #0f172a;
  padding: 40px; /* Matching structural symmetry padding measurements */
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 32px; /* Distinctly separates the input elements row from the filter tabs line */
}

/* Wide Command Row: Spans fully across the page bounds layout */
.search-action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.search-field-box {
  position: relative;
  flex-grow: 1; /* Maximizes horizontal search display focus area space naturally */
  display: flex;
  align-items: center;
}

/* Subtle clean vector search glass emblem placement icon inside the text input box */
.search-lens-icon {
  position: absolute;
  left: 18px;
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
}

.figma-search {
  width: 100%; 
  padding: 0 18px 0 48px; /* Offset padding avoids writing text over the search magnifying glass */
  font-family: inherit;
  font-size: 15px;
  border: 1px solid #cbd5e1; 
  border-radius: 6px; 
  background-color: #ffffff;
  color: #0f172a;
  height: 52px; /* Locked alignment baseline heights */
  box-sizing: border-box;
  transition: all 0.15s ease;
}

.figma-search:focus {
  outline: none;
  border-color: #0f172a;
  box-shadow: 0 0 0 1px #0f172a;
}

.scrape-action-btn {
  background-color: #0f172a; 
  color: #ffffff; 
  border: none;
  font-family: inherit;
  padding: 0 32px; 
  font-size: 15px; 
  font-weight: 600; 
  border-radius: 6px; 
  cursor: pointer;
  height: 52px; 
  white-space: nowrap; 
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  flex-shrink: 0;
  transition: background-color 0.15s ease;
}

.scrape-action-btn:hover:not(:disabled) {
  background-color: #1e293b;
}

.scrape-action-btn:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

/* Rebuilt Filter Navigation: Clean enterprise underline alignment strip style */
.filter-navigation-tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid #e2e8f0; /* Soft anchoring baseline divider rule */
  width: 100%;
}

.filter-navigation-tabs button {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  padding: 12px 20px;
  cursor: pointer;
  position: relative;
  transition: color 0.15s ease;
}

.filter-navigation-tabs button:hover {
  color: #0f172a;
}

/* Premium Highlight State: Adds a clean base indicator tab bar matching standard professional SaaS products */
.filter-navigation-tabs button.active-tab-pill {
  color: #0f172a;
  font-weight: 700;
}

.filter-navigation-tabs button.active-tab-pill::after {
  content: '';
  position: absolute;
  bottom: -1px; /* Overlaps perfectly on top of the border tracking layout rule line */
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #0f172a;
}

/* Explicitly empty layout container layer blocks out space cleanly below your part */
.teammate-workspace-zone {
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
