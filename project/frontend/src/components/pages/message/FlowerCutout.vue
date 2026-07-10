<script setup>
/**
 * 部品名: 献花 — 花画像（背景透過PNG）
 */
defineProps({
  src: { type: String, required: true },
  alt: { type: String, default: '' },
  /** sm=一覧カード / md=モーダル / lg=強調 */
  size: { type: String, default: 'md' },
})
</script>

<template>
  <span class="flower-cutout" :class="`flower-cutout--${size}`">
    <img
      :src="src"
      :alt="alt"
      class="flower-cutout__img"
      decoding="async"
      loading="lazy"
    />
  </span>
</template>

<style scoped>
.flower-cutout {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: transparent;
  overflow: visible;
}

.flower-cutout__img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center bottom;
  filter: drop-shadow(0 6px 16px rgba(59, 47, 42, 0.14));
}

.flower-cutout--sm {
  width: 100px;
  height: 124px;
}

.flower-cutout--md {
  width: 112px;
  height: 136px;
}

.flower-cutout--lg {
  width: 128px;
  height: 156px;
}
</style>
