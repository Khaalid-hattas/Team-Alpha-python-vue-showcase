<script setup>
import { computed, inject } from 'vue'

const globalSources = inject('globalSources', { value: [] })
const globalArticles = inject('globalArticles', { value: [] })

const props = defineProps({
  sourceHealth: {
    type: Array,
    default: () => [],
  },
  averageSuccessRate: {
    type: Number,
    default: 0,
  },
  lastRefresh: {
    type: String,
    default: '',
  },
  lastDurationSeconds: {
    type: Number,
    default: 0,
  },
})

const activeSources = computed(() => globalSources.value.filter((source) => source.isActive).length)
const sourceHealth = computed(() => props.sourceHealth ?? [])
const sourceCoverage = computed(() => {
  if (globalSources.value.length === 0) {
    return '0%'
  }

  const ratio = (activeSources.value / globalSources.value.length) * 100
  return `${Math.round(ratio)}%`
})

const totalSuccessRate = computed(() => `${props.averageSuccessRate}%`)
</script>

<template>
  <section class="stats-shell">
    <div class="stats-grid">
      <article class="card stat-card">
        <span class="stat-label">Total Sources</span>
        <strong class="stat-value">{{ globalSources.length }}</strong>
      </article>

      <article class="card stat-card">
        <span class="stat-label">Active Sources</span>
        <strong class="stat-value">{{ activeSources }}</strong>
      </article>

      <article class="card stat-card">
        <span class="stat-label">Mapped Articles</span>
        <strong class="stat-value">{{ globalArticles.length }}</strong>
      </article>

      <article class="card stat-card">
        <span class="stat-label">Average Success Rate</span>
        <strong class="stat-value">{{ totalSuccessRate }}</strong>
      </article>
    </div>

    <div class="card health-strip">
      <div class="health-header">
        <div>
          <h3>Live source health</h3>
          <p>
            Last refresh {{ lastRefresh || 'not yet available' }}
            <span v-if="lastDurationSeconds">· {{ lastDurationSeconds.toFixed(2) }}s</span>
          </p>
        </div>
      </div>

      <div class="health-grid">
        <article
          v-for="source in sourceHealth"
          :key="source.source_name"
          class="health-card"
          :class="source.status"
        >
          <div class="health-card-head">
            <strong>{{ source.display_name }}</strong>
            <span class="health-pill">{{ source.success_rate }}%</span>
          </div>

          <p>{{ source.city }}, {{ source.country }}</p>
          <small>
            {{ source.last_status }} · {{ source.last_articles }} articles · {{ source.attempts }} checks
          </small>
        </article>
      </div>

      <p
        v-if="sourceHealth.length === 0"
        class="empty-msg"
      >
        No live source statistics available yet.
      </p>
    </div>
  </section>
</template>

<style scoped>
.stats-shell {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.stat-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.stat-value {
  color: var(--text);
  font-size: 24px;
  font-weight: 700;
}

.health-strip {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 18px;
}

.health-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.health-header p,
.health-card p,
.health-card small {
  color: var(--text-muted);
}

.health-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.health-card {
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
  background: #fdfefe;
}

.health-card.green {
  border-color: #ceead6;
  background: #f3fbf4;
}

.health-card.red {
  border-color: #f9c5bf;
  background: #fff5f4;
}

.health-card-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 8px;
}

.health-pill {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
  background: #e8f0fe;
  border: 1px solid #d2e3fc;
  border-radius: 999px;
  padding: 4px 8px;
  white-space: nowrap;
}

.empty-msg {
  margin-top: 12px;
  color: var(--text-muted);
}

@media (max-width: 1100px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .health-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .health-grid {
    grid-template-columns: 1fr;
  }
}
</style>
