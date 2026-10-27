<script setup lang="ts">
const { cover, signupUrl } = useAppConfig()
const year = new Date().getFullYear()
const parkModel = useFeature('parkModel')

// Phones get a Menu button; wider screens show the links in a row. Close the menu on navigation and Escape.
const menuOpen = ref(false)
const route = useRoute()
watch(() => route.fullPath, () => { menuOpen.value = false })
function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape' && menuOpen.value) menuOpen.value = false
}
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <div class="site">
    <Html lang="en" />
    <Meta property="og:image" :content="cover" />
    <a class="skip-link" href="#main">Skip to content</a>

    <header class="site-header on-dark">
      <div class="wrap header-inner">
        <NuxtLink to="/" class="brand">
          <span class="blaze" aria-hidden="true" />
          <span>Friends of Woodmont Park</span>
        </NuxtLink>
        <button
          type="button"
          class="menu-toggle"
          :aria-expanded="menuOpen"
          aria-controls="site-nav"
          @click="menuOpen = !menuOpen"
        >
          <span class="menu-icon" :class="{ open: menuOpen }" aria-hidden="true"><i /><i /><i /></span>
          <span class="menu-label">{{ menuOpen ? 'Close' : 'Menu' }}</span>
        </button>
        <nav id="site-nav" class="header-links" :class="{ open: menuOpen }" aria-label="Site">
          <NuxtLink class="header-link" to="/projects">Projects</NuxtLink>
          <NuxtLink class="header-link" to="/nature">Nature map</NuxtLink>
          <NuxtLink v-if="parkModel" class="header-link" to="/explore">Explore in 3D</NuxtLink>
          <NuxtLink class="header-link" to="/board">Board portal</NuxtLink>
          <a class="header-link" :href="signupUrl" target="_blank" rel="noopener noreferrer">Get updates</a>
        </nav>
      </div>
    </header>

    <main id="main">
      <slot />
    </main>

    <footer class="site-footer">
      <div class="wrap footer-inner">
        <div class="footer-about">
          <p class="footer-name">
            <span class="blaze" aria-hidden="true" />
            Friends of Woodmont Park
          </p>
          <p>
            A Virginia nonstock corporation serving the Woodmont neighborhood of North Chesterfield, VA.
            Our 501(c)(3) application is pending, so donations are not yet tax-deductible.
          </p>
          <p><EmailAddress /></p>
          <p><NuxtLink to="/projects">See what we're working on</NuxtLink></p>
          <p><NuxtLink to="/board">Board portal sign-in</NuxtLink></p>
        </div>
        <div class="footer-partners">
          <h2 class="footer-heading">Community partners</h2>
          <ul>
            <li><a href="https://woodmont4fun.org">Woodmont Recreation Association</a></li>
            <li><a href="https://woodmontbonair.com">Woodmont Civic Association</a></li>
          </ul>
        </div>
      </div>
      <div class="wrap footer-legal">
        <p>&copy; {{ year }} Friends of Woodmont Park</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0.5rem;
  z-index: 10;
  background: var(--blaze);
  color: var(--hemlock-deep);
  padding: 0.5rem 1rem;
  font-weight: 700;
}
.skip-link:focus {
  left: 0.5rem;
}

.site-header {
  background: var(--hemlock);
  color: var(--on-dark);
}
.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  min-height: 4rem;
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--on-dark);
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.15rem;
  text-decoration: none;
}
.header-links {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.25rem 1.25rem;
}
.header-link {
  color: var(--on-dark);
  font-weight: 600;
  font-size: 0.95rem;
  white-space: nowrap;
}
.menu-toggle {
  display: none;
}
/* Phones and small tablets: a Menu button opens the links as a full-width list under the bar. */
@media (max-width: 759px) {
  .header-inner {
    flex-wrap: wrap;
    gap: 0;
  }
  .brand {
    min-height: 3.5rem;
    font-size: 1.05rem;
  }
  .menu-toggle {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    min-height: 2.75rem;
    padding: 0 0.85rem;
    margin-right: -0.5rem;
    border: 1px solid rgba(233, 240, 234, 0.35);
    border-radius: 8px;
    background: transparent;
    color: var(--on-dark);
    font: 600 0.95rem var(--font-body);
    cursor: pointer;
  }
  .menu-icon {
    display: inline-grid;
    gap: 3px;
    width: 1rem;
  }
  .menu-icon i {
    display: block;
    height: 2px;
    border-radius: 1px;
    background: currentColor;
    transition: transform 0.2s, opacity 0.2s;
  }
  .menu-icon.open i:nth-child(1) {
    transform: translateY(5px) rotate(45deg);
  }
  .menu-icon.open i:nth-child(2) {
    opacity: 0;
  }
  .menu-icon.open i:nth-child(3) {
    transform: translateY(-5px) rotate(-45deg);
  }
  .header-links {
    display: none;
    flex-basis: 100%;
    flex-direction: column;
    flex-wrap: nowrap;
    gap: 0;
    padding-bottom: 0.5rem;
  }
  .header-links.open {
    display: flex;
  }
  .header-link {
    display: flex;
    align-items: center;
    min-height: 3rem;
    border-top: 1px solid rgba(233, 240, 234, 0.14);
    font-size: 1.05rem;
    text-decoration: none;
  }
  .header-link.router-link-active {
    color: var(--blaze);
  }
}
/* The narrowest phones: keep the name and the button on one line; the label stays for screen readers. */
@media (max-width: 380px) {
  .brand {
    gap: 0.5rem;
    font-size: 0.98rem;
  }
  .menu-toggle {
    padding: 0 0.75rem;
  }
  .menu-label {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip-path: inset(50%);
    white-space: nowrap;
  }
}
@media (prefers-reduced-motion: reduce) {
  .menu-icon i {
    transition: none;
  }
}

.site-footer {
  background: var(--fern);
  color: var(--ink-soft);
  font-size: 0.95rem;
  padding-top: 3rem;
}
.footer-inner {
  display: grid;
  gap: 2rem;
}
@media (min-width: 720px) {
  .footer-inner {
    grid-template-columns: 2fr 1fr;
  }
}
.footer-inner p {
  margin: 0 0 0.75rem;
  max-width: 34rem;
}
.footer-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.15rem;
  color: var(--hemlock);
}
.footer-heading {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 0 0 0.6rem;
}
.footer-partners ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.footer-partners li + li {
  margin-top: 0.4rem;
}
.footer-legal {
  margin-top: 2rem;
  padding-top: 1.25rem;
  padding-bottom: 2rem;
  border-top: 1px solid var(--rule);
  font-size: 0.85rem;
}
.footer-legal p {
  margin: 0;
}
</style>
