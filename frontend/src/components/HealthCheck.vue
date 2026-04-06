<template>
  <div class="bg-gray-900 rounded-lg p-4 mb-6 border border-gray-800">
    <div class="flex justify-between items-center">
      <div class="flex items-center gap-3">
        <div :class="['w-3 h-3 rounded-full', healthOk ? 'bg-green-500' : 'bg-red-500']"></div>
        <span class="text-gray-300">Backend: {{ healthOk ? 'Online' : 'Offline' }}</span>
      </div>
      <button
        @click="checkHealth"
        class="px-3 py-1 rounded text-sm transition"
        style="background-color: #ffc60e; color: #000; font-weight: 500"
      >
        Refresh
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const healthOk = ref(false)

async function checkHealth() {
  try {
    const res = await fetch('http://localhost:8000/health')
    healthOk.value = res.ok
  } catch {
    healthOk.value = false
  }
}

onMounted(() => {
  checkHealth()
})
</script>
