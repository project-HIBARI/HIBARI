<script setup>
/**
 * ページ: Music Memory Book
 * 構成: TOP / 年別アルバム / 思い出詳細
 */
import { ref, watch, onMounted, computed } from 'vue'
import MemoryBookTopView from './memorybook/MemoryBookTopView.vue'
import MemoryBookYearView from './memorybook/MemoryBookYearView.vue'
import MemoryBookDetailView from './memorybook/MemoryBookDetailView.vue'
import MemoryBookFilteredView from './memorybook/MemoryBookFilteredView.vue'
import { useMemoryBookData } from '../../composables/useMemoryBookData.js'
import { useMemoryBookCover } from '../../composables/useMemoryBookCover.js'
import MemoryBookCoverPicker from './memorybook/MemoryBookCoverPicker.vue'
import MemoryBookEditModal from './memorybook/MemoryBookEditModal.vue'
import MemoryBookShareModal from './memorybook/MemoryBookShareModal.vue'
import MemoryBookAiRecapModal from './memorybook/MemoryBookAiRecapModal.vue'
import { parseMemoryItemRef } from '../../lib/memoryBookFromApi.js'
import { updatePost, deletePost } from '../../api/posts.js'
import { updateFlowerOffering, deleteFlowerOffering } from '../../api/flowers.js'
import { exportYearAlbumPdf } from '../../lib/memoryBookPdf.js'
import { COVER_DESIGNS } from '../../lib/memoryBookCoverDesigns.js'

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
  getFilterViewData,
  getCategoryViewData,
} = useMemoryBookData()

const { getCoverDesign, setCoverDesign, coversByYear } = useMemoryBookCover()

const view = ref('top')
const selectedYear = ref(new Date().getFullYear())
const selectedItemId = ref(null)
const showCoverPicker = ref(false)
const showEditModal = ref(false)
const showShareModal = ref(false)
const showRecapModal = ref(false)
const editSubmitting = ref(false)
const editError = ref('')
const filterMode = ref(null)
const filterSourceId = ref(null)
const categoryFilterId = ref(null)

const yearData = computed(() => getYearDetail(selectedYear.value))
const itemDetail = computed(() =>
  selectedItemId.value ? getItemDetail(selectedItemId.value) : null,
)
const selectedCoverDesign = computed(() => {
  void coversByYear.value
  return getCoverDesign(selectedYear.value)
})
const filterData = computed(() => {
  if (!filterMode.value || !filterSourceId.value) return null
  return getFilterViewData(filterMode.value, filterSourceId.value)
})
const categoryData = computed(() => {
  if (!categoryFilterId.value) return null
  return getCategoryViewData(categoryFilterId.value)
})
const coverDesignLabel = computed(() => {
  const design = COVER_DESIGNS.find((d) => d.id === selectedCoverDesign.value)
  return design?.label ?? 'デザイン 1'
})

watch(view, () => {
  window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
})

onMounted(() => {
  fetchMemoryBook()
})

function openYear(year) {
  selectedYear.value = Number(year)
  selectedItemId.value = null
  filterMode.value = null
  filterSourceId.value = null
  categoryFilterId.value = null
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
  categoryFilterId.value = catId
  view.value = 'category'
}

function onCategoryEmptyAction(action) {
  if (action === 'message') emit('navigate', 'message')
  else if (action === 'memories') emit('navigate', 'memories')
  else if (action === 'disco') emit('navigate', 'disco')
  else if (action === 'ai') emit('open-modal', 'ai')
}

