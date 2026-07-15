<script setup>
/**
 * 部品名: 献花 — 献花数カウンター
 */
import { useCountUp } from '../../../composables/useCountUp.js'

const props = defineProps({
  total: { type: Number, default: 0 },
})

const display = useCountUp(() => props.total)
</script>

<template>
  <section class="msg-count" aria-label="現在の献花数">
    <p class="msg-count__label">現在の献花数</p>
    <p class="msg-count__value">
      <span class="msg-count__num" aria-live="polite">{{ display.toLocaleString() }}</span>
      <span class="msg-count__icon" aria-hidden="true">🌸</span>
    </p>
  </section>
</template>

<style scoped>
.msg-count {
  text-align: center;
  margin-bottom: var(--sp-7);
  padding: var(--sp-6) var(--sp-5);
  border-radius: 24px;
  background: color-mix(in srgb, var(--site-surface) 72%, transparent);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid color-mix(in srgb, var(--kin-500) 28%, var(--site-border));
  box-shadow: 0 12px 40px rgba(59, 47, 42, 0.06);
}

.msg-count__label {
  margin: 0 0 var(--sp-3);
  font-family: var(--ff-latin);
  font-size: var(--font-size-caption);
  letter-spacing: 0.28em;
  color: var(--kin-600);
}

.msg-count__value {
  margin: 0;
  display: inline-flex;
  align-items: center;
  gap: var(--sp-4);
}

.msg-count__num {
  font-family: var(--ff-mincho);
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 800;
  letter-spacing: 0.04em;
  line-height: 1;
  color: var(--murasaki-700);
}

.msg-count__icon {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  line-height: 1;
  filter: drop-shadow(0 4px 8px rgba(201, 169, 97, 0.25));
}
</style>
