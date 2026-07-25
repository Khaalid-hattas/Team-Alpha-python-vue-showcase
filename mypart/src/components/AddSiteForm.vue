<script setup>
import { ref } from 'vue'

const emit = defineEmits(['site-added'])

const siteName = ref('')
const siteUrl = ref('')
const category = ref('News')
const error = ref('')

function isValidUrl(string) {
  try { new URL(string); return true } 
  catch (_) { return false }
}

async function handleAdd() {
  error.value = ''
  if (!siteName.value.trim()) {
    error.value = 'Site name is required'
    return
  }
  if (!isValidUrl(siteUrl.value)) {
    error.value = 'Please enter a valid URL'
    return
  }

  const payload = { name: siteName.value, url: siteUrl.value, category: category.value }
  emit('site-added', payload)
  
  siteName.value = ''
  siteUrl.value = ''
  category.value = 'News'
}
</script>

<template>
  <div class="manager-card">
    <div class="card-header">
      <h3>Register a new source</h3>
      <p class="card-sub">GET / POST / api / websites</p>
    </div>

    <div class="form-row">
      <div class="input-group">
        <label class="field-label">Site Name</label>
        <input v-model="siteName" type="text" placeholder="e.g. Eyewitness News" class="figma-input" />
      </div>
      
      <div class="input-group-url">
        <label class="field-label">Target URL</label>
        <input v-model="siteUrl" type="url" placeholder="https://ewn.co.za" class="figma-input" />
      </div>
      
      <div class="input-group">
        <label class="field-label">Category</label>
        <input v-model="category" type="text" placeholder="News" class="figma-input" />
      </div>
      
      <div class="btn-group">
        <button @click="handleAdd" class="add-btn">Add Source</button>
      </div>
    </div>

    <p v-if="error" class="error-text">{{ error }}</p>
  </div>
</template>

<style scoped>
.manager-card { 
  background: #ffffff; 
  color: #0f172a;
  border-radius: 8px; 
  padding: 48px; /* Explicit structural layout match symmetry */
  border: 1px solid #e2e8f0; 
  width: 100%;
  box-sizing: border-box;
}

.card-header h3 { 
  font-size: 24px; 
  font-weight: 700; 
  color: #0f172a;
}

.card-sub { 
  font-size: 14px; 
  color: #64748b; 
  font-family: monospace;
  margin: 6px 0 36px 0; 
}

.form-row { 
  display: grid; 
  grid-template-columns: 1fr 2fr 1fr 160px; /* Standardize final fractional button width column */
  gap: 24px; 
  align-items: flex-end; 
  width: 100%;
}

.input-group, .input-group-url, .btn-group {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.field-label {
  font-size: 15px; 
  font-weight: 600;
  color: #334155;
  margin-bottom: 10px;
  line-height: 1;
}

.figma-input { 
  padding: 0 18px; 
  border: 1px solid #cbd5e1; 
  border-radius: 6px; 
  font-family: inherit;
  font-size: 15px; 
  background: #ffffff; 
  height: 52px; /* Matching pixel field framework line */
  width: 100%;
  box-sizing: border-box;
  transition: border-color 0.15s ease;
}

.figma-input:focus {
  outline: none;
  border-color: #0f172a;
}

.add-btn { 
  background-color: #0f172a; 
  color: #ffffff; 
  border: none; 
  font-family: inherit;
  font-size: 15px; 
  font-weight: 600; 
  border-radius: 6px; 
  cursor: pointer; 
  height: 52px; /* Perfect linear alignment matching structure */
  width: 100%; 
  white-space: nowrap; 
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  transition: background-color 0.15s ease;
}

.add-btn:hover {
  background-color: #1e293b;
}

.error-text { 
  color: #dc2626; 
  font-size: 13px; 
  margin-top: 14px; 
  font-weight: 500;
}

@media (max-width: 1024px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
