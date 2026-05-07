<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-5 col-lg-4">
          <div class="text-center mb-4">
            <router-link to="/" class="text-decoration-none">
              <span style="font-size:2rem;">🛠️</span>
              <h2 style="font-weight:800; color:var(--primary);">Servi<span style="color:var(--secondary);">App</span></h2>
            </router-link>
            <p class="text-muted">Bienvenido de vuelta</p>
          </div>

          <div class="card p-4">
            <h5 class="fw-bold mb-4 text-center">Iniciar sesión</h5>

            <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>

            <form @submit.prevent="login">
              <div class="mb-3">
                <label class="form-label fw-semibold small">Usuario</label>
                <input v-model="form.username" type="text" class="form-control" placeholder="Tu nombre de usuario" required />
              </div>
              <div class="mb-3">
                <label class="form-label fw-semibold small">Contraseña</label>
                <input v-model="form.password" type="password" class="form-control" placeholder="Tu contraseña" required />
              </div>
              <button type="submit" class="btn btn-primary w-100 py-2 fw-bold" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Iniciando...' : 'Iniciar sesión' }}
              </button>
            </form>

            <hr class="my-3">
            <p class="text-center small text-muted mb-0">
              ¿No tienes cuenta?
              <router-link to="/register" class="text-primary fw-semibold">Regístrate gratis</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../auth.js'
import api from '../api.js'

const router = useRouter()
const error = ref('')
const loading = ref(false)
const form = ref({ username: '', password: '' })

async function login() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.post('users/login/', form.value)
    auth.login(res.data.access, res.data.user)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || 'Credenciales incorrectas'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%); min-height: 100vh; }
.card { border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.12); }
.form-control:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(255,107,53,0.15); }
</style>
