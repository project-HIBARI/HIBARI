<script setup>
/**
 * ページ: 献花・メッセージ（花）
 * 用途: 献花ヒーロー・一覧・モーダルフォームを表示する
 */
import { ref, computed, onMounted } from 'vue'
import MessageHeroSection from './message/MessageHeroSection.vue'
import MessageAnniversaryCards from './message/MessageAnniversaryCards.vue'
import MessageWallGrid from './message/MessageWallGrid.vue'
import MessageOfferingModal from './message/MessageOfferingModal.vue'
import MessageRelatedCards from './message/MessageRelatedCards.vue'
import { fetchFlowerOfferings } from '../../api/flowers.js'
import { mapOfferingToCard } from '../../lib/flowers.js'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { useScrollReveal } from '../../composables/useScrollReveal.js'

const pageRoot = ref(null)
useScrollReveal(pageRoot)

const emit = defineEmits(['navigate', 'open-auth'])

const offerings = ref([])
const apiFailed = ref(false)
const modalOpen = ref(false)

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

function openOffer() {
  modalOpen.value = true
}

function closeOffer() {
  modalOpen.value = false
}

async function onSubmitted() {
  await loadOfferings()
}

onMounted(loadOfferings)
</script>

<template>
  <div ref="pageRoot" class="page-message">
    <MessageHeroSection
      class="motion-section site-reveal site-reveal--slow"
      :total-count="totalCount"
      :monthly-count="monthlyCount"
      @open-offer="openOffer"
      @scroll-wall="scrollToWall"
    />

    <div class="page-message__content">
      <MessageAnniversaryCards class="site-reveal site-reveal--slow site-reveal--delay-1" />
      <MessageWallGrid
        id="message-wall"
        class="site-reveal site-reveal--slow site-reveal--delay-2"
        :items="wallItems"
      />
      <MessageRelatedCards
        class="site-reveal site-reveal--slow site-reveal--delay-3"
        @navigate="(id) => emit('navigate', id)"
        @coming-soon="(mode) => emit('open-auth', mode)"
      />
    </div>

    <MessageOfferingModal
      :open="modalOpen"
      @close="closeOffer"
      @submitted="onSubmitted"
    />
  </div>
</template>

<style scoped>
.page-message {
  color: var(--site-text);
  position: relative;
}

.page-message::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: -1;
  pointer-events: none;
  background:
    radial-gradient(ellipse at 12% 18%, rgba(252, 232, 236, 0.45) 0%, transparent 42%),
    radial-gradient(ellipse at 88% 72%, rgba(245, 235, 224, 0.4) 0%, transparent 45%),
    linear-gradient(180deg, #fffdf9 0%, var(--site-bg-warm) 40%, var(--site-bg) 100%);
}

.page-message__content {
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .page-message__content {
    padding: 0 var(--sp-2);
  }
}
</style>
