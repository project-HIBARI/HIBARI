/**
 * Music Memory Book — APIデータ読み込み
 */
import { ref, readonly } from 'vue'
import { createMemoryBookApi, loadMemoryBookFromApi } from '../lib/memoryBookFromApi.js'

const loading = ref(false)
const error = ref('')
const summary = ref(null)
const categories = ref([])
const years = ref([])
const items = ref([])
const bookVersion = ref(0)
let bookApi = null

function applyBookApi(nextBookApi) {
  bookApi = nextBookApi
  summary.value = nextBookApi.summary
  categories.value = nextBookApi.categories
  years.value = nextBookApi.years
  items.value = nextBookApi.items
  bookVersion.value += 1
}

async function fetchMemoryBook(options = {}) {
  const silent = options.silent === true
  if (!silent) {
    loading.value = true
  }
  error.value = ''
  try {
    const loaded = await loadMemoryBookFromApi()
    applyBookApi(loaded)
    return loaded
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
    bookVersion.value += 1
    throw err
  } finally {
    if (!silent) {
      loading.value = false
    }
  }
}

function removeItemLocally(id) {
  if (!bookApi || !id) return
  const nextItems = bookApi.items.filter((item) => item.id !== id)
  applyBookApi(createMemoryBookApi(nextItems))
}

function replaceItemLocally(id, nextItem) {
  if (!bookApi || !id || !nextItem) return
  const nextItems = bookApi.items.map((item) => (item.id === id ? nextItem : item))
  applyBookApi(createMemoryBookApi(nextItems))
}

function getYearDetail(year) {
  void bookVersion.value
  return bookApi?.getYearDetail(year) ?? {
    year,
    summary: { flowers: 0, posts: 0, songs: 0, aiChats: 0, total: 0 },
    timeline: [],
  }
}

function getItemDetail(id) {
  void bookVersion.value
  return bookApi?.getItemDetail(id) ?? null
}

function getFilterViewData(mode, memoryId) {
  void bookVersion.value
  return bookApi?.getFilterViewData(mode, memoryId) ?? null
}

function getCategoryViewData(categoryId) {
  void bookVersion.value
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
    bookVersion: readonly(bookVersion),
    fetchMemoryBook,
    removeItemLocally,
    replaceItemLocally,
    getYearDetail,
    getItemDetail,
    getFilterViewData,
    getCategoryViewData,
  }
}
