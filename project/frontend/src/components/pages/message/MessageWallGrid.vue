<script setup>
/**
 * 部品名: 献花 — 寄せられたメッセージ一覧（ガラス風カード）
 */
import { ref, computed, watch, nextTick } from 'vue'
import { flowerByName } from '../../../lib/flowers.js'
import FlowerCutout from './FlowerCutout.vue'
import UiButton from '../../ui/UiButton.vue'
import { aosAttrs, refreshAosHard } from '../../../lib/aos.js'

const PAGE_SIZE = 12

const props = defineProps({
  items: {
    type: Array,
    default: () => [],
  },
})

const page = ref(1)
const wallRoot = ref(null)

const sorted = computed(() =>
  [...props.items].sort((a, b) => {
    const da = new Date(a.date?.replace(/\./g, '-') || 0).getTime()
    const db = new Date(b.date?.replace(/\./g, '-') || 0).getTime()
    return db - da
  }),
)

const totalPages = computed(() => Math.max(1, Math.ceil(sorted.value.length / PAGE_SIZE)))

const paginatedItems = computed(() => {
  const start = (page.value - 1) * PAGE_SIZE
  return sorted.value.slice(start, start + PAGE_SIZE)
})

watch(
  () => props.items.length,
  () => {
    page.value = 1
    nextTick(() => refreshAosHard())
  },
)

watch(totalPages, (nextTotal) => {
  if (page.value > nextTotal) {
    page.value = nextTotal
  }
})

function scrollToListTop() {
  wallRoot.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function changePage(next) {
  if (next < 1 || next > totalPages.value || next === page.value) return
  page.value = next
  nextTick(() => {
    scrollToListTop()
    refreshAosHard()
  })
}

function goPrev() {
  changePage(page.value - 1)
}

function goNext() {
  changePage(page.value + 1)
}
</script>

<template>
  <section ref="wallRoot" class="msg-wall" aria-labelledby="msg-wall-title">
    <header class="msg-wall__head" v-bind="aosAttrs()">
      <h2 id="msg-wall-title" class="msg-wall__title">みなさんの献花・メッセージ</h2>
      <p class="msg-wall__sort" aria-label="並び順">新しい順</p>
    </header>

    <div v-if="sorted.length" class="msg-wall__grid">
      <article
        v-for="(m, i) in paginatedItems"
        :key="m.id ?? `${page}-${i}`"
        class="msg-wall__card"
        v-bind="aosAttrs(i * 80)"
      >
        <div class="msg-wall__flower">
          <FlowerCutout :src="flowerByName(m.flower).image" :alt="m.flower" size="sm" />
          <span class="msg-wall__flower-name">{{ m.flower }}</span>
        </div>
        <div class="msg-wall__body-wrap">
          <p class="msg-wall__body">{{ m.body }}</p>
          <footer class="msg-wall__meta">
            <span class="msg-wall__author">{{ m.name }}</span>
            <span v-if="m.location" class="msg-wall__location">{{ m.location }}</span>
            <time class="msg-wall__date" :datetime="m.date">{{ m.date }}</time>
          </footer>
        </div>
      </article>
    </div>

    <nav
      v-if="sorted.length"
      class="msg-wall__pager"
      aria-label="献花・メッセージのページ送り"
    >
      <UiButton variant="outline" size="sm" aos :disabled="page <= 1" @click="goPrev">
        前へ
      </UiButton>
      <span class="msg-wall__pager-info" aria-live="polite">
        {{ page }} / {{ totalPages }}
      </span>
      <UiButton variant="outline" size="sm" aos :disabled="page >= totalPages" @click="goNext">
        次へ
      </UiButton>
    </nav>

    <p v-else class="msg-wall__empty">まだ献花はありません。最初の想いを届けてみませんか。</p>
  </section>
</template>

<style scoped>
.msg-wall {
  margin-bottom: var(--sp-7);
  scroll-margin-top: 96px;
}

.msg-wall__head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-6);
  flex-wrap: wrap;
}

.msg-wall__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(1.25rem, 2.4vw, 1.625rem);
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--site-text);
}

.msg-wall__sort {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: var(--font-size-badge);
  letter-spacing: 0.2em;
  color: var(--kin-600);
}

.msg-wall__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-5);
}

.msg-wall__card {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  padding: var(--sp-5);
  border-radius: 24px;
  background: color-mix(in srgb, var(--site-surface) 68%, transparent);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid color-mix(in srgb, var(--site-border) 80%, rgba(255, 255, 255, 0.6));
  box-shadow: 0 10px 32px rgba(59, 47, 42, 0.06);
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.4s ease;
  overflow: hidden;
}

.msg-wall__card:hover {
  transform: scale(1.02);
  box-shadow: 0 18px 48px rgba(59, 47, 42, 0.1);
}

.msg-wall__flower {
  display: flex;
  align-items: flex-end;
  gap: var(--sp-3);
  min-height: 124px;
}

.msg-wall__card:hover :deep(.flower-cutout__img) {
  transform: scale(1.06);
}

.msg-wall__card :deep(.flower-cutout__img) {
  transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
}

.msg-wall__flower-name {
  font-family: var(--ff-mincho);
  font-size: var(--font-size-button);
  letter-spacing: 0.1em;
  color: var(--murasaki-700);
}

.msg-wall__body-wrap {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: var(--sp-4);
}

.msg-wall__body {
  margin: 0;
  font-size: var(--font-size-small);
  line-height: 1.95;
  color: var(--site-text);
  flex: 1;
}

.msg-wall__meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 10px;
  font-size: var(--font-size-caption);
  color: var(--site-text-light);
  letter-spacing: 0.06em;
  padding-top: var(--sp-3);
  border-top: 1px solid color-mix(in srgb, var(--site-border) 70%, transparent);
}

.msg-wall__author {
  font-family: var(--ff-mincho);
  color: var(--site-text-muted);
}

.msg-wall__location::before {
  content: '·';
  margin-right: 10px;
}

.msg-wall__date {
  margin-left: auto;
  font-family: var(--ff-mono);
}

.msg-wall__empty {
  margin: 0;
  padding: var(--sp-8) var(--sp-5);
  text-align: center;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-small);
  line-height: 1.9;
  color: var(--site-text-muted);
  border-radius: 24px;
  background: color-mix(in srgb, var(--site-surface) 60%, transparent);
  border: 1px dashed var(--site-border);
}

.msg-wall__pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-4);
  margin-top: var(--sp-6);
  padding-top: var(--sp-4);
}

.msg-wall__pager-info {
  min-width: 4.5em;
  text-align: center;
  font-family: var(--ff-mono);
  font-size: var(--font-size-caption);
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
}

@media (max-width: 1024px) {
  .msg-wall__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .msg-wall__grid {
    grid-template-columns: 1fr;
    gap: var(--sp-4);
  }
  .msg-wall__card {
    padding: var(--sp-5) var(--sp-4);
  }
}
</style>
