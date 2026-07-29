<script setup>
import { ref, inject, computed } from 'vue'
import DataDisplay from './DataDisplay.vue'

const query = ref('')
const activeFilter = ref('All')
const loading = ref(false)

const filters = [
  'All',
  'Politics',
  'World',
  'Local',
  'Sport',
  'Business'
]

const globalSources = inject('globalSources')
const globalArticles = inject('globalArticles')

const globalStats = computed(() => {
  const counts = {}

  globalArticles.value.forEach(article => {
    counts[article.category] = (counts[article.category] || 0) + 1
  })

  return {
    top_categories: Object.entries(counts).map(([name, count]) => ({
      name,
      count
    }))
  }
})

async function fetchRSS(url) {
  const proxy1 = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(url)}`

  try {
    const res = await fetch(proxy1)
    const data = await res.json()

    if (data.status === 'ok') {
      return data.items
    }

    throw new Error(data.message)
  } catch (e) {
    console.warn('rss2json failed, trying backup')

    const proxy2 = `https://api.allorigins.win/get?url=${encodeURIComponent(url)}`

    const res2 = await fetch(proxy2)
    const data2 = await res2.json()

    const parser = new DOMParser()

    const xml = parser.parseFromString(
      data2.contents,
      'text/xml'
    )

    return Array.from(xml.querySelectorAll('item')).map(item => ({
      title: item.querySelector('title')?.textContent || '',
      link: item.querySelector('link')?.textContent || '#',
      description:
        item.querySelector('description')?.textContent || ''
    }))
  }
}

const filteredArticles = computed(() => {
  let articles = globalArticles.value

  if (activeFilter.value !== 'All') {
    articles = articles.filter(
      article =>
        article.category.toLowerCase() ===
        activeFilter.value.toLowerCase()
    )
  }

  if (query.value.trim()) {
    const search = query.value.toLowerCase()

    articles = articles.filter(article =>
      article.title.toLowerCase().includes(search) ||
      article.description.toLowerCase().includes(search) ||
      article.sourceName.toLowerCase().includes(search)
    )
  }

  return articles
})

async function handleScrape() {
  loading.value = true
  globalArticles.value = []

  const timestamp = new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  })
    for (const source of globalSources.value.filter(s => s.isActive)) {
    try {
      const items = await fetchRSS(source.url)

      items.slice(0, 15).forEach((item, index) => {
        globalArticles.value.push({
          id: `${source.id}-${index}-${Date.now()}`,
          title: item.title,
          link: item.link,
          description:
            (item.description || '')
              .replace(/<[^>]*>/g, '')
              .substring(0, 200) + '...',
          sourceName: source.name,
          category: source.category
        })
      })

      source.lastScrape = `Success: ${timestamp}`
    } catch (error) {
      console.error(error)
      source.lastScrape = 'Failed'
    }
  }

  loading.value = false
}
</script>

<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <div>
        <h1>Dashboard Overview</h1>
        <p class="muted">
          Real-time asynchronous news parsing engine
        </p>
      </div>

      <button
        class="btn-primary"
        @click="handleScrape"
        :disabled="loading"
      >
        {{ loading ? 'Running Extraction...' : 'Run Scrape Job' }}
      </button>
    </div>

    <div class="stats-grid">
      <div class="card stat">
        <div class="stat-label">Total Items Fetched</div>
        <div class="stat-value">{{ globalArticles.length }}</div>
      </div>

      <div class="card stat">
        <div class="stat-label">Showing</div>
        <div class="stat-value">{{ filteredArticles.length }}</div>
      </div>

      <div class="card stat">
        <div class="stat-label">Active Sources</div>
        <div class="stat-value">
          {{ globalSources.filter(s => s.isActive).length }}/{{ globalSources.length }}
        </div>
      </div>
    </div>

    <DataDisplay :stats="globalStats" />

    <div class="card filter-card">
      <div class="search-row">
        <input
          v-model="query"
          class="search-input"
          type="text"
          placeholder="Search headlines, sources..."
        />
      </div>

      <div class="filter-pills">
        <button
          v-for="filter in filters"
          :key="filter"
          class="filter-btn"
          :class="{ active: activeFilter === filter }"
          @click="activeFilter = filter"
        >
          {{ filter }}
        </button>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <h2>
          Aggregated Articles Output Feed
          ({{ filteredArticles.length }} entries found)
        </h2>
      </div>

      <div class="articles">
                <a
          v-for="article in filteredArticles"
          :key="article.id"
          :href="article.link"
          target="_blank"
          class="article-card"
        >
          <div class="article-meta">
            <span class="source">{{ article.sourceName }}</span>
            <span class="cat">{{ article.category }}</span>
          </div>

          <h3>{{ article.title }}</h3>

          <p>{{ article.description }}</p>
        </a>

        <div
          v-if="filteredArticles.length === 0 && !loading"
          class="empty"
        >
          No articles match your filters. Click "Run Scrape Job".
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-header h1 {
  font-size: 24px;
  font-weight: 700;
}

.muted {
  color: var(--text-muted);
}

.btn-primary {
  height: 40px;
  padding: 0 24px;
  background: #1b1464;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
}

.btn-primary:hover:not(:disabled) {
  background: #130d43;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat {
  padding: 24px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-muted);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  margin-top: 8px;
}

.filter-card {
  padding: 20px 24px;
}

.search-row {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}

.search-input:focus {
  outline: none;
  border-color: #1b1464;
}

.filter-pills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-btn {
  background: #f1f3f4;
  border: 1px solid var(--border);
  color: var(--text);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  transition: all 0.15s ease;
}

.filter-btn:hover {
  background: #e8eaed;
}

.filter-btn.active {
  background: #1b1464;
  color: white;
  border-color: #1b1464;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.card-header h2 {
  font-size: 16px;
  font-weight: 600;
}

.articles {
  padding: 16px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 16px;
}

.article-card {
  display: block;
  padding: 20px;
  border: 1px solid var(--border);
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.15s ease;
}

.article-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-color: #c4c7c5;
}

.article-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.source,
.cat {
  background: #f1f3f4;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.article-card h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
  line-height: 1.4;
}

.article-card p {
  font-size: 14px;
  color: var(--text-muted);
  line-height: 1.5;
}

.empty {
  padding: 60px;
  text-align: center;
  color: var(--text-muted);
}
</style>