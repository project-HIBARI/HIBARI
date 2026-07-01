<script setup>
/**
 * 部品名: ゆかりの地 — 検索・フィルタパネル
 * 用途: 地方・都道府県・カテゴリ・キーワードでの絞り込み
 */
import { computed } from 'vue'
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const region = defineModel('region', { type: String, default: 'all' })
const prefecture = defineModel('prefecture', { type: String, default: 'all' })
const category = defineModel('category', { type: String, default: 'all' })
const keyword = defineModel('keyword', { type: String, default: '' })

const props = defineProps({
  resultCount: { type: Number, default: 0 },
})

const emit = defineEmits(['search', 'reset'])

const regions = HIBARU_DATA.placeRegions

const prefectures = computed(() => {
  const set = new Set()
  HIBARU_DATA.places.forEach((p) => {
    if (region.value === 'all' || p.region === region.value) {
      set.add(p.prefecture)
    }
  })
  return ['all', ...[...set].sort()]
})

function onRegionChange(e) {
  region.value = e.target.value
  prefecture.value = 'all'
}
</script>

<template>
  <!-- スポット検索・絞り込み -->
  <UiCard tone="white" padding="md" class="places-filter">
    <div class="places-filter__search">
      <UiIco name="search" :size="15" color="var(--kin-600)" class="places-filter__search-icon" />
      <input
        v-model="keyword"
        type="search"
        class="places-filter__input"
        placeholder="スポット名・住所・説明で検索"
        aria-label="スポットを検索"
        @keydown.enter="emit('search')"
      />
    </div>

    <div class="places-filter__row">
      <label class="places-filter__field">
        <span class="places-filter__label">地方</span>
        <select :value="region" class="places-filter__select" aria-label="地方" @change="onRegionChange">
          <option v-for="r in regions" :key="r.key" :value="r.key">{{ r.label }}</option>
        </select>
      </label>
      <label class="places-filter__field">
        <span class="places-filter__label">都道府県</span>
        <select v-model="prefecture" class="places-filter__select" aria-label="都道府県">
          <option value="all">すべて</option>
          <option v-for="p in prefectures.filter((x) => x !== 'all')" :key="p" :value="p">{{ p }}</option>
        </select>
      </label>
      <label class="places-filter__field">
        <span class="places-filter__label">カテゴリ</span>
        <select v-model="category" class="places-filter__select" aria-label="カテゴリ">
          <option v-for="c in HIBARU_DATA.placeCategories" :key="c.key" :value="c.key">{{ c.label }}</option>
        </select>
      </label>
    </div>

    <div class="places-filter__actions">
      <UiButton variant="primary" size="sm" @click="emit('search')">
        <UiIco name="search" :size="14" color="#fff" />
        検索
      </UiButton>
      <UiButton variant="outline" size="sm" @click="emit('reset')">リセット</UiButton>
      <span class="places-filter__result">{{ resultCount }} 件</span>
    </div>
  </UiCard>
</template>

<style scoped>
.places-filter {
  margin-bottom: var(--sp-5);
}
.places-filter__search {
  position: relative;
  margin-bottom: var(--sp-4);
}
.places-filter__search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}
.places-filter__input {
  width: 100%;
  padding: 12px 14px 12px 40px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface-muted);
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  color: var(--site-text);
}
.places-filter__input:focus {
  outline: 2px solid var(--murasaki-400);
  outline-offset: 0;
  border-color: var(--murasaki-400);
}
.places-filter__row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
  margin-bottom: var(--sp-4);
}
.places-filter__field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.places-filter__label {
  font-size: 11px;
  letter-spacing: 0.1em;
  color: var(--site-text-muted);
}
.places-filter__select {
  padding: 10px 12px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  background: var(--site-surface);
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  color: var(--site-text);
}
.places-filter__select:focus {
  outline: 2px solid var(--murasaki-400);
  outline-offset: 0;
}
.places-filter__actions {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  flex-wrap: wrap;
}
.places-filter__result {
  margin-left: auto;
  font-family: var(--ff-mono);
  font-size: 12px;
  color: var(--kin-600);
  letter-spacing: 0.08em;
}

@media (max-width: 768px) {
  .places-filter__row {
    grid-template-columns: 1fr;
  }
}
</style>
