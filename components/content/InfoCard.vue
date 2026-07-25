<template>
  <div class="info-card">
    <h3 class="info-card-title">{{ title }}</h3>
    <div class="info-card-body"><ContentSlot :use="$slots.default" unwrap="p" /></div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  title: { type: String, required: true },
})
</script>

<style scoped>
.info-card {
  background: #fff;
  border: 1px solid #e4e0d5;
  border-radius: 10px;
  padding: 1.25rem 1.4rem;
}
:root.dark .info-card {
  background: #1f2937;
  border-color: #374151;
}
.info-card-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #2d5a40;
  margin-bottom: 0.4rem;
}
:root.dark .info-card-title {
  color: #6ee7b7;
}
.info-card-body {
  font-size: 0.95rem;
  color: #5c6f63;
}
:root.dark .info-card-body {
  color: #9ca3af;
}
</style>
