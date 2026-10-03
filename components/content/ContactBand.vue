<script setup lang="ts">
defineProps({
  id: { type: String, default: 'contact' },
  title: { type: String, required: true },
})
const { signupUrl } = useAppConfig()
</script>

<template>
  <section :id="id" class="band on-dark">
    <div class="wrap">
      <h2 class="band-title">{{ title }}</h2>
      <div class="band-body">
        <ContentSlot :use="$slots.default" unwrap="p" />
      </div>
      <a class="btn btn-blaze" :href="signupUrl" target="_blank" rel="noopener noreferrer">Sign up for updates</a>
      <p class="band-email">Or email us at <EmailAddress /></p>
    </div>
  </section>
</template>

<style scoped>
.band {
  background: var(--hemlock);
  color: var(--on-dark);
  padding: clamp(3rem, 7vw, 4.5rem) 0;
  scroll-margin-top: 1rem;
}
.band-title {
  margin: 0 0 0.75rem;
  max-width: 34rem;
  color: var(--on-dark);
  font-size: clamp(1.85rem, 4vw, 2.5rem);
  font-weight: 700;
}
.band-body {
  margin: 0 0 1.75rem;
  max-width: 36rem;
  font-size: 1.1rem;
  color: var(--on-dark-soft);
}
.band-email {
  margin: 1.5rem 0 0;
  color: var(--on-dark-soft);
}
.band-email :deep(a) {
  color: var(--on-dark);
}
</style>
