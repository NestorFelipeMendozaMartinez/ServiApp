<template>
  <div>
    <div class="page-header">
      <div class="container">
        <h1>{{ auth.isProvider ? 'Solicitudes disponibles' : 'Mis solicitudes' }}</h1>
        <p>{{ auth.isProvider ? 'Encuentra trabajos que se ajusten a tu experiencia' : 'Gestiona todas tus solicitudes de servicio' }}</p>
      </div>
    </div>

    <div class="container pb-5">
      <!-- Filters -->
      <div class="card p-3 mb-4">
        <div class="row g-2 align-items-end">
          <div class="col-md-4">
            <label class="form-label small fw-semibold">Categoría</label>
            <select v-model="filters.category" @change="load" class="form-select">
              <option value="">Todas las categorías</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
            </select>
          </div>
          <div class="col-md-3" v-if="!auth.isProvider">
            <label class="form-label small fw-semibold">Estado</label>
            <select v-model="filters.status" @change="load" class="form-select">
              <option value="">Todos</option>
              <option value="open">Abierta</option>
              <option value="in_progress">En Progreso</option>
              <option value="completed">Completada</option>
              <option value="cancelled">Cancelada</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Ciudad</label>
            <input v-model="filters.city" @input="debouncedLoad" type="text" class="form-control" placeholder="Ciudad..." />
          </div>
          <div class="col-md-2">
            <router-link v-if="!auth.isProvider" to="/requests/create" class="btn btn-primary w-100">
              + Nueva
            </router-link>
          </div>
        </div>
      </div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary"></div>
      </div>
      <div v-else-if="!requests.length" class="empty-state">
        <div class="icon">📋</div>
        <h5>{{ auth.isProvider ? 'No hay solicitudes abiertas' : 'No tienes solicitudes aún' }}</h5>
        <router-link v-if="!auth.isProvider" to="/requests/create" class="btn btn-primary mt-2">
          Crear primera solicitud
        </router-link>
      </div>
      <div v-else class="d-flex flex-column gap-3">
        <router-link v-for="r in requests" :key="r.id" :to="`/requests/${r.id}`" class="text-decoration-none">
          <div class="card p-3 req-card">
            <div class="row align-items-center g-2">
              <div class="col">
                <div class="d-flex align-items-center gap-2 mb-1">
                  <span class="badge-cat">{{ r.category_name }}</span>
                  <span v-if="r.city || r.location" class="text-muted small">📍 {{ r.city || r.location }}</span>
                </div>
                <h6 class="mb-1 fw-bold">{{ r.title }}</h6>
                <p class="text-muted small mb-1" style="line-height:1.4;">
                  {{ r.description.length > 120 ? r.description.slice(0, 120) + '...' : r.description }}
                </p>
                <small class="text-muted">
                  👤 {{ r.client_username }} · {{ timeAgo(r.created_at) }}
                  <span v-if="auth.isProvider"> · 🤝 {{ r.offers_count }} oferta(s)</span>
                </small>
              </div>
              <div class="col-auto">
                <span :class="`status-badge status-${r.status}`">{{ statusLabel(r.status) }}</span>
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
import { auth } from '../auth.js'
import api from '../api.js'

const loading = ref(true)
const requests = ref([])
const categories = ref([])
let debounceTimer = null

const filters = ref({ category: '', status: '', city: '' })

function debouncedLoad() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(load, 400)
}

function statusLabel(s) {
  return { open: 'Abierta', in_progress: 'En Progreso', completed: 'Completada', cancelled: 'Cancelada' }[s] || s
}

function timeAgo(d) {
  const diff = (new Date() - new Date(d)) / 1000
  if (diff < 3600) return `${Math.floor(diff / 60)}m`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  return `${Math.floor(diff / 86400)}d`
}

async function load() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.status) params.status = filters.value.status
    if (filters.value.city) params.city = filters.value.city
    const res = await api.get('requests/requests/', { params })
    requests.value = res.data.results || res.data
  } catch {} finally {
    loading.value = false
  }
}

onMounted(async () => {
  const catRes = await api.get('services/categories/').catch(() => ({ data: [] }))
  categories.value = catRes.data
  load()
})
</script>

<style scoped>
.req-card { transition: all 0.2s; }
.req-card:hover { transform: translateX(4px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
</style>
