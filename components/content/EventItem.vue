<script setup lang="ts">
defineProps({
  month: { type: String, required: true },
  day: { type: String, required: true },
  weekday: { type: String, default: '' },
  title: { type: String, required: true },
})
</script>

<template>
  <li class="event">
    <div class="date" aria-hidden="true">
      <span class="month">{{ month }}</span>
      <span class="day">{{ day }}</span>
    </div>
    <div class="details">
      <h3 class="event-title">{{ title }}</h3>
      <p class="when">{{ weekday }}, {{ month }} {{ day }}</p>
      <div class="md">
        <ContentSlot :use="$slots.default" />
      </div>
    </div>
  </li>
</template>

<style scoped>
.event {
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
}
.date {
  flex: none;
  width: 4.75rem;
  text-align: center;
  background: var(--hemlock);
  color: var(--on-dark);
  border-radius: 4px;
  padding: 0.55rem 0 0.65rem;
  border-top: 6px solid var(--blaze);
}
.month {
  display: block;
  font-weight: 700;
  font-size: 0.95rem;
}
.day {
  display: block;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 2.1rem;
  line-height: 1;
}
.event-title {
  margin: 0;
  font-size: 1.45rem;
  font-weight: 700;
}
.when {
  margin: 0.15rem 0 0.5rem;
  font-weight: 600;
  color: var(--ink-soft);
}
</style>
