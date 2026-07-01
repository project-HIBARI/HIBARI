<script setup>
/**
 * 部品名: PC メインナビ
 * 役割: ホーム・ディスコグラフィー・歩み・ゆかりの地・思い出・献花への切替
 */
defineProps({
  items: { type: Array, required: true },
  page: { type: String, required: true },
})

const emit = defineEmits(['navigate'])
</script>

<template>
  <nav class="app-main-nav pc-only" role="navigation" aria-label="メインナビゲーション">
    <button
      v-for="n in items"
      :key="n.id"
      type="button"
      class="app-main-nav__link"
      :class="{ 'app-main-nav__link--active': page === n.id }"
      :aria-current="page === n.id ? 'page' : undefined"
      @click="emit('navigate', n.id)"
    >
      {{ n.label }}
    </button>
  </nav>
</template>
