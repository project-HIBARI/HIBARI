<script setup>
/**
 * 部品名: ホーム — サブスク / ニュース / イベント 3カラム
 * 用途: ヒーロー直下の主要パネル群をまとめる
 */
import TopSubscriptionCard from './TopSubscriptionCard.vue'
import TopNewsPanel from './TopNewsPanel.vue'
import TopEventsPanel from './TopEventsPanel.vue'

defineEmits(['open-fanclub', 'open-news', 'open-events'])
</script>

<template>
  <section class="top-main-panels" aria-label="おすすめと最新情報">
    <TopSubscriptionCard @open-detail="$emit('open-fanclub')" />
    <TopNewsPanel @open-all="$emit('open-news')" />
    <TopEventsPanel @open-all="$emit('open-events')" />
  </section>
</template>

<style scoped>
.top-main-panels {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr) minmax(0, 1fr);
  gap: 24px;
  align-items: stretch;
}

.top-main-panels > * {
  min-width: 0;
}

@media (max-width: 1100px) {
  .top-main-panels {
    grid-template-columns: 1fr 1fr;
  }
  .top-main-panels > :first-child {
    grid-column: 1 / -1;
  }
}

@media (max-width: 767px) {
  .top-main-panels {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
