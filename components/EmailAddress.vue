<script setup lang="ts">
// Shows the address as text with a copy button, because a mailto link
// does nothing on computers without a mail app set up.
const { email } = useAppConfig()
const copied = ref(false)

async function copy() {
  try {
    await navigator.clipboard.writeText(email)
  } catch {
    const field = document.createElement('textarea')
    field.value = email
    document.body.appendChild(field)
    field.select()
    document.execCommand('copy')
    field.remove()
  }
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>

<template>
  <span class="email-address">
    <a :href="`mailto:${email}`">{{ email }}</a>
    <button type="button" class="copy" @click="copy">
      {{ copied ? 'Copied' : 'Copy' }}
    </button>
    <span class="visually-hidden" aria-live="polite">{{ copied ? 'Email address copied' : '' }}</span>
  </span>
</template>

<style scoped>
.email-address {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem 0.75rem;
}
a {
  color: inherit;
  font-weight: 600;
  overflow-wrap: anywhere;
}
.copy {
  font: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1;
  padding: 0.4rem 0.7rem;
  min-width: 4.5rem;
  color: inherit;
  background: transparent;
  border: 1.5px solid currentColor;
  border-radius: 4px;
  cursor: pointer;
  opacity: 0.85;
}
.copy:hover {
  opacity: 1;
}
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
}
</style>
