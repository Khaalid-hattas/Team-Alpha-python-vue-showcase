<script setup>
const props = defineProps({
  nodes: {
    type: Array,
    default: () => [],
  },
})

const legendItems = [
  {
    label: 'Green pulse = healthy API success rate',
    color: '#34a853',
  },
  {
    label: 'Red pulse = degraded API success rate',
    color: '#ea4335',
  },
]
</script>

<template>
  <section class="card legend-card">
    <div class="card-head">
      <h3>Legend</h3>
    </div>

    <div class="legend-block">
      <ul class="legend-list">
        <li v-for="item in legendItems" :key="item.label">
          <span class="dot" :style="{ backgroundColor: item.color }" aria-hidden="true"></span>
          <span>{{ item.label }}</span>
        </li>
      </ul>
    </div>

    <div class="source-list-block">
      <h4>Mapped sources</h4>

      <ul class="source-list">
        <li v-for="node in props.nodes" :key="node.source_name">
          <div>
            <strong>{{ node.display_name }}</strong>
            <span>{{ node.city }}, {{ node.country }}</span>
          </div>

          <span class="location-chip">{{ node.success_rate }}%</span>
        </li>
      </ul>
    </div>
  </section>
</template>

<style scoped>
.legend-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.card-head {
  padding: 16px 18px;
  border-bottom: 1px solid var(--border);
}

.card-head h3,
.source-list-block h4 {
  font-size: 14px;
  font-weight: 600;
}

.legend-block,
.source-list-block {
  padding: 14px 18px 16px;
}

.legend-block {
  border-bottom: 1px solid var(--border);
}

.legend-list,
.source-list {
  list-style: none;
  display: grid;
  gap: 10px;
}

.legend-list li,
.source-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-content: space-between;
  color: var(--text-muted);
  font-size: 13px;
}

.source-list li div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.source-list strong {
  color: var(--text);
}

.source-list span {
  font-size: 12px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.location-chip {
  font-size: 12px;
  color: var(--primary);
  background: #e8f0fe;
  border: 1px solid #d2e3fc;
  border-radius: 999px;
  padding: 4px 8px;
  font-weight: 600;
}
</style>
