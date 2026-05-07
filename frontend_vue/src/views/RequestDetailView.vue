<template>
  <div>
    <div v-if="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
    <div v-else-if="!request" class="empty-state mt-5"><div class="icon">😕</div><h5>Solicitud no encontrada</h5></div>

    <template v-else>
      <div class="page-header">
        <div class="container">
          <div class="d-flex align-items-center gap-2 mb-1">
            <span class="badge-cat">{{ request.category_name }}</span>
            <span :class="`status-badge status-${request.status}`">{{ statusLabel(request.status) }}</span>
          </div>
          <h1>{{ request.title }}</h1>
          <p>📍 {{ request.city || request.location }} · {{ timeAgo(request.created_at) }}</p>
        </div>
      </div>

      <div class="container pb-5">
        <div class="row g-4">
          <div class="col-lg-7">
            <!-- Description -->
            <div class="card p-4 mb-4">
              <h5 class="fw-bold mb-3">Descripción</h5>
              <p style="line-height:1.7;">{{ request.description }}</p>
            </div>

            <!-- Offers -->
            <div class="card p-4 mb-4">
              <h5 class="fw-bold mb-3">Ofertas ({{ offers.length }})</h5>

              <!-- Submit offer (provider) -->
              <div v-if="auth.isProvider && request.status === 'open' && !myOffer" class="offer-form mb-4">
                <h6 class="fw-semibold mb-2">Enviar mi oferta</h6>
                <div v-if="offerError" class="alert alert-danger py-2 small">{{ offerError }}</div>
                <div class="mb-2">
                  <label class="form-label small">Precio (COP)</label>
                  <div class="input-group">
                    <span class="input-group-text">$</span>
                    <input v-model="offerForm.price" type="number" class="form-control" placeholder="50000" min="0" />
                  </div>
                </div>
                <div class="mb-2">
                  <label class="form-label small">Mensaje para el cliente</label>
                  <textarea v-model="offerForm.message" class="form-control" rows="3"
                    placeholder="Cuéntale tu experiencia y por qué eres la mejor opción..."></textarea>
                </div>
                <button @click="submitOffer" class="btn btn-primary btn-sm" :disabled="offerLoading">
                  {{ offerLoading ? 'Enviando...' : '📤 Enviar oferta' }}
                </button>
              </div>
              <div v-else-if="myOffer" class="alert alert-success py-2 mb-4">
                ✅ Ya enviaste una oferta por ${{ Number(myOffer.price).toLocaleString() }}
              </div>

              <div v-if="!offers.length" class="text-muted text-center py-3">
                Aún no hay ofertas
              </div>
              <div v-else class="d-flex flex-column gap-3">
                <div v-for="o in offers" :key="o.id"
                  :class="['offer-card p-3', o.status === 'accepted' && 'offer-accepted', o.status === 'rejected' && 'offer-rejected']">
                  <div class="d-flex justify-content-between align-items-start mb-2">
                    <div class="d-flex align-items-center gap-2">
                      <div class="mini-avatar">{{ o.provider_username?.slice(0,2).toUpperCase() }}</div>
                      <div>
                        <router-link :to="`/providers/${o.provider_id}`" class="fw-bold text-decoration-none">
                          {{ o.provider_username }}
                        </router-link>
                        <div class="stars" style="font-size:0.75rem;">
                          {{ '★'.repeat(Math.round(o.provider_rating || 0)) }}
                          <small class="text-muted">{{ o.provider_rating?.toFixed(1) }}</small>
                        </div>
                      </div>
                    </div>
                    <div class="text-end">
                      <div class="fw-bold text-primary fs-5">${{ Number(o.price).toLocaleString() }}</div>
                      <span :class="`offer-status offer-${o.status}`">{{ offerStatusLabel(o.status) }}</span>
                    </div>
                  </div>
                  <p class="small mb-2" style="line-height:1.4;">{{ o.message }}</p>

                  <!-- Client actions -->
                  <div v-if="isMyRequest && request.status === 'open' && o.status === 'pending'" class="d-flex gap-2">
                    <button @click="acceptOffer(o)" class="btn btn-success btn-sm">✅ Aceptar</button>
                    <button @click="rejectOffer(o)" class="btn btn-outline-danger btn-sm">❌ Rechazar</button>
                  </div>
                  <div v-if="o.status === 'accepted' && isMyRequest" class="mt-2">
                    <button @click="openChat(o)" class="btn btn-outline-primary btn-sm me-2">💬 Chat</button>
                    <a :href="`http://127.0.0.1:8000/api/requests/offers/${o.id}/contract/`"
                      target="_blank" class="btn btn-outline-secondary btn-sm">📄 Ver contrato</a>
                  </div>
                </div>
              </div>
            </div>

            <!-- Chat section (when in_progress) -->
            <div v-if="request.status === 'in_progress'" class="card p-4">
              <h5 class="fw-bold mb-3">💬 Chat</h5>
              <div ref="chatBox" class="chat-messages mb-3">
                <div v-for="m in messages" :key="m.id"
                  :class="['message', m.sender_id === auth.user?.id ? 'mine' : 'theirs']">
                  <div class="msg-bubble">{{ m.content }}</div>
                  <div class="msg-meta">{{ m.sender_username }} · {{ timeAgo(m.created_at) }}</div>
                </div>
              </div>
              <div class="d-flex gap-2">
                <input v-model="chatMsg" @keyup.enter="sendMessage" type="text"
                  class="form-control" placeholder="Escribe un mensaje..." />
                <button @click="sendMessage" class="btn btn-primary px-3">Enviar</button>
              </div>
            </div>

            <!-- Review (completed, client) -->
            <div v-if="request.status === 'completed' && isMyRequest && !hasReview" class="card p-4 mt-4">
              <h5 class="fw-bold mb-3">⭐ Califica al proveedor</h5>
              <div class="mb-3">
                <div class="d-flex gap-1 mb-1">
                  <button v-for="i in 5" :key="i" @click="reviewForm.rating = i"
                    :class="['star-btn', i <= reviewForm.rating && 'active']">★</button>
                </div>
              </div>
              <textarea v-model="reviewForm.comment" class="form-control mb-3" rows="3"
                placeholder="Comparte tu experiencia con este proveedor..."></textarea>
              <button @click="submitReview" class="btn btn-primary btn-sm" :disabled="reviewLoading">
                {{ reviewLoading ? 'Enviando...' : 'Publicar reseña' }}
              </button>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="col-lg-5">
            <div class="card p-4 mb-3">
              <h6 class="fw-bold mb-3">Detalles de la solicitud</h6>
              <table class="table table-borderless table-sm mb-0">
                <tr><td class="text-muted">Cliente</td><td class="fw-semibold">{{ request.client_username }}</td></tr>
                <tr><td class="text-muted">Ciudad</td><td>{{ request.city || '—' }}</td></tr>
                <tr><td class="text-muted">Ubicación</td><td>{{ request.location || '—' }}</td></tr>
                <tr><td class="text-muted">Estado</td><td><span :class="`status-badge status-${request.status}`">{{ statusLabel(request.status) }}</span></td></tr>
                <tr><td class="text-muted">Publicada</td><td>{{ formatDate(request.created_at) }}</td></tr>
              </table>
            </div>

            <!-- Complete button (client, in_progress) -->
            <div v-if="isMyRequest && request.status === 'in_progress'" class="card p-4 mb-3">
              <h6 class="fw-bold mb-2">¿El servicio fue completado?</h6>
              <p class="text-muted small">Si el proveedor ya terminó el trabajo, marca la solicitud como completada.</p>
              <button @click="markCompleted" class="btn btn-success w-100">
                ✅ Marcar como completada
              </button>
            </div>

            <!-- Cancel (client, open) -->
            <div v-if="isMyRequest && request.status === 'open'" class="card p-4">
              <button @click="cancelRequest" class="btn btn-outline-danger w-100 btn-sm">
                🚫 Cancelar solicitud
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { auth } from '../auth.js'
import api from '../api.js'

