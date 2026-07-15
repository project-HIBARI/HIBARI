<script setup>
/**
 * 部品名: ゆかりの地 — スポットグリッド
 * 用途: 絞り込み結果のカード一覧表示
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import PlacesSpotCard from './PlacesSpotCard.vue'

defineProps({
  spots: { type: Array, required: true },
  favorites: { type: Object, required: true },
})

const emit = defineEmits(['toggle-favorite', 'select'])
</script>

<template>
  <!-- スポット一覧グリッド -->
  <section class="places-grid" aria-label="スポット一覧">
    <SectionTitle title="スポット一覧" sub="Spots" size="md" />

    <p v-if="spots.length === 0" class="places-grid__empty" role="status">
      条件に一致するスポットが見つかりませんでした。フィルタを変更してお試しください。
    </p>

    <div v-else class="places-grid__list">
      <PlacesSpotCard
        v-for="(spot, i) in spots"
        :key="spot.id"
        :index="i"
        :spot="spot"
        :is-favorite="favorites.has(spot.id)"
        @toggle-favorite="emit('toggle-favorite', $event)"
        @select="emit('select', $event)"
      />
    </div>
  </section>
</template>

<style scoped>
.places-grid {
  margin-bottom: var(--sp-7);
}
.places-grid__list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-5);
}
.places-grid__empty {
  padding: var(--sp-7) var(--sp-5);
  text-align: center;
  font-size: var(--font-size-small);
  color: var(--site-text-muted);
  background: var(--site-surface-muted);
  border: 1px dashed var(--site-border);
  border-radius: var(--site-radius-lg);
}

@media (max-width: 1024px) {
  .places-grid__list {
    grid-template-columns: 1fr;
  }
}
</style>
