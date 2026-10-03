<script setup lang="ts">
const { cover, signupUrl, roadmapUrl } = useAppConfig()
const year = new Date().getFullYear()
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
        <a class="header-link" :href="signupUrl" target="_blank" rel="noopener noreferrer">Get updates</a>
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
          <p><a :href="roadmapUrl">See our community roadmap</a></p>
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
.header-link {
  color: var(--on-dark);
  font-weight: 600;
  font-size: 0.95rem;
  white-space: nowrap;
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
