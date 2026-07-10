<script setup>
/**
 * ページ: ホーム（top）
 */
import { ref } from 'vue'
import TopHeroSection from './top/TopHeroSection.vue'
import TopQuickNav from './top/TopQuickNav.vue'
import TopSpotlight from './top/TopSpotlight.vue'
import TopVideoPromo from './top/TopVideoPromo.vue'
import TopEnjoyGuide from './top/TopEnjoyGuide.vue'
import TopSubscriptionCard from './top/TopSubscriptionCard.vue'
import TopNewsPanel from './top/TopNewsPanel.vue'
import TopEventsPanel from './top/TopEventsPanel.vue'
import TopCategoryCards from './top/TopCategoryCards.vue'
import { useHomeMotion } from '../../composables/useHomeMotion.js'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal', 'use-feature'])

const pageRoot = ref(null)
useHomeMotion(pageRoot)

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

function onEnjoyNavigate(target) {
  if (target === 'ai') {
    emit('open-modal', 'ai')
    return
  }
  emit('navigate', target)
}
</script>

<template>
  <div ref="pageRoot" class="page-top">
    <TopHeroSection
      @open-auth="(m) => emit('open-auth', m)"
      @open-ai="emit('open-modal', 'ai')"
      @scroll-enjoy="scrollToEnjoy"
    />

    <TopQuickNav
      @navigate="(id) => emit('navigate', id)"
      @open-auth="(m) => emit('open-auth', m)"
    />

    <TopSpotlight @navigate="(id) => emit('navigate', id)" />

    <TopVideoPromo class="page-top__promo home-motion-stagger__item" />

    <TopEnjoyGuide
      class="page-top__enjoy"
      @navigate="onEnjoyNavigate"
    />

    <div class="page-top__body">
      <section
        class="page-top__columns home-motion-stagger"
        aria-label="おすすめと最新情報"
      >
        <div class="page-top__panel home-motion-stagger__item">
          <TopSubscriptionCard
            @open-detail="emit('open-modal', 'fanclub')"
            @use-feature="(f) => emit('use-feature', f)"
          />
        </div>
        <div class="page-top__panel home-motion-stagger__item">
          <TopNewsPanel
            @navigate="(id) => emit('navigate', id)"
            @need-auth="(m) => emit('open-auth', m)"
          />
        </div>
        <div class="page-top__panel home-motion-stagger__item">
          <TopEventsPanel
            @open-all="emit('open-modal', 'events')"
            @need-auth="(m) => emit('open-auth', m)"
          />
        </div>
      </section>

      <TopCategoryCards
        @navigate="(id) => emit('navigate', id)"
        @coming-soon="onComingSoon"
      />
    </div>
  </div>
</template>

<style scoped>
.page-top__body {
  overflow-x: clip;
}
.page-top__promo {
  margin-bottom: var(--sp-8);
}
.page-top__enjoy {
  margin-bottom: var(--sp-7);
  padding: 0 var(--sp-6);
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}
.page-top__columns {
  display: grid;
  grid-template-columns: 1.15fr 1fr 1fr;
  gap: 22px;
  margin-bottom: var(--sp-8);
  align-items: stretch;
}
.page-top__panel {
  min-width: 0;
  height: 100%;
}
.page-top__panel > :deep(.ui-card),
.page-top__panel > :deep(.top-subscription),
.page-top__panel > :deep(.top-news),
.page-top__panel > :deep(.top-events) {
  height: 100%;
}

@media (max-width: 1024px) {
  .page-top__columns {
    grid-template-columns: 1fr;
  }
}
</style>
