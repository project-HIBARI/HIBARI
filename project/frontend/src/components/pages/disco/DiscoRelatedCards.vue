<script setup>
/**
 * 部品名: ディスコグラフィ — 関連ページ導線カード
 * 用途: 歩み・ゆかりの地・ギャラリー等へのナビゲーション
 */
import PageImageCard from '../../common/PageImageCard.vue'
import SectionTitle from '../../ui/SectionTitle.vue'
import { PAGE_IMAGES } from '../../../lib/pageImages.js'

const emit = defineEmits(['navigate', 'coming-soon'])

const cards = [
  {
    id: 'profile',
    title: '歩み',
    desc: '五十二年の生涯と年表',
    deco: 'timeline',
    useImage: false,
    action: 'navigate',
    target: 'profile',
  },
  {
    id: 'map',
    title: 'ゆかりの地',
    desc: '歌碑・記念館・舞台を地図で',
    deco: 'map',
    useImage: false,
    action: 'navigate',
    target: 'map',
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
  <section class="disco-related" aria-label="関連コンテンツ">
    <SectionTitle title="あわせて読む" sub="Explore More" size="md" />

    <div class="disco-related__grid">
      <button
        v-for="c in cards"
        :key="c.id"
        type="button"
        class="disco-related__card"
        :class="c.deco ? `disco-related__card--${c.deco}` : undefined"
        :aria-label="c.title"
        @click="onClick(c)"
      >
        <div class="disco-related__visual">
          <PageImageCard
            v-if="c.useImage"
            :image="c.image"
            :alt="c.alt"
            image-only
            compact
            fit="contain"
          />
        </div>
        <div class="disco-related__body">
          <h3 class="disco-related__title">{{ c.title }}</h3>
          <p class="disco-related__desc">{{ c.desc }}</p>
          <span class="disco-related__arrow">›</span>
        </div>
      </button>
    </div>
  </section>
</template>

<style scoped>
.disco-related {
  margin-bottom: var(--sp-6);
}
.disco-related__grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--sp-4);
}
.disco-related__card {
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
.disco-related__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.disco-related__visual {
  height: 80px;
  background: var(--site-surface-muted);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
.disco-related__card--timeline .disco-related__visual {
  background:
    linear-gradient(90deg, transparent 49%, rgba(201, 169, 97, 0.3) 49%, rgba(201, 169, 97, 0.3) 51%, transparent 51%),
    linear-gradient(160deg, var(--site-bg-pink), var(--site-surface-muted));
  background-size: 24px 100%, 100% 100%;
}
.disco-related__card--map .disco-related__visual {
  background:
    radial-gradient(circle at 30% 50%, rgba(93, 58, 107, 0.2) 0%, transparent 40%),
    radial-gradient(circle at 70% 40%, rgba(201, 169, 97, 0.25) 0%, transparent 35%),
    linear-gradient(160deg, #e8f0e8, #f5ebe0);
}
.disco-related__body {
  padding: var(--sp-4);
  position: relative;
}
.disco-related__title {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.disco-related__desc {
  margin: 0;
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-muted);
}
.disco-related__arrow {
  position: absolute;
  right: 14px;
  bottom: 14px;
  font-size: 18px;
  color: var(--murasaki-500);
}

@media (max-width: 1024px) {
  .disco-related__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 600px) {
  .disco-related__grid {
    grid-template-columns: 1fr;
  }
}
</style>
