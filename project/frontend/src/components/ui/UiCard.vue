<script setup>
/**
 * 部品名: 共通カード
 * 用途: ホーム・歩み・ディスコグラフィー・ゆかりの地の各ページで
 *       情報ブロックをまとめて表示するライトテーマ用カード
 */
defineProps({
  /** パディング量: sm / md / lg */
  padding: { type: String, default: 'md' },
  /** 背景トーン: white / warm / pink / purple */
  tone: { type: String, default: 'white' },
  /** 枠線を表示するか */
  bordered: { type: Boolean, default: true },
})
</script>

<template>
  <article
    class="ui-card"
    :class="[
      `ui-card--pad-${padding}`,
      `ui-card--tone-${tone}`,
      { 'ui-card--bordered': bordered },
    ]"
  >
    <slot />
  </article>
</template>

<style scoped>
.ui-card {
  border-radius: var(--site-radius-lg);
  box-shadow: var(--site-shadow);
  overflow: hidden;
}
.ui-card--bordered {
  border: 1px solid var(--site-border);
}
.ui-card--pad-sm {
  padding: var(--sp-4);
}
.ui-card--pad-md {
  padding: var(--sp-5);
}
.ui-card--pad-lg {
  padding: var(--sp-6);
}
.ui-card--tone-white {
  background: var(--site-surface);
}
.ui-card--tone-warm {
  background: var(--site-surface-muted);
}
.ui-card--tone-pink {
  background: linear-gradient(135deg, var(--site-bg-pink) 0%, var(--site-surface) 100%);
}
.ui-card--tone-purple {
  background: linear-gradient(135deg, var(--murasaki-800) 0%, var(--murasaki-700) 100%);
  color: var(--paper-50);
  border-color: rgba(255, 255, 255, 0.15);
  box-shadow: var(--site-shadow-md);
}
</style>
