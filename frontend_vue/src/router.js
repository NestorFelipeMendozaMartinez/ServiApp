import { createRouter, createWebHistory } from 'vue-router'
import { auth } from './auth.js'

const routes = [
  { path: '/', component: () => import('./views/HomeView.vue') },
  { path: '/login', component: () => import('./views/LoginView.vue') },
  { path: '/register', component: () => import('./views/RegisterView.vue') },

  { path: '/dashboard', component: () => import('./views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/profile', component: () => import('./views/ProfileView.vue'), meta: { requiresAuth: true } },
  { path: '/notifications', component: () => import('./views/NotificationsView.vue'), meta: { requiresAuth: true } },

  { path: '/services', component: () => import('./views/ServicesView.vue') },
  { path: '/services/create', component: () => import('./views/CreateServiceView.vue'), meta: { requiresAuth: true, providerOnly: true } },
  { path: '/services/:id', component: () => import('./views/ServiceDetailView.vue') },

  { path: '/requests', component: () => import('./views/RequestsView.vue'), meta: { requiresAuth: true } },
  { path: '/requests/create', component: () => import('./views/CreateRequestView.vue'), meta: { requiresAuth: true } },
  { path: '/requests/:id', component: () => import('./views/RequestDetailView.vue'), meta: { requiresAuth: true } },

  { path: '/offers', component: () => import('./views/OffersView.vue'), meta: { requiresAuth: true } },
  { path: '/providers/:id', component: () => import('./views/PublicProfileView.vue') },

  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    next('/login')
  } else if (to.meta.providerOnly && !auth.isProvider) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
