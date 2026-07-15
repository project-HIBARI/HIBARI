<script setup>
/**
 * 部品名: ゆかりの地 — カテゴリタブ
 * 用途: スポット種別のクイック絞り込み
 */
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const category = defineModel('category', { type: String, default: 'all' })

const tabs = HIBARU_DATA.placeCategories
</script>

<template>
  <!-- カテゴリ別クイックフィルタ -->
  <div class="places-cats" role="tablist" aria-label="カテゴリで絞り込み">
    <button
      v-for="tab in tabs"
      :key="tab.key"
      type="button"
      role="tab"
      class="places-cats__tab"
      :class="{ 'places-cats__tab--active': category === tab.key }"
      :aria-selected="category === tab.key"
      @click="category = tab.key"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<style scoped>
.places-cats {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-2);
  margin-bottom: var(--sp-5);
}
.places-cats__tab {
  padding: 8px 14px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: var(--site-surface);
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  letter-spacing: 0.06em;
  color: var(--site-text-muted);
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}
.places-cats__tab:hover {
  border-color: rgba(122, 80, 136, 0.3);
  color: var(--site-text);
}
.places-cats__tab--active {
  background: var(--murasaki-100);
  border-color: var(--murasaki-500);
  color: var(--murasaki-800);
  font-weight: 500;
}
.places-cats__tab:focus-visible {
  outline: 2px solid var(--murasaki-500);
  outline-offset: 2px;
}
</style>
