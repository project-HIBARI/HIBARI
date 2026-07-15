<script setup>
/**
 * 部品名: 共通ボタン
 * 用途: ヘッダー・各ページの CTA・フィルタ等で使うライトテーマ用ボタン
 */
import { aosAttrs } from '../../lib/aos.js'

defineProps({
  /** primary=紫 / outline=線枠 / ghost=透明 / gold=金アクセント */
  variant: { type: String, default: 'primary' },
  /** sm / md / lg */
  size: { type: String, default: 'md' },
  /** button / submit / reset */
  type: { type: String, default: 'button' },
  /** 無効状態 */
  disabled: { type: Boolean, default: false },
  /** AOS スクロールアニメーション */
  aos: { type: Boolean, default: false },
  /** AOS 遅延（ms） */
  aosDelay: { type: Number, default: 0 },
})

defineEmits(['click'])
</script>

<template>
  <button
    :type="type"
    class="ui-btn"
    :class="[`ui-btn--${variant}`, `ui-btn--${size}`]"
    :disabled="disabled"
    v-bind="aos ? aosAttrs(aosDelay) : {}"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

<style scoped>
.ui-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-sizing: border-box;
  font-family: var(--ff-sans-jp);
  font-weight: 500;
  letter-spacing: 0.08em;
  line-height: 1.35;
  cursor: pointer;
  border-radius: var(--site-radius-sm);
  transition: background 0.2s, border-color 0.2s, color 0.2s, box-shadow 0.2s, transform 0.45s cubic-bezier(0.22, 1, 0.36, 1);
  /* 短い操作ラベル向け。長い文言は幅可変で対応し、強制2行化はしない */
  white-space: nowrap;
}
.ui-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.ui-btn:focus-visible {
  outline: 2px solid var(--murasaki-600);
  outline-offset: 2px;
}
.ui-btn--sm {
  padding: 0.375rem 0.875rem;
  font-size: var(--font-size-button-sm);
  /* 文字サイズ「小」でもタップ領域を 44px 未満へ縮小しない */
  min-height: max(44px, 2.75rem);
}
.ui-btn--md {
  padding: 0.625rem 1.25rem;
  font-size: var(--font-size-button);
  min-height: max(44px, 2.75rem);
}
.ui-btn--lg {
  padding: 0.875rem 1.75rem;
  font-size: var(--font-size-button-lg);
  /* 中: 48px相当。小でも 44px 下限を保証 */
  min-height: max(44px, 3rem);
}
.ui-btn--primary {
  background: var(--murasaki-700);
  color: #fff;
  border: 1px solid var(--murasaki-800);
  box-shadow: 0 2px 8px rgba(93, 58, 107, 0.2);
}
.ui-btn--primary:hover:not(:disabled) {
  background: var(--murasaki-800);
}
.ui-btn--outline {
  background: var(--site-surface);
  color: var(--murasaki-700);
  border: 1px solid var(--murasaki-400);
}
.ui-btn--outline:hover:not(:disabled) {
  background: var(--murasaki-100);
  border-color: var(--murasaki-600);
}
.ui-btn--ghost {
  background: transparent;
  color: var(--site-text-muted);
  border: 1px solid var(--site-border);
}
.ui-btn--ghost:hover:not(:disabled) {
  border-color: var(--murasaki-400);
  color: var(--murasaki-700);
}
.ui-btn--gold {
  background: linear-gradient(180deg, var(--kin-400) 0%, var(--kin-500) 100%);
  color: var(--ink-900);
  border: 1px solid var(--kin-600);
}
.ui-btn--gold:hover:not(:disabled) {
  filter: brightness(1.05);
}
</style>
