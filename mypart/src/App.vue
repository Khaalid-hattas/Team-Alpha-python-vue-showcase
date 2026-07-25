<script setup>
import { ref } from 'vue'
import MainControls from './components/MainControls.vue'
import WebsiteManager from './components/WebsiteManager.vue'

const activeTab = ref('Dashboard')
</script>

<template>
  <div class="app-wrapper">
    <header class="global-header">
      <div class="header-inner">
        <h1 class="brand">SCRAPING ANALYTICS<br/>PLATFORM</h1>
        
        <nav class="top-nav">
          <button 
            :class="{ 'active-nav': activeTab === 'Dashboard' }" 
            @click="activeTab = 'Dashboard'"
          >
            Dashboard
          </button>
          <button 
            :class="{ 'active-nav': activeTab === 'Websites' }" 
            @click="activeTab = 'Websites'"
          >
            Websites
          </button>
        </nav>
      </div>
    </header>

    <main class="dashboard-frame">
      <div class="content-container">
        <Transition name="page-fade" mode="out-in">
          <MainControls v-if="activeTab === 'Dashboard'" />
          <WebsiteManager v-else-if="activeTab === 'Websites'" />
        </Transition>
      </div>
    </main>
  </div>
</template>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, #app {
  height: 100%;
  width: 100%;
}

body {
  /* Removed the dark background completely. Replaced with an off-white canvas layout background */
  background-color: #f8fafc; 
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  color: #0f172a;
  -webkit-font-smoothing: antialiased;
}

.app-wrapper { 
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.global-header {
  background: #ffffff; 
  color: #0f172a;
  width: 100%;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
  border-bottom: 1px solid #e2e8f0;
}

.header-inner {
  width: 100%;
  max-width: 95%; /* Expanded screen area width to mirror EWN's wide navbar format */
  padding: 24px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.5px;
  line-height: 1.2;
  color: #0f172a;
}

.top-nav { display: flex; gap: 40px; }

.top-nav button {
  background: none;
  border: none;
  font-family: inherit;
  font-size: 16px; /* Scaled up for natural readability */
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  padding: 6px 0;
  transition: color 0.15s ease;
}

.top-nav button:hover {
  color: #0f172a;
}

.top-nav button.active-nav {
  color: #0f172a;
  border-bottom: 3px solid #0f172a; /* Solid clean tracking line */
}

.dashboard-frame {
  width: 100%;
  padding: 40px 0;
  display: flex;
  justify-content: center;
}

.content-container {
  width: 100%;
  max-width: 95%; /* Expanded to allow cards to fill screen real estate naturally */
  display: flex;
  flex-direction: column;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.15s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}
</style>
