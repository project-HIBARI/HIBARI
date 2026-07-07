<script setup>
/**
 * ページ: ホーム（top）
 * 構成: ヒーロー / 3カラム / カテゴリ導線 / 楽しみ方
 */
import TopHeroSection from './top/TopHeroSection.vue'
import TopMainPanels from './top/TopMainPanels.vue'
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
    <div class="page-top__hero-wrap">
      <TopHeroSection
        @open-auth="(m) => emit('open-auth', m)"
        @scroll-enjoy="scrollToEnjoy"
        @open-ai="emit('open-modal', 'ai')"
      />
    </div>

    <div class="page-top__body">
      <TopMainPanels
        @open-fanclub="emit('open-modal', 'fanclub')"
        @open-news="emit('open-auth', 'news')"
        @open-events="emit('open-auth', 'events')"
      />

      <TopCategoryCards @navigate="(id) => emit('navigate', id)" @coming-soon="onComingSoon" />

      <TopEnjoyGuide @navigate="onGuideNavigate" />
    </div>
  </div>
</template>

<style scoped>
.page-top {
  --site-max: 1400px;
  --main-pad-x: 64px;
}

.page-top__hero-wrap {
  --bleed: max(
    var(--main-pad-x),
    calc((100vw - min(100vw, var(--site-max))) / 2 + var(--main-pad-x))
  );
  width: calc(100% + 2 * var(--bleed));
  margin-inline: calc(-1 * var(--bleed));
  margin-bottom: var(--sp-8);
}

.page-top__body {
  display: flex;
  flex-direction: column;
  gap: var(--sp-8);
}

@media (max-width: 767px) {
  .page-top {
    --main-pad-x: 16px;
  }
  .page-top__hero-wrap {
    margin-bottom: var(--sp-6);
  }
  .page-top__body {
    gap: var(--sp-6);
  }
}

@media (max-width: 480px) {
  .page-top {
    --main-pad-x: 12px;
  }
}
</style>
