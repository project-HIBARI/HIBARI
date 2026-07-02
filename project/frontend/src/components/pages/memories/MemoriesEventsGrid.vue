<script setup>
/**
 * 部品名: 思い出ページ — 交流イベントカード群
 * 用途: 思い出ページのイベントタブで交流イベント一覧を表示する
 */
import UiButton from '../../ui/UiButton.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const eventTypes = {
  nodojiman: { label: 'のど自慢', color: 'var(--murasaki-700)' },
  karaoke: { label: 'カラオケ', color: '#5a7a9a' },
  tour: { label: 'ゆかりの地ツアー', color: '#6a8a5a' },
  photo: { label: 'フォトコンテスト', color: '#7a5a9a' },
}
</script>

<template>
  <div class="mem-events">
    <article v-for="ev in HIBARU_DATA.events" :key="ev.id" class="mem-events__card">
      <div class="mem-events__tags">
        <span
          class="mem-events__type"
          :style="{ background: (eventTypes[ev.type] || { color: 'var(--site-text-muted)' }).color }"
        >
          {{ (eventTypes[ev.type] || { label: ev.type }).label }}
        </span>
        <span v-if="ev.partner" class="mem-events__partner">{{ ev.partner }}</span>
      </div>
      <h3 class="mem-events__title">{{ ev.title }}</h3>
      <dl class="mem-events__dl">
        <dt>日時</dt><dd>{{ ev.date }}</dd>
        <dt>会場</dt><dd>{{ ev.place }}</dd>
        <dt>定員</dt><dd>{{ ev.capacity }}</dd>
        <dt>料金</dt><dd>{{ ev.fee }}</dd>
      </dl>
      <div class="mem-events__actions">
        <UiButton variant="primary" size="sm">申し込む</UiButton>
        <UiButton variant="outline" size="sm">縁ページへ ›</UiButton>
      </div>
    </article>
  </div>
</template>

<style scoped>
.mem-events {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-5);
  margin-top: var(--sp-5);
}
.mem-events__card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  padding: var(--sp-5);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}
.mem-events__tags {
  display: flex;
  gap: 8px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.mem-events__type {
  font-size: 10px;
  color: #fff;
  padding: 3px 10px;
  letter-spacing: 0.15em;
  font-family: var(--ff-mincho);
  border-radius: var(--site-radius-sm);
}
.mem-events__partner {
  font-size: 10px;
  border: 1px solid var(--kin-500);
  color: var(--kin-600);
  padding: 3px 8px;
  letter-spacing: 0.1em;
  font-family: var(--ff-mincho);
  border-radius: var(--site-radius-sm);
}
.mem-events__title {
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 12px;
  color: var(--site-text);
}
.mem-events__dl {
  display: grid;
  grid-template-columns: 60px 1fr;
  gap: 6px 12px;
  font-size: 13px;
  color: var(--site-text-muted);
  margin: 0;
}
.mem-events__dl dt {
  color: var(--kin-600);
  font-family: var(--ff-mincho);
  font-weight: 700;
}
.mem-events__dl dd {
  margin: 0;
}
.mem-events__actions {
  display: flex;
  gap: 10px;
  margin-top: var(--sp-5);
  flex-wrap: wrap;
}

@media (max-width: 767px) {
  .mem-events {
    grid-template-columns: 1fr;
  }
}
</style>
