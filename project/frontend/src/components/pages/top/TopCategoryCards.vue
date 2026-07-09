<script setup>
/**
 * 部品名: ホーム — 下部カテゴリ導線カード
 */
import SiteCategoryCards from '../../common/SiteCategoryCards.vue'
import { HOME_CATEGORY_CARDS } from '../../../lib/categoryCards.js'

const emit = defineEmits(['navigate', 'coming-soon'])
</script>

<template>
  <SiteCategoryCards
    :cards="HOME_CATEGORY_CARDS"
    home-motion
    @navigate="emit('navigate', $event)"
    @coming-soon="emit('coming-soon', $event)"
  />
</template>
