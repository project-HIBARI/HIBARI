<script setup>
/**
 * ページ: ゆかりの地（地図・巡礼）
 * 構成: ヒーロー / 地図 / フィルタ / カテゴリ / スポット一覧 / ランキング /
 *       ギャラリー / エピソード / 関連楽曲 / AI / CTA
 */
import { ref, computed, watch, onMounted } from 'vue'
import PlacesHeroSection from './places/PlacesHeroSection.vue'
import PlacesMapPanel from './places/PlacesMapPanel.vue'
import PlacesFilterPanel from './places/PlacesFilterPanel.vue'
import PlacesCategoryTabs from './places/PlacesCategoryTabs.vue'
import PlacesSpotGrid from './places/PlacesSpotGrid.vue'
import PlacesRankingPanel from './places/PlacesRankingPanel.vue'
import PlacesGalleryPanel from './places/PlacesGalleryPanel.vue'
import PlacesEpisodePanel from './places/PlacesEpisodePanel.vue'
import PlacesRelatedSongs from './places/PlacesRelatedSongs.vue'
import PlacesAiCard from './places/PlacesAiCard.vue'
import PlacesCtaSection from './places/PlacesCtaSection.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { aosAttrs } from '../../lib/aos.js'

const FAV_KEY = 'hbr-places-favorites'

const emit = defineEmits(['open-modal', 'open-auth', 'navigate'])

const regionFilter = ref('all')
const prefectureFilter = ref('all')
const categoryFilter = ref('all')
const keywordDraft = ref('')
const appliedKeyword = ref('')

const selected = ref(HIBARU_DATA.places[0])
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

const filteredPlaces = computed(() => {
  const q = appliedKeyword.value.toLowerCase().trim()
  return HIBARU_DATA.places.filter((p) => {
    const matchRegion = regionFilter.value === 'all' || p.region === regionFilter.value
    const matchPref = prefectureFilter.value === 'all' || p.prefecture === prefectureFilter.value
    const matchCat = categoryFilter.value === 'all' || p.category === categoryFilter.value
    const matchQ =
      !q ||
      p.name.includes(appliedKeyword.value) ||
      p.area.includes(appliedKeyword.value) ||
      (p.description && p.description.includes(appliedKeyword.value)) ||
      (p.note && p.note.includes(appliedKeyword.value)) ||
      p.prefecture.includes(appliedKeyword.value)
    return matchRegion && matchPref && matchCat && matchQ
  })
})

watch(filteredPlaces, (list) => {
  if (list.length && !list.find((p) => p.id === selected.value?.id)) {
    selected.value = list[0]
  }
})

watch(regionFilter, () => {
  prefectureFilter.value = 'all'
})

function applySearch() {
  appliedKeyword.value = keywordDraft.value
}

function resetFilters() {
  regionFilter.value = 'all'
  prefectureFilter.value = 'all'
  categoryFilter.value = 'all'
  keywordDraft.value = ''
  appliedKeyword.value = ''
}

function selectSpot(spot) {
  selected.value = spot
  const el = document.getElementById('places-spot-grid')
  el?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
</script>

<template>
  <div class="page-places">
    <PlacesHeroSection v-bind="aosAttrs()" @open-ai="emit('open-modal', 'ai')" />

    <div class="page-places__map-layout" v-bind="aosAttrs(80)">
      <PlacesMapPanel
        :places="filteredPlaces"
        :selected="selected"
        :region-key="regionFilter"
        @select="selected = $event"
      />
      <aside class="page-places__sidebar">
        <PlacesRankingPanel @select="selectSpot" />
      </aside>
    </div>

    <PlacesFilterPanel
      v-model:region="regionFilter"
      v-model:prefecture="prefectureFilter"
      v-model:category="categoryFilter"
      v-model:keyword="keywordDraft"
      :result-count="filteredPlaces.length"
      @search="applySearch"
      @reset="resetFilters"
    />

    <PlacesCategoryTabs v-model:category="categoryFilter" v-bind="aosAttrs(120)" />

    <div id="places-spot-grid">
      <PlacesSpotGrid
        :spots="filteredPlaces"
        :favorites="favorites"
        @toggle-favorite="toggleFavorite"
        @select="selected = $event"
      />
    </div>

    <PlacesGalleryPanel
      v-bind="aosAttrs(160)"
      @open-gallery="emit('open-auth', 'gallery')"
      @need-auth="(m) => emit('open-auth', m)"
    />

    <PlacesEpisodePanel v-bind="aosAttrs(200)" />

    <PlacesRelatedSongs v-bind="aosAttrs(240)" />

    <PlacesAiCard v-bind="aosAttrs(280)" @open-ai="emit('open-modal', 'ai')" />

    <PlacesCtaSection
      v-bind="aosAttrs(320)"
      @open-auth="(mode) => emit('open-auth', mode)"
      @navigate="(id) => emit('navigate', id)"
    />
  </div>
</template>

<style scoped>
.page-places {
  color: var(--site-text);
}
.page-places__map-layout {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: var(--sp-6);
  align-items: start;
  margin-bottom: var(--sp-6);
}
.page-places__sidebar {
  position: sticky;
  top: var(--sp-5);
}

@media (max-width: 1024px) {
  .page-places__map-layout {
    grid-template-columns: 1fr;
  }
  .page-places__sidebar {
    position: static;
  }
}
</style>
