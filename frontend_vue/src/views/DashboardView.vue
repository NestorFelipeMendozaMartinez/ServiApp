<template>
  <div>
    <div class="page-header">
      <div class="container">
        <div class="d-flex align-items-center gap-3">
          <div class="avatar-lg">{{ initials }}</div>
          <div>
            <h1>Hola, {{ auth.user?.first_name || auth.user?.username }} 👋</h1>
            <p>{{ auth.isProvider ? '⚙️ Panel de Proveedor' : '👤 Panel de Cliente' }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="container pb-5">
      <!-- Stats row -->
      <div class="row g-3 mb-4">
        <div class="col-6 col-md-3" v-for="s in stats" :key="s.label">
          <div class="card p-3 text-center">
            <div style="font-size:1.8rem;">{{ s.icon }}</div>
            <div class="fw-bold fs-4 text-primary">{{ s.value }}</div>
            <div class="text-muted small">{{ s.label }}</div>
          </div>
        </div>
      </div>

      <!-- Quick actions -->
      <div class="row g-3 mb-4">
        <div class="col-12">
          <h5 class="fw-bold mb-3">Acciones rápidas</h5>
        </div>
        <div class="col-6 col-md-3" v-for="a in quickActions" :key="a.label">
          <router-link :to="a.to" class="action-card text-decoration-none d-block text-center p-3">
            <div style="font-size:2rem;" class="mb-2">{{ a.icon }}</div>
            <div class="fw-semibold small">{{ a.label }}</div>
          </router-link>
        </div>
      </div>

      <div class="row g-4">
        <!-- Recent requests (client) or open requests (provider) -->
        <div class="col-lg-7">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="fw-bold mb-0">
              {{ auth.isProvider ? 'Solicitudes abiertas' : 'Mis solicitudes recientes' }}
            </h5>
            <router-link to="/requests" class="btn btn-sm btn-outline-primary">Ver todas</router-link>
          </div>

          <div v-if="loadingRequests" class="text-center py-4">
            <div class="spinner-border text-primary"></div>
          </div>
          <div v-else-if="!requests.length" class="empty-state">
            <div class="icon">📋</div>
            <p>{{ auth.isProvider ? 'No hay solicitudes abiertas' : 'No tienes solicitudes aún' }}</p>
            <router-link v-if="!auth.isProvider" to="/requests/create" class="btn btn-primary btn-sm">
              Crear primera solicitud
            </router-link>
          </div>
          <div v-else class="d-flex flex-column gap-3">
            <router-link v-for="r in requests.slice(0,4)" :key="r.id" :to="`/requests/${r.id}`"
              class="text-decoration-none">
              <div class="card p-3">
                <div class="d-flex justify-content-between align-items-start">
                  <div class="flex-grow-1">
                    <span class="badge-cat mb-1">{{ r.category_name }}</span>
                    <h6 class="mb-1 fw-bold">{{ r.title }}</h6>
                    <small class="text-muted">{{ r.city || r.location }} · {{ timeAgo(r.created_at) }}</small>
                  </div>
                  <span :class="`status-badge status-${r.status}`">{{ statusLabel(r.status) }}</span>
                </div>
                <div v-if="auth.isProvider" class="mt-2">
                  <small class="text-muted">{{ r.offers_count }} oferta(s)</small>
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- My services (provider) or providers nearby (client) -->
        <div class="col-lg-5">
          <template v-if="auth.isProvider">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-bold mb-0">Mis servicios</h5>
              <router-link to="/services/create" class="btn btn-sm btn-primary">+ Nuevo</router-link>
            </div>
            <div v-if="!myServices.length" class="empty-state">
              <div class="icon">🛠️</div>
              <p>Publica tu primer servicio</p>
            </div>
            <div v-else class="d-flex flex-column gap-2">
              <div v-for="s in myServices.slice(0,4)" :key="s.id" class="card p-3">
                <div class="d-flex justify-content-between">
                  <div>
                    <span class="badge-cat mb-1">{{ s.category_name }}</span>
                    <h6 class="mb-0 fw-bold small">{{ s.title }}</h6>
                  </div>
                  <span v-if="s.price" class="fw-bold text-primary">${{ s.price }}</span>
                </div>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="d-flex justify-content-between align-items-center mb-3">
              <h5 class="fw-bold mb-0">Mis ofertas recibidas</h5>
            </div>
            <div v-if="!myOffers.length" class="empty-state">
              <div class="icon">🤝</div>
              <p>Las ofertas aparecerán aquí</p>
            </div>
            <div v-else class="d-flex flex-column gap-2">
              <div v-for="o in myOffers.slice(0,4)" :key="o.id" class="card p-3">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <div class="fw-semibold small">{{ o.request_title }}</div>
                    <small class="text-muted">{{ o.provider_username }}</small>
                  </div>
                  <span class="fw-bold text-primary">${{ o.price }}</span>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { auth } from '../auth.js'
import api from '../api.js'

const requests = ref([])
const myServices = ref([])
const myOffers = ref([])
const loadingRequests = ref(true)
const statsData = ref({ requests: 0, offers: 0, services: 0, rating: 0 })

const initials = computed(() => (auth.user?.username || 'U').slice(0, 2).toUpperCase())

const stats = computed(() => auth.isProvider
  ? [
    { icon: '🛠️', value: myServices.value.length, label: 'Mis Servicios' },
    { icon: '📋', value: statsData.value.requests, label: 'Solicitudes vistas' },
    { icon: '🤝', value: statsData.value.offers, label: 'Ofertas enviadas' },
    { icon: '⭐', value: auth.user?.rating?.toFixed(1) || '0.0', label: 'Calificación' },
  ]
  : [
    { icon: '📋', value: requests.value.length, label: 'Mis Solicitudes' },
    { icon: '🤝', value: myOffers.value.length, label: 'Ofertas recibidas' },
    { icon: '✅', value: requests.value.filter(r => r.status === 'completed').length, label: 'Completadas' },
    { icon: '⭐', value: '4.8', label: 'Calificación' },
  ]
)

const quickActions = computed(() => auth.isProvider
  ? [
    { icon: '📋', label: 'Ver solicitudes', to: '/requests' },
    { icon: '🤝', label: 'Mis ofertas', to: '/offers' },
    { icon: '➕', label: 'Nuevo servicio', to: '/services/create' },
    { icon: '👤', label: 'Mi perfil', to: '/profile' },
  ]
  : [
    { icon: '➕', label: 'Nueva solicitud', to: '/requests/create' },
    { icon: '🔍', label: 'Buscar servicios', to: '/services' },
    { icon: '📋', label: 'Mis solicitudes', to: '/requests' },
    { icon: '👤', label: 'Mi perfil', to: '/profile' },
  ]
)

function statusLabel(s) {
  return { open: 'Abierta', in_progress: 'En Progreso', completed: 'Completada', cancelled: 'Cancelada' }[s] || s
}

function timeAgo(dateStr) {
  const diff = (new Date() - new Date(dateStr)) / 1000
  if (diff < 3600) return `${Math.floor(diff / 60)}m`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  return `${Math.floor(diff / 86400)}d`
}

onMounted(async () => {
  try {
    const [reqRes, offersRes] = await Promise.all([
      api.get('requests/requests/'),
      api.get('requests/offers/'),
    ])
    requests.value = reqRes.data.results || reqRes.data
    myOffers.value = offersRes.data.results || offersRes.data
    statsData.value.requests = requests.value.length
    statsData.value.offers = myOffers.value.length

    if (auth.isProvider) {
      const svcRes = await api.get(`services/?provider=${auth.user.id}`)
      myServices.value = svcRes.data.results || svcRes.data
    }
  } catch {} finally {
    loadingRequests.value = false
  }
})
</script>

<style scoped>
.avatar-lg {
  width: 60px; height: 60px; border-radius: 50%;
  background: rgba(255,255,255,0.3); color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 1.3rem;
}
.action-card {
  background: #fff; border-radius: 12px; border: 2px solid transparent;
  box-shadow: var(--card-shadow); transition: all 0.2s; color: var(--text);
}
.action-card:hover { border-color: var(--primary); transform: translateY(-2px); }
</style>
