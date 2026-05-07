<script setup>
/**
 * 部品名: 判子（はんこ）
 * 役割: ロゴ横の印影風バッジ。「雲雀」など短い文字列を表示
 */
defineProps({
  text: { type: String, default: '雲雀' },
  size: { type: Number, default: 48 },
  rotate: { type: Number, default: -4 },
})
</script>

<template>
  <span
    class="hanko"
    :style="{
      width: size + 'px',
      height: size + 'px',
      fontSize: size * 0.32 + 'px',
      transform: `rotate(${rotate}deg)`,
      writingMode: text.length > 2 ? 'vertical-rl' : 'horizontal-tb',
    }"
  >{{ text }}</span>
</template>
