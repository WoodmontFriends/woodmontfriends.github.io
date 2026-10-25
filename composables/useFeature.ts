// Feature flags live in app.config.ts under `features`.
// A flag that's off can still be previewed in one browser by visiting a page with
// ?flag=<flagName> (remembered on that device); ?flag=off clears it.
export function useFeature(name: string) {
  const config = useAppConfig() as { features?: Record<string, boolean> }
  const route = useRoute()
  const enabled = ref(Boolean(config.features?.[name]))

  onMounted(() => {
    if (enabled.value) return
    const key = `fwp-preview:${name}`
    const preview = route.query.flag
    try {
      if (preview === name) localStorage.setItem(key, '1')
      if (preview === 'off') localStorage.removeItem(key)
      if (localStorage.getItem(key)) enabled.value = true
    } catch {
      // Storage can be blocked (private windows); the query string still works for this visit.
    }
    if (preview === name) enabled.value = true
  })

  return enabled
}