const route = useRoute()
const router = useRouter()
const request = ref(null)
const offers = ref([])
const messages = ref([])
const loading = ref(true)
const offerLoading = ref(false)
const reviewLoading = ref(false)
const offerError = ref('')
const chatMsg = ref('')
const chatBox = ref(null)
let pollInterval = null

const offerForm = ref({ price: '', message: '' })
const reviewForm = ref({ rating: 0, comment: '' })

const isMyRequest = computed(() => request.value?.client_id === auth.user?.id)
const myOffer = computed(() => auth.isProvider ? offers.value.find(o => o.provider_id === auth.user?.id) : null)
const hasReview = ref(false)

function statusLabel(s) {
  return { open: 'Abierta', in_progress: 'En Progreso', completed: 'Completada', cancelled: 'Cancelada' }[s] || s
}
function offerStatusLabel(s) {
  return { pending: 'Pendiente', accepted: '✅ Aceptada', rejected: '❌ Rechazada' }[s] || s
}
function timeAgo(d) {
  const diff = (new Date() - new Date(d)) / 1000
  if (diff < 3600) return `${Math.floor(diff / 60)}m`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  return new Date(d).toLocaleDateString('es-CO')
}
function formatDate(d) {
  return new Date(d).toLocaleDateString('es-CO', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function load() {
  try {
    const [reqRes, offersRes] = await Promise.all([
      api.get(`requests/requests/${route.params.id}/`),
      api.get(`requests/offers/?request=${route.params.id}`),
    ])
    request.value = reqRes.data
    offers.value = offersRes.data.results || offersRes.data

    if (request.value.status === 'in_progress') loadMessages()
    if (request.value.status === 'completed' && isMyRequest.value) {
      const revRes = await api.get(`requests/reviews/?received=true`).catch(() => ({ data: [] }))
      hasReview.value = (revRes.data.results || revRes.data).some(r => r.request === request.value.id)
    }
  } catch {} finally {
    loading.value = false
  }
}

async function loadMessages() {
  try {
    const res = await api.get(`requests/messages/?request=${route.params.id}`)
    messages.value = res.data.results || res.data
    await nextTick()
    if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
  } catch {}
}

async function submitOffer() {
  offerLoading.value = true
  offerError.value = ''
  try {
    await api.post('requests/offers/', { request: route.params.id, ...offerForm.value })
    offerForm.value = { price: '', message: '' }
    const res = await api.get(`requests/offers/?request=${route.params.id}`)
    offers.value = res.data.results || res.data
  } catch (e) {
    const d = e.response?.data
    offerError.value = d ? Object.values(d).flat().join(' ') : 'Error al enviar oferta'
  } finally {
    offerLoading.value = false
  }
}

async function acceptOffer(offer) {
  await api.patch(`requests/offers/${offer.id}/`, { status: 'accepted' })
  load()
}

async function rejectOffer(offer) {
  await api.patch(`requests/offers/${offer.id}/`, { status: 'rejected' })
  load()
}

function openChat(offer) {
  chatBox.value?.scrollIntoView({ behavior: 'smooth' })
}

async function sendMessage() {
  if (!chatMsg.value.trim()) return
  try {
    await api.post('requests/messages/', { service_request: route.params.id, content: chatMsg.value })
    chatMsg.value = ''
    loadMessages()
  } catch {}
}

async function markCompleted() {
  if (!confirm('¿Confirmas que el servicio fue completado?')) return
  await api.post(`requests/requests/${route.params.id}/complete/`)
  load()
}

async function cancelRequest() {
  if (!confirm('¿Cancelar esta solicitud?')) return
  await api.patch(`requests/requests/${route.params.id}/`, { status: 'cancelled' })
  load()
}

async function submitReview() {
  if (!reviewForm.value.rating) return alert('Selecciona una calificación')
  reviewLoading.value = true
  try {
    const acceptedOffer = offers.value.find(o => o.status === 'accepted')
    await api.post('requests/reviews/', {
      request: route.params.id,
      reviewed: acceptedOffer?.provider_id,
      ...reviewForm.value,
    })
    hasReview.value = true
  } catch (e) {
    alert(e.response?.data ? Object.values(e.response.data).flat().join(' ') : 'Error')
  } finally {
    reviewLoading.value = false
  }
}

onMounted(() => {
  load()
  pollInterval = setInterval(() => {
    if (request.value?.status === 'in_progress') loadMessages()
  }, 5000)
})

import { onUnmounted } from 'vue'
onUnmounted(() => clearInterval(pollInterval))
</script>

<style scoped>
.offer-card {
  border: 2px solid #dee2e6; border-radius: 12px; background: #fff;
}
.offer-accepted { border-color: #28a745; background: #f0fff4; }
.offer-rejected { border-color: #dc3545; background: #fff0f0; opacity: 0.7; }
.offer-status { font-size: 0.75rem; font-weight: 600; }
.offer-pending { color: #856404; }
.offer-accepted { color: #155724; }
.offer-rejected { color: #721c24; }
.mini-avatar {
  width: 32px; height: 32px; border-radius: 50%; background: var(--primary);
  color: #fff; font-size: 0.7rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.stars { color: #ffc107; }
.offer-form { background: #f8f9fa; border-radius: 12px; padding: 1rem; }

.chat-messages {
  height: 300px; overflow-y: auto; padding: 1rem;
  background: #f8f9fa; border-radius: 12px;
  display: flex; flex-direction: column; gap: 8px;
}
.message { display: flex; flex-direction: column; }
.message.mine { align-items: flex-end; }
.message.theirs { align-items: flex-start; }
.msg-bubble {
  max-width: 70%; padding: 8px 14px; border-radius: 16px;
  font-size: 0.9rem; line-height: 1.4;
}
.mine .msg-bubble { background: var(--primary); color: #fff; border-bottom-right-radius: 4px; }
.theirs .msg-bubble { background: #fff; border: 1px solid #dee2e6; border-bottom-left-radius: 4px; }
.msg-meta { font-size: 0.7rem; color: var(--muted); margin-top: 2px; }

.star-btn { border: none; background: none; font-size: 1.5rem; color: #dee2e6; cursor: pointer; transition: color 0.1s; padding: 0 2px; }
.star-btn.active, .star-btn:hover { color: #ffc107; }
</style>
