<script setup>
/**
 * 部品名: Music Memory Book — パンくず
 */
defineProps({
  items: { type: Array, required: true },
})

const emit = defineEmits(['navigate'])
</script>

<template>
  <nav class="mmb-crumb" aria-label="パンくず">
    <template v-for="(item, i) in items" :key="i">
      <span v-if="i > 0" class="mmb-crumb__sep" aria-hidden="true">›</span>
      <button
        v-if="item.action && i < items.length - 1"
        type="button"
        class="mmb-crumb__link"
        @click="emit('navigate', item.action)"
      >
        {{ item.label }}
      </button>
      <span v-else class="mmb-crumb__current" :aria-current="i === items.length - 1 ? 'page' : undefined">
        {{ item.label }}
      </span>
    </template>
  </nav>
</template>

<style scoped>
.mmb-crumb {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: var(--sp-5);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-caption);
  letter-spacing: 0.04em;
}

.mmb-crumb__sep {
  color: var(--site-text-light);
}

.mmb-crumb__link {
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--murasaki-600);
  cursor: pointer;
  font: inherit;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.mmb-crumb__link:hover {
  color: var(--murasaki-800);
}

.mmb-crumb__current {
  color: var(--site-text-muted);
}
</style>
