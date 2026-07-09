<script setup>
/**
 * 部品名: ディスコグラフィ — 関連ページ導線カード
 * 用途: ホーム・歩み・献花と同じ下部カテゴリ導線カードを表示する
 */
import SiteCategoryCards from '../../common/SiteCategoryCards.vue'
import { HOME_CATEGORY_CARDS } from '../../../lib/categoryCards.js'

const emit = defineEmits(['navigate', 'coming-soon'])
</script>

<template>
  <SiteCategoryCards
    class="disco-related"
    :cards="HOME_CATEGORY_CARDS"
    aria-label="関連コンテンツ"
    @navigate="emit('navigate', $event)"
    @coming-soon="emit('coming-soon', $event)"
  />
</template>

<style scoped>
.disco-related {
  margin-top: var(--sp-8);
  margin-bottom: var(--sp-6);
}
</style>
