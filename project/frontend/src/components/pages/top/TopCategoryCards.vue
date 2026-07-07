<script setup>
/**
 * 部品名: ホーム — 下部カテゴリ導線カード
 * 用途: 各ページや準備中機能への誘導カード5枚を横並びで表示する
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import RelatedPageCard from '../../ui/RelatedPageCard.vue'
import RelatedPageCardGrid from '../../ui/RelatedPageCardGrid.vue'

const emit = defineEmits(['navigate', 'coming-soon'])

const cards = [
  {
    id: 'profile',
    title: '美空ひばりについて',
    subtitle: '彼女の人生と軌跡',
    variant: 'rose',
    action: 'navigate',
    target: 'profile',
  },
  {
    id: 'disco',
    title: 'ディスコグラフィー',
    subtitle: '楽曲・アルバム一覧',
    variant: 'record',
    action: 'navigate',
    target: 'disco',
  },
  {
    id: 'gallery',
    title: 'ギャラリー',
    subtitle: '写真でたどる軌跡',
    variant: 'gallery',
    action: 'coming-soon',
    target: 'gallery',
  },
  {
    id: 'events',
    title: 'イベント情報',
    subtitle: 'コンサート・企画展など',
    variant: 'stage',
    action: 'coming-soon',
    target: 'events',
  },
  {
    id: 'fanclub',
    title: 'ファンクラブ',
    subtitle: '入会・会員特典',
    variant: 'fanclub',
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
    <SectionTitle title="コンテンツを探す" sub="Explore" size="md" />

    <RelatedPageCardGrid :columns="5">
      <RelatedPageCard
        v-for="c in cards"
        :key="c.id"
        :title="c.title"
        :subtitle="c.subtitle"
        :variant="c.variant"
        @click="onClick(c)"
      />
    </RelatedPageCardGrid>
  </section>
</template>

<style scoped>
.top-categories {
  margin: 0;
}
</style>
