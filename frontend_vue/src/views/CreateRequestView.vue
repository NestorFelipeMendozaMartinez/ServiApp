<template>
  <div>
    <div class="page-header">
      <div class="container">
        <h1>Nueva solicitud de servicio</h1>
        <p>Describe lo que necesitas y recibe ofertas de proveedores</p>
      </div>
    </div>

    <div class="container pb-5">
      <div class="row justify-content-center">
        <div class="col-lg-7">
          <div class="card p-4">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <form @submit.prevent="submit">
              <div class="mb-3">
                <label class="form-label fw-semibold">¿Qué necesitas? *</label>
                <input v-model="form.title" type="text" class="form-control"
                  placeholder="Ej: Necesito un electricista para reparar instalación" required />
              </div>

              <div class="mb-3">
                <label class="form-label fw-semibold">Categoría *</label>
                <select v-model="form.category" class="form-select" required>
                  <option value="">Selecciona una categoría</option>
                  <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label fw-semibold">Descripción detallada *</label>
                <textarea v-model="form.description" class="form-control" rows="5"
                  placeholder="Describe el problema, el lugar, urgencia, horario disponible, etc."
                  required></textarea>
              </div>

              <div class="row g-3 mb-3">
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Ciudad *</label>
                  <input v-model="form.city" type="text" class="form-control" placeholder="Bogotá, Medellín..." required />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Barrio / Dirección</label>
                  <input v-model="form.location" type="text" class="form-control" placeholder="Barrio o referencia" />
                </div>
              </div>

              <div class="d-flex gap-3 mt-4">
                <button type="submit" class="btn btn-primary px-4 fw-bold" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Publicando...' : 'Publicar solicitud' }}
                </button>
                <router-link to="/requests" class="btn btn-outline-secondary">Cancelar</router-link>
              </div>
            </form>
          </div>

          <!-- Tips -->
          <div class="card p-4 mt-3" style="border-left: 4px solid var(--primary);">
            <h6 class="fw-bold mb-2">💡 Consejos para una buena solicitud</h6>
            <ul class="text-muted small mb-0 ps-3">
              <li>Describe el problema con el mayor detalle posible</li>
              <li>Menciona si tienes alguna urgencia de tiempo</li>
              <li>Indica el horario en que puedes recibir al proveedor</li>
              <li>Sé específico sobre la ubicación para recibir más ofertas</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'

const router = useRouter()
const error = ref('')
const loading = ref(false)
const categories = ref([])
const form = ref({ title: '', category: '', description: '', city: '', location: '' })

onMounted(async () => {
  const res = await api.get('services/categories/')
  categories.value = res.data
})

async function submit() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.post('requests/requests/', form.value)
    router.push(`/requests/${res.data.id}`)
  } catch (e) {
    const data = e.response?.data
    error.value = data ? Object.values(data).flat().join(' ') : 'Error al publicar'
  } finally {
    loading.value = false
  }
}
</script>
