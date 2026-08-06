<script setup>
import { ref, inject, computed } from "vue";
import DataDisplay from "./DataDisplay.vue";
import { runScrape, getItems } from "@/services/api";

const query = ref("");
const activeFilter = ref("All");
const loading = ref(false);

const filters = ["All", "Politics", "World", "Local", "Sport", "Business"];

const globalSources = inject("globalSources");
const globalArticles = inject("globalArticles");
const selectedSourceName = inject("selectedSourceName", ref(""));
const clearSelectedSourceName = inject("clearSelectedSourceName", () => {});

const globalStats = computed(() => {
  const counts = {};

  globalArticles.value.forEach((article) => {
    counts[article.category] = (counts[article.category] || 0) + 1;
  });

  return {
    top_categories: Object.entries(counts).map(([name, count]) => ({
      name,
      count,
    })),
  };
});

const filteredArticles = computed(() => {
  let articles = globalArticles.value;

  if (selectedSourceName.value) {
    articles = articles.filter(
      (article) => article.sourceName === selectedSourceName.value,
    );
  }

  if (activeFilter.value !== "All") {
    articles = articles.filter(
      (article) =>
        article.category.toLowerCase() === activeFilter.value.toLowerCase(),
    );
  }

  if (query.value.trim()) {
    const search = query.value.toLowerCase();

    articles = articles.filter(
      (article) =>
        article.title.toLowerCase().includes(search) ||
        article.description.toLowerCase().includes(search) ||
        article.sourceName.toLowerCase().includes(search),
    );
  }

  return articles;
});

async function handleScrape() {
  loading.value = true;

  const timestamp = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  const activeSources = globalSources.value.filter((s) => s.isActive);

  try {
    // Kick off a fresh scrape on the backend, then pull the stored items.
    await runScrape();
    const res = await getItems(1);
    const items = res.data?.items || [];

    globalArticles.value = items.map((item, index) => ({
      id: `${item.source}-${index}-${item.scraped_at || Date.now()}`,
      title: item.title,
      link: item.url || "#",
      description: (item.description || item.summary || "")
        .replace(/<[^>]*>/g, "")
        .substring(0, 180) + "...",
      sourceName: item.source,
      category: item.category || "General",
    }));

    activeSources.forEach((source) => {
      source.lastScrape = `Success: ${timestamp}`;
    });
  } catch (error) {
    console.error("Scrape failed:", error);
    activeSources.forEach((source) => {
      source.lastScrape = "Failed";
    });
  }

  loading.value = false;
}
</script>
<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <div>
        <h1>Dashboard Overview</h1>
        <p class="muted">Real-time asynchronous news parsing engine</p>
      </div>

      <button class="btn-primary" @click="handleScrape" :disabled="loading">
        {{ loading ? "Running Extraction..." : "Run Scrape Job" }}
      </button>
    </div>

    <div class="guide-card">
      <div class="guide-step">
        <strong>1.</strong> Select the sources you want to scrape from the Websites page.
      </div>
      <div class="guide-step">
        <strong>2.</strong> Return to Dashboard and click <em>Run Scrape Job</em>.
      </div>
      <div class="guide-step">
        <strong>3.</strong> Wait a few seconds while the scraper collects the latest headlines.
      </div>
      <div class="guide-tip">Tip: use filters or search to narrow results after the scrape finishes.</div>
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
          {{ globalSources.filter((s) => s.isActive).length }}/{{
            globalSources.length
          }}
        </div>
      </div>
    </div>

    <DataDisplay :stats="globalStats" />

    <div class="card filter-card">
      <div v-if="selectedSourceName" class="selection-banner">
        <div>
          <strong>Map filter active:</strong>
          <span>{{ selectedSourceName }}</span>
        </div>

        <button class="clear-filter-btn" @click="clearSelectedSourceName()">
          Show all sources
        </button>
      </div>

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
          Aggregated Articles Output Feed ({{ filteredArticles.length }} entries
          found)
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

        <div v-if="filteredArticles.length === 0 && !loading" class="empty">
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
  font-family: "Inter", sans-serif;
}

.btn-primary:hover:not(:disabled) {
  background: #130d43;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.guide-card {
  padding: 18px 22px;
  background: white;
  border: 1px solid rgba(33, 33, 97, 0.08);
  border-radius: 14px;
  display: grid;
  gap: 10px;
}

.guide-step {
  display: flex;
  gap: 10px;
  color: var(--text);
  font-size: 14px;
}

.guide-tip {
  margin-top: 10px;
  font-size: 13px;
  color: var(--text-muted);
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

.selection-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 12px 14px;
  border-radius: 8px;
  background: #eef4ff;
  border: 1px solid #d6e4ff;
  color: var(--text);
}

.selection-banner strong {
  margin-right: 6px;
}

.selection-banner span {
  color: var(--primary);
  font-weight: 600;
}

.clear-filter-btn {
  background: white;
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 6px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
}

.clear-filter-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
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
  font-family: "Inter", sans-serif;
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
  font-family: "Inter", sans-serif;
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