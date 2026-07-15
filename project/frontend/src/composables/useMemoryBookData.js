/**
 * Music Memory Book — APIデータ読み込み
 */
import { ref, readonly } from 'vue'
import { loadMemoryBookFromApi } from '../lib/memoryBookFromApi.js'

const loading = ref(false)
const error = ref('')
const summary = ref(null)
const categories = ref([])
const years = ref([])
const items = ref([])
let bookApi = null

async function fetchMemoryBook() {
  loading.value = true
  error.value = ''
  try {
    bookApi = await loadMemoryBookFromApi()
    summary.value = bookApi.summary
    categories.value = bookApi.categories
    years.value = bookApi.years
    items.value = bookApi.items
    return bookApi
  } catch (err) {
    error.value = err?.message || '思い出帳の読み込みに失敗しました'
    summary.value = {
      total: 0,
      startedAt: '—',
      categories: { flowers: 0, posts: 0, songs: 0, aiChats: 0 },
      currentYear: { year: new Date().getFullYear(), total: 0 },
    }
    categories.value = []
    years.value = [{ year: new Date().getFullYear(), total: 0, tone: 'purple' }]
    items.value = []
    bookApi = null
    throw err
  } finally {
    loading.value = false
  }
}

function getYearDetail(year) {
  return bookApi?.getYearDetail(year) ?? {
    year,
    summary: { flowers: 0, posts: 0, songs: 0, aiChats: 0, total: 0 },
    timeline: [],
  }
}

function getItemDetail(id) {
  return bookApi?.getItemDetail(id) ?? null
}

function getFilterViewData(mode, memoryId) {
  return bookApi?.getFilterViewData(mode, memoryId) ?? null
}

function getCategoryViewData(categoryId) {
  return bookApi?.getCategoryViewData(categoryId) ?? null
}

export function useMemoryBookData() {
  return {
    loading: readonly(loading),
    error: readonly(error),
    summary: readonly(summary),
    categories: readonly(categories),
    years: readonly(years),
    items: readonly(items),
    fetchMemoryBook,
    getYearDetail,
    getItemDetail,
    getFilterViewData,
    getCategoryViewData,
  }
}
