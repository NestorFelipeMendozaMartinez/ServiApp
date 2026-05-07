<template>
  <div>
    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <div class="row align-items-center min-vh-hero">
          <div class="col-lg-6">
            <span class="badge rounded-pill mb-3" style="background:rgba(255,255,255,0.2); color:#fff; font-size:0.85rem; padding:6px 16px;">
              🇨🇴 La plataforma de servicios de Colombia
            </span>
            <h1 class="hero-title">Encuentra el servicio que necesitas <span class="text-warning">cerca de ti</span></h1>
            <p class="hero-sub">Conectamos personas con técnicos, mensajeros, plomeros, electricistas y profesionales independientes en tu ciudad.</p>
            <div class="d-flex gap-3 flex-wrap mt-4">
              <router-link to="/services" class="btn btn-light btn-lg fw-bold px-4">
                🔍 Explorar Servicios
              </router-link>
              <router-link v-if="!auth.isLoggedIn" to="/register" class="btn btn-outline-light btn-lg px-4">
                Registrarse gratis
              </router-link>
              <router-link v-else-if="!auth.isProvider" to="/requests/create" class="btn btn-outline-light btn-lg px-4">
                📋 Crear Solicitud
              </router-link>
            </div>
            <!-- Quick search -->
            <div class="search-bar mt-4">
              <input v-model="searchQuery" @keyup.enter="goSearch" type="text"
                class="form-control form-control-lg" placeholder="¿Qué servicio buscas?" />
              <button @click="goSearch" class="btn btn-warning fw-bold">Buscar</button>
            </div>
          </div>
          <div class="col-lg-6 d-none d-lg-flex justify-content-center">
            <div class="hero-illustration">
              <div class="floating-card card-1">🔧 Técnico disponible</div>
              <div class="floating-card card-2">⭐ 4.9 calificación</div>
              <div class="floating-card card-3">🛵 En camino</div>
              <div class="hero-emoji">🏙️</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats-bar py-4">
      <div class="container">
        <div class="row text-center g-4">
          <div class="col-6 col-md-3" v-for="s in stats" :key="s.label">
            <div class="stat-item">
              <div class="stat-num">{{ s.num }}</div>
              <div class="stat-label">{{ s.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories -->
    <section class="py-5">
      <div class="container">
        <div class="section-header">
          <h2>Explora por categoría</h2>
          <p class="text-muted">Encuentra exactamente lo que necesitas</p>
        </div>
        <div class="row g-3">
          <div class="col-6 col-md-4 col-lg-3" v-for="cat in categories" :key="cat.id">
            <router-link :to="`/services?category=${cat.id}`" class="category-card text-decoration-none">
              <div class="cat-icon">{{ cat.icon }}</div>
              <div class="cat-name">{{ cat.name }}</div>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- How it works -->
    <section class="how-it-works py-5">
      <div class="container">
        <div class="section-header">
          <h2>¿Cómo funciona?</h2>
          <p class="text-muted">En 3 simples pasos</p>
        </div>
        <div class="row g-4">
          <div class="col-md-4" v-for="step in steps" :key="step.num">
            <div class="step-card text-center">
              <div class="step-num">{{ step.num }}</div>
              <div class="step-icon">{{ step.icon }}</div>
              <h5 class="fw-700 mt-3">{{ step.title }}</h5>
              <p class="text-muted">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Recent services -->
    <section class="py-5 bg-white">
      <div class="container">
        <div class="section-header">
          <h2>Servicios recientes</h2>
          <router-link to="/services" class="btn btn-outline-primary btn-sm">Ver todos →</router-link>
        </div>
        <div class="row g-3" v-if="services.length">
          <div class="col-md-6 col-lg-4" v-for="s in services" :key="s.id">
            <router-link :to="`/services/${s.id}`" class="text-decoration-none">
              <div class="card h-100 service-card">
                <div class="card-body">
                  <span class="badge-cat">{{ s.category_name }}</span>
                  <h6 class="mt-2 fw-bold">{{ s.title }}</h6>
                  <p class="text-muted small" style="line-height:1.4;">{{ s.description.slice(0, 80) }}...</p>
                  <div class="d-flex justify-content-between align-items-center mt-3">
                    <span class="text-muted small">👤 {{ s.provider_username }}</span>
                    <span v-if="s.price" class="fw-bold text-primary">${{ s.price }}</span>
                    <span v-else class="text-muted small">Precio a convenir</span>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section py-5">
      <div class="container text-center">
        <h2 class="text-white fw-bold">¿Eres un profesional independiente?</h2>
        <p class="text-white opacity-75 mb-4">Únete a ServiApp, crea tu perfil y empieza a conseguir clientes hoy mismo.</p>
        <router-link to="/register" class="btn btn-light btn-lg fw-bold px-5">
          Quiero ser proveedor 🚀
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../auth.js'
import api from '../api.js'

const router = useRouter()
const searchQuery = ref('')
const categories = ref([])
const services = ref([])

const stats = [
  { num: '500+', label: 'Proveedores' },
  { num: '1,200+', label: 'Servicios' },
  { num: '3,500+', label: 'Solicitudes' },
  { num: '4.8⭐', label: 'Calificación promedio' },
]

const steps = [
  { num: '01', icon: '📋', title: 'Publica tu solicitud', desc: 'Describe lo que necesitas, la categoría y tu ciudad.' },
  { num: '02', icon: '🤝', title: 'Recibe ofertas', desc: 'Proveedores cercanos te envían sus propuestas y precios.' },
  { num: '03', icon: '✅', title: 'Contrata y califica', desc: 'Elige la mejor oferta, confirma el servicio y paga.' },
]

function goSearch() {
  if (searchQuery.value.trim()) router.push(`/services?search=${searchQuery.value}`)
}

onMounted(async () => {
  try {
    const [catRes, svcRes] = await Promise.all([
      api.get('services/categories/'),
      api.get('services/?limit=6'),
    ])
    categories.value = catRes.data
    services.value = svcRes.data.results || svcRes.data
  } catch {}
})
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%);
  padding: 5rem 0 4rem;
  color: #fff;
}
.min-vh-hero { min-height: 60vh; }
.hero-title { font-size: 2.8rem; font-weight: 800; line-height: 1.2; }
.hero-sub { font-size: 1.1rem; opacity: 0.9; max-width: 500px; }
.search-bar {
  display: flex; gap: 8px; max-width: 480px;
  background: rgba(255,255,255,0.15); padding: 6px; border-radius: 12px;
}
.search-bar .form-control { border: none; background: transparent; color: #fff; }
.search-bar .form-control::placeholder { color: rgba(255,255,255,0.6); }
.hero-illustration { position: relative; width: 400px; height: 400px; }
.hero-emoji { font-size: 10rem; text-align: center; }
.floating-card {
  position: absolute; background: #fff; border-radius: 12px; padding: 8px 16px;
  font-size: 0.85rem; font-weight: 600; box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  animation: float 3s ease-in-out infinite;
}
.card-1 { top: 20%; left: 0; color: var(--text); }
.card-2 { top: 50%; right: 0; color: #f59e0b; animation-delay: 1s; }
.card-3 { bottom: 20%; left: 10%; color: var(--accent); animation-delay: 2s; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }

.stats-bar { background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.stat-num { font-size: 1.8rem; font-weight: 800; color: var(--primary); }
.stat-label { color: var(--muted); font-size: 0.85rem; }

.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.section-header h2 { font-weight: 700; margin: 0; }

.category-card {
  display: block; background: #fff; border-radius: 12px; padding: 1.5rem 1rem;
  text-align: center; border: 2px solid transparent;
  box-shadow: var(--card-shadow); transition: all 0.2s;
}
.category-card:hover { border-color: var(--primary); transform: translateY(-4px); }
.cat-icon { font-size: 2.2rem; margin-bottom: 0.5rem; }
.cat-name { font-weight: 600; color: var(--text); font-size: 0.9rem; }

.how-it-works { background: #F0F4FF; }
.step-card { padding: 2rem 1rem; background: #fff; border-radius: 16px; box-shadow: var(--card-shadow); }
.step-num { font-size: 2.5rem; font-weight: 900; color: rgba(255,107,53,0.2); line-height: 1; }
.step-icon { font-size: 2.5rem; }

.service-card { transition: all 0.2s; }
.service-card:hover { transform: translateY(-4px); }

.cta-section {
  background: linear-gradient(135deg, var(--secondary) 0%, #1A936F 100%);
}
</style>