function backFromCategory() {
  categoryFilterId.value = null
  goTop()
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

function openEditModal() {
  editError.value = ''
  showEditModal.value = true
}

function closeEditModal() {
  if (editSubmitting.value) return
  showEditModal.value = false
  editError.value = ''
}

async function onSaveEdit({ category, payload }) {
  const refInfo = parseMemoryItemRef(selectedItemId.value)
  if (!refInfo) {
    editError.value = 'この思い出は編集できません。'
    return
  }

  editSubmitting.value = true
  editError.value = ''
  try {
    if (category === 'flowers') {
      await updateFlowerOffering(refInfo.sourceId, payload)
    } else if (category === 'posts') {
      await updatePost(refInfo.sourceId, payload)
    }
    await fetchMemoryBook()
    showEditModal.value = false
  } catch (err) {
    editError.value = err?.message || '保存に失敗しました。'
  } finally {
    editSubmitting.value = false
  }
}

async function onDeleteMemory() {
  const memory = itemDetail.value
  const refInfo = parseMemoryItemRef(selectedItemId.value)
  if (!memory || !refInfo) return

  const label = memory.category === 'flowers' ? '献花の記録' : '思い出の投稿'
  const confirmed = window.confirm(`この${label}を削除しますか？\n削除すると元に戻せません。`)
  if (!confirmed) return

  try {
    if (refInfo.category === 'flowers') {
      await deleteFlowerOffering(refInfo.sourceId)
    } else if (refInfo.category === 'posts') {
      await deletePost(refInfo.sourceId)
    }
    await fetchMemoryBook()
    selectedItemId.value = null
    goYear()
  } catch (err) {
    window.alert(err?.message || '削除に失敗しました。')
  }
}

function onExportPdf() {
  try {
    exportYearAlbumPdf({
      year: selectedYear.value,
      summary: yearData.value.summary,
      timeline: yearData.value.timeline,
      coverDesignLabel: coverDesignLabel.value,
    })
  } catch (err) {
    window.alert(err?.message || 'PDFの出力に失敗しました。')
  }
}

function onShareAlbum() {
  showShareModal.value = true
}

function onOpenRecap() {
  showRecapModal.value = true
}

function onFilterRelated(mode) {
  const sourceId = selectedItemId.value
  const memory = getItemDetail(sourceId)
  if (!memory) {
    window.alert('思い出が見つかりませんでした。')
    return
  }
  if (mode === 'same-place' && (!memory.location || memory.location === '—')) {
    window.alert('場所が記録されていないため、同じ場所の思い出は表示できません。')
    return
  }
  const data = getFilterViewData(mode, sourceId)
  if (!data?.timeline.length) {
    window.alert(data?.emptyMessage || '該当する思い出は見つかりませんでした。')
    return
  }
  filterSourceId.value = sourceId
  filterMode.value = mode
  view.value = 'filter'
}

function backFromFilter() {
  selectedItemId.value = filterSourceId.value
  filterMode.value = null
  filterSourceId.value = null
  view.value = 'detail'
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
      @export-pdf="onExportPdf"
      @share="onShareAlbum"
      @open-recap="onOpenRecap"
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
      @retry="onRetry"
      @edit="openEditModal"
      @delete="onDeleteMemory"
      @filter-related="onFilterRelated"
    />

    <MemoryBookFilteredView
      v-else-if="view === 'filter' && filterData"
      :loading="loading"
      :error="error"
      :data="filterData"
      back-label="詳細に戻る"
      @back="backFromFilter"
      @open-detail="openDetail"
      @retry="onRetry"
    />

    <MemoryBookFilteredView
      v-else-if="view === 'category' && categoryData"
      :loading="loading"
      :error="error"
      :data="categoryData"
      back-label="TOPに戻る"
      @back="backFromCategory"
      @open-detail="openDetail"
      @retry="onRetry"
      @empty-action="onCategoryEmptyAction"
    />
  </div>

  <MemoryBookCoverPicker
    :open="showCoverPicker"
    :year="selectedYear"
    :selected-design-id="selectedCoverDesign"
    @close="showCoverPicker = false"
    @select="onSelectCover"
  />

  <MemoryBookEditModal
    :open="showEditModal"
    :memory="itemDetail"
    :submitting="editSubmitting"
    :error="editError"
    @close="closeEditModal"
    @save="onSaveEdit"
  />

  <MemoryBookShareModal
    :open="showShareModal"
    :year="selectedYear"
    :summary="yearData.summary"
    :timeline="yearData.timeline"
    @close="showShareModal = false"
  />

  <MemoryBookAiRecapModal
    :open="showRecapModal"
    :year="selectedYear"
    :summary="yearData.summary"
    :timeline="yearData.timeline"
    @close="showRecapModal = false"
  />
</template>

<style scoped>
.page-memory-book {
  color: var(--site-text);
  min-width: 960px;
}
</style>
