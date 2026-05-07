<script setup>
/**
 * 部品名: タブバー（ページ内サブナビ）
 * 用途: ゆかりの地（地図/一覧）、思い出（投稿/イベント）、AI モーダルなど
 */
import UiIco from './UiIco.vue'

defineProps({
  tabs: { type: Array, required: true },
  active: { type: String, required: true },
  /** true なら墨背景向けの明るい文字色 */
  dark: { type: Boolean, default: true },
})

const emit = defineEmits(['update:active'])
</script>

<template>
  <nav
    :style="{
      display: 'flex',
      gap: '2px',
      borderBottom: dark ? '1px solid rgba(201,169,97,0.2)' : '1px solid rgba(26,20,16,0.12)',
      fontFamily: 'var(--ff-mincho)',
      fontSize: '14px',
    }"
  >
    <button
      v-for="t in tabs"
      :key="t.id"
      type="button"
      :style="{
        background: 'transparent',
        border: 0,
        padding: '10px 14px',
        color: t.id === active ? 'var(--beni-500)' : dark ? 'var(--paper-300)' : 'var(--ink-500)',
        borderBottom: t.id === active ? '2px solid var(--beni-500)' : '2px solid transparent',
        cursor: 'pointer',
        marginBottom: '-1px',
        fontWeight: t.id === active ? 700 : 400,
        display: 'inline-flex',
        alignItems: 'center',
        gap: '6px',
      }"
      @click="emit('update:active', t.id)"
    >
      <UiIco v-if="t.icon" :name="t.icon" :size="14" />
      {{ t.label }}
    </button>
  </nav>
</template>
