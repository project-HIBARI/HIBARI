/**
 * 文字サイズ切替（全インスタンスで状態を共有）
 */
import { ref, readonly } from 'vue'

const STORAGE_KEY = 'hibari-text-size'
const VALID = ['s', 'm', 'l', 'xl']
const SIZE_PX = { s: '14px', m: '16px', l: '19px', xl: '22px' }

function readStoredSize() {
  if (typeof window === 'undefined') return 'm'
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored && VALID.includes(stored)) return stored
  } catch {
    /* ignore */
  }
  const attr = document.documentElement.getAttribute('data-text-size')
  return VALID.includes(attr) ? attr : 'm'
}

function applyTextSize(value) {
  if (typeof document === 'undefined') return
  document.documentElement.setAttribute('data-text-size', value)
  document.documentElement.style.fontSize = SIZE_PX[value] || SIZE_PX.m
}

const size = ref(readStoredSize())
applyTextSize(size.value)

if (typeof window !== 'undefined') {
  window.addEventListener('storage', (event) => {
    if (event.key !== STORAGE_KEY || !event.newValue || !VALID.includes(event.newValue)) return
    size.value = event.newValue
    applyTextSize(event.newValue)
  })
}

export function useTextSize() {
  function setSize(value) {
    if (!VALID.includes(value)) return
    size.value = value
    applyTextSize(value)
    try {
      localStorage.setItem(STORAGE_KEY, value)
    } catch {
      /* ignore */
    }
  }

  return {
    size: readonly(size),
    setSize,
    presets: [
      ['s', '小'],
      ['m', '中'],
      ['l', '大'],
      ['xl', '特'],
    ],
  }
}
