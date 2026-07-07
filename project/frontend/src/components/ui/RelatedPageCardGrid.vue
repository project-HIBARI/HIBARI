<script setup>
/**
 * 部品名: 関連ページ導線カードグリッド
 * 用途: RelatedPageCard を横並びに配置するラッパー
 */
defineProps({
  columns: { type: Number, default: 5 },
})
</script>

<template>
  <div
    class="related-grid"
    :style="{ '--related-cols': columns }"
  >
    <slot />
  </div>
</template>

<style scoped>
.related-grid {
  display: grid;
  grid-template-columns: repeat(var(--related-cols, 5), minmax(0, 1fr));
  gap: 16px;
}

@media (max-width: 1200px) {
  .related-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 767px) {
  .related-grid {
    grid-template-columns: 1fr;
  }
}
</style>
