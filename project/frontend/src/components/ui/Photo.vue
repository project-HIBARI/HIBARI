<script setup>
/**
 * 部品名: 写真プレースホルダー
 * 役割: 実写真が無いときの和紙風ダミー枠＋キャプション
 */
defineProps({
  w: { type: Number, default: 240 },
  h: { type: Number, default: 320 },
  caption: { type: String, default: 'portrait' },
  variant: { type: String, default: 'default' },
})
</script>

<template>
  <div
    class="photo-ph"
    :class="{ dark: variant === 'dark', sepia: variant === 'sepia' }"
    :style="{ width: w + 'px', height: h + 'px' }"
  >
    <span>▣ {{ caption }}</span>
  </div>
</template>
