<script setup lang="ts">
// `photo` (a path under /public) and a bio in the default slot are optional,
// so members can be listed by name now and filled in later.
defineProps({
  name: { type: String, required: true },
  role: { type: String, default: '' },
  photo: { type: String, default: '' },
})
</script>

<template>
  <li class="board-member" :class="{ 'has-photo': photo }">
    <img v-if="photo" class="board-photo" :src="photo" :alt="name" loading="lazy">
    <div>
      <p class="board-name">{{ name }}</p>
      <p v-if="role" class="board-role">{{ role }}</p>
      <div v-if="$slots.default" class="md board-bio">
        <ContentSlot :use="$slots.default" />
      </div>
    </div>
  </li>
</template>

<style scoped>
.board-member {
  padding-top: 0.75rem;
  border-top: 2px solid var(--hemlock);
}
.board-member.has-photo {
  display: grid;
  grid-template-columns: 5rem 1fr;
  gap: 1rem;
  align-items: start;
}
.board-photo {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
  object-fit: cover;
}
.board-name {
  margin: 0;
  font-family: 'Zilla Slab', serif;
  font-size: 1.2rem;
  font-weight: 700;
}
.board-role {
  margin: 0.1rem 0 0;
  font-size: 0.95rem;
  opacity: 0.8;
}
.board-bio {
  margin-top: 0.4rem;
}
</style>
