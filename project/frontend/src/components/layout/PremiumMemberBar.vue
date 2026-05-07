<script setup>
/**
 * 部品名: プレミアム会員お知らせバー
 */
const emit = defineEmits(['open-fanclub'])
</script>

<template>
  <div
    role="complementary"
    style="background: rgba(201,169,97,0.12); border-bottom: 1px solid rgba(201,169,97,0.25); padding: 8px 32px; text-align: center; font-size: 12px; font-family: var(--ff-mincho); letter-spacing: 0.2em"
  >
    <button
      type="button"
      style="background: transparent; border: 0; cursor: pointer; color: var(--kin-500); font-size: 12px; font-family: var(--ff-mincho); letter-spacing: 0.2em"
      @click="emit('open-fanclub')"
    >
      ✦ プレミアム会員特典を見る ›
    </button>
  </div>
</template>
