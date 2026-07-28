<template>
  <div class="charts-row">
    <div class="chart-card">
      <h3>Articles by category</h3>
      <bar :data="chartData" :options="chartOptions"/>
    </div>
    <div class="table-card">
      <h3>Top Categories</h3>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Count</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in stats.top_categories" :key="item.name">
            <td><span class="it-name"></span>{{ item.name }}</td>
            <td>{{ item.count }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import api from './services/api';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  components: { Bar },
  props: ['stats'],
  computed: {
    chartData() {
      return {
        labels: this.stats.top_categories?.map((c) => c.name) || [],
        datasets: [{
          label: 'Articles',
          backgroundColor: 'var(--color-primary)',
          borderColor: 'var(--color-secondary)',
          data: this.stats.top_categories?.map((c) => c.count) || []
        }]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        }
      }
    }
  }
}
</script>
<style>
.charts-row {
  display: flex;
  gap: 20px;
  padding: 20px;
}
.chart-card, .table-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  flex: 1;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 8px;
  border-bottom: 1px solid #eee;
  text-align: left;
}
h3 {
  margin-top: 0;
}
</style>