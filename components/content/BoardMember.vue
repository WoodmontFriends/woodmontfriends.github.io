<script setup lang="ts">
// `photo` (a path under /public) and a bio in the default slot are optional, so members
// can be listed now and filled in later. Without a photo, their initials stand in.
const props = defineProps({
  name: { type: String, required: true },
  role: { type: String, default: '' },
  photo: { type: String, default: '' },
})
const initials = computed(() =>
  props.name.split(/[\s-]+/).filter(Boolean).map(w => w[0]).slice(0, 2).join('').toUpperCase())
</script>

<template>
  <li class="board-member">
    <img v-if="photo" class="board-photo" :src="photo" :alt="name" loading="lazy">
    <span v-else class="board-photo board-initials" aria-hidden="true">{{ initials }}</span>
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
  display: grid;
  grid-template-columns: 4.5rem 1fr;
  gap: 1rem;
  align-items: center;
  padding-top: 1rem;
  border-top: 2px solid var(--hemlock);
}
.board-photo {
  width: 4.5rem;
  height: 4.5rem;
  border-radius: 50%;
  object-fit: cover;
}
.board-initials {
  display: grid;
  place-items: center;
  background: var(--fern);
  color: var(--hemlock);
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1.4rem;
}
.board-name {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
}
.board-role {
  margin: 0.1rem 0 0;
  font-size: 0.95rem;
  color: var(--ink-soft);
}
.board-bio {
  margin-top: 0.4rem;
}
</style>
