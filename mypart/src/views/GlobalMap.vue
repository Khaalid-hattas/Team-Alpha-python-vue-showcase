<script setup>
import { computed, inject, onBeforeUnmount, onMounted, ref } from "vue";
import Globe from "../components/global-map/Globe.vue";
import Legend from "../components/global-map/Legend.vue";
import StatisticsCards from "../components/global-map/StatisticsCards.vue";

const selectedSourceName = inject("selectedSourceName", ref(""));
const setSelectedSourceName = inject("setSelectedSourceName", () => {});
const clearSelectedSourceName = inject("clearSelectedSourceName", () => {});

const statistics = ref({
  running: false,
  interval_minutes: 0,
  stored_articles: 0,
  source_health: [],
  last_refresh: null,
  last_duration_seconds: null,
});
const loading = ref(false);
const errorMessage = ref("");

const fallbackNodes = [
  {
    source_name: "EWN",
    display_name: "EWN News",
    city: "Johannesburg",
    country: "South Africa",
    lat: -26.2041,
    lng: 28.0473,
    success_rate: 0,
    last_status: "unknown",
    status: "red",
  },
  {
    source_name: "News24",
    display_name: "News24",
    city: "Cape Town",
    country: "South Africa",
    lat: -33.9249,
    lng: 18.4241,
    success_rate: 0,
    last_status: "unknown",
    status: "red",
  },
  {
    source_name: "SABC News",
    display_name: "SABC News",
    city: "Johannesburg",
    country: "South Africa",
    lat: -26.2041,
    lng: 28.0473,
    success_rate: 0,
    last_status: "unknown",
    status: "red",
  },
];

const sourceHealth = computed(() => statistics.value.source_health || []);

const nodes = computed(() => {
  const bySource = new Map(
    sourceHealth.value.map((item) => [item.source_name, item]),
  );

  return fallbackNodes.map((node) => {
    const live = bySource.get(node.source_name);

    if (!live) {
      return node;
    }

    return {
      ...node,
      ...live,
    };
  });
});

const averageSuccessRate = computed(() => {
  if (sourceHealth.value.length === 0) {
    return 0;
  }

  const total = sourceHealth.value.reduce(
    (sum, item) => sum + (item.success_rate || 0),
    0,
  );
  return Math.round(total / sourceHealth.value.length);
});

async function loadStatistics() {
  loading.value = true;
  errorMessage.value = "";

  try {
    const response = await fetch("/api/statistics");
    if (!response.ok) {
      throw new Error(`Statistics request failed with ${response.status}`);
    }

    const data = await response.json();

    console.log("API data:", data);
    console.log("Source health length:", data.source_health?.length);

    statistics.value = {
      running: data.running ?? false,
      interval_minutes: data.interval_minutes ?? 0,
      stored_articles: data.stored_articles ?? 0,
      source_health: data.source_health ?? [],
      last_refresh: data.last_refresh ?? null,
      last_duration_seconds: data.last_duration_seconds ?? null,
    };
  } catch (error) {
    errorMessage.value =
      "Live API statistics are unavailable. The globe is using fallback source positions.";
    console.error(error);
  } finally {
    loading.value = false;
  }
}

function handleSelectSource(node) {
  setSelectedSourceName(node.source_name);
}

function handleClearSelection() {
  clearSelectedSourceName();
}

let refreshTimer;

onMounted(() => {
  loadStatistics();
  refreshTimer = window.setInterval(loadStatistics, 30000);
});

onBeforeUnmount(() => {
  if (refreshTimer) {
    window.clearInterval(refreshTimer);
  }
});
</script>

<template>
  <section class="global-map-page">
    <header class="page-header">
      <div>
        <p class="breadcrumb">Dashboard / Global Map</p>
        <h1>Global Map</h1>
        <p class="subtitle">
          Interactive 3D target globe showing where EWN News, News24, and SABC
          News operate.
        </p>
      </div>

      <div class="header-actions">
        <span
          class="refresh-state"
          :class="{
            loading,
            online: !loading && statistics.running,
            offline: !loading && !statistics.running,
          }"
        >
          {{
            loading
              ? "Refreshing..."
              : statistics.running
                ? "Scheduler Running"
                : "Scheduler Offline"
          }}
        </span>

        <button
          v-if="selectedSourceName"
          class="header-btn"
          @click="handleClearSelection"
        >
          Clear filter
        </button>
      </div>
    </header>

    <div v-if="selectedSourceName" class="selection-banner">
      Dashboard table is filtered by <strong>{{ selectedSourceName }}</strong
      >. Click another node or clear the filter to reset.
    </div>

    <div v-if="errorMessage" class="error-banner">
      {{ errorMessage }}
    </div>

    <div class="content-grid">
      <Globe
        :nodes="nodes"
        :selected-source-name="selectedSourceName"
        @select="handleSelectSource"
      />
      <Legend :nodes="nodes" />
    </div>

    <StatisticsCards
      :source-health="sourceHealth"
      :average-success-rate="averageSuccessRate"
      :last-refresh="statistics.last_refresh"
      :last-duration-seconds="statistics.last_duration_seconds"
      :stored-articles="statistics.stored_articles"
      :total-sources="sourceHealth.length"
      :active-sources="
        sourceHealth.filter((s) => s.last_status === 'success').length
      "
    />
  </section>
</template>

<style scoped>
.global-map-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.breadcrumb {
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 8px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
}

.subtitle {
  color: var(--text-muted);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.refresh-state {
  font-size: 12px;
  font-weight: 600;
  color: #137333;
  background: #e6f4ea;
  border: 1px solid #ceead6;
  border-radius: 999px;
  padding: 7px 12px;
}

.refresh-state.online {
  color: #137333;
  background: #e6f4ea;
  border-color: #ceead6;
}

.refresh-state.offline {
  color: #b3261e;
  background: #fce8e6;
  border-color: #f4b7b7;
}

.refresh-state.loading {
  color: #1a73e8;
  background: #e8f0fe;
  border-color: #c7dafd;
}

.header-btn {
  border: 1px solid var(--border);
  background: white;
  color: var(--text);
  border-radius: 8px;
  padding: 9px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.header-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.selection-banner,
.error-banner {
  padding: 14px 16px;
  border-radius: 8px;
  border: 1px solid #d6e4ff;
  background: #eef4ff;
  color: var(--text);
}

.selection-banner strong {
  color: var(--primary);
}

.error-banner {
  border-color: #fbc4c4;
  background: #fce8e6;
  color: #b3261e;
}

.content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 16px;
  align-items: start;
}

@media (max-width: 1024px) {
  .page-header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}
</style>
