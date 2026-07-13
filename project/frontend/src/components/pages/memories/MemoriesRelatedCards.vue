<script setup>
/**
 * 部品名: 思い出 — 下部関連ページ導線カード
 * 用途: ホーム・歩み・ディスコグラフィ等への誘導カード5枚を表示する
 */
import SiteCategoryCards from '../../common/SiteCategoryCards.vue'
import { HOME_CATEGORY_CARDS } from '../../../lib/categoryCards.js'

const emit = defineEmits(['navigate', 'coming-soon'])
</script>

<template>
  <SiteCategoryCards
    class="memories-related"
    :cards="HOME_CATEGORY_CARDS"
    aria-label="関連コンテンツ"
    home-motion
    @navigate="emit('navigate', $event)"
    @coming-soon="emit('coming-soon', $event)"
  />
</template>

<style scoped>
.memories-related {
  margin-top: var(--sp-8);
  margin-bottom: var(--sp-6);
}
</style>
