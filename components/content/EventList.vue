<template>
  <ul class="events">
    <ContentSlot :use="$slots.default" />
  </ul>
</template>

<style scoped>
.events {
  list-style: none;
  margin: 2rem 0 0;
  padding: 0;
  display: grid;
  gap: 2rem;
}
@media (min-width: 760px) {
  .events {
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
  }
}
</style>
