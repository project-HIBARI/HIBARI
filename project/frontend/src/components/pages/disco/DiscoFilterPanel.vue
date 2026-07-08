<script setup>
/**
 * 部品名: ディスコグラフィ — フィルタパネル
 * 用途: 検索・形態・ジャンル・年代・並び替えの絞り込み UI
 */
import UiCard from '../../ui/UiCard.vue'
import UiIco from '../../ui/UiIco.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const props = defineProps({
  query: { type: String, default: '' },
  typeFilter: { type: String, default: 'all' },
  genre: { type: String, default: 'all' },
  sort: { type: String, default: 'year-asc' },
  yearStart: { type: Number, default: 1949 },
  yearEnd: { type: Number, default: 1989 },
  resultCount: { type: Number, default: 0 },
  favoriteCount: { type: Number, default: 0 },
})

const emit = defineEmits([
  'update:query',
  'update:typeFilter',
  'update:genre',
  'update:sort',
  'update:yearStart',
  'update:yearEnd',
])

const stats = HIBARU_DATA.discographyStats
const genres = ['演歌', '歌謡曲', '民謡', 'ポップス']

const typeTabs = [
  { key: 'all', label: 'すべて' },
  { key: 'シングル', label: 'シングル' },
  { key: 'アルバム', label: 'アルバム' },
  { key: 'favorites', label: 'お気に入り' },
]

const decades = [
  { label: '全期間', start: stats.yearStart, end: stats.yearEnd },
  { label: '40年代', start: 1949, end: 1949 },
  { label: '50年代', start: 1950, end: 1959 },
  { label: '60年代', start: 1960, end: 1969 },
  { label: '70年代', start: 1970, end: 1979 },
  { label: '80年代', start: 1980, end: 1989 },
]

function setYearStart(v) {
  const n = +v
  let end = props.yearEnd
  if (n > end) end = n
  emit('update:yearStart', n)
  if (end !== props.yearEnd) emit('update:yearEnd', end)
}

function setYearEnd(v) {
  const n = +v
  let start = props.yearStart
  if (n < start) start = n
  emit('update:yearEnd', n)
  if (start !== props.yearStart) emit('update:yearStart', start)
}

function applyDecade(start, end) {
  emit('update:yearStart', start)
  emit('update:yearEnd', end)
}

function isDecadeActive(start, end) {
  return props.yearStart === start && props.yearEnd === end
}
</script>

<template>
  <!-- 楽曲一覧の絞り込みコントロール -->
  <UiCard tone="warm" padding="md" class="disco-filter">
    <div class="disco-filter__search">
      <UiIco name="search" :size="15" color="var(--kin-600)" class="disco-filter__search-icon" />
      <input
        :value="query"
        type="search"
        class="disco-filter__input"
        placeholder="曲名・ローマ字・作詞・作曲で検索"
        aria-label="楽曲を検索"
        @input="emit('update:query', $event.target.value)"
      />
    </div>

    <div class="disco-filter__row">
      <div class="disco-filter__tabs" role="tablist" aria-label="形態で絞り込み">
        <button
          v-for="tab in typeTabs"
          :key="tab.key"
          type="button"
          role="tab"
          class="disco-filter__tab"
          :class="{ 'disco-filter__tab--active': typeFilter === tab.key }"
          :aria-selected="typeFilter === tab.key"
          @click="emit('update:typeFilter', tab.key)"
        >
          {{ tab.label }}
          <span v-if="tab.key === 'favorites' && favoriteCount > 0" class="disco-filter__badge">
            {{ favoriteCount }}
          </span>
        </button>
      </div>
    </div>

    <div class="disco-filter__row disco-filter__row--wrap">
      <label class="disco-filter__field">
        <span class="disco-filter__label">ジャンル</span>
        <select
          :value="genre"
          class="disco-filter__select"
          aria-label="ジャンル"
          @change="emit('update:genre', $event.target.value)"
        >
          <option value="all">全ジャンル</option>
          <option v-for="g in genres" :key="g" :value="g">{{ g }}</option>
        </select>
      </label>

      <label class="disco-filter__field">
        <span class="disco-filter__label">並び替え</span>
        <select
          :value="sort"
          class="disco-filter__select"
          aria-label="並び替え"
          @change="emit('update:sort', $event.target.value)"
        >
          <option value="year-asc">年代（古い順）</option>
          <option value="year-desc">年代（新しい順）</option>
          <option value="title-asc">曲名（あいうえお順）</option>
        </select>
      </label>

      <span class="disco-filter__count">{{ resultCount }} 曲</span>
    </div>

    <div class="disco-filter__decades">
      <button
        v-for="d in decades"
        :key="d.label"
        type="button"
        class="disco-filter__decade"
        :class="{ 'disco-filter__decade--active': isDecadeActive(d.start, d.end) }"
        @click="applyDecade(d.start, d.end)"
      >
        {{ d.label }}
      </button>
    </div>

    <div class="disco-filter__range">
      <span class="disco-filter__range-label">{{ yearStart }}年</span>
      <input
        type="range"
        class="disco-filter__slider"
        :min="stats.yearStart"
        :max="stats.yearEnd"
        :value="yearStart"
        aria-label="開始年"
        @input="setYearStart($event.target.value)"
      />
      <span class="disco-filter__range-sep">〜</span>
      <input
        type="range"
        class="disco-filter__slider"
        :min="stats.yearStart"
        :max="stats.yearEnd"
        :value="yearEnd"
        aria-label="終了年"
        @input="setYearEnd($event.target.value)"
      />
      <span class="disco-filter__range-label">{{ yearEnd }}年</span>
    </div>
  </UiCard>
