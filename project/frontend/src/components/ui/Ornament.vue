<script setup>
/**
 * 部品名: 装飾ライン（金／紅の区切り）
 * 役割: セクション間の視覚的な「間」を取る
 */
defineProps({
  tone: { type: String, default: 'gold' },
})
</script>

<template>
  <div
    :style="{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '10px',
    }"
  >
    <span
      :style="{
        flex: 1,
        height: '1px',
        background: tone === 'gold' ? 'var(--kin-500)' : 'var(--beni-700)',
        opacity: 0.5,
      }"
    />
    <span
      :style="{
        color: tone === 'gold' ? 'var(--kin-500)' : 'var(--beni-700)',
        fontSize: '10px',
        letterSpacing: '0.3em',
      }"
    >◆◆◆</span>
    <span
      :style="{
        flex: 1,
        height: '1px',
        background: tone === 'gold' ? 'var(--kin-500)' : 'var(--beni-700)',
        opacity: 0.5,
      }"
    />
  </div>
</template>
