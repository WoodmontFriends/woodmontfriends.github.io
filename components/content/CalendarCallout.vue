<script setup lang="ts">
// "Add our calendar" call-out: one-tap subscribe links for the public FWP Community Events
// calendar. Body text (optional) is the slot; the links are built from communityCalendarId.
defineProps({
  id: { type: String, default: 'calendar' }, // anchor, e.g. the home hero links to #calendar
  title: { type: String, default: 'Add our calendar' },
  compact: { type: Boolean, default: false }, // narrower card for a side column
})
const { google, ics, web } = useCommunityCalendar()
</script>

<template>
  <aside :id="id" class="callout" :class="{ compact }" aria-labelledby="calendar-callout-title">
    <span class="mark" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="4.5" width="18" height="16.5" rx="2" />
        <path d="M3 9.5h18M8 2.5v4M16 2.5v4" />
        <path d="m9 15 2 2 4-4" />
      </svg>
    </span>
    <div class="body">
      <h3 id="calendar-callout-title" class="title">{{ title }}</h3>
      <div class="text">
        <ContentSlot :use="$slots.default" unwrap="p" />
      </div>
      <div class="actions">
        <a class="btn btn-blaze" :href="google" target="_blank" rel="noopener noreferrer">Add to Google Calendar</a>
        <a class="btn btn-outline" :href="ics">Apple or Outlook</a>
        <a class="view" :href="web" target="_blank" rel="noopener noreferrer">View the calendar</a>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.callout {
  scroll-margin-top: 1.5rem;
  display: flex;
  gap: 1.1rem;
  align-items: flex-start;
  margin: 2rem 0 0;
  padding: 1.4rem 1.5rem;
  background: var(--hemlock);
  color: var(--on-dark);
  border-radius: 6px;
  border-left: 6px solid var(--blaze);
  max-width: 46rem;
}
.mark {
  flex: none;
  color: var(--blaze);
  margin-top: 0.15rem;
}
.title {
  color: #fff;
  font-size: 1.45rem;
  margin: 0 0 0.35rem;
}
.text {
  color: var(--on-dark-soft);
  margin: 0 0 1rem;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.6rem 0.9rem;
}
.btn-outline {
  color: var(--on-dark);
  border-color: rgba(233, 240, 234, 0.45);
}
.btn-outline:hover {
  border-color: var(--on-dark);
}
.view {
  color: var(--on-dark);
  font-weight: 600;
}
.compact {
  flex-direction: column;
  gap: 0.6rem;
  margin: 0;
  padding: 1.2rem 1.25rem;
}
.compact .title {
  font-size: 1.25rem;
}
.compact .text {
  font-size: 0.95rem;
}
.compact .actions .btn {
  width: 100%;
  justify-content: center;
}
@media (max-width: 520px) {
  .callout {
    flex-direction: column;
    padding: 1.2rem;
  }
  .actions .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
