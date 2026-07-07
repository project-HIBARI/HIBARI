<script setup>
/**
 * 部品名: 歩み — 下部関連ページ導線カード
 * 用途: ディスコグラフィー・ギャラリー等への誘導カード5枚を表示する
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
    useImage: true,
    action: 'navigate',
    target: 'profile',
  },
  {
    id: 'disco',
    title: 'ディスコグラフィー',
    desc: '楽曲・アルバム一覧',
    image: PAGE_IMAGES.disco,
    alt: 'ディスコグラフィー',
    useImage: true,
    action: 'navigate',
    target: 'disco',
  },
  {
    id: 'gallery',
    title: 'ギャラリー',
    desc: '写真でたどる軌跡',
    image: PAGE_IMAGES.gallery,
    alt: 'ギャラリー',
    useImage: true,
    action: 'coming-soon',
    target: 'gallery',
  },
  {
    id: 'events',
    title: 'イベント情報',
    desc: 'コンサート・企画展など',
    image: PAGE_IMAGES.events,
    alt: 'イベント情報',
    useImage: true,
    action: 'coming-soon',
    target: 'events',
  },
  {
    id: 'fanclub',
    title: 'ファンクラブ',
    desc: '入会・会員特典',
    image: PAGE_IMAGES.fanclub,
    alt: 'ファンクラブ',
    useImage: true,
    action: 'coming-soon',
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
  <section class="profile-related" aria-label="関連コンテンツ">
    <div class="profile-related__grid">
      <button
        v-for="c in cards"
        :key="c.id"
        type="button"
        class="profile-related__card"
        :aria-label="c.title"
        @click="onClick(c)"
      >
        <div class="profile-related__visual">
          <PageImageCard
            v-if="c.useImage"
            :image="c.image"
            :alt="c.alt"
            image-only
            compact
            fit="contain"
          />
        </div>
        <div class="profile-related__body">
          <h3 class="profile-related__title">{{ c.title }}</h3>
          <p class="profile-related__desc">{{ c.desc }}</p>
          <span class="profile-related__arrow">›</span>
        </div>
      </button>
    </div>
  </section>
</template>

<style scoped>
.profile-related {
  margin-top: var(--sp-8);
  margin-bottom: var(--sp-6);
}
.profile-related__grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}
.profile-related__card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  overflow: hidden;
  cursor: pointer;
  text-align: left;
  padding: 0;
  transition: transform 0.2s, box-shadow 0.2s;
}
.profile-related__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.profile-related__visual {
  height: 100px;
  background: var(--site-surface-muted);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.profile-related__body {
  padding: 16px 18px 18px;
  position: relative;
}
.profile-related__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.profile-related__desc {
  margin: 0;
  font-size: 12px;
  line-height: 1.6;
  color: var(--site-text-muted);
}
.profile-related__arrow {
  position: absolute;
  right: 16px;
  bottom: 18px;
  font-size: 20px;
  color: var(--murasaki-500);
  line-height: 1;
}

@media (max-width: 1024px) {
  .profile-related__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 767px) {
  .profile-related__grid {
    grid-template-columns: 1fr;
  }
}
</style>
