<template>
  <ul class="help-list">
    <ContentSlot :use="$slots.default" />
  </ul>
</template>

<style scoped>
.help-list {
  list-style: none;
  margin: 2rem 0 0;
  padding: 0;
  display: grid;
  gap: 2rem 3rem;
}
@media (min-width: 720px) {
  .help-list {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
