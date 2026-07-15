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
    <template v-else-if="name === 'eye'">
      <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z" />
      <circle cx="12" cy="12" r="3" />
    </template>
    <template v-else-if="name === 'eye-off'">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-10-8-10-8a18.45 18.45 0 0 1 5.06-5.94" />
      <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 10 8 10 8a18.5 18.5 0 0 1-2.16 3.19" />
      <line x1="1" y1="1" x2="23" y2="23" />
    </template>
    <template v-else-if="name === 'bookmark'">
      <path d="M6 3h12v18l-6-4.5L6 21V3z" />
    </template>
    <template v-else-if="name === 'share'">
      <circle cx="18" cy="5" r="2.6" />
      <circle cx="6" cy="12" r="2.6" />
      <circle cx="18" cy="19" r="2.6" />
      <line x1="8.3" y1="10.7" x2="15.7" y2="6.3" />
      <line x1="8.3" y1="13.3" x2="15.7" y2="17.7" />
    </template>
    <template v-else-if="name === 'more'">
      <circle cx="5" cy="12" r="1.4" fill="currentColor" stroke="none" />
      <circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none" />
      <circle cx="19" cy="12" r="1.4" fill="currentColor" stroke="none" />
    </template>
    <template v-else-if="name === 'plus'">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </template>
    <template v-else-if="name === 'send'">
      <line x1="21" y1="3" x2="10" y2="14" />
      <polygon points="21,3 14,21 10,14 3,10" />
    </template>
    <template v-else-if="name === 'image'">
      <rect x="3" y="4" width="18" height="16" rx="1.5" />
      <circle cx="8.5" cy="9.5" r="1.8" />
      <path d="M4 17l5-5 4 4 3-3 4 4" />
    </template>
    <template v-else-if="name === 'video'">
      <rect x="2.5" y="6" width="13" height="12" rx="1.5" />
      <polygon points="21.5,8.5 21.5,15.5 15.5,12" />
    </template>
    <template v-else-if="name === 'close'">
      <line x1="5" y1="5" x2="19" y2="19" />
      <line x1="19" y1="5" x2="5" y2="19" />
    </template>
    <template v-else-if="name === 'home'">
      <path d="M4 11.5 12 4l8 7.5" />
      <path d="M6 10v10h12V10" />
    </template>
    <template v-else-if="name === 'user'">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8" />
    </template>
    <template v-else-if="name === 'mail'">
      <rect x="3" y="5" width="18" height="14" rx="1.5" />
      <path d="M4 6.5l8 6 8-6" />
    </template>
    <template v-else-if="name === 'story-ring'">
      <circle cx="12" cy="12" r="9.5" />
    </template>
    <template v-else-if="name === 'camera'">
      <path d="M4 8h3l1.6-2.4h6.8L17 8h3a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z" />
      <circle cx="12" cy="14" r="3.6" />
    </template>
    <template v-else-if="name === 'crown'">
      <path d="M3 8l4 3 5-6 5 6 4-3-2 10H5L3 8z" />
      <line x1="5" y1="21" x2="19" y2="21" />
    </template>
    <template v-else-if="name === 'download'">
      <path d="M12 3v12" />
      <polyline points="7,10 12,15 17,10" />
      <path d="M4 19h16" />
    </template>
    <template v-else-if="name === 'copy'">
      <rect x="3" y="3" width="13" height="13" rx="1.5" />
      <path d="M8 16v3a1 1 0 0 0 1 1h10a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1h-3" />
    </template>
    <template v-else-if="name === 'book'">
      <path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H12v18H6.5A2.5 2.5 0 0 0 4 22.5z" />
      <path d="M20 4.5A2.5 2.5 0 0 0 17.5 2H12v18h5.5A2.5 2.5 0 0 1 20 22.5z" />
      <line x1="12" y1="2" x2="12" y2="20" />
    </template>
    <template v-else-if="name === 'bell'">
      <path d="M6 10a6 6 0 0 1 12 0c0 4 1.5 6 2.5 7H3.5C4.5 16 6 14 6 10z" />
      <path d="M9.5 20a2.5 2.5 0 0 0 5 0" />
    </template>
    <template v-else-if="name === 'spark'">
      <path d="M12 2v4" />
      <path d="M12 18v4" />
      <path d="M2 12h4" />
      <path d="M18 12h4" />
      <path d="M5 5l2.5 2.5" />
      <path d="M16.5 16.5 19 19" />
      <path d="M19 5l-2.5 2.5" />
      <path d="M7.5 16.5 5 19" />
      <circle cx="12" cy="12" r="2.2" />
    </template>
    <template v-else-if="name === 'tear'">
      <path d="M12 2s6 8 6 12.5a6 6 0 0 1-12 0C6 10 12 2 12 2z" />
    </template>
    <template v-else-if="name === 'nostalgic'">
      <circle cx="12" cy="13" r="7" />
      <path d="M12 9v4l3 2" />
      <path d="M9 3l-2 2" />
      <path d="M15 3l2 2" />
    </template>
    <template v-else-if="name === 'loved-one'">
      <path d="M12 20.5s-7-4.5-7-10a4 4 0 0 1 7-2.5 4 4 0 0 1 7 2.5c0 5.5-7 10-7 10z" />
    </template>
    <template v-else-if="name === 'energized'">
      <polygon points="13,2 4,14 11,14 10,22 20,9 13,9" />
    </template>
    <template v-else-if="name === 'special-moment'">
      <path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M18 6l-2.5 2.5M8.5 15.5L6 18" />
      <circle cx="12" cy="12" r="3" />
    </template>
  </svg>
</template>