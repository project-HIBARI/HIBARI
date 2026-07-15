/**
 * Music Memory Book — 年別アルバム表紙の選択状態（localStorage）
 */
import { ref, readonly } from 'vue'
import { normalizeCoverDesignId } from '../lib/memoryBookCoverDesigns.js'

const STORAGE_KEY = 'hbr-mmb-covers'

const coversByYear = ref(loadCovers())

function loadCovers() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return {}
    const parsed = JSON.parse(raw)
    return parsed && typeof parsed === 'object' ? parsed : {}
  } catch {
    return {}
  }
}

function persistCovers() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(coversByYear.value))
  } catch {
    /* ignore */
  }
}

function getCoverDesign(year) {
  const key = String(year)
  return normalizeCoverDesignId(coversByYear.value[key] ?? 1)
}

function setCoverDesign(year, designId) {
  const key = String(year)
  coversByYear.value = {
    ...coversByYear.value,
    [key]: normalizeCoverDesignId(designId),
  }
  persistCovers()
}

export function useMemoryBookCover() {
  return {
    coversByYear: readonly(coversByYear),
    getCoverDesign,
    setCoverDesign,
  }
}
