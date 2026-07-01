<script setup>
/**
 * ページ: ホーム（top）
 * 構成: ヒーロー / サブスク・ニュース・イベント / カテゴリ導線 / 楽しみ方
 */
import TopHeroSection from './top/TopHeroSection.vue'
import TopSubscriptionCard from './top/TopSubscriptionCard.vue'
import TopNewsPanel from './top/TopNewsPanel.vue'
import TopEventsPanel from './top/TopEventsPanel.vue'
import TopCategoryCards from './top/TopCategoryCards.vue'
import TopEnjoyGuide from './top/TopEnjoyGuide.vue'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

function scrollToEnjoy() {
  const el = document.getElementById('home-enjoy-guide')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function onGuideNavigate(target) {
  if (target === 'ai') {
    emit('open-modal', 'ai')
  } else {
    emit('navigate', target)
  }
}

function onComingSoon(mode) {
  emit('open-auth', mode)
}
</script>

<template>
  <div class="page-top">
    <TopHeroSection
      @open-auth="(m) => emit('open-auth', m)"
      @scroll-enjoy="scrollToEnjoy"
      @open-ai="emit('open-modal', 'ai')"
    />

    <section class="page-top__columns" aria-label="おすすめと最新情報">
      <TopSubscriptionCard @open-detail="emit('open-modal', 'fanclub')" />
      <TopNewsPanel @open-all="emit('open-auth', 'news')" />
      <TopEventsPanel @open-all="emit('open-auth', 'events')" />
    </section>

    <TopCategoryCards @navigate="(id) => emit('navigate', id)" @coming-soon="onComingSoon" />

    <TopEnjoyGuide @navigate="onGuideNavigate" />
  </div>
</template>

<style scoped>
.page-top__columns {
  display: grid;
  grid-template-columns: 1.1fr 1fr 1fr;
  gap: 20px;
  margin-bottom: var(--sp-8);
  align-items: stretch;
}

@media (max-width: 1024px) {
  .page-top__columns {
    grid-template-columns: 1fr;
  }
}
</style>
