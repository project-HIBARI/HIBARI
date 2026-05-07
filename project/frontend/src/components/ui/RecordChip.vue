<script setup>
/**
 * 部品名: レコード盤チップ
 * 役割: ディスコグラフィ一覧で品番つきの円形ビジュアル
 */
defineProps({
  no: { type: String, default: '' },
  color: { type: String, default: 'var(--beni-700)' },
})
</script>

<template>
  <div
    :style="{
      width: '92px',
      height: '92px',
      borderRadius: '50%',
      background: `radial-gradient(circle at 50% 50%, ${color} 0 32%, #0a0a0a 32% 34%, ${color} 34% 55%, #0a0a0a 55% 57%, #1a1410 57% 100%)`,
      position: 'relative',
      flexShrink: 0,
      boxShadow: '0 4px 12px rgba(0,0,0,0.25)',
    }"
  >
    <div
      :style="{
        position: 'absolute',
        inset: '50% 0 0 50%',
        transform: 'translate(-50%, -50%)',
        width: '6px',
        height: '6px',
        borderRadius: '50%',
        background: 'var(--paper-100)',
      }"
    />
    <div
      :style="{
        position: 'absolute',
        top: '4px',
        left: '50%',
        transform: 'translateX(-50%)',
        fontSize: '8px',
        color: 'var(--paper-100)',
        fontFamily: 'var(--ff-mono)',
        letterSpacing: '0.1em',
      }"
    >{{ no }}</div>
  </div>
</template>
