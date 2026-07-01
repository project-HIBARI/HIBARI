<script setup>
/**
 * 部品名: ホーム — 最新ニュース一覧
 * 用途: ホーム中段のニュースカード内に最新5件を表示する
 */
import { computed } from 'vue'
import UiCard from '../../ui/UiCard.vue'
import SectionTitle from '../../ui/SectionTitle.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['open-all'])

const typeLabels = {
  tv: 'テレビ',
  event: 'イベント',
  goods: 'グッズ',
  info: 'お知らせ',
}

const items = computed(() =>
  HIBARU_DATA.news.slice(0, 5).map((n) => ({
    ...n,
    label: n.label || typeLabels[n.type] || 'お知らせ',
  })),
)
</script>

<template>
  <UiCard tone="white" padding="md" class="top-news">
    <SectionTitle
      title="最新ニュース"
      size="md"
      link-label="一覧を見る ›"
      @link-click="emit('open-all')"
    />

    <ul class="top-news__list">
      <li v-for="(n, i) in items" :key="i" class="top-news__item">
        <time class="top-news__date">{{ n.date }}</time>
        <span class="top-news__label">{{ n.label }}</span>
        <p class="top-news__title">{{ n.title }}</p>
      </li>
    </ul>
  </UiCard>
</template>

<style scoped>
.top-news {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.top-news__list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
}
.top-news__item {
  padding: 14px 0;
  border-bottom: 1px solid var(--site-border);
}
.top-news__item:last-child {
  border-bottom: 0;
}
.top-news__date {
  display: block;
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--site-text-light);
  letter-spacing: 0.04em;
  margin-bottom: 4px;
}
.top-news__label {
  display: inline-block;
  padding: 2px 8px;
  margin-bottom: 6px;
  font-size: 10px;
  font-family: var(--ff-sans-jp);
  letter-spacing: 0.06em;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid rgba(122, 80, 136, 0.2);
  border-radius: 3px;
}
.top-news__title {
  margin: 0;
  font-size: 13px;
  line-height: 1.65;
  color: var(--site-text);
}
</style>
