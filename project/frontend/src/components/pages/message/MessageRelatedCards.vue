<script setup>
/**
 * 部品名: 献花 — 下部関連ページ導線カード
 * 用途: 歩み・ディスコグラフィー等への誘導カード5枚を表示する
 */
import SiteCategoryCards from '../../common/SiteCategoryCards.vue'
import { HOME_CATEGORY_CARDS } from '../../../lib/categoryCards.js'

const emit = defineEmits(['navigate', 'coming-soon'])
</script>

<template>
  <SiteCategoryCards
    class="message-related"
    :cards="HOME_CATEGORY_CARDS"
    aria-label="関連コンテンツ"
    @navigate="emit('navigate', $event)"
    @coming-soon="emit('coming-soon', $event)"
  />
</template>

<style scoped>
.message-related {
  margin-top: var(--sp-8);
}
</style>
