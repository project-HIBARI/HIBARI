<script setup>
/**
 * 部品名: PC メインナビ（序・曲・歴…）
 */
defineProps({
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['navigate'])
</script>

<template>
  <nav
    class="pc-only"
    role="navigation"
    aria-label="メインナビゲーション"
    style="display: flex; border-top: 1px solid rgba(201,169,97,0.2); background: #0a0604"
  >
    <button
      v-for="n in items"
      :key="n.id"
      type="button"
      :style="{
        flex: 1,
        border: 0,
        background: page === n.id ? 'var(--beni-800)' : 'transparent',
        color: page === n.id ? 'var(--paper-50)' : 'var(--paper-200)',
        padding: '13px 8px',
        cursor: 'pointer',
        borderRight: '1px solid rgba(201,169,97,0.12)',
        borderTop: page === n.id ? '2px solid var(--kin-500)' : '2px solid transparent',
        marginTop: '-1px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '4px',
        fontFamily: 'var(--ff-mincho)',
      }"
      :aria-current="page === n.id ? 'page' : undefined"
      @click="emit('navigate', n.id)"
    >
      <span style="font-size: 22px; font-weight: 700">{{ n.kanji }}</span>
      <span style="font-size: 11px; letter-spacing: 0.12em; opacity: 0.85">{{ n.label }}</span>
    </button>
  </nav>
</template>
