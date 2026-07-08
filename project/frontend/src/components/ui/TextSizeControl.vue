<script setup>
/**
 * 部品名: 文字サイズ切替（小・中・大・特）
 * 役割: html[data-text-size] を更新し tokens.css のスケールを反映
 */
import { ref, watch } from 'vue'

const STORAGE_KEY = 'hibari-text-size'

const props = defineProps({
  /** ink: 明るい紙面向け / paper: 暗いヘッダー向け */
  tone: { type: String, default: 'ink' },
  /** default / header（ヘッダー内コンパクト表示） */
  variant: { type: String, default: 'default' },
})

function readInitialSize() {
  if (typeof document === 'undefined') return 'm'
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored && ['s', 'm', 'l', 'xl'].includes(stored)) return stored
  } catch {
    /* ignore */
  }
  return document.documentElement.getAttribute('data-text-size') || 'm'
}

const size = ref(readInitialSize())

watch(
  size,
  (v) => {
    document.documentElement.setAttribute('data-text-size', v)
    try {
      localStorage.setItem(STORAGE_KEY, v)
    } catch {
      /* ignore */
    }
  },
  { immediate: true },
)

const presets = [
  ['s', '小'],
  ['m', '中'],
  ['l', '大'],
  ['xl', '特'],
]
</script>

<template>
  <div
    class="text-size-control"
    :class="[
      `text-size-control--${tone}`,
      `text-size-control--${variant}`,
    ]"
  >
    <span class="text-size-control__label">文字サイズ</span>
    <div class="text-size-control__group" role="group" aria-label="文字サイズ">
      <button
        v-for="[k, lbl] in presets"
        :key="k"
        type="button"
        class="text-size-control__btn"
        :class="{ 'text-size-control__btn--active': size === k }"
        :aria-pressed="size === k"
        @click="size = k"
      >
        {{ lbl }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.text-size-control {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  flex-shrink: 0;
}

.text-size-control__label {
  font-size: 11px;
  letter-spacing: 0.06em;
  white-space: nowrap;
}

.text-size-control--ink .text-size-control__label {
  color: var(--site-text-muted);
}

.text-size-control--paper .text-size-control__label {
  color: var(--paper-100);
  opacity: 0.85;
}

.text-size-control__group {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 2px;
  border: 1px solid rgba(201, 169, 97, 0.45);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.6);
}

.text-size-control--paper .text-size-control__group {
  border-color: rgba(244, 237, 224, 0.35);
  background: rgba(0, 0, 0, 0.12);
}

.text-size-control__btn {
  min-width: 28px;
  height: 28px;
  padding: 0 6px;
  border: 0;
  border-radius: 4px;
  background: transparent;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: 12px;
  line-height: 1;
  color: var(--site-text);
  transition: background 0.2s, color 0.2s;
}

.text-size-control--paper .text-size-control__btn {
  color: var(--paper-100);
}

.text-size-control__btn:hover {
  background: rgba(201, 169, 97, 0.12);
}

.text-size-control__btn--active {
  background: var(--murasaki-700);
  color: #fff;
}

.text-size-control--paper .text-size-control__btn--active {
  background: var(--paper-100);
  color: var(--ink-900);
}

/* ヘッダー内コンパクト表示 */
.text-size-control--header {
  gap: 10px;
}

.text-size-control--header .text-size-control__label {
  font-size: 12px;
}

.text-size-control--header .text-size-control__group {
  gap: 3px;
}

.text-size-control--header .text-size-control__btn {
  min-width: 30px;
  height: 30px;
  font-size: 12px;
}

@media (max-width: 1199px) {
  .text-size-control--header .text-size-control__label {
    display: none;
  }
}
</style>
