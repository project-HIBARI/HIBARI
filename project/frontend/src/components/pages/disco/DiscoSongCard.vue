<script setup>
/**
 * 部品名: ディスコグラフィ — 楽曲カード
 * 用途: 一覧グリッド内の1曲分カード（レコードチップ・メタデータ・お気に入り）
 */
import RecordChip from '../../ui/RecordChip.vue'
import UiIco from '../../ui/UiIco.vue'

const props = defineProps({
  song: { type: Object, required: true },
  index: { type: Number, default: 0 },
  isFavorite: { type: Boolean, default: false },
})

const emit = defineEmits(['open', 'toggle-favorite'])

const chipColors = ['var(--beni-700)', '#3a2a1a', 'var(--murasaki-700)']
const chipColor = chipColors[props.index % chipColors.length]
const hasAward = props.song.note && props.song.note.includes('賞')

function onFavoriteClick(e) {
  e.stopPropagation()
  emit('toggle-favorite', props.song.id)
}
</script>

<template>
  <article class="disco-song-card">
    <button
      type="button"
      class="disco-song-card__main"
      :aria-label="song.title + 'の詳細を見る'"
      @click="emit('open', song)"
    >
      <RecordChip :no="song.no" :color="chipColor" />
      <div class="disco-song-card__body">
        <span class="disco-song-card__meta">{{ song.year }} · {{ song.no }} · {{ song.genre }}</span>
        <h3 class="disco-song-card__title">{{ song.title }}</h3>
        <p class="disco-song-card__romaji">{{ song.romaji }}</p>
        <p class="disco-song-card__credits">作詞：{{ song.lyric }} / 作曲：{{ song.music }}</p>
        <p v-if="song.note" class="disco-song-card__note">{{ song.note }}</p>
      </div>
      <div class="disco-song-card__actions" aria-hidden="true">
        <span class="disco-song-card__play">
          <UiIco name="play" :size="13" color="var(--murasaki-700)" />
        </span>
        <span v-if="hasAward" class="disco-song-card__award">受賞</span>
      </div>
    </button>
    <button
      type="button"
      class="disco-song-card__fav"
      :class="{ 'disco-song-card__fav--on': isFavorite }"
      :aria-label="isFavorite ? 'お気に入りから外す' : 'お気に入りに追加'"
      :aria-pressed="isFavorite"
      @click="onFavoriteClick"
    >
      <UiIco name="heart" :size="16" :color="isFavorite ? 'var(--beni-600)' : 'var(--site-text-muted)'" />
    </button>
  </article>
</template>

<style scoped>
.disco-song-card {
  position: relative;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  transition: box-shadow 0.2s, border-color 0.2s;
}
.disco-song-card:hover {
  border-color: rgba(122, 80, 136, 0.25);
  box-shadow: var(--site-shadow-md);
}
.disco-song-card__main {
  display: grid;
  grid-template-columns: 92px 1fr auto;
  gap: var(--sp-4);
  width: 100%;
  padding: var(--sp-4);
  padding-right: 44px;
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
  color: inherit;
  align-items: center;
}
.disco-song-card__meta {
  display: block;
  font-family: var(--ff-mono);
  font-size: 10px;
  letter-spacing: 0.12em;
  color: var(--kin-600);
  margin-bottom: 4px;
}
.disco-song-card__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
}
.disco-song-card__romaji {
  margin: 2px 0 0;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: 12px;
  color: var(--site-text-muted);
}
.disco-song-card__credits {
  margin: 6px 0 0;
  font-size: 11px;
  color: var(--site-text-muted);
  line-height: 1.5;
}
.disco-song-card__note {
  margin: 4px 0 0;
  font-size: 11px;
  color: var(--site-text);
  line-height: 1.5;
}
.disco-song-card__actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}
.disco-song-card__play {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid var(--murasaki-400);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--murasaki-100);
}
.disco-song-card__award {
  font-size: 9px;
  color: var(--kin-600);
  border: 1px solid var(--kin-500);
  padding: 2px 6px;
  letter-spacing: 0.1em;
  font-family: var(--ff-mincho);
}
.disco-song-card__fav {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, border-color 0.2s;
}
.disco-song-card__fav:hover {
  border-color: var(--beni-500);
  background: rgba(252, 232, 236, 0.5);
}
.disco-song-card__fav--on {
  border-color: var(--beni-500);
  background: rgba(252, 232, 236, 0.8);
}

@media (max-width: 600px) {
  .disco-song-card__main {
    grid-template-columns: 72px 1fr;
  }
  .disco-song-card__actions {
    display: none;
  }
}
</style>
