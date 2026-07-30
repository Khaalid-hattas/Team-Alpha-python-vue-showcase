<script setup>
import { ref } from 'vue'

const emit = defineEmits(['site-added'])

const siteName = ref('')
const siteUrl = ref('')
const category = ref('Local')

function handleAdd() {
  if (!siteName.value.trim() || !siteUrl.value.trim()) return

  let url = siteUrl.value.trim()

  // Automatically add https:// if the user doesn't type it
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = `https://${url}`
  }

  emit('site-added', {
    name: siteName.value.trim(),
    url,
    category: category.value
  })

  siteName.value = ''
  siteUrl.value = ''
  category.value = 'Local'
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <h2>Register Pipeline Feed Stream</h2>
      <p class="subtitle">
        Connect automated targets via remote XML/RSS protocols
      </p>
    </div>

    <form @submit.prevent="handleAdd" class="form">
      <div class="field">
        <label>Stream Reference Name</label>
        <input
          v-model="siteName"
          type="text"
          placeholder="e.g. BBC World News"
          required
        />
      </div>

      <div class="field">
        <label>Remote Target RSS URL Link</label>
        <input
          v-model="siteUrl"
          type="text"
          placeholder="https://feeds.bbci.co.uk/news/rss.xml"
          required
        />
      </div>

      <div class="field">
        <label>Category Mapped Tag</label>

        <select v-model="category">
          <option>Local</option>
          <option>Politics</option>
          <option>World</option>
          <option>Sport</option>
          <option>Business</option>
        </select>
      </div>

      <div class="field button-field">
        <button type="submit" class="btn-primary">
          Add Pipeline Stream
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.card-header {
  padding: 24px;
  padding-bottom: 0;
}

.card-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.subtitle {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.form {
  padding: 0 24px 24px;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr auto;
  gap: 20px;
  align-items: end;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

.field input,
.field select {
  width: 100%;
  height: 46px;
  padding: 0 14px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 15px;
  font-family: 'Inter', sans-serif;
  background: #fff;
  transition: border-color 0.2s ease;
}

.field input:focus,
.field select:focus {
  outline: none;
  border-color: var(--primary);
}

.button-field {
  justify-content: flex-end;
}

.btn-primary {
  height: 46px;
  padding: 0 24px;
  background: #1b1464;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  transition: background 0.2s ease;
}

.btn-primary:hover {
  background: #130d43;
}

@media (max-width: 1100px) {
  .form {
    grid-template-columns: 1fr;
  }

  .button-field {
    justify-content: stretch;
  }

  .btn-primary {
    width: 100%;
  }
}
</style>