<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6 col-lg-5">
          <div class="text-center mb-4">
            <router-link to="/" class="text-decoration-none">
              <span style="font-size:2rem;">🛠️</span>
              <h2 style="font-weight:800; color:var(--primary);">Servi<span style="color:var(--secondary);">App</span></h2>
            </router-link>
            <p class="text-muted">Crea tu cuenta gratis</p>
          </div>

          <div class="card p-4">
            <!-- Role selector -->
            <div class="role-selector mb-4">
              <button type="button" @click="form.is_provider = false"
                :class="['role-btn', !form.is_provider && 'active']">
                👤 Soy Cliente
              </button>
              <button type="button" @click="form.is_provider = true"
                :class="['role-btn', form.is_provider && 'active']">
                ⚙️ Soy Proveedor
              </button>
            </div>
            <p class="text-muted small text-center mb-4">
              {{ form.is_provider ? 'Ofrece tus servicios y consigue clientes' : 'Encuentra servicios cerca de ti' }}
            </p>

            <div v-if="error" class="alert alert-danger py-2 small">{{ error }}</div>
            <div v-if="success" class="alert alert-success py-2 small">{{ success }}</div>

            <form @submit.prevent="register">
              <div class="row g-3">
                <div class="col-6">
                  <label class="form-label fw-semibold small">Nombre</label>
                  <input v-model="form.first_name" type="text" class="form-control" placeholder="Nombre" />
                </div>
                <div class="col-6">
                  <label class="form-label fw-semibold small">Apellido</label>
                  <input v-model="form.last_name" type="text" class="form-control" placeholder="Apellido" />
                </div>
                <div class="col-12">
                  <label class="form-label fw-semibold small">Usuario *</label>
                  <input v-model="form.username" type="text" class="form-control" placeholder="Elige un nombre de usuario" required />
                </div>
                <div class="col-12">
                  <label class="form-label fw-semibold small">Correo electrónico *</label>
                  <input v-model="form.email" type="email" class="form-control" placeholder="tucorreo@email.com" required />
                </div>
                <div class="col-12">
                  <label class="form-label fw-semibold small">Contraseña *</label>
                  <input v-model="form.password" type="password" class="form-control" placeholder="Mínimo 6 caracteres" required minlength="6" />
                </div>
              </div>

              <button type="submit" class="btn btn-primary w-100 py-2 fw-bold mt-4" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
              </button>
            </form>

            <hr class="my-3">
            <p class="text-center small text-muted mb-0">
              ¿Ya tienes cuenta?
              <router-link to="/login" class="text-primary fw-semibold">Iniciar sesión</router-link>
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
const success = ref('')
const loading = ref(false)
const form = ref({ username: '', email: '', password: '', first_name: '', last_name: '', is_provider: false })

async function register() {
  loading.value = true
  error.value = ''
  try {
    await api.post('users/register/', form.value)
    // Auto-login after register
    const loginRes = await api.post('users/login/', { username: form.value.username, password: form.value.password })
    auth.login(loginRes.data.access, loginRes.data.user)
    router.push('/dashboard')
  } catch (e) {
    const data = e.response?.data
    if (data && typeof data === 'object') {
      error.value = Object.values(data).flat().join(' ')
    } else {
      error.value = 'Error al registrarse. Intenta de nuevo.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%); min-height: 100vh; padding: 2rem 0; }
.card { border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.12); }
.form-control:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(255,107,53,0.15); }
.role-selector { display: flex; gap: 8px; }
.role-btn {
  flex: 1; padding: 10px; border-radius: 10px; font-weight: 600; font-size: 0.9rem;
  border: 2px solid #dee2e6; background: #fff; cursor: pointer; transition: all 0.2s;
}
.role-btn.active { border-color: var(--primary); background: rgba(255,107,53,0.08); color: var(--primary); }
</style>
