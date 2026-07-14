<script setup>
/**
 * ページ: Music Memory Book
 * 構成: TOP / 年別アルバム / 思い出詳細
 */
import { ref, watch } from 'vue'
import MemoryBookTopView from './memorybook/MemoryBookTopView.vue'
import MemoryBookYearView from './memorybook/MemoryBookYearView.vue'
import MemoryBookDetailView from './memorybook/MemoryBookDetailView.vue'

const emit = defineEmits(['navigate', 'open-auth', 'open-modal'])

const view = ref('top')
const selectedYear = ref(2026)

watch(view, () => {
  window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
})

function openYear(year) {
  selectedYear.value = year
  view.value = 'year'
}

function openDetail() {
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
</script>

<template>
  <div class="page-memory-book">
    <MemoryBookTopView
      v-if="view === 'top'"
      @open-year="openYear"
      @open-detail="openDetail"
      @open-fanclub="openFanclub"
      @open-category="onCategory"
    />

    <MemoryBookYearView
      v-else-if="view === 'year'"
      @back="goTop"
      @open-detail="openDetail"
      @open-fanclub="openFanclub"
      @coming-soon="onComingSoon"
    />

    <MemoryBookDetailView
      v-else-if="view === 'detail'"
      @back="goTop"
      @back-year="goYear"
      @open-fanclub="openFanclub"
      @coming-soon="onComingSoon"
    />
  </div>
</template>

<style scoped>
.page-memory-book {
  color: var(--site-text);
  min-width: 960px;
}
</style>
