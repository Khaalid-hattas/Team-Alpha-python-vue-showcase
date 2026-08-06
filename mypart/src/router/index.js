import { createRouter, createWebHistory } from 'vue-router'
import MainControls from '../components/MainControls.vue'
import WebsitesView from '../components/WebsitesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: HomeView,
    },
    {
      path: '/websites',
      name: 'Websites',
      component: () => import('../views/WebsitesView.vue'),
    },
    {
      path: '/global-map',
      name: 'GlobalMap',
      component: () => import('../views/GlobalMap.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router