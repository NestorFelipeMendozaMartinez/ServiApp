<template>
  <div>
    <div class="page-header">
      <div class="container d-flex justify-content-between align-items-center">
        <div>
          <h1>Notificaciones</h1>
          <p>Mantente al día con tu actividad</p>
        </div>
        <button v-if="notifications.some(n => !n.read)" @click="markAllRead"
          class="btn btn-outline-light btn-sm">
          ✅ Marcar todas como leídas
        </button>
      </div>
    </div>

    <div class="container pb-5">
      <div v-if="loading" class="text-center py-5"><div class="spinner-border text-primary"></div></div>
      <div v-else-if="!notifications.length" class="empty-state">
        <div class="icon">🔔</div>
        <h5>No tienes notificaciones</h5>
        <p>Aquí aparecerán tus alertas de actividad</p>
      </div>
      <div v-else class="d-flex flex-column gap-2">
        <div v-for="n in notifications" :key="n.id"
          :class="['card p-3 notif-card', !n.read && 'unread']"
          @click="goTo(n)">
          <div class="d-flex align-items-start gap-3">
            <div class="notif-icon">{{ typeIcon(n.type) }}</div>
            <div class="flex-grow-1">
              <div class="fw-semibold">{{ n.title }}</div>
              <div class="text-muted small">{{ n.body }}</div>
              <div class="text-muted" style="font-size:0.75rem; margin-top:4px;">{{ timeAgo(n.created_at) }}</div>
            </div>
            <div v-if="!n.read" class="unread-dot"></div>
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
const loading = ref(true)
const notifications = ref([])

const typeIcon = (t) => ({
  new_offer: '🤝', offer_accepted: '✅', offer_rejected: '❌',
  new_message: '💬', request_completed: '🎉', new_review: '⭐',
}[t] || '🔔')

function timeAgo(d) {
  const diff = (new Date() - new Date(d)) / 1000
  if (diff < 3600) return `hace ${Math.floor(diff / 60)} min`
  if (diff < 86400) return `hace ${Math.floor(diff / 3600)} h`
  return `hace ${Math.floor(diff / 86400)} días`
}

async function goTo(n) {
  if (n.link) router.push(n.link)
}

async function markAllRead() {
  await api.post('requests/notifications/read/')
  notifications.value = notifications.value.map(n => ({ ...n, read: true }))
}

onMounted(async () => {
  try {
    const res = await api.get('requests/notifications/')
    notifications.value = res.data.results || res.data
  } catch {} finally {
    loading.value = false
  }
})
</script>

<style scoped>
.notif-card { cursor: pointer; transition: all 0.2s; border-left: 4px solid transparent; }
.notif-card:hover { transform: translateX(2px); }
.notif-card.unread { border-left-color: var(--primary); background: rgba(255,107,53,0.03); }
.notif-icon { font-size: 1.4rem; width: 36px; text-align: center; }
.unread-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--primary); flex-shrink: 0; margin-top: 6px; }
</style>
