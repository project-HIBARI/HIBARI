<script setup>
/**
 * 部品名: サイト内検索モーダル
 */
import { ref, computed } from 'vue'
import ModalShell from './ModalShell.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'

const emit = defineEmits(['close', 'navigate'])

const query = ref('')

const searchableItems = computed(() => {
  const items = []
  for (const n of HIBARU_DATA.news || []) {
    items.push({ type: 'ニュース', label: n.title, page: 'news', key: `news-${n.id}` })
  }
  for (const d of HIBARU_DATA.discography || []) {
    items.push({ type: '楽曲', label: d.title, page: 'disco', key: `disco-${d.title}` })
  }
  for (const p of HIBARU_DATA.places || []) {
    items.push({ type: 'ゆかりの地', label: p.name, page: 'map', key: `place-${p.id}` })
  }
  for (const e of HIBARU_DATA.events || []) {
    items.push({ type: 'イベント', label: e.title, page: 'memories', key: `event-${e.id}` })
  }
  items.push(
    { type: 'ページ', label: 'ファンクラブ', page: 'fanclub', key: 'page-fanclub' },
    { type: 'ページ', label: '献花', page: 'message', key: 'page-message' },
    { type: 'ページ', label: 'お問い合わせ', page: 'contact', key: 'page-contact' },
    { type: 'ページ', label: 'FAQ', page: 'faq', key: 'page-faq' },
  )
  return items
})

const results = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return []
  return searchableItems.value.filter((item) => item.label.toLowerCase().includes(q)).slice(0, 12)
})

function select(item) {
  emit('navigate', item.page)
  emit('close')
}
</script>

<template>
  <ModalShell title="サイト内検索" @close="emit('close')">
    <div class="site-search">
      <input
        v-model="query"
        type="search"
        class="site-search__input"
        placeholder="キーワードを入力（例: 川の流れ、野毛、ツアー）"
        autofocus
        aria-label="検索キーワード"
      />
      <ul v-if="results.length" class="site-search__list">
        <li v-for="item in results" :key="item.key">
          <button type="button" class="site-search__item" @click="select(item)">
            <span class="site-search__type">{{ item.type }}</span>
            <span class="site-search__label">{{ item.label }}</span>
          </button>
        </li>
      </ul>
      <p v-else-if="query.trim()" class="site-search__empty">該当する項目が見つかりませんでした。</p>
      <p v-else class="site-search__hint">ページ名・楽曲名・スポット名などで検索できます。</p>
    </div>
  </ModalShell>
</template>

<style scoped>
.site-search__input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--site-border-strong);
  border-radius: var(--site-radius-sm);
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  margin-bottom: 16px;
}
.site-search__list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.site-search__item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px 0;
  border: 0;
  border-bottom: 1px solid var(--site-border);
  background: transparent;
  text-align: left;
  cursor: pointer;
}
.site-search__item:hover {
  color: var(--murasaki-700);
}
.site-search__type {
  flex-shrink: 0;
  font-size: 10px;
  padding: 2px 8px;
  background: var(--murasaki-100);
  color: var(--murasaki-700);
  border-radius: 999px;
}
.site-search__label {
  font-size: 14px;
}
.site-search__empty,
.site-search__hint {
  margin: 0;
  font-size: 13px;
  color: var(--site-text-muted);
  line-height: 1.7;
}
</style>
