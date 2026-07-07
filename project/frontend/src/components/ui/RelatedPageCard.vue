<script setup>
/**
 * 部品名: 関連ページ導線カード
 * 用途: ホーム等の横並びカテゴリ導線（他ページ展開用の最小共通部品）
 */
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  variant: { type: String, default: 'default' },
})

defineEmits(['click'])
</script>

<template>
  <button
    type="button"
    class="related-card"
    :class="`related-card--${variant}`"
    @click="$emit('click')"
  >
    <div class="related-card__body">
      <h3 class="related-card__title">{{ title }}</h3>
      <p v-if="subtitle" class="related-card__subtitle">{{ subtitle }}</p>
      <span class="related-card__arrow" aria-hidden="true">›</span>
    </div>
    <div class="related-card__visual" aria-hidden="true" />
  </button>
</template>

<style scoped>
.related-card {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  width: 100%;
  min-height: 128px;
  padding: 0;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: linear-gradient(135deg, #fffefb 0%, #fff9f6 100%);
  box-shadow: var(--site-shadow);
  overflow: hidden;
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.related-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.related-card__body {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px 16px 20px 20px;
  min-width: 0;
}
.related-card__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.05em;
  line-height: 1.45;
  color: var(--site-text);
}
.related-card__subtitle {
  margin: 0;
  font-size: 11px;
  line-height: 1.55;
  color: var(--site-text-muted);
  letter-spacing: 0.03em;
}
.related-card__arrow {
  position: absolute;
  right: 14px;
  bottom: 18px;
  font-size: 18px;
  color: var(--murasaki-500);
  line-height: 1;
}
.related-card__visual {
  width: 40%;
  min-width: 92px;
  max-width: 120px;
  flex-shrink: 0;
  position: relative;
  background: var(--site-surface-muted);
}
.related-card--rose .related-card__visual {
  background:
    radial-gradient(circle at 28% 62%, rgba(220, 120, 140, 0.4) 0%, transparent 52%),
    radial-gradient(circle at 72% 38%, rgba(240, 160, 180, 0.35) 0%, transparent 48%),
    linear-gradient(155deg, #fce8ec, #f5ebe0);
}
.related-card--record .related-card__visual {
  background:
    radial-gradient(circle at center, #2a201a 28%, transparent 29%),
    repeating-radial-gradient(circle at center, #333 0 1px, #222 1px 3px),
    linear-gradient(160deg, #3a2a1a, #1a1410);
}
.related-card--record .related-card__visual::after {
  content: '';
  position: absolute;
  inset: 50% auto auto 50%;
  transform: translate(-50%, -50%);
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 2px solid rgba(201, 169, 97, 0.45);
  background: radial-gradient(circle, var(--beni-700) 0%, #5e1111 100%);
}
.related-card--gallery .related-card__visual {
  background:
    linear-gradient(135deg, #d9c7a6 0%, #c4a882 100%),
    repeating-linear-gradient(-12deg, transparent, transparent 8px, rgba(255, 255, 255, 0.15) 8px, rgba(255, 255, 255, 0.15) 10px);
  box-shadow: inset 0 0 0 6px rgba(255, 255, 255, 0.28);
}
.related-card--stage .related-card__visual {
  background:
    radial-gradient(ellipse at 50% 0%, rgba(255, 220, 100, 0.55) 0%, transparent 58%),
    linear-gradient(180deg, #4a1520 0%, #2a0810 100%);
}
.related-card--fanclub .related-card__visual {
  background: linear-gradient(135deg, var(--murasaki-700), var(--murasaki-900));
}
.related-card--fanclub .related-card__visual::after {
  content: 'FC';
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--ff-latin);
  font-size: 22px;
  font-weight: 700;
  color: var(--kin-400);
  letter-spacing: 0.12em;
}
</style>
