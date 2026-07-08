<script setup>
/**
 * ページ: ホーム（top）
 * 構成: ヒーロー / サブスク・ニュース・イベント / カテゴリ導線
 */
import TopHeroSection from './top/TopHeroSection.vue'
import TopSubscriptionCard from './top/TopSubscriptionCard.vue'
import TopNewsPanel from './top/TopNewsPanel.vue'
import TopEventsPanel from './top/TopEventsPanel.vue'
import TopCategoryCards from './top/TopCategoryCards.vue'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

function scrollToEnjoy() {
  const el = document.getElementById('home-enjoy-guide')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function onComingSoon(target) {
  if (target === 'fanclub') {
    emit('open-modal', 'fanclub')
  } else {
    emit('open-auth', target)
  }
}
</script>

<template>
  <div class="page-top">
    <TopHeroSection
      @open-auth="(m) => emit('open-auth', m)"
      @scroll-enjoy="scrollToEnjoy"
    />

    <div class="page-top__body">
      <section class="page-top__columns" aria-label="おすすめと最新情報">
        <TopSubscriptionCard
          @open-detail="emit('open-modal', 'fanclub')"
          @use-feature="(f) => emit('open-auth', f)"
        />
        <TopNewsPanel
          @open-all="emit('open-modal', 'news')"
          @need-auth="(m) => emit('open-auth', m)"
        />
        <TopEventsPanel
          @open-all="emit('open-modal', 'events')"
          @need-auth="(m) => emit('open-auth', m)"
        />
      </section>

      <TopCategoryCards @navigate="(id) => emit('navigate', id)" @coming-soon="onComingSoon" />
    </div>
  </div>
</template>

<style scoped>
.page-top__body {
  overflow-x: clip;
}
.page-top__columns {
  display: grid;
  grid-template-columns: 1.15fr 1fr 1fr;
  gap: 22px;
  margin-bottom: var(--sp-8);
  align-items: stretch;
}

@media (max-width: 1024px) {
  .page-top__columns {
    grid-template-columns: 1fr;
  }
}
</style>
