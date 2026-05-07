<template>
  <div>
    <div class="page-header">
      <div class="container">
        <h1>Mis ofertas</h1>
        <p>Seguimiento de las ofertas que has enviado</p>
      </div>
    </div>

    <div class="container pb-5">
      <div v-if="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
      <div v-else-if="!offers.length" class="empty-state">
        <div class="icon">🤝</div>
        <h5>No has enviado ofertas aún</h5>
        <router-link to="/requests" class="btn btn-primary mt-2">Ver solicitudes disponibles</router-link>
      </div>
      <div v-else class="d-flex flex-column gap-3">
        <router-link v-for="o in offers" :key="o.id" :to="`/requests/${o.request}`" class="text-decoration-none">
          <div class="card p-3">
            <div class="d-flex justify-content-between align-items-start">
              <div class="flex-grow-1">
                <h6 class="fw-bold mb-1">{{ o.request_title }}</h6>
                <p class="text-muted small mb-1">{{ o.message.slice(0, 100) }}...</p>
                <small class="text-muted">{{ timeAgo(o.created_at) }}</small>
              </div>
              <div class="text-end ms-3">
                <div class="fw-bold text-primary fs-5">${{ Number(o.price).toLocaleString() }}</div>
                <span :class="`offer-status-badge offer-${o.status}`">{{ statusLabel(o.status) }}</span>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api.js'

const loading = ref(true)
const offers = ref([])

function statusLabel(s) {
  return { pending: 'Pendiente', accepted: '✅ Aceptada', rejected: '❌ Rechazada' }[s] || s
}
function timeAgo(d) {
  const diff = (new Date() - new Date(d)) / 1000
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  return `${Math.floor(diff / 86400)}d`
}

onMounted(async () => {
  try {
    const res = await api.get('requests/offers/')
    offers.value = res.data.results || res.data
  } catch {} finally {
    loading.value = false
  }
})
</script>

<style scoped>
.offer-status-badge { font-size: 0.78rem; font-weight: 600; }
.offer-pending { color: #856404; }
.offer-accepted { color: #155724; }
.offer-rejected { color: #721c24; }
</style>
