<script setup>
/**
 * ページ: 献花・メッセージ（花）
 */
import PageHead from '../ui/PageHead.vue'
import MessageAnniversaryCards from './message/MessageAnniversaryCards.vue'
import MessageOfferingBlock from './message/MessageOfferingBlock.vue'
import MessageWallGrid from './message/MessageWallGrid.vue'
</script>

<template>
  <div>
    <PageHead kanji="花" title="献花・メッセージ" sub="Offering · 誕生日 五月二十九日 · 不死鳥忌 六月二十四日" />
    <MessageAnniversaryCards />
    <MessageOfferingBlock />
    <MessageWallGrid />
  </div>
</template>
