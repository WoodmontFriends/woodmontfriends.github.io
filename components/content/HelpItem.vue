<script setup lang="ts">
defineProps({
  title: { type: String, required: true },
})
</script>

<template>
  <li class="help-item">
    <h3 class="help-title">{{ title }}</h3>
    <div class="md">
      <ContentSlot :use="$slots.default" />
    </div>
  </li>
</template>

<style scoped>
.help-item {
  padding-top: 1rem;
  border-top: 2px solid var(--hemlock);
}
.help-title {
  margin: 0 0 0.3rem;
  font-size: 1.3rem;
  font-weight: 700;
}
</style>
