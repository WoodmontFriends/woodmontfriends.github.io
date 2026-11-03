<script setup lang="ts">
// Zeffy donation form (::zeffy-form). Zeffy's embed script finds the [data-zeffy-embed] element
// and sizes the form to fit. If the script can't load (blocked, offline), show Zeffy's plain iframe instead.
const { zeffyFormSlug } = useAppConfig() as { zeffyFormSlug: string }
const fallback = ref(false)
const iframeSrc = `https://www.zeffy.com/embed/donation-form/${zeffyFormSlug}`
const pageUrl = `https://www.zeffy.com/en-US/donation-form/${zeffyFormSlug}`

onMounted(() => {
  const script = document.createElement('script')
  script.src = 'https://www.zeffy.com/embed/v2/zeffy-embed.js'
  script.async = true
  script.onerror = () => { fallback.value = true }
  document.body.appendChild(script)
})
</script>

<template>
  <div class="zeffy">
    <div v-if="!fallback" data-zeffy-embed :data-form-url="`/embed/donation-form/${zeffyFormSlug}`" />
    <div v-else class="zeffy-frame">
      <iframe title="Donation form powered by Zeffy" :src="iframeSrc" allowpaymentrequest allowtransparency="true" />
    </div>
    <p class="zeffy-note">
      Form not showing? <a :href="pageUrl" target="_blank" rel="noopener noreferrer">Donate on Zeffy's site</a>.
    </p>
  </div>
</template>

<style scoped>
.zeffy {
  /* Zeffy's script sets the form to max-width 600px with auto margins, which centers it in a wide
     column. Capping our box at the same width keeps it lined up with the text above. */
  max-width: 600px;
  margin-top: 1.5rem;
}
.zeffy-frame {
  position: relative;
  height: 900px;
  width: 100%;
}
.zeffy-frame iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
}
.zeffy-note {
  margin: 1rem 0 0;
  font-size: 0.9rem;
  color: var(--ink-soft);
}
</style>
