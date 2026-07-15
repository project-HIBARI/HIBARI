<script setup>
/**
 * 部品名: ディスコグラフィ — 楽曲グリッド
 * 用途: フィルタ結果の楽曲カード一覧、または空状態を表示する
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import DiscoSongCard from './DiscoSongCard.vue'

defineProps({
  items: { type: Array, default: () => [] },
  favorites: { type: Set, default: () => new Set() },
  emptyType: { type: String, default: 'search' },
})

const emit = defineEmits(['open', 'toggle-favorite', 'download'])

const emptyMessages = {
  search: '該当する楽曲が見つかりませんでした',
  album: 'アルバムのデータは準備中です。現在はシングルのみ掲載しています。',
  favorites: 'お気に入りに登録した楽曲がここに表示されます。ハートアイコンをタップして追加してください。',
}
</script>

<template>
  <!-- 楽曲カード一覧または空状態 -->
  <section class="disco-grid" aria-label="楽曲一覧">
    <SectionTitle title="楽曲一覧" sub="Song Catalog" size="md" />

    <div v-if="items.length === 0" class="disco-grid__empty">
      <p>{{ emptyMessages[emptyType] || emptyMessages.search }}</p>
    </div>

    <div v-else class="disco-grid__list">
      <DiscoSongCard
        v-for="(song, i) in items"
        :key="song.id"
        :song="song"
        :index="i"
        :is-favorite="favorites.has(song.id)"
        @open="emit('open', $event)"
        @toggle-favorite="emit('toggle-favorite', $event)"
        @download="emit('download', $event)"
      />
    </div>
  </section>
</template>

<style scoped>
.disco-grid {
  margin-bottom: var(--sp-5);
}
.disco-grid__list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.disco-grid__empty {
  text-align: center;
  padding: var(--sp-8) var(--sp-4);
  background: var(--site-surface-muted);
  border: 1px dashed var(--site-border-strong);
  border-radius: var(--site-radius-lg);
  color: var(--site-text-muted);
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  line-height: 1.8;
}
.disco-grid__empty p {
  margin: 0;
  max-width: 420px;
  margin-inline: auto;
}

@media (max-width: 900px) {
  .disco-grid__list {
    grid-template-columns: 1fr;
  }
}
</style>
