<script setup>
import { inject } from 'vue'
import AddSiteForm from './AddSiteForm.vue'
import { AVAILABILITY_NOTE } from '../constants/sources'

const sources = inject('globalSources')
const globalArticles = inject('globalArticles')

const availabilityNote = AVAILABILITY_NOTE

function handleSiteAdded(newSite) {
  sources.value.push({
    id: Date.now(),
    name: newSite.name,
    url: newSite.url,
    category: newSite.category || 'Local',
    lastScrape: 'Never Scraped',
    isActive: true
  })
}

function removeSource(id) {
  sources.value = sources.value.filter(s => s.id !== id)
  globalArticles.value = []
}
</script>

<template>
  <div class="websites-page">
    <div class="page-header">
      <h1>Website Manager</h1>
      <p>Add, Monitor and Remove Scraping Targets</p>
    </div>

    <AddSiteForm :existing-names="sources.map(s => s.name)" @site-added="handleSiteAdded" />

        <div class="card">
          <div class="card-header">
            <h2>Registered Target Pipelines</h2>
          </div>

          <div v-if="availabilityNote" class="availability-note">
            {{ availabilityNote }}
          </div>

      <div class="table-wrapper">
        <table class="table">
          <thead>
            <tr>
              <th>STATUS</th>
              <th>PIPELINE NAME</th>
              <th>FEED ENDPOINT XML URL</th>
              <th>MAPPED CATEGORY</th>
              <th>LAST EXTRACTION RUN</th>
              <th>ACTIONS</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="source in sources"
              :key="source.id"
            >
              <td>
                <span class="badge-active">Active</span>
              </td>

              <td class="bold">
                {{ source.name }}
              </td>

              <td>
                <code class="url">{{ source.url }}</code>
              </td>

              <td>
                <span class="badge-category">
                  {{ source.category }}
                </span>
              </td>

              <td class="muted">
                {{ source.lastScrape }}
              </td>

              <td>
                <button
                  class="btn-remove"
                  @click="removeSource(source.id)"
                >
                  Remove
                </button>
              </td>
            </tr>

            <tr v-if="sources.length === 0">
              <td colspan="6" class="empty">
                No pipelines registered yet. Use the form above.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.websites-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.page-header p {
  color: var(--text-muted);
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.card-header h2 {
  font-size: 16px;
  font-weight: 600;
}

.availability-note {
  padding: 12px 24px;
  font-size: 13px;
  color: #7a5b00;
  background: #fff8e1;
  border-bottom: 1px solid var(--border);
}

.table-wrapper {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  min-width: 900px;
}

.table th {
  text-align: left;
  padding: 12px 24px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  background: #f8f9fa;
  text-transform: uppercase;
}

.table td {
  padding: 16px 24px;
  border-top: 1px solid var(--border);
}

.bold {
  font-weight: 600;
}

.muted {
  color: var(--text-muted);
}

.url {
  background: #f1f3f4;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
}

.badge-active {
  background: #e6f4ea;
  color: #137333;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid #ceead6;
}

.badge-category {
  background: #e8f0fe;
  color: var(--primary);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.btn-remove {
  background: #fff;
  color: #d93025;
  border: 1px solid #fbc4c4;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.15s;
}

.btn-remove:hover {
  background: #fce8e6;
}

.empty {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}
</style>
