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

const items = computed(() => HIBARU_DATA.news.slice(0, 5))
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
        <div class="top-news__row">
          <time class="top-news__date">{{ n.date }}</time>
          <span v-if="i === 0 || n.isNew" class="top-news__new">NEW</span>
        </div>
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
  min-height: 380px;
}
.top-news__list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
}
.top-news__item {
  padding: 13px 0;
  border-bottom: 1px solid var(--site-border);
}
.top-news__item:last-child {
  border-bottom: 0;
}
.top-news__row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}
.top-news__date {
  font-family: var(--ff-mono);
  font-size: 12px;
  color: var(--site-text-light);
  letter-spacing: 0.04em;
}
.top-news__new {
  display: inline-block;
  padding: 1px 7px;
  font-size: 9px;
  font-family: var(--ff-sans-jp);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #fff;
  background: var(--beni-500);
  border-radius: 3px;
}
.top-news__title {
  margin: 0;
  font-size: 13px;
  line-height: 1.65;
  color: var(--site-text);
}

@media (max-width: 767px) {
  .top-news {
    min-height: auto;
  }
}
</style>
