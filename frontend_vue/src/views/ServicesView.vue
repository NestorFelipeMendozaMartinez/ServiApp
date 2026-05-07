<template>
  <div>
    <div class="page-header">
      <div class="container">
        <h1>Servicios disponibles</h1>
        <p>Encuentra el profesional ideal cerca de ti</p>
      </div>
    </div>

    <div class="container pb-5">
      <!-- Filters -->
      <div class="card p-3 mb-4">
        <div class="row g-2 align-items-end">
          <div class="col-md-4">
            <label class="form-label small fw-semibold">Buscar</label>
            <input v-model="filters.search" @input="debouncedSearch" type="text"
              class="form-control" placeholder="🔍 Busca un servicio..." />
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Categoría</label>
            <select v-model="filters.category" @change="load" class="form-select">
              <option value="">Todas las categorías</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label small fw-semibold">Ciudad</label>
            <input v-model="filters.city" @input="debouncedSearch" type="text"
              class="form-control" placeholder="Ciudad..." />
          </div>
          <div class="col-md-2">
            <button @click="clearFilters" class="btn btn-outline-secondary w-100">Limpiar</button>
          </div>
        </div>
      </div>

      <!-- Results count -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <span class="text-muted small">{{ services.length }} servicio(s) encontrado(s)</span>
        <router-link v-if="auth.isProvider" to="/services/create" class="btn btn-primary btn-sm">
          ➕ Publicar servicio
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary"></div>
        <p class="mt-2 text-muted">Cargando servicios...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="!services.length" class="empty-state">
        <div class="icon">🔍</div>
        <h5>No se encontraron servicios</h5>
        <p>Intenta cambiar los filtros de búsqueda</p>
      </div>

      <!-- Grid -->
      <div v-else class="row g-3">
        <div class="col-md-6 col-lg-4" v-for="s in services" :key="s.id">
          <router-link :to="`/services/${s.id}`" class="text-decoration-none">
            <div class="card h-100 svc-card">
              <div class="card-body d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <span class="badge-cat">{{ s.category_name }}</span>
                  <span v-if="s.city" class="text-muted small">📍 {{ s.city }}</span>
                </div>
                <h6 class="fw-bold">{{ s.title }}</h6>
                <p class="text-muted small flex-grow-1" style="line-height:1.4;">
                  {{ s.description.length > 100 ? s.description.slice(0, 100) + '...' : s.description }}
                </p>
                <div class="border-top pt-2 mt-2 d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center gap-2">
                    <div class="mini-avatar">{{ s.provider_username?.slice(0,2).toUpperCase() }}</div>
                    <div>
                      <div class="small fw-semibold">{{ s.provider_username }}</div>
                      <div class="stars" style="font-size:0.75rem;">
                        {{ '★'.repeat(Math.round(s.provider_rating || 0)) }}{{ '☆'.repeat(5 - Math.round(s.provider_rating || 0)) }}
                      </div>
                    </div>
                  </div>
                  <span v-if="s.price" class="fw-bold text-primary fs-6">${{ Number(s.price).toLocaleString() }}</span>
                  <span v-else class="text-muted small">Cotizar</span>
                </div>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { auth } from '../auth.js'
import api from '../api.js'

const route = useRoute()
const loading = ref(true)
const services = ref([])
const categories = ref([])
let searchTimer = null

const filters = ref({
  search: route.query.search || '',
  category: route.query.category || '',
  city: '',
})

function debouncedSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(load, 400)
}

function clearFilters() {
  filters.value = { search: '', category: '', city: '' }
  load()
}

async function load() {
  loading.value = true
  try {
    const params = {}
    if (filters.value.search) params.search = filters.value.search
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.city) params.city = filters.value.city
    const res = await api.get('services/', { params })
    services.value = res.data.results || res.data
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
.svc-card { transition: all 0.2s; }
.svc-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.mini-avatar {
  width: 28px; height: 28px; border-radius: 50%; background: var(--primary);
  color: #fff; font-size: 0.65rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.stars { color: #ffc107; }
</style>
