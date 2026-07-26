import { createRouter, createWebHistory } from 'vue-router'
import MainControls from '../components/MainControls.vue'
import WebsitesView from '../components/WebsitesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'dashboard', component: MainControls },
    { path: '/websites', name: 'websites', component: WebsitesView },
  ],
})

export default router