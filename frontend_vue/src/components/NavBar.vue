<template>
  <nav class="navbar navbar-expand-lg fixed-top" style="background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    <div class="container">
      <router-link to="/" class="navbar-brand d-flex align-items-center gap-2">
        <span style="font-size:1.6rem;">🛠️</span>
        <span style="font-weight:800; color:var(--primary); font-size:1.2rem;">Servi<span style="color:var(--secondary);">App</span></span>
      </router-link>

      <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navMenu">
        <ul class="navbar-nav me-auto gap-1">
          <li class="nav-item">
            <router-link to="/services" class="nav-link">Servicios</router-link>
          </li>
          <li class="nav-item" v-if="auth.isLoggedIn">
            <router-link to="/requests" class="nav-link">
              {{ auth.isProvider ? 'Solicitudes' : 'Mis Solicitudes' }}
            </router-link>
          </li>
          <li class="nav-item" v-if="auth.isProvider">
            <router-link to="/offers" class="nav-link">Mis Ofertas</router-link>
          </li>
        </ul>

        <ul class="navbar-nav align-items-center gap-2">
          <template v-if="!auth.isLoggedIn">
            <li class="nav-item">
              <router-link to="/login" class="nav-link">Iniciar sesión</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register" class="btn btn-primary btn-sm px-3">Registrarse</router-link>
            </li>
          </template>

          <template v-else>
            <!-- Notifications bell -->
            <li class="nav-item">
              <router-link to="/notifications" class="nav-link position-relative">
                🔔
                <span v-if="unreadCount > 0"
                  class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                  style="font-size:0.6rem;">
                  {{ unreadCount }}
                </span>
              </router-link>
            </li>

            <!-- User dropdown -->
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle d-flex align-items-center gap-2" href="#" data-bs-toggle="dropdown">
                <div class="avatar-circle">{{ initials }}</div>
                <span class="d-none d-lg-inline" style="font-size:0.9rem; font-weight:600;">{{ auth.user?.username }}</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end shadow border-0">
                <li><span class="dropdown-item-text text-muted" style="font-size:0.8rem;">{{ auth.isProvider ? '⚙️ Proveedor' : '👤 Cliente' }}</span></li>
                <li><hr class="dropdown-divider m-1"></li>
                <li><router-link to="/dashboard" class="dropdown-item">📊 Dashboard</router-link></li>
                <li><router-link to="/profile" class="dropdown-item">👤 Mi Perfil</router-link></li>
                <li v-if="auth.isProvider">
                  <router-link to="/services/create" class="dropdown-item">➕ Publicar Servicio</router-link>
                </li>
                <li v-if="!auth.isProvider">
                  <router-link to="/requests/create" class="dropdown-item">📋 Nueva Solicitud</router-link>
                </li>
                <li><hr class="dropdown-divider m-1"></li>
                <li><button class="dropdown-item text-danger" @click="logout">🚪 Cerrar sesión</button></li>
              </ul>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../auth.js'
import api from '../api.js'

const router = useRouter()
const unreadCount = ref(0)

const initials = computed(() => {
  const u = auth.user?.username || 'U'
  return u.slice(0, 2).toUpperCase()
})

async function fetchNotifications() {
  if (!auth.isLoggedIn) return
  try {
    const res = await api.get('requests/notifications/')
    unreadCount.value = res.data.filter(n => !n.read).length
  } catch {}
}

function logout() {
  auth.logout()
  router.push('/login')
}

onMounted(() => {
  fetchNotifications()
  // Poll notifications every 30s
  setInterval(fetchNotifications, 30000)
})
</script>

<style scoped>
.nav-link {
  font-weight: 500;
  color: var(--text) !important;
  padding: 0.4rem 0.75rem !important;
  border-radius: 8px;
  transition: all 0.2s;
}
.nav-link:hover, .router-link-active {
  background: rgba(255,107,53,0.1);
  color: var(--primary) !important;
}
.router-link-exact-active.nav-link { color: var(--primary) !important; }
.avatar-circle {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: var(--primary);
  color: #fff;
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 0.75rem;
}
.dropdown-item { font-size: 0.9rem; padding: 0.5rem 1rem; border-radius: 6px; margin: 2px 4px; }
.dropdown-item:hover { background: rgba(255,107,53,0.1); }
.dropdown-menu { min-width: 200px; border-radius: 12px; padding: 0.5rem; }
</style>
