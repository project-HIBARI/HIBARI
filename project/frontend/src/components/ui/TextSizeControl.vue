<script setup>
/**
 * 部品名: 文字サイズ切替（小・中・大）
 * 役割: html[data-text-size] を更新し tokens.css のスケールを反映
 */
import { useId } from 'vue'
import { useTextSize } from '../../composables/useTextSize.js'

defineProps({
  /** ink: 明るい紙面向け / paper: 暗いヘッダー向け */
  tone: { type: String, default: 'ink' },
  /** default / header（ヘッダー内コンパクト表示） */
  variant: { type: String, default: 'default' },
})

const labelId = useId()
const { size, setSize, presets } = useTextSize()

const ariaLabels = {
  s: '文字サイズ：小',
  m: '文字サイズ：中',
  l: '文字サイズ：大',
}
</script>

<template>
  <div
    class="text-size-control"
    :class="[
      `text-size-control--${tone}`,
      `text-size-control--${variant}`,
    ]"
  >
    <span :id="labelId" class="text-size-control__label">文字サイズ</span>
    <div
      class="text-size-control__group"
      role="group"
      :aria-labelledby="labelId"
    >
      <button
        v-for="[k, lbl] in presets"
        :key="k"
        type="button"
        class="text-size-control__btn"
        :class="{ 'text-size-control__btn--active': size === k }"
        :aria-label="ariaLabels[k]"
        :aria-pressed="size === k"
        @click="setSize(k)"
      >
        {{ lbl }}
      </button>
    </div>
  </div>
</template>

<style scoped>
/*
 * 切替UI自体はユーザー文字サイズ設定で極端に拡大しないよう固定pxを使用する
 */
.text-size-control {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--ff-sans-jp);
  flex-shrink: 0;
}

.text-size-control__label {
  font-size: var(--font-size-caption);
  letter-spacing: 0.06em;
  white-space: nowrap;
  line-height: 1.2;
}

.text-size-control--ink .text-size-control__label {
  color: var(--site-text-muted);
}

.text-size-control--paper .text-size-control__label {
  color: var(--paper-100, #f4ede0);
  opacity: 0.9;
}

.text-size-control__group {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  border: 1px solid rgba(201, 169, 97, 0.45);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.6);
}

.text-size-control--paper .text-size-control__group {
  border-color: rgba(244, 237, 224, 0.35);
  background: rgba(0, 0, 0, 0.18);
}

.text-size-control__btn {
  box-sizing: border-box;
  min-width: 44px;
  min-height: 44px;
  padding: 0 10px;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-button);
  font-weight: 500;
  line-height: 1;
  color: var(--site-text);
  transition: background 0.2s, color 0.2s, border-color 0.2s, font-weight 0.2s;
}

.text-size-control--paper .text-size-control__btn {
  color: var(--paper-100, #f4ede0);
}

.text-size-control__btn:hover {
  background: rgba(201, 169, 97, 0.14);
}

.text-size-control__btn:focus-visible {
  outline: 2px solid var(--murasaki-600, #6b4578);
  outline-offset: 2px;
}

.text-size-control--paper .text-size-control__btn:focus-visible {
  outline-color: var(--kin-400, #d9bd7d);
}

.text-size-control__btn--active {
  background: var(--murasaki-700);
  border-color: var(--murasaki-800, #4a2d5e);
  color: #fff;
  font-weight: 700;
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.18);
}

.text-size-control--paper .text-size-control__btn--active {
  background: var(--paper-100, #f4ede0);
  border-color: var(--kin-400, #d9bd7d);
  color: var(--ink-900, #15110e);
  box-shadow: inset 0 0 0 1px rgba(21, 17, 14, 0.08);
}

/* ヘッダー内コンパクト表示（タップ領域は維持） */
.text-size-control--header {
  gap: 8px;
}

.text-size-control--header .text-size-control__label {
  font-size: var(--font-size-caption);
}

.text-size-control--header .text-size-control__group {
  gap: 2px;
  padding: 2px;
}

.text-size-control--header .text-size-control__btn {
  min-width: 40px;
  min-height: 40px;
  padding: 0 8px;
  font-size: var(--font-size-caption);
}

@media (max-width: 1199px) {
  .text-size-control--header .text-size-control__label {
    display: none;
  }
}
</style>
