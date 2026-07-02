<script setup>
/**
 * ページ: 献花・メッセージ（花）
 * 用途: 誕生日・不死鳥忌の献花とメッセージ壁を表示する（ライトテーマ）
 */
import PageHead from '../ui/PageHead.vue'
import MessageAnniversaryCards from './message/MessageAnniversaryCards.vue'
import MessageOfferingBlock from './message/MessageOfferingBlock.vue'
import MessageWallGrid from './message/MessageWallGrid.vue'
</script>

<template>
  <div class="page-message">
    <PageHead kanji="花" title="献花・メッセージ" sub="Offering · 誕生日 五月二十九日 · 不死鳥忌 六月二十四日" />
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
