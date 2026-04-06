<template>
  <div class="min-h-screen bg-black text-white font-sans">
    <div class="max-w-2xl mx-auto p-6">
      <h1 class="text-3xl font-bold mb-6" style="color: #ffc60e">Task Dashboard</h1>
      <HealthCheck />
      <AuditHandle />
    </div>
  </div>
</template>

<script setup lang="ts">
import HealthCheck from './components/HealthCheck.vue'
import AuditHandle from './components/AuditHandle.vue'
</script>
