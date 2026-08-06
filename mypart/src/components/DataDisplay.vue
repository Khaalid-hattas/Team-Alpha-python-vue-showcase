<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const props = defineProps({
  stats: {
    type: Object,
    default: () => ({
      top_categories: []
    })
  }
})

const categories = computed(() => props.stats?.top_categories ?? [])

const chartData = computed(() => ({
  labels: categories.value.map(c => c.name),
  datasets: [{
    label: 'Articles',
    data: categories.value.map(c => c.count),
    backgroundColor: '#4285f4'
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } }
}
</script>

<template>
  <div class="charts-row">
    <!-- Left Empty Space Holder for Layout Consistency -->
    <!-- Top Categories Bar Chart -->
    <div class="card chart-card">
      <div class="card-header-inline">
        <h3>System Metrics Panel</h3>
      </div>
      <div class="chart-box">
        <Bar v-if="categories.length" :data="chartData" :options="chartOptions" />
        <div v-else class="empty-msg-box">No analytics data yet.</div>
      </div>
    </div>

    <!-- Analytics Breakdown Metrics Data Table -->
    <div class="card table-card">
      <div class="card-header-inline">
        <h3>Top Categories Metrics</h3>
      </div>

      <div class="table-container">
        <table class="analytics-table">
          <thead>
            <tr>
              <th>CATEGORY DESCRIPTION MAPPED TAG</th>
              <th class="text-right">TOTAL COUNT</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in categories"
              :key="item.name"
            >
              <td class="bold-text">
                <span class="badge-category">
                  {{ item.name }}
                </span>
              </td>

              <td class="text-right count-text">
                {{ item.count }}
              </td>
            </tr>

            <tr v-if="categories.length === 0">
              <td colspan="2" class="empty-msg">
                No analytics summary data discovered.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.charts-row {
  display: flex;
  gap: 20px;
  width: 100%;
}

.chart-box {
  padding: 20px;
  height: 280px;
}

.chart-card,
.table-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-header-inline {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.card-header-inline h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

.empty-msg-box {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
  font-size: 14px;
  margin: auto;
}

.table-container {
  width: 100%;
}

.analytics-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.analytics-table th {
  text-align: left;
  padding: 12px 24px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  background: #f8f9fa;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.analytics-table td {
  padding: 16px 24px;
  border-top: 1px solid var(--border);
  vertical-align: middle;
}

.bold-text {
  font-weight: 600;
}

.count-text {
  font-weight: 700;
  color: var(--navy);
}

.text-right {
  text-align: right !important;
}

.badge-category {
  background: #e8f0fe;
  color: var(--primary);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}

.empty-msg {
  padding: 32px !important;
  text-align: center;
  color: var(--text-muted);
}

@media (max-width: 992px) {
  .charts-row {
    flex-direction: column;
  }
}
</style>
