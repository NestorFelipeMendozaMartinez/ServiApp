<template>
  <div>
    <h2>Componente de ejemplo Vue</h2>
    <button @click="getPing">Probar conexión API</button>
    <p v-if="response">Respuesta: {{ response }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '../api';

const response = ref('');

async function getPing() {
  try {
    const res = await api.get('users/profile/'); // Cambia por un endpoint real
    response.value = JSON.stringify(res.data);
  } catch (e) {
    response.value = 'Error de conexión';
  }
}
</script>
