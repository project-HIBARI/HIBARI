<script setup>
/**
 * 部品名: サイト共通 — カテゴリ導線カード
 * 用途: ホーム・歩み・ディスコグラフィ・献花などで横並び導線カードを表示する
 */
import PageImageCard from './PageImageCard.vue'

defineProps({
  cards: { type: Array, required: true },
  ariaLabel: { type: String, default: 'コンテンツ一覧' },
  motion: { type: Boolean, default: false },
  homeMotion: { type: Boolean, default: false },
})

const emit = defineEmits(['navigate', 'coming-soon'])

function onClick(card) {
  if (card.action === 'navigate') {
    emit('navigate', card.target)
  } else {
    emit('coming-soon', card.target)
  }
}
</script>

<template>
  <section
    class="site-categories"
    :class="{
      'top-categories': homeMotion,
      'home-motion-stagger': homeMotion,
      'motion-stagger site-reveal-stagger': motion && !homeMotion,
      'motion-section--delay-2': motion && !homeMotion,
    }"
    :aria-label="ariaLabel"
  >
    <button
      v-for="(c, i) in cards"
      :key="c.id"
      type="button"
      class="site-categories__card"
      :class="{
        'top-categories__card': homeMotion,
        'home-category-card': homeMotion,
        'home-motion-stagger__item': homeMotion,
        'stagger-item motion-card': motion && !homeMotion,
      }"
      :style="motion && !homeMotion ? { '--stagger-i': i } : undefined"
      :aria-label="c.title"
      @click="onClick(c)"
    >
      <div class="site-categories__body" :class="{ 'top-categories__body': homeMotion }">
        <h3 class="site-categories__title" :class="{ 'top-categories__title': homeMotion }">{{ c.title }}</h3>
        <p class="site-categories__desc" :class="{ 'top-categories__desc': homeMotion }">{{ c.desc }}</p>
        <span
          class="site-categories__arrow"
          :class="{ 'top-categories__arrow': homeMotion }"
        >›</span>
      </div>
      <div
        class="site-categories__visual"
        :class="{
          'top-categories__visual': homeMotion,
          'home-category-card__visual': homeMotion,
        }"
      >
        <PageImageCard
          :image="c.image"
          :alt="c.alt"
          image-only
          compact
          fit="contain"
        />
      </div>
    </button>
  </section>
</template>

<style scoped>
.site-categories {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  margin-bottom: var(--sp-8);
}
.site-categories__card {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, #fff 0%, #fff9f7 100%);
  box-shadow: var(--site-shadow);
  overflow: hidden;
  cursor: pointer;
  text-align: left;
  padding: 0;
  min-height: 118px;
  transition:
    transform 0.45s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.45s cubic-bezier(0.22, 1, 0.36, 1),
    border-color 0.45s ease;
}
.site-categories__card:not(.home-category-card):hover {
  transform: translateY(-4px);
  box-shadow: var(--site-shadow-md);
  border-color: rgba(122, 80, 136, 0.22);
}
.site-categories__card:not(.home-category-card):hover .site-categories__arrow {
  transform: translateX(3px);
  color: var(--murasaki-700);
}
.site-categories__body {
  flex: 1;
  padding: 18px 14px 18px 18px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}
.site-categories__visual {
  width: 42%;
  min-width: 88px;
  flex-shrink: 0;
  display: flex;
  align-items: stretch;
  background: var(--site-surface-muted);
  overflow: hidden;
}
.home-category-card:hover .site-categories__visual :deep(.page-image-card__img),
.home-category-card:hover .site-categories__visual :deep(img) {
  transform: scale(1.05);
}
.site-categories__visual :deep(.page-image-card__img),
.site-categories__visual :deep(img) {
  transition: transform 0.75s cubic-bezier(0.22, 1, 0.36, 1);
}
.site-categories__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
  line-height: 1.45;
}
.site-categories__desc {
  margin: 0;
  font-size: 11px;
  line-height: 1.55;
  color: var(--site-text-muted);
}
.site-categories__arrow {
  position: absolute;
  right: 12px;
  bottom: 16px;
  font-size: 18px;
  color: var(--murasaki-500);
  line-height: 1;
  transition: transform 0.45s cubic-bezier(0.22, 1, 0.36, 1), color 0.35s ease;
}

@media (max-width: 1200px) {
  .site-categories {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 1024px) {
  .site-categories {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 767px) {
  .site-categories {
    grid-template-columns: 1fr;
  }
  .site-categories__visual {
    min-width: 72px;
  }
}
</style>
