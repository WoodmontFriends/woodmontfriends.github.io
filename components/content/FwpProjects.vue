<script setup lang="ts">
// Public projects board: cards the board labels "public" in the admin app, read in the browser
// from admin.woodmontfriends.org/api/public/board, so the site never needs a rebuild when it changes.
type Column = 'planned' | 'inProgress' | 'done'
interface PublicCard {
  id: string
  title: string
  column: Column
  target: string // YYYY-MM or ''
  topics: string[]
  updated: string
}
interface PublicBoard {
  updatedAt: string
  columns: Record<Column, PublicCard[]>
}

const { publicBoardUrl, email } = useAppConfig() as { publicBoardUrl: string; email: string }
const board = ref<PublicBoard | null>(null)
const state = ref<'loading' | 'ready' | 'error'>('loading')

const columns: { key: Column; title: string; empty: string }[] = [
  { key: 'planned', title: 'Planned', empty: 'Nothing new on deck yet.' },
  { key: 'inProgress', title: 'In progress', empty: 'Nothing underway right now.' },
  { key: 'done', title: 'Recently done', empty: 'Nothing finished in the last two months.' },
]

const total = computed(() => (board.value ? columns.reduce((n, c) => n + board.value!.columns[c.key].length, 0) : 0))

function month(target: string) {
  const d = new Date(`${target}-15T12:00:00`)
  return Number.isNaN(d.getTime()) ? '' : d.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
}

onMounted(async () => {
  try {
    const res = await fetch(publicBoardUrl, { headers: { accept: 'application/json' } })
    if (!res.ok) throw new Error(String(res.status))
    board.value = (await res.json()) as PublicBoard
    state.value = 'ready'
  } catch {
    state.value = 'error'
  }
})
</script>

<template>
  <div class="projects" :aria-busy="state === 'loading'">
    <p v-if="state === 'error'" class="note">
      We couldn't load our project list just now. Please try again in a few minutes, or email
      <a :href="`mailto:${email}`">{{ email }}</a> to ask what we're working on.
    </p>
    <p v-else-if="state === 'ready' && total === 0" class="note">Nothing scheduled yet. Check back soon!</p>
    <div v-else class="columns">
      <section v-for="col in columns" :key="col.key" class="column" :aria-labelledby="`col-${col.key}`">
        <h3 :id="`col-${col.key}`" class="column-title">
          {{ col.title }}
          <span v-if="board" class="count">{{ board.columns[col.key].length }}</span>
        </h3>
        <ul v-if="state === 'loading'" class="cards" aria-hidden="true">
          <li v-for="n in 2" :key="n" class="card skeleton" />
        </ul>
        <ul v-else-if="board && board.columns[col.key].length" class="cards">
          <li v-for="card in board.columns[col.key]" :key="card.id" class="card" :class="`in-${col.key}`">
            <p class="card-title">{{ card.title }}</p>
            <p v-if="card.target && col.key !== 'done'" class="target">Target: {{ month(card.target) }}</p>
            <ul v-if="card.topics.length" class="topics">
              <li v-for="t in card.topics" :key="t" class="topic">{{ t }}</li>
            </ul>
          </li>
        </ul>
        <p v-else class="empty">{{ col.empty }}</p>
      </section>
    </div>
  </div>
</template>

<style scoped>
.projects {
  margin-top: 2rem;
}
.columns {
  display: grid;
  gap: 2rem;
}
@media (min-width: 860px) {
  .columns {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1.5rem;
  }
}
.column-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.35rem;
  margin: 0 0 0.85rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--blaze);
}
.count {
  font-family: var(--font-body);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--ink-soft);
  background: var(--fern);
  border-radius: 999px;
  padding: 0.05rem 0.55rem;
}
.cards {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.75rem;
}
.card {
  background: var(--paper);
  border: 1px solid var(--rule);
  border-left: 4px solid var(--hemlock);
  border-radius: 4px;
  padding: 0.8rem 1rem;
}
.card.in-done {
  border-left-color: var(--rule);
}
.card-title {
  margin: 0;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.35;
}
.in-done .card-title::before {
  content: '✓ ';
  color: var(--hemlock);
}
.target {
  margin: 0.3rem 0 0;
  font-size: 0.9rem;
  color: var(--ink-soft);
}
.topics {
  list-style: none;
  margin: 0.55rem 0 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}
.topic {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--hemlock);
  background: var(--fern);
  border-radius: 999px;
  padding: 0.1rem 0.6rem;
}
.empty,
.note {
  margin: 0;
  color: var(--ink-soft);
}
.skeleton {
  height: 4.25rem;
  background: linear-gradient(90deg, var(--fern), #f6f9f5, var(--fern));
  background-size: 200% 100%;
  animation: shimmer 1.4s ease-in-out infinite;
  border-left-color: var(--rule);
}
@keyframes shimmer {
  to {
    background-position: -200% 0;
  }
}
@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation: none;
  }
}
</style>
