<script setup>
/**
 * 部品名: 文字サイズ切替（大中小）
 * 役割: html[data-text-size] を更新し tokens.css のスケールを反映
 */
import { ref, watch } from 'vue'

defineProps({
  /** ink: 明るい紙面向け / paper: 暗いヘッダー向け */
  tone: { type: String, default: 'ink' },
})

const size = ref(
  typeof document !== 'undefined'
    ? document.documentElement.getAttribute('data-text-size') || 'm'
    : 'm',
)

watch(
  size,
  (v) => {
    document.documentElement.setAttribute('data-text-size', v)
  },
  { immediate: true },
)

const presets = [
  ['s', '小', 12],
  ['m', '中', 14],
  ['l', '大', 16],
  ['xl', '特', 18],
]
</script>

<template>
  <div
    :style="{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      fontFamily: 'var(--ff-serif)',
      fontSize: '11px',
      color: tone === 'paper' ? 'var(--paper-100)' : 'var(--ink-800)',
    }"
  >
    <span :style="{ opacity: 0.7 }">文字サイズ</span>
    <div
      :style="{
        display: 'inline-flex',
        border: `1px solid ${tone === 'paper' ? 'rgba(244,237,224,0.3)' : 'rgba(26,20,16,0.2)'}`,
        borderRadius: '2px',
      }"
    >
      <button
        v-for="([k, lbl, fs], idx) in presets"
        :key="k"
        type="button"
        :style="{
          border: 0,
          background:
            size === k
              ? tone === 'paper'
                ? 'var(--paper-100)'
                : 'var(--ink-900)'
              : 'transparent',
          color:
            size === k
              ? tone === 'paper'
                ? 'var(--ink-900)'
                : 'var(--paper-100)'
              : tone === 'paper'
                ? 'var(--paper-100)'
                : 'var(--ink-800)',
          padding: '4px 10px',
          cursor: 'pointer',
          fontSize: fs + 'px',
          fontFamily: 'var(--ff-mincho)',
          borderRight: idx < presets.length - 1 ? `1px solid ${tone === 'paper' ? 'rgba(244,237,224,0.3)' : 'rgba(26,20,16,0.2)'}` : 'none',
        }"
        @click="size = k"
      >
        {{ lbl }}
      </button>
    </div>
  </div>
</template>
