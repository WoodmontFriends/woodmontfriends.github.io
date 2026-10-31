<script setup lang="ts">
defineProps({
  title: { type: String, default: '' },
})
</script>

<template>
  <div class="board">
    <h3 v-if="title" class="board-heading">{{ title }}</h3>
    <ul class="board-list">
      <ContentSlot :use="$slots.default" />
    </ul>
  </div>
</template>

<style scoped>
.board {
  margin-top: 2rem;
}
.board-heading {
  margin: 0 0 0.25rem;
  font-size: 1.5rem;
  font-weight: 700;
}
.board-list {
  list-style: none;
  margin: 0.75rem 0 0;
  padding: 0;
  display: grid;
  gap: 1rem 2rem;
}
@media (min-width: 560px) {
  .board-list {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
