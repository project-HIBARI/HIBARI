<script setup>
/**
 * 部品名: ホーム — 下部カテゴリ導線カード
 * 用途: 各ページや準備中機能への誘導カード5枚を横並びで表示する
 */
import PageImageCard from '../../common/PageImageCard.vue'
import { PAGE_IMAGES } from '../../../lib/pageImages.js'

const emit = defineEmits(['navigate', 'coming-soon'])

const cards = [
  {
    id: 'profile',
    title: '美空ひばりについて',
    desc: '彼女の人生と軌跡',
    image: PAGE_IMAGES.about,
    alt: '美空ひばりについて',
    action: 'navigate',
    target: 'profile',
  },
  {
    id: 'disco',
    title: 'ディスコグラフィー',
    desc: '楽曲・アルバム一覧',
    image: PAGE_IMAGES.disco,
    alt: 'ディスコグラフィー',
    action: 'navigate',
    target: 'disco',
  },
  {
    id: 'gallery',
    title: 'ギャラリー',
    desc: '写真でたどる軌跡',
    image: PAGE_IMAGES.gallery,
    alt: 'ギャラリー',
    action: 'coming-soon',
    target: 'gallery',
  },
  {
    id: 'events',
    title: 'イベント情報',
    desc: 'コンサート・企画展など',
    image: PAGE_IMAGES.events,
    alt: 'イベント情報',
    action: 'coming-soon',
    target: 'events',
  },
  {
    id: 'fanclub',
    title: 'ファンクラブ',
    desc: '入会・会員特典',
    image: PAGE_IMAGES.fanclub,
    alt: 'ファンクラブ',
    action: 'modal',
    target: 'fanclub',
  },
]

function onClick(card) {
  if (card.action === 'navigate') {
    emit('navigate', card.target)
  } else {
    emit('coming-soon', card.target)
  }
}
</script>

<template>
  <section class="top-categories" aria-label="コンテンツ一覧">
    <button
      v-for="c in cards"
      :key="c.id"
      type="button"
      class="top-categories__card"
      :aria-label="c.title"
      @click="onClick(c)"
    >
      <div class="top-categories__body">
        <h3 class="top-categories__title">{{ c.title }}</h3>
        <p class="top-categories__desc">{{ c.desc }}</p>
        <span class="top-categories__arrow">›</span>
      </div>
      <div class="top-categories__visual">
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
.top-categories {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  margin-bottom: var(--sp-8);
}
.top-categories__card {
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
  transition: transform 0.2s, box-shadow 0.2s;
}
.top-categories__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.top-categories__body {
  flex: 1;
  padding: 18px 14px 18px 18px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}
.top-categories__visual {
  width: 42%;
  min-width: 88px;
  flex-shrink: 0;
  display: flex;
  align-items: stretch;
  background: var(--site-surface-muted);
  overflow: hidden;
}
.top-categories__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
  line-height: 1.45;
}
.top-categories__desc {
  margin: 0;
  font-size: 11px;
  line-height: 1.55;
  color: var(--site-text-muted);
}
.top-categories__arrow {
  position: absolute;
  right: 12px;
  bottom: 16px;
  font-size: 18px;
  color: var(--murasaki-500);
  line-height: 1;
}

@media (max-width: 1200px) {
  .top-categories {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 1024px) {
  .top-categories {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 767px) {
  .top-categories {
    grid-template-columns: 1fr;
  }
  .top-categories__visual {
    min-width: 72px;
  }
}
</style>
