<script setup>
/**
 * 部品名: ディスコグラフィ — 楽曲カード
 * 用途: 一覧グリッド内の1曲分カード（レコードチップ・メタデータ・お気に入り・DL）
 */
import RecordChip from '../../ui/RecordChip.vue'
import UiIco from '../../ui/UiIco.vue'
import { aosAttrs } from '../../../lib/aos.js'

const props = defineProps({
  song: { type: Object, required: true },
  index: { type: Number, default: 0 },
  isFavorite: { type: Boolean, default: false },
})

const emit = defineEmits(['open', 'toggle-favorite', 'download'])

const chipColors = ['var(--beni-700)', '#3a2a1a', 'var(--murasaki-700)']
const chipColor = chipColors[props.index % chipColors.length]
const hasAward = props.song.note && props.song.note.includes('賞')

function onFavoriteClick(e) {
  e.stopPropagation()
  emit('toggle-favorite', props.song.id)
}

function onDownloadClick(e) {
  e.stopPropagation()
  emit('download', props.song)
}

function onOpenDetail(e) {
  e.stopPropagation()
  emit('open', props.song)
}

function onPlayClick(e) {
  e.stopPropagation()
  if (!props.song.audioUrl) return
  window.open(props.song.audioUrl, '_blank', 'noopener,noreferrer')
}
</script>

<template>
  <article class="disco-song-card motion-card" v-bind="aosAttrs(index * 80)">
    <div class="disco-song-card__main">
      <button
        type="button"
        class="disco-song-card__chip motion-button"
        :aria-label="song.title + 'の詳細を見る'"
        @click="onOpenDetail"
      >
        <RecordChip :no="song.no" :color="chipColor" />
      </button>
      <button
        type="button"
        class="disco-song-card__body"
        :aria-label="song.title + 'の詳細を見る'"
        @click="onOpenDetail"
      >
        <span class="disco-song-card__meta">{{ song.year }} · {{ song.no }} · {{ song.genre }}</span>
        <h3 class="disco-song-card__title">{{ song.title }}</h3>
        <p class="disco-song-card__romaji">{{ song.romaji }}</p>
        <p class="disco-song-card__credits">作詞：{{ song.lyric }} / 作曲：{{ song.music }}</p>
        <p v-if="song.note" class="disco-song-card__note">{{ song.note }}</p>
      </button>
      <div class="disco-song-card__actions">
        <button
          type="button"
          class="disco-song-card__fav motion-button"
          :class="{ 'disco-song-card__fav--on': isFavorite }"
          :aria-label="isFavorite ? 'お気に入りから外す' : 'お気に入りに追加'"
          :aria-pressed="isFavorite"
          @click="onFavoriteClick"
        >
          <UiIco name="heart" :size="16" :color="isFavorite ? 'var(--beni-600)' : 'var(--site-text-muted)'" />
        </button>
        <button
          type="button"
          class="disco-song-card__play motion-button"
          :aria-label="song.title + 'を再生'"
          :disabled="!song.audioUrl"
          @click="onPlayClick"
        >
          <UiIco name="play" :size="13" color="var(--murasaki-700)" />
        </button>
        <button
          type="button"
          class="disco-song-card__dl motion-button"
          :aria-label="song.title + 'をダウンロード'"
          @click="onDownloadClick"
        >
          <UiIco name="download" :size="16" color="var(--site-text-muted)" />
        </button>
        <span v-if="hasAward" class="disco-song-card__award">受賞</span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.disco-song-card {
  position: relative;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
}
.disco-song-card__chip,
.disco-song-card__play,
.disco-song-card__fav,
.disco-song-card__dl {
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1), color 0.4s ease, background 0.4s ease;
}
.disco-song-card__meta,
.disco-song-card__title {
  transition: color 0.45s ease;
}
.disco-song-card:hover .disco-song-card__title {
  color: var(--murasaki-700);
}
.disco-song-card__main {
  display: grid;
  grid-template-columns: 92px 1fr auto;
  gap: var(--sp-4);
  width: 100%;
  padding: var(--sp-4);
  align-items: center;
}
.disco-song-card__chip,
.disco-song-card__body {
  border: 0;
  background: transparent;
  cursor: pointer;
  text-align: left;
  color: inherit;
  padding: 0;
}
.disco-song-card__chip {
  display: block;
  flex-shrink: 0;
  border-radius: 50%;
  transition: opacity 0.2s;
}
.disco-song-card__chip:hover {
  opacity: 0.85;
}
.disco-song-card__body {
  min-width: 0;
}
.disco-song-card__meta {
  display: block;
  font-family: var(--ff-mono);
  font-size: var(--font-size-badge);
  letter-spacing: 0.12em;
  color: var(--kin-600);
  margin-bottom: 4px;
}
.disco-song-card__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-emphasis);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
  overflow-wrap: anywhere;
  white-space: normal;
}
.disco-song-card__romaji {
  margin: 2px 0 0;
  font-family: var(--ff-latin);
  font-style: italic;
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}
.disco-song-card__credits {
  margin: 6px 0 0;
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
  line-height: 1.5;
}
.disco-song-card__note {
  margin: 4px 0 0;
  font-size: var(--font-size-caption);
  color: var(--site-text);
  line-height: 1.5;
}
.disco-song-card__actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  flex-shrink: 0;
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
  cursor: pointer;
  padding: 0;
  margin-left: -40px;
  transition: background 0.2s, border-color 0.2s;
}
.disco-song-card__play:hover:not(:disabled) {
  background: var(--murasaki-200, #e8dff0);
  border-color: var(--murasaki-500);
}
.disco-song-card__play:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.disco-song-card__award {
  font-size: var(--font-size-badge);
  color: var(--kin-600);
  border: 1px solid var(--kin-500);
  padding: 2px 6px;
  letter-spacing: 0.1em;
  font-family: var(--ff-mincho);
}
.disco-song-card__fav,
.disco-song-card__dl {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--site-border);
  background: var(--site-surface);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
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
.disco-song-card__dl:hover {
  border-color: var(--murasaki-500);
  background: rgba(232, 223, 240, 0.5);
}

@media (max-width: 600px) {
  .disco-song-card__main {
    grid-template-columns: 72px 1fr auto;
    gap: var(--sp-3);
  }
  .disco-song-card__actions {
    gap: 6px;
  }
  .disco-song-card__play {
    width: 36px;
    height: 36px;
  }
}
</style>
