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
  <UiCard tone="white" padding="md" class="top-events">
    <SectionTitle
      title="今後の放送・イベント"
      size="md"
      link-label="一覧を見る ›"
      @link-click="emit('open-all')"
    />

    <ul class="top-events__list">
      <li v-for="ev in items" :key="ev.id" class="top-events__item">
        <div class="top-events__date-col">
          <span class="top-events__date">{{ ev.date }}</span>
          <span v-if="ev.time" class="top-events__time">{{ ev.time }}</span>
        </div>
        <div class="top-events__body">
          <p class="top-events__title">{{ ev.title }}</p>
          <p v-if="ev.note" class="top-events__note">{{ ev.note }}</p>
        </div>
      </li>
    </ul>
  </UiCard>
</template>

<style scoped>
.top-events {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 380px;
}
.top-events__list {
  flex: 1;
}
.top-events__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.top-events__item {
  display: flex;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid var(--site-border);
  align-items: flex-start;
}
.top-events__item:last-child {
  border-bottom: 0;
}
.top-events__date-col {
  flex-shrink: 0;
  width: 72px;
  text-align: center;
}
.top-events__date {
  display: block;
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 800;
  line-height: 1.25;
  color: var(--murasaki-700);
  letter-spacing: 0.02em;
}
.top-events__time {
  display: block;
  margin-top: 4px;
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--site-text-muted);
}
.top-events__body {
  flex: 1;
  min-width: 0;
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

@media (max-width: 767px) {
  .top-events {
    min-height: auto;
  }
  .top-events__date {
    font-size: 16px;
  }
}
</style>
