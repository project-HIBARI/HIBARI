<script setup>
/**
 * ページ: Music Memory Book
 * 構成: TOP / 年別アルバム / 思い出詳細
 */
import { ref, watch, onMounted, computed } from 'vue'
import MemoryBookTopView from './memorybook/MemoryBookTopView.vue'
import MemoryBookYearView from './memorybook/MemoryBookYearView.vue'
import MemoryBookDetailView from './memorybook/MemoryBookDetailView.vue'
import { useMemoryBookData } from '../../composables/useMemoryBookData.js'
import { useMemoryBookCover } from '../../composables/useMemoryBookCover.js'
import MemoryBookCoverPicker from './memorybook/MemoryBookCoverPicker.vue'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

const {
  loading,
  error,
  summary,
  categories,
  years,
  fetchMemoryBook,
  getYearDetail,
  getItemDetail,
} = useMemoryBookData()

const { getCoverDesign, setCoverDesign, coversByYear } = useMemoryBookCover()

const view = ref('top')
const selectedYear = ref(new Date().getFullYear())
const selectedItemId = ref(null)
const showCoverPicker = ref(false)

const yearData = computed(() => getYearDetail(selectedYear.value))
const itemDetail = computed(() =>
  selectedItemId.value ? getItemDetail(selectedItemId.value) : null,
)
const selectedCoverDesign = computed(() => {
  void coversByYear.value
  return getCoverDesign(selectedYear.value)
})

watch(view, () => {
  window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
})

onMounted(() => {
  fetchMemoryBook()
})

function openYear(year) {
  selectedYear.value = year
  view.value = 'year'
}

function openDetail(itemId) {
  selectedItemId.value = itemId
  view.value = 'detail'
}

function goTop() {
  view.value = 'top'
}

function goYear() {
  view.value = 'year'
}

function openFanclub() {
  emit('navigate', 'fanclub')
}

function onCategory(catId) {
  if (catId === 'albums') {
    goTop()
    return
  }
  if (catId === 'flowers') emit('navigate', 'message')
  else if (catId === 'posts') emit('navigate', 'memories')
  else if (catId === 'songs') emit('navigate', 'disco')
  else if (catId === 'ai') emit('open-modal', 'ai')
}

function onComingSoon() {
  emit('open-auth', 'register-premium')
}

function onRetry() {
  fetchMemoryBook()
}

function openCoverPicker(year) {
  selectedYear.value = year
  showCoverPicker.value = true
}

function onSelectCover(designId) {
  setCoverDesign(selectedYear.value, designId)
  showCoverPicker.value = false
}
</script>

<template>
  <div class="page-memory-book">
    <MemoryBookTopView
      v-if="view === 'top'"
      :loading="loading"
      :error="error"
      :summary="summary"
      :categories="categories"
      :years="years"
      :get-cover-design="getCoverDesign"
      :covers-by-year="coversByYear"
      @open-year="openYear"
      @open-detail="openDetail"
      @open-fanclub="openFanclub"
      @open-category="onCategory"
      @retry="onRetry"
    />

    <MemoryBookYearView
      v-else-if="view === 'year'"
      :loading="loading"
      :error="error"
      :data="yearData"
      :cover-design-id="selectedCoverDesign"
      @back="goTop"
      @open-detail="openDetail"
      @open-fanclub="openFanclub"
      @coming-soon="onComingSoon"
      @change-cover="openCoverPicker(selectedYear)"
      @retry="onRetry"
    />

    <MemoryBookDetailView
      v-else-if="view === 'detail'"
      :loading="loading"
      :error="error"
      :memory="itemDetail"
      @back="goTop"
      @back-year="goYear"
      @open-detail="openDetail"
      @open-fanclub="openFanclub"
      @coming-soon="onComingSoon"
      @retry="onRetry"
    />
  </div>

  <MemoryBookCoverPicker
    :open="showCoverPicker"
    :year="selectedYear"
    :selected-design-id="selectedCoverDesign"
    @close="showCoverPicker = false"
    @select="onSelectCover"
  />
</template>

<style scoped>
.page-memory-book {
  color: var(--site-text);
  min-width: 960px;
}
</style>
