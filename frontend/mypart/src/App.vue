<script>
import MainControls from './components/MainControls.vue'
import DataDisplay from './components/DataDisplay.vue'
import api from './services/api.js';

export default {
  components: { MainControls, DataDisplay },
  data() {
    return {
      stats: {
        top_categories: []
      }
    }
  },
  async mounted() {
    const res = await api.getStats()
    this.stats = res.data
  }
}
</script>

<template>
  <MainControls />
  <DataDisplay :stats="stats"/>
</template>

<style>
/* This bypasses the default template margins and fills the whole screen */
#app {
  max-width: 100% !important;
  width: 100vw !important;
  margin: 0 !important;
  padding: 0 !important;
  display: block !important;
}

body {
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
  font-family: system-ui, sans-serif;
}
</style>
