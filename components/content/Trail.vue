<template>
  <ol class="trail">
    <ContentSlot :use="$slots.default" />
  </ol>
</template>

<style scoped>
.trail {
  list-style: none;
  margin: 2rem 0 0;
  padding: 0;
  max-width: 42rem;
}
</style>
