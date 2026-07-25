<script setup>
import AddSiteForm from './AddSiteForm.vue'

function handleSiteAdded(newSite) {
  console.log('Site successfully captured by form component:', newSite)
}
</script>

<template>
  <div class="website-manager">
    <div class="form-focus-container">
      <AddSiteForm @site-added="handleSiteAdded" />
    </div>
  </div>
</template>

<style scoped>
.website-manager { 
  width: 100%; 
  height: 100%; 
  display: flex;
  flex-direction: column;
}

.form-focus-container {
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
