<template>
  <div>
    <div class="page-header">
      <div class="container">
        <h1>{{ isEditing ? 'Editar servicio' : 'Publicar nuevo servicio' }}</h1>
        <p>Describe tu servicio para que los clientes puedan encontrarte</p>
      </div>
    </div>

    <div class="container pb-5">
      <div class="row justify-content-center">
        <div class="col-lg-7">
          <div class="card p-4">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>

            <form @submit.prevent="submit">
              <div class="mb-3">
                <label class="form-label fw-semibold">Título del servicio *</label>
                <input v-model="form.title" type="text" class="form-control"
                  placeholder="Ej: Reparación de electrodomésticos a domicilio" required />
              </div>

              <div class="mb-3">
                <label class="form-label fw-semibold">Categoría *</label>
                <select v-model="form.category" class="form-select" required>
                  <option value="">Selecciona una categoría</option>
                  <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.icon }} {{ c.name }}</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label fw-semibold">Descripción *</label>
                <textarea v-model="form.description" class="form-control" rows="5"
                  placeholder="Describe detalladamente lo que ofreces, tu experiencia, materiales incluidos, etc."
                  required></textarea>
              </div>

              <div class="row g-3 mb-3">
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Precio (opcional)</label>
                  <div class="input-group">
                    <span class="input-group-text">$</span>
                    <input v-model="form.price" type="number" class="form-control" placeholder="0" min="0" step="100" />
                  </div>
                  <small class="text-muted">Deja vacío para "precio a convenir"</small>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-semibold">Ciudad</label>
                  <input v-model="form.city" type="text" class="form-control" placeholder="Bogotá, Medellín..." />
                </div>
              </div>

              <div class="d-flex gap-3 mt-4">
                <button type="submit" class="btn btn-primary px-4 fw-bold" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Guardando...' : (isEditing ? 'Actualizar servicio' : 'Publicar servicio') }}
                </button>
                <router-link to="/dashboard" class="btn btn-outline-secondary">Cancelar</router-link>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api.js'

const route = useRoute()
const router = useRouter()
const error = ref('')
const loading = ref(false)
const categories = ref([])
const isEditing = computed(() => !!route.params.id)

const form = ref({ title: '', category: '', description: '', price: '', city: '' })

onMounted(async () => {
  const catRes = await api.get('services/categories/')
  categories.value = catRes.data

  if (isEditing.value) {
    const res = await api.get(`services/${route.params.id}/`)
    const s = res.data
    form.value = { title: s.title, category: s.category, description: s.description, price: s.price || '', city: s.city || '' }
  }
})

async function submit() {
  loading.value = true
  error.value = ''
  try {
    const payload = { ...form.value }
    if (!payload.price) delete payload.price

    if (isEditing.value) {
      await api.patch(`services/${route.params.id}/`, payload)
    } else {
      await api.post('services/', payload)
    }
    router.push('/dashboard')
  } catch (e) {
    const data = e.response?.data
    error.value = data ? Object.values(data).flat().join(' ') : 'Error al guardar'
  } finally {
    loading.value = false
  }
}
</script>
