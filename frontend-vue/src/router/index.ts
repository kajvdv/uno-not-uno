import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('@/views/start/StartView.vue'),
    },
    {
      path: '/new',
      component: () => import('@/views/new/NewGameView.vue'),
    },
  ],
})

export default router
