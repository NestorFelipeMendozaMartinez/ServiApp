<template>
  <span class="stars">
    <span v-for="i in 5" :key="i">
      <span v-if="interactive" @click="$emit('update:modelValue', i)" style="cursor:pointer;">
        {{ i <= (hovered || modelValue) ? '★' : '☆' }}
      </span>
      <span v-else>{{ i <= Math.round(value) ? '★' : '☆' }}</span>
    </span>
    <small v-if="showCount && count !== undefined" class="text-muted ms-1">({{ count }})</small>
  </span>
</template>

<script setup>
import { ref } from 'vue'
defineProps({ value: Number, modelValue: Number, interactive: Boolean, showCount: Boolean, count: Number })
defineEmits(['update:modelValue'])
const hovered = ref(0)
</script>

<style scoped>
.stars { color: #ffc107; letter-spacing: 2px; }
</style>
