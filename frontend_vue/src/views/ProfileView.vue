<template>
  <div>
    <div class="page-header">
      <div class="container">
        <h1>Mi Perfil</h1>
        <p>Actualiza tu información personal y profesional</p>
      </div>
    </div>

    <div class="container pb-5">
      <div class="row g-4">
        <!-- Profile form -->
        <div class="col-lg-7">
          <div class="card p-4">
            <h5 class="fw-bold mb-4">Información personal</h5>
            <div v-if="success" class="alert alert-success py-2">{{ success }}</div>
            <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

            <form @submit.prevent="saveProfile">
              <div class="row g-3">
                <div class="col-12 text-center mb-2">
                  <div class="avatar-preview mb-2">
                    <img v-if="profile.avatar_url" :src="profile.avatar_url" class="avatar-img" />
                    <div v-else class="avatar-placeholder">{{ initials }}</div>
                  </div>
                  <label class="btn btn-outline-secondary btn-sm">
                    📷 Cambiar foto
                    <input type="file" @change="onAvatarChange" accept="image/*" class="d-none" />
                  </label>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-semibold small">Teléfono</label>
                  <input v-model="profile.phone" type="tel" class="form-control" placeholder="+57 300 000 0000" />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-semibold small">Ciudad</label>
                  <input v-model="profile.city" type="text" class="form-control" placeholder="Bogotá" />
                </div>
                <div class="col-12">
                  <label class="form-label fw-semibold small">Ubicación / Barrio</label>
                  <input v-model="profile.location" type="text" class="form-control" placeholder="Barrio o sector" />
                </div>
                <div class="col-12">
                  <label class="form-label fw-semibold small">
                    Descripción {{ auth.isProvider ? '/ Habilidades' : '' }}
                  </label>
                  <textarea v-model="profile.bio" class="form-control" rows="4"
                    :placeholder="auth.isProvider ? 'Cuéntales a los clientes tu experiencia, especialidades y lo que te hace diferente...' : 'Cuéntanos un poco sobre ti...'"></textarea>
                </div>
                <div class="col-12">
                  <label class="form-label fw-semibold small">Rol</label>
                  <div class="d-flex gap-3">
                    <div class="form-check">
                      <input class="form-check-input" type="radio" v-model="profile.is_provider" :value="false" id="isClient" />
                      <label class="form-check-label" for="isClient">👤 Cliente</label>
                    </div>
                    <div class="form-check">
                      <input class="form-check-input" type="radio" v-model="profile.is_provider" :value="true" id="isProvider" />
                      <label class="form-check-label" for="isProvider">⚙️ Proveedor</label>
                    </div>
                  </div>
                </div>
              </div>
              <button type="submit" class="btn btn-primary mt-4 px-4" :disabled="saving">
                <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                {{ saving ? 'Guardando...' : 'Guardar cambios' }}
              </button>
            </form>
          </div>
        </div>

        <!-- Stats sidebar -->
        <div class="col-lg-5">
          <div class="card p-4 mb-3">
            <h6 class="fw-bold mb-3">Tu calificación</h6>
            <div class="text-center">
              <div class="rating-big">{{ profile.rating?.toFixed(1) || '0.0' }}</div>
              <div class="stars fs-4">
                {{ '★'.repeat(Math.round(profile.rating || 0)) }}{{ '☆'.repeat(5 - Math.round(profile.rating || 0)) }}
              </div>
              <p class="text-muted small mt-1">{{ profile.total_ratings }} reseña(s)</p>
            </div>
          </div>

          <div class="card p-4 mb-3">
            <h6 class="fw-bold mb-3">Cuenta</h6>
            <table class="table table-borderless table-sm mb-0">
              <tr><td class="text-muted">Usuario</td><td class="fw-semibold">@{{ profile.username }}</td></tr>
              <tr><td class="text-muted">Email</td><td>{{ profile.email }}</td></tr>
              <tr><td class="text-muted">Tipo</td><td>{{ profile.is_provider ? '⚙️ Proveedor' : '👤 Cliente' }}</td></tr>
            </table>
          </div>

          <div v-if="auth.isProvider" class="card p-4">
            <h6 class="fw-bold mb-3">Mis servicios</h6>
            <div v-if="!myServices.length" class="text-muted small">Sin servicios publicados</div>
            <div v-else class="d-flex flex-column gap-2">
              <div v-for="s in myServices" :key="s.id" class="d-flex justify-content-between align-items-center">
                <span class="small fw-semibold">{{ s.title }}</span>
                <span v-if="s.price" class="text-primary small">${{ Number(s.price).toLocaleString() }}</span>
              </div>
            </div>
            <router-link to="/services/create" class="btn btn-outline-primary btn-sm w-100 mt-3">
              ➕ Nuevo servicio
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { auth } from '../auth.js'
import api from '../api.js'

const profile = ref({})
const myServices = ref([])
const saving = ref(false)
const success = ref('')
const error = ref('')
const avatarFile = ref(null)

const initials = computed(() => (profile.value.username || 'U').slice(0, 2).toUpperCase())

function onAvatarChange(e) {
  avatarFile.value = e.target.files[0]
  if (avatarFile.value) {
    profile.value.avatar_url = URL.createObjectURL(avatarFile.value)
  }
}

async function saveProfile() {
  saving.value = true
  success.value = ''
  error.value = ''
  try {
    const formData = new FormData()
    formData.append('phone', profile.value.phone || '')
    formData.append('city', profile.value.city || '')
    formData.append('location', profile.value.location || '')
    formData.append('bio', profile.value.bio || '')
    formData.append('is_provider', profile.value.is_provider)
    if (avatarFile.value) formData.append('avatar', avatarFile.value)

    const res = await api.patch('users/profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    profile.value = { ...profile.value, ...res.data }
    auth.updateUser({ is_provider: res.data.is_provider, city: res.data.city })
    success.value = '¡Perfil actualizado correctamente!'
    avatarFile.value = null
  } catch (e) {
    error.value = 'Error al guardar el perfil'
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  const [profRes] = await Promise.all([
    api.get('users/profile/'),
  ])
  profile.value = profRes.data

  if (auth.isProvider) {
    const svcRes = await api.get(`services/?provider=${auth.user.id}`)
    myServices.value = svcRes.data.results || svcRes.data
  }
})
</script>

<style scoped>
.stars { color: #ffc107; }
.rating-big { font-size: 3.5rem; font-weight: 900; color: var(--primary); line-height: 1; }
.avatar-preview { display: inline-block; }
.avatar-img { width: 90px; height: 90px; border-radius: 50%; object-fit: cover; border: 3px solid var(--primary); }
.avatar-placeholder {
  width: 90px; height: 90px; border-radius: 50%; background: var(--primary); color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 800;
}
</style>
