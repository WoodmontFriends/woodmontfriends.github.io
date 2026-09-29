<template>
  <figure class="mission">
    <blockquote>
      <p><ContentSlot :use="$slots.default" unwrap="p" /></p>
    </blockquote>
    <figcaption>Our mission, from our Articles of Incorporation</figcaption>
  </figure>
</template>

<style scoped>
.mission {
  margin: 0;
  padding: 0.25rem 0 0.25rem 1.5rem;
  border-left: 6px solid var(--blaze);
}
blockquote {
  margin: 0;
}
blockquote p {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.35rem, 2.6vw, 1.7rem);
  font-weight: 500;
  line-height: 1.35;
  color: var(--hemlock);
}
figcaption {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: var(--ink-soft);
}
</style>
