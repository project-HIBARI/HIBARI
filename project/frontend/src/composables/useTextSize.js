/**
 * 文字サイズ切替（Music Memories 全体で状態を共有）
 * html[data-text-size="s|m|l"] と tokens.css の変数で適用する。
 */
import { ref, readonly } from 'vue'

export const STORAGE_KEY = 'hibari-text-size'
const VALID = ['s', 'm', 'l']

const PRESETS = [
  ['s', '小'],
  ['m', '中'],
  ['l', '大'],
]

/**
 * 保存値・属性値を正規化する（xl は互換のため l へ）
 * @param {unknown} value
 * @returns {'s'|'m'|'l'}
 */
export function normalizeTextSize(value) {
  if (value === 'xl') return 'l'
  if (value === 's' || value === 'm' || value === 'l') return value
  return 'm'
}

function readRawStored() {
  if (typeof window === 'undefined') return null
  try {
    return localStorage.getItem(STORAGE_KEY)
  } catch {
    return null
  }
}

function persistSize(value) {
  if (typeof window === 'undefined') return
  try {
    localStorage.setItem(STORAGE_KEY, value)
  } catch {
    /* ignore */
  }
}

function readStoredSize() {
  const stored = readRawStored()
  if (stored != null) {
    const normalized = normalizeTextSize(stored)
    if (stored === 'xl') persistSize(normalized)
    return normalized
  }
  if (typeof document !== 'undefined') {
    return normalizeTextSize(document.documentElement.dataset.textSize)
  }
  return 'm'
}

function clearLegacyInlineStyles(root) {
  root.style.removeProperty('font-size')
  root.style.removeProperty('--text-scale')
}

function applyTextSize(value) {
  if (typeof document === 'undefined') return
  const root = document.documentElement
  const next = normalizeTextSize(value)
  clearLegacyInlineStyles(root)
  if (root.dataset.textSize === next) return
  root.dataset.textSize = next
}

const size = ref(readStoredSize())
applyTextSize(size.value)

let storageListening = false

function onStorage(event) {
  if (event.key !== STORAGE_KEY) return
  const next = event.newValue == null ? 'm' : normalizeTextSize(event.newValue)
  if (size.value === next) {
    applyTextSize(next)
    return
  }
  size.value = next
  applyTextSize(next)
  if (event.newValue === 'xl') persistSize(next)
}

function ensureStorageListener() {
  if (storageListening || typeof window === 'undefined') return
  storageListening = true
  window.addEventListener('storage', onStorage)
}

ensureStorageListener()

export function useTextSize() {
  function setSize(value) {
    if (value !== 's' && value !== 'm' && value !== 'l' && value !== 'xl') return
    const next = normalizeTextSize(value)
    if (size.value === next) {
      applyTextSize(next)
      return
    }
    size.value = next
    applyTextSize(next)
    persistSize(next)
  }

  return {
    size: readonly(size),
    setSize,
    presets: PRESETS,
  }
}
