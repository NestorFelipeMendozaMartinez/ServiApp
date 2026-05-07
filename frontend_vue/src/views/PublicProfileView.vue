<template>
  <div>
    <div v-if="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div v-else-if="!provider" class="empty-state mt-5"><div class="icon">😕</div><h5>Perfil no encontrado</h5></div>
    <template v-else>
      <div class="provider-hero">
        <div class="container">
          <div class="d-flex align-items-center gap-4">
            <div class="provider-avatar-lg">
              <img v-if="provider.avatar_url" :src="provider.avatar_url" class="avatar-img-lg" />
              <span v-else>{{ provider.username?.slice(0,2).toUpperCase() }}</span>
            </div>
            <div>
              <h1 class="mb-1">{{ provider.first_name ? provider.first_name + ' ' + provider.last_name : provider.username }}</h1>
              <div class="d-flex align-items-center gap-3 flex-wrap">
                <span class="stars fs-5">
                  {{ '★'.repeat(Math.round(provider.rating || 0)) }}{{ '☆'.repeat(5-Math.round(provider.rating || 0)) }}
                  <span class="fw-bold ms-1">{{ provider.rating?.toFixed(1) || '0.0' }}</span>
                </span>
                <span class="text-white-50">{{ provider.total_ratings }} reseña(s)</span>
                <span v-if="provider.city">📍 {{ provider.city }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="container pb-5">
        <div class="row g-4">
          <div class="col-lg-8">
            <div v-if="provider.bio" class="card p-4 mb-4">
              <h5 class="fw-bold mb-2">Acerca de</h5>
              <p class="mb-0" style="line-height:1.7;">{{ provider.bio }}</p>
            </div>

            <!-- Services -->
            <div class="card p-4 mb-4">
              <h5 class="fw-bold mb-3">Servicios que ofrece</h5>
              <div v-if="!services.length" class="text-muted">Sin servicios publicados</div>
              <div v-else class="row g-3">
                <div class="col-md-6" v-for="s in services" :key="s.id">
                  <router-link :to="`/services/${s.id}`" class="text-decoration-none">
                    <div class="card p-3">
                      <span class="badge-cat mb-1">{{ s.category_name }}</span>
                      <h6 class="fw-bold mb-1">{{ s.title }}</h6>
                      <p class="text-muted small mb-1">{{ s.description.slice(0, 80) }}...</p>
                      <span v-if="s.price" class="fw-bold text-primary">${{ Number(s.price).toLocaleString() }}</span>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Reviews -->
            <div class="card p-4">
              <h5 class="fw-bold mb-3">Reseñas</h5>
              <div v-if="!reviews.length" class="text-muted">Sin reseñas aún</div>
              <div v-else class="d-flex flex-column gap-3">
                <div v-for="r in reviews" :key="r.id" class="review-row">
                  <div class="d-flex justify-content-between align-items-start">
                    <span class="fw-semibold">{{ r.reviewer_username }}</span>
                    <span class="stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5-r.rating) }}</span>
                  </div>
                  <p class="text-muted small mb-0 mt-1">{{ r.comment }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-4">
            <div class="card p-4 mb-3 text-center">
              <div class="rating-big">{{ provider.rating?.toFixed(1) || '0.0' }}</div>
              <div class="stars fs-3 my-1">
                {{ '★'.repeat(Math.round(provider.rating || 0)) }}{{ '☆'.repeat(5-Math.round(provider.rating || 0)) }}
              </div>
              <p class="text-muted">{{ provider.total_ratings }} calificaciones</p>
            </div>

            <div class="card p-4 mb-3">
              <h6 class="fw-bold mb-3">Resumen</h6>
              <table class="table table-borderless table-sm mb-0">
                <tr><td class="text-muted">Ciudad</td><td>{{ provider.city || '—' }}</td></tr>
                <tr><td class="text-muted">Servicios</td><td>{{ services.length }}</td></tr>
              </table>
            </div>

            <div v-if="auth.isLoggedIn && !auth.isProvider" class="card p-4">
              <router-link to="/requests/create" class="btn btn-primary w-100 mb-2">
                📋 Solicitar servicio
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { auth } from '../auth.js'
import api from '../api.js'

const route = useRoute()
const provider = ref(null)
const services = ref([])
const reviews = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [profRes, svcRes, revRes] = await Promise.all([
      api.get(`users/providers/${route.params.id}/`),
      api.get(`services/?provider=${route.params.id}`),
      api.get(`requests/reviews/?provider=${route.params.id}`),
    ])
    provider.value = profRes.data
    services.value = svcRes.data.results || svcRes.data
    reviews.value = revRes.data.results || revRes.data
  } catch {} finally {
    loading.value = false
  }
})
</script>

<style scoped>
.provider-hero {
  background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
  color: #fff; padding: 3rem 0 2.5rem;
  margin-bottom: 2rem;
}
.provider-avatar-lg {
  width: 80px; height: 80px; border-radius: 50%;
  background: rgba(255,255,255,0.2); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.8rem; font-weight: 800; overflow: hidden;
  border: 3px solid rgba(255,255,255,0.5);
}
.avatar-img-lg { width: 100%; height: 100%; object-fit: cover; }
.stars { color: #ffc107; }
.rating-big { font-size: 3rem; font-weight: 900; color: var(--primary); line-height: 1; }
.review-row { padding-bottom: 1rem; border-bottom: 1px solid #f0f0f0; }
.review-row:last-child { border-bottom: none; padding-bottom: 0; }
</style>
