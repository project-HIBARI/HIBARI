<script setup>
/**
 * ページ: 献花・メッセージ（花）
 * 用途: 献花ヒーロー・投稿フォーム・一覧を表示する
 */
import { ref, computed, onMounted } from 'vue'
import MessageHeroSection from './message/MessageHeroSection.vue'
import MessageAnniversaryCards from './message/MessageAnniversaryCards.vue'
import MessageOfferingBlock from './message/MessageOfferingBlock.vue'
import MessageWallGrid from './message/MessageWallGrid.vue'
import MessageAiCard from './message/MessageAiCard.vue'
import MessageRelatedCards from './message/MessageRelatedCards.vue'
import { fetchFlowerOfferings } from '../../api/flowers.js'
import { mapOfferingToCard } from '../../lib/flowers.js'
import { HIBARU_DATA } from '../../data/hibaruData.js'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

const offerings = ref([])
const apiFailed = ref(false)

const wallItems = computed(() => {
  if (apiFailed.value || !offerings.value.length) {
    return HIBARU_DATA.messages.map((m, i) => ({ ...m, id: `fallback-${i}` }))
  }
  return offerings.value
})

const totalCount = computed(() => {
  if (offerings.value.length) return offerings.value.length
  return 128456
})

const monthlyCount = computed(() => {
  if (!offerings.value.length) return 5842
  const now = new Date()
  const y = now.getFullYear()
  const m = now.getMonth() + 1
  return offerings.value.filter((o) => {
    const parts = o.date?.split('.')
    if (!parts || parts.length < 3) return false
    return Number(parts[0]) === y && Number(parts[1]) === m
  }).length
})

function scrollToWall() {
  document.getElementById('message-wall')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function scrollToOffer() {
  document.getElementById('message-offer')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

async function loadOfferings() {
  try {
    const rows = await fetchFlowerOfferings()
    offerings.value = Array.isArray(rows) ? rows.map(mapOfferingToCard) : []
    apiFailed.value = false
  } catch {
    offerings.value = []
    apiFailed.value = true
  }
}

async function onSubmitted() {
  await loadOfferings()
}

onMounted(loadOfferings)
</script>

<template>
  <div class="page-message">
    <MessageHeroSection
      :total-count="totalCount"
      :monthly-count="monthlyCount"
      @open-offer="scrollToOffer"
      @scroll-wall="scrollToWall"
    />

    <MessageAnniversaryCards />

    <div
      id="message-wall"
      class="page-message__wall-layout"
    >
      <MessageOfferingBlock @submitted="onSubmitted" />
      <MessageWallGrid :items="wallItems" />
    </div>

    <MessageAiCard @open-ai="emit('open-modal', 'ai')" />

    <MessageRelatedCards
      @navigate="(id) => emit('navigate', id)"
      @coming-soon="(mode) => emit('open-auth', mode)"
    />
  </div>
</template>

<style scoped>
.page-message {
  color: var(--site-text);
}

.page-message__wall-layout {
  display: grid;
  grid-template-columns: minmax(400px, 480px) minmax(0, 1fr);
  gap: var(--sp-7);
  align-items: start;
  margin-bottom: var(--sp-7);
}

@media (max-width: 1024px) {
  .page-message__wall-layout {
    grid-template-columns: 1fr;
    gap: var(--sp-6);
  }
}
</style>
