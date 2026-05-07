<template>
  <div>
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary"></div>
    </div>
    <div v-else-if="!service" class="empty-state mt-5">
      <div class="icon">😕</div><h5>Servicio no encontrado</h5>
    </div>
    <template v-else>
      <div class="page-header">
        <div class="container">
          <span class="badge-cat mb-2">{{ service.category_name }}</span>
          <h1>{{ service.title }}</h1>
          <div class="d-flex align-items-center gap-3 mt-2">
            <span v-if="service.city">📍 {{ service.city }}</span>
            <span v-if="service.price" class="fw-bold fs-5">${{ Number(service.price).toLocaleString() }}</span>
          </div>
        </div>
      </div>

      <div class="container pb-5">
        <div class="row g-4">
          <div class="col-lg-8">
            <div class="card p-4 mb-4">
              <h5 class="fw-bold mb-3">Descripción del servicio</h5>
              <p style="line-height:1.7;">{{ service.description }}</p>
            </div>

            <!-- Reviews -->
            <div class="card p-4">
              <h5 class="fw-bold mb-3">Reseñas del proveedor</h5>
              <div v-if="!reviews.length" class="text-muted">Aún no hay reseñas</div>
              <div v-else class="d-flex flex-column gap-3">
                <div v-for="r in reviews" :key="r.id" class="review-item">
                  <div class="d-flex justify-content-between">
                    <span class="fw-semibold">{{ r.reviewer_username }}</span>
                    <span class="stars">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5-r.rating) }}</span>
                  </div>
                  <p class="text-muted small mb-0 mt-1">{{ r.comment }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-lg-4">
            <!-- Provider card -->
            <div class="card p-4 mb-3">
              <h6 class="fw-bold mb-3">Proveedor</h6>
              <div class="d-flex align-items-center gap-3 mb-3">
                <div class="provider-avatar">{{ service.provider_username?.slice(0,2).toUpperCase() }}</div>
                <div>
                  <div class="fw-bold">{{ service.provider_username }}</div>
                  <div class="stars">
                    {{ '★'.repeat(Math.round(service.provider_rating || 0)) }}{{ '☆'.repeat(5 - Math.round(service.provider_rating || 0)) }}
                    <small class="text-muted">{{ service.provider_rating?.toFixed(1) }}</small>
                  </div>
                </div>
              </div>
              <router-link :to="`/providers/${service.provider_id}`" class="btn btn-outline-primary w-100 btn-sm mb-2">
                Ver perfil completo
              </router-link>
            </div>

            <!-- Action card -->
            <div class="card p-4">
              <div v-if="service.price" class="text-center mb-3">
                <div class="text-muted small">Precio</div>
                <div class="fw-bold fs-3 text-primary">${{ Number(service.price).toLocaleString() }}</div>
              </div>

              <template v-if="auth.isLoggedIn && !auth.isProvider && auth.user?.id !== service.provider_id">
                <router-link to="/requests/create" class="btn btn-primary w-100 mb-2">
                  📋 Solicitar este servicio
                </router-link>
              </template>
              <template v-else-if="!auth.isLoggedIn">
                <router-link to="/register" class="btn btn-primary w-100 mb-2">
                  Registrate para solicitar
                </router-link>
              </template>
              <template v-else-if="auth.user?.id === service.provider_id">
                <router-link :to="`/services/${service.id}/edit`" class="btn btn-outline-primary w-100 mb-2">
                  ✏️ Editar servicio
                </router-link>
                <button @click="deleteService" class="btn btn-outline-danger w-100 btn-sm">
                  🗑️ Eliminar
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { auth } from '../auth.js'
import api from '../api.js'

const route = useRoute()
const router = useRouter()
const service = ref(null)
const reviews = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [svcRes, revRes] = await Promise.all([
      api.get(`services/${route.params.id}/`),
      api.get(`requests/reviews/?provider=${service.value?.provider_id || ''}`),
    ])
    service.value = svcRes.data
    const revRes2 = await api.get(`requests/reviews/?provider=${service.value.provider_id}`)
    reviews.value = revRes2.data.results || revRes2.data
  } catch {} finally {
    loading.value = false
  }
})

async function deleteService() {
  if (!confirm('¿Eliminar este servicio?')) return
  try {
    await api.delete(`services/${route.params.id}/`)
    router.push('/services')
  } catch { alert('Error al eliminar') }
}
</script>

<style scoped>
.provider-avatar {
  width: 48px; height: 48px; border-radius: 50%; background: var(--primary);
  color: #fff; font-weight: 700; display: flex; align-items: center; justify-content: center;
}
.stars { color: #ffc107; }
.review-item { padding-bottom: 1rem; border-bottom: 1px solid #f0f0f0; }
.review-item:last-child { border-bottom: none; padding-bottom: 0; }
</style>