</template>

<style scoped>
.disco-filter {
  margin-bottom: var(--sp-5);
}
.disco-filter__search {
  position: relative;
  margin-bottom: var(--sp-4);
}
.disco-filter__search-icon {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  pointer-events: none;
}
.disco-filter__input {
  width: 100%;
  padding: 10px 12px 10px 36px;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  font-family: var(--ff-serif);
  font-size: 13px;
  color: var(--site-text);
  outline: none;
}
.disco-filter__input:focus {
  border-color: var(--murasaki-400);
  box-shadow: 0 0 0 2px rgba(122, 80, 136, 0.12);
}
.disco-filter__row {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  margin-bottom: var(--sp-4);
}
.disco-filter__row--wrap {
  flex-wrap: wrap;
}
.disco-filter__tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.disco-filter__tab {
  padding: 7px 16px;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  font-family: var(--ff-mincho);
  font-size: 12px;
  letter-spacing: 0.08em;
  color: var(--site-text-muted);
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, color 0.2s;
}
.disco-filter__tab:hover {
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}
.disco-filter__tab--active {
  background: var(--murasaki-700);
  border-color: var(--murasaki-800);
  color: #fff;
}
.disco-filter__badge {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 6px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  font-size: 10px;
}
.disco-filter__field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.disco-filter__label {
  font-family: var(--ff-mincho);
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--site-text-muted);
}
.disco-filter__select {
  padding: 8px 12px;
  background: var(--site-surface);
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  font-family: var(--ff-serif);
  font-size: 13px;
  color: var(--site-text);
  min-width: 140px;
}
.disco-filter__count {
  margin-left: auto;
  font-family: var(--ff-mono);
  font-size: 12px;
  color: var(--kin-600);
  letter-spacing: 0.08em;
}
.disco-filter__decades {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: var(--sp-3);
}
.disco-filter__decade {
  padding: 5px 12px;
  background: transparent;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: var(--site-text-muted);
  cursor: pointer;
}
.disco-filter__decade--active {
  background: var(--murasaki-100);
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}
.disco-filter__range {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  font-family: var(--ff-mono);
  font-size: 11px;
  color: var(--site-text-muted);
}
.disco-filter__slider {
  flex: 1;
  min-width: 80px;
  max-width: 160px;
  accent-color: var(--murasaki-700);
}
.disco-filter__range-sep {
  opacity: 0.5;
}

@media (max-width: 767px) {
  .disco-filter__row {
    flex-direction: column;
    align-items: stretch;
  }
  .disco-filter__field {
    width: 100%;
  }
  .disco-filter__select {
    width: 100%;
    min-width: 0;
  }
  .disco-filter__count {
    margin-left: 0;
    text-align: right;
  }
  .disco-filter__range {
    flex-direction: column;
    align-items: stretch;
  }
  .disco-filter__slider {
    max-width: none;
    width: 100%;
  }
}
</style>
