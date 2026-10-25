<script setup lang="ts">
// Shows the default slot when the flag is on (or being previewed), otherwise the #off slot.
// While a flag is off, the page also asks search engines not to index it.
const props = defineProps({
  name: { type: String, required: true },
})
const config = useAppConfig() as { features?: Record<string, boolean> }
const enabled = useFeature(props.name)

if (!config.features?.[props.name]) {
  useHead({ meta: [{ name: 'robots', content: 'noindex' }] })
}
</script>

<template>
  <div v-if="enabled">
    <ContentSlot :use="$slots.default" />
  </div>
  <div v-else>
    <ContentSlot :use="$slots.off" />
  </div>
</template>
