<script setup>
/**
 * 部品名: 登録ステップインジケーター
 * 用途: ウィザードの現在地（何ステップ目か）を視覚化する
 * props: steps=ラベル配列, current=現在のステップ番号(0始まり)
 */
defineProps({
  steps: { type: Array, required: true },
  current: { type: Number, default: 0 },
})
</script>

<template>
  <ol class="reg-steps" aria-label="登録の進行状況">
    <li
      v-for="(label, i) in steps"
      :key="label"
      class="reg-steps__item"
      :class="{
        'reg-steps__item--done': i < current,
        'reg-steps__item--active': i === current,
      }"
      :aria-current="i === current ? 'step' : undefined"
    >
      <span class="reg-steps__dot">
        <span v-if="i < current" aria-hidden="true">✓</span>
        <span v-else>{{ i + 1 }}</span>
      </span>
      <span class="reg-steps__label">{{ label }}</span>
    </li>
  </ol>
</template>

<style scoped>
.reg-steps {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0;
  list-style: none;
  margin: 0 0 28px;
  padding: 0;
}
.reg-steps__item {
  position: relative;
  flex: 1 1 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  max-width: 120px;
}
/* ステップ間をつなぐ線 */
.reg-steps__item::before {
  content: '';
  position: absolute;
  top: 15px;
  right: 50%;
  width: 100%;
  height: 2px;
  background: var(--site-border);
}
.reg-steps__item:first-child::before {
  display: none;
}
.reg-steps__item--done::before,
.reg-steps__item--active::before {
  background: var(--kin-500);
}
.reg-steps__dot {
  position: relative;
  z-index: 1;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: var(--site-surface);
  border: 1.5px solid var(--site-border-strong);
  font-family: var(--ff-latin);
  font-size: 13px;
  font-weight: 700;
  color: var(--site-text-light);
  transition: background 0.25s, border-color 0.25s, color 0.25s;
}
.reg-steps__item--done .reg-steps__dot {
  background: var(--kin-500);
  border-color: var(--kin-600);
  color: var(--ink-900);
}
.reg-steps__item--active .reg-steps__dot {
  background: var(--murasaki-700);
  border-color: var(--murasaki-800);
  color: #fff;
  box-shadow: 0 0 0 4px rgba(122, 80, 136, 0.15);
}
.reg-steps__label {
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.02em;
  text-align: center;
  color: var(--site-text-light);
  line-height: 1.4;
}
.reg-steps__item--active .reg-steps__label {
  color: var(--murasaki-700);
  font-weight: 700;
}
.reg-steps__item--done .reg-steps__label {
  color: var(--site-text-muted);
}

@media (max-width: 480px) {
  .reg-steps__label {
    font-size: 10px;
  }
  .reg-steps__dot {
    width: 28px;
    height: 28px;
    font-size: 12px;
  }
  .reg-steps__item::before {
    top: 13px;
  }
}
</style>
