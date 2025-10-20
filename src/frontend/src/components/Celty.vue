<template>
  <div>
    <img :src="imageUrl" alt="Server-side image" class="celty-class" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
const imageUrl = ref('/static/images/celty.png')
</script>

<style scoped>
.celty-class {
  border: 2px solid rgba(0, 0, 0, 0.65);
  width: 50%;
}
</style>
