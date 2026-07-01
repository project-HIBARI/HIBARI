<script setup>
/**
 * 部品名: アイコン（線画 SVG セット）
 * 用途: 検索・再生・矢印など UI 全体で共通利用
 */
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
  size: { type: Number, default: 18 },
  color: { type: String, default: 'currentColor' },
})

const common = computed(() => ({
  width: props.size,
  height: props.size,
  fill: 'none',
  stroke: props.color,
  strokeWidth: 1.4,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
}))
</script>

<template>
  <svg viewBox="0 0 24 24" v-bind="common">
    <template v-if="name === 'play'">
      <polygon points="6,4 20,12 6,20" :fill="color" stroke="none" />
    </template>
    <template v-else-if="name === 'search'">
      <circle cx="10" cy="10" r="6" />
      <line x1="15" y1="15" x2="20" y2="20" />
    </template>
    <template v-else-if="name === 'arrow'">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="13,6 19,12 13,18" />
    </template>
    <template v-else-if="name === 'pin'">
      <path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z" />
      <circle cx="12" cy="10" r="2.5" />
    </template>
    <template v-else-if="name === 'map'">
      <polygon points="3,6 9,4 15,6 21,4 21,18 15,20 9,18 3,20" />
      <line x1="9" y1="4" x2="9" y2="18" />
      <line x1="15" y1="6" x2="15" y2="20" />
    </template>
    <template v-else-if="name === 'chat'">
      <path d="M4 5h16v11H9l-5 4V5z" />
    </template>
    <template v-else-if="name === 'calendar'">
      <rect x="3" y="5" width="18" height="16" rx="1" />
      <line x1="3" y1="10" x2="21" y2="10" />
      <line x1="8" y1="3" x2="8" y2="7" />
      <line x1="16" y1="3" x2="16" y2="7" />
    </template>
    <template v-else-if="name === 'disc'">
      <circle cx="12" cy="12" r="9" />
      <circle cx="12" cy="12" r="2" />
    </template>
    <template v-else-if="name === 'flower'">
      <circle cx="12" cy="12" r="2.2" />
      <circle cx="12" cy="6" r="3" />
      <circle cx="12" cy="18" r="3" />
      <circle cx="6" cy="12" r="3" />
      <circle cx="18" cy="12" r="3" />
    </template>
    <template v-else-if="name === 'heart'">
      <path d="M12 20.5s-7-4.5-7-10a4 4 0 0 1 7-2.5 4 4 0 0 1 7 2.5c0 5.5-7 10-7 10z" />
    </template>
  </svg>
</template>
