<script setup>
/**
 * ページ: ディスコグラフィ（曲）
 * 構成: ヒーロー / PV / フィルタ / 楽曲グリッド / ページネーション / AI / 関連導線
 */
import { ref, computed, watch, onMounted } from 'vue'
import DiscoHeroSection from './disco/DiscoHeroSection.vue'
import DiscoPvSection from './disco/DiscoPvSection.vue'
import DiscoFilterPanel from './disco/DiscoFilterPanel.vue'
import DiscoSongGrid from './disco/DiscoSongGrid.vue'
import DiscoPagination from './disco/DiscoPagination.vue'
import DiscoAiCard from './disco/DiscoAiCard.vue'
import DiscoRelatedCards from './disco/DiscoRelatedCards.vue'
import DiscoDetailDialog from './disco/DiscoDetailDialog.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'

const FAV_KEY = 'hbr-disco-favorites'
const PAGE_SIZE = 8

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

const query = ref('')
const typeFilter = ref('all')
const genre = ref('all')
const sort = ref('year-asc')
const yearStart = ref(HIBARU_DATA.discographyStats.yearStart)
const yearEnd = ref(HIBARU_DATA.discographyStats.yearEnd)
const currentPage = ref(1)
const detail = ref(null)
const favorites = ref(new Set())

onMounted(() => {
  try {
    const raw = localStorage.getItem(FAV_KEY)
    if (raw) {
      const ids = JSON.parse(raw)
      if (Array.isArray(ids)) favorites.value = new Set(ids)
    }
  } catch {
    /* ignore */
  }
})

function saveFavorites() {
  try {
    localStorage.setItem(FAV_KEY, JSON.stringify([...favorites.value]))
  } catch {
    /* ignore */
  }
}

function toggleFavorite(id) {
  const next = new Set(favorites.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  favorites.value = next
  saveFavorites()
}

const filteredItems = computed(() => {
  let list = HIBARU_DATA.discography.filter((d) => {
    const q = query.value.toLowerCase().trim()
    const matchQ =
      !q ||
      d.title.includes(query.value) ||
      d.romaji.toLowerCase().includes(q) ||
      d.lyric.includes(query.value) ||
      d.music.includes(query.value)
    const matchG = genre.value === 'all' || d.genre === genre.value
    const matchY = d.year >= yearStart.value && d.year <= yearEnd.value

    if (typeFilter.value === 'favorites') {
      return matchQ && matchG && matchY && favorites.value.has(d.id)
    }
    if (typeFilter.value === 'アルバム') {
      return false
    }
    const matchT = typeFilter.value === 'all' || d.type === typeFilter.value
    return matchQ && matchT && matchG && matchY
  })

  const sorted = [...list]
  if (sort.value === 'year-asc') sorted.sort((a, b) => a.year - b.year)
  else if (sort.value === 'year-desc') sorted.sort((a, b) => b.year - a.year)
  else if (sort.value === 'title-asc') sorted.sort((a, b) => a.title.localeCompare(b.title, 'ja'))

  return sorted
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredItems.value.length / PAGE_SIZE)))

const paginatedItems = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return filteredItems.value.slice(start, start + PAGE_SIZE)
})

const emptyType = computed(() => {
  if (typeFilter.value === 'アルバム') return 'album'
  if (typeFilter.value === 'favorites') return 'favorites'
  return 'search'
})

watch([query, typeFilter, genre, sort, yearStart, yearEnd], () => {
  currentPage.value = 1
})

function openDetail(song) {
  detail.value = song
}
</script>

<template>
  <div class="page-disco">
    <DiscoHeroSection
      @open-detail="openDetail"
      @open-ai="emit('open-modal', 'ai')"
    />

    <DiscoPvSection
      @coming-soon="emit('open-auth', 'pv')"
      @need-auth="(m) => emit('open-auth', m)"
    />

    <DiscoFilterPanel
      :query="query"
      :type-filter="typeFilter"
      :genre="genre"
      :sort="sort"
      :year-start="yearStart"
      :year-end="yearEnd"
      :result-count="filteredItems.length"
      :favorite-count="favorites.size"
      @update:query="query = $event"
      @update:type-filter="typeFilter = $event"
      @update:genre="genre = $event"
      @update:sort="sort = $event"
      @update:year-start="yearStart = $event"
      @update:year-end="yearEnd = $event"
    />

    <DiscoSongGrid
      :items="paginatedItems"
      :favorites="favorites"
      :empty-type="emptyType"
      @open="openDetail"
      @toggle-favorite="toggleFavorite"
    />

    <DiscoPagination
      :page="currentPage"
      :total-pages="totalPages"
      :total-items="filteredItems.length"
      :page-size="PAGE_SIZE"
      @update:page="currentPage = $event"
    />

    <DiscoAiCard @open-ai="emit('open-modal', 'ai')" />

    <DiscoRelatedCards
      @navigate="(id) => emit('navigate', id)"
      @coming-soon="(mode) => emit('open-auth', mode)"
    />

    <DiscoDetailDialog :detail="detail" @close="detail = null" />
  </div>
</template>

<style scoped>
.page-disco {
  color: var(--site-text);
}
</style>
