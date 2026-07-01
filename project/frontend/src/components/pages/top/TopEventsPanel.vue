<script setup>
/**
 * 部品名: ホーム — 今後の放送・イベント一覧
 * 用途: ホーム中段のイベントカード内に放送・イベント4件を表示する
 */
import UiCard from '../../ui/UiCard.vue'
import SectionTitle from '../../ui/SectionTitle.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['open-all'])

const items = HIBARU_DATA.homeSchedule.slice(0, 4)
</script>

<template>
  <UiCard tone="warm" padding="md" class="top-events">
    <SectionTitle
      title="今後の放送・イベント"
      size="md"
      link-label="一覧を見る ›"
      @link-click="emit('open-all')"
    />

    <ul class="top-events__list">
      <li v-for="ev in items" :key="ev.id" class="top-events__item">
        <div class="top-events__meta">
          <span class="top-events__date">{{ ev.date }}</span>
          <span v-if="ev.time" class="top-events__time">{{ ev.time }}</span>
        </div>
        <p class="top-events__title">{{ ev.title }}</p>
        <p v-if="ev.note" class="top-events__note">{{ ev.note }}</p>
      </li>
    </ul>
  </UiCard>
</template>

<style scoped>
.top-events {
  height: 100%;
}
.top-events__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.top-events__item {
  padding: 14px 0;
  border-bottom: 1px solid var(--site-border);
}
.top-events__item:last-child {
  border-bottom: 0;
}
.top-events__meta {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 6px;
}
.top-events__date {
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  color: var(--murasaki-700);
}
.top-events__time {
  font-family: var(--ff-mono);
  font-size: 12px;
  color: var(--site-text-muted);
}
.top-events__title {
  margin: 0 0 4px;
  font-size: 13px;
  line-height: 1.6;
  font-weight: 500;
  color: var(--site-text);
}
.top-events__note {
  margin: 0;
  font-size: 11px;
  line-height: 1.5;
  color: var(--site-text-light);
}
</style>
