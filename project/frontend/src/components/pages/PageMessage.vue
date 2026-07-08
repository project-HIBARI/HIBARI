<script setup>
/**
 * ページ: 献花・メッセージ（花）
 * 用途: 誕生日・不死鳥忌の献花とメッセージ壁を表示する（ライトテーマ）
 */
import MessageHero from './message/MessageHero.vue'
import MessageAnniversaryCards from './message/MessageAnniversaryCards.vue'
import MessageOfferingBlock from './message/MessageOfferingBlock.vue'
import MessageWallGrid from './message/MessageWallGrid.vue'
</script>

<template>
  <div class="page-message">
    <MessageHero />
    <MessageAnniversaryCards />
    <MessageOfferingBlock />
    <MessageWallGrid />
  </div>
</template>

<style scoped>
.page-message {
  color: var(--site-text);
}
</style>
