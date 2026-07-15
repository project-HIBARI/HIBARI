<script setup>
/**
 * 部品名: Music Memories アーティストカード
 * 用途: ホームのファンクラブ一覧・アーティスト図鑑の共通カード
 */
import { decadeLabel, genderLabel, statusLabel } from '../../../data/musicMemoriesData.js'

const props = defineProps({
  artist: { type: Object, required: true },
  /** 図鑑向けに活動年代・性別などのメタタグを表示 */
  showMeta: { type: Boolean, default: false },
})

const emit = defineEmits(['enter-site'])

function onEnter() {
  if (props.artist.status !== 'open') return
  emit('enter-site', props.artist.siteId)
}

const decadeTags = (props.artist.activeDecades || []).slice(0, 2).map(decadeLabel)
const metaTags = [
  ...decadeTags,
  genderLabel(props.artist.gender),
  ...(props.artist.genres || []).slice(0, 1),
  statusLabel(props.artist.status),
].filter(Boolean)
</script>

<template>
  <article
    class="mm-artist-card"
    :class="{
      'mm-artist-card--open': artist.status === 'open',
      'mm-artist-card--soon': artist.status === 'soon',
    }"
    :role="artist.status === 'open' ? 'link' : undefined"
    :tabindex="artist.status === 'open' ? 0 : undefined"
    :aria-label="artist.status === 'open' ? `${artist.name}のファンクラブへ` : undefined"
    @click="onEnter"
    @keydown.enter.prevent="onEnter"
    @keydown.space.prevent="onEnter"
  >
    <div class="mm-artist-card__visual" aria-hidden="true">
      <img
        v-if="artist.image"
        :src="artist.image"
        :alt="artist.name"
        class="mm-artist-card__image"
        loading="lazy"
        decoding="async"
      />
      <div v-else class="mm-artist-card__placeholder">
        <span>♪</span>
      </div>
    </div>

    <div class="mm-artist-card__body">
      <p class="mm-artist-card__en">{{ artist.nameEn }}</p>
      <h3 class="mm-artist-card__name">{{ artist.name }}</h3>
      <p class="mm-artist-card__tagline">{{ artist.tagline }}</p>

      <ul v-if="showMeta && metaTags.length" class="mm-artist-card__meta" aria-label="アーティスト属性">
        <li v-for="tag in metaTags" :key="tag" class="mm-artist-card__meta-tag">{{ tag }}</li>
      </ul>

      <span
        v-if="artist.status === 'open'"
        class="mm-artist-card__cta"
        aria-hidden="true"
      >
        ファンクラブへ
      </span>
      <span
        v-else
        class="mm-artist-card__badge"
        aria-disabled="true"
      >
        準備中
      </span>
    </div>
  </article>
</template>

<style scoped>
.mm-artist-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: var(--site-radius-lg);
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.04);
  transition: transform 0.35s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.35s, border-color 0.35s;
}

.mm-artist-card:hover {
  transform: translateY(-4px);
  border-color: rgba(201, 169, 97, 0.45);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
}

.mm-artist-card--open {
  cursor: pointer;
}

.mm-artist-card--open:focus-visible {
  outline: 2px solid var(--kin-400);
  outline-offset: 3px;
}

.mm-artist-card--soon {
  opacity: 0.65;
}

.mm-artist-card__visual {
  aspect-ratio: 16 / 10;
  background: #1e161e;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.mm-artist-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  background: #1e161e;
}

.mm-artist-card__placeholder {
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.2);
}

.mm-artist-card__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px 22px 24px;
  gap: 6px;
}

.mm-artist-card__en {
  margin: 0;
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--kin-400);
}

.mm-artist-card__name {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 1.35rem;
  letter-spacing: 0.06em;
  color: #f8f4ef;
}

.mm-artist-card__tagline {
  margin: 0 0 12px;
  flex: 1;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  line-height: 1.7;
  color: rgba(248, 244, 239, 0.65);
}

.mm-artist-card__meta {
  list-style: none;
  margin: 0 0 12px;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.mm-artist-card__meta-tag {
  display: inline-flex;
  padding: 3px 8px;
  border-radius: 999px;
  border: 1px solid rgba(201, 169, 97, 0.28);
  background: rgba(201, 169, 97, 0.08);
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  letter-spacing: 0.06em;
  color: rgba(248, 244, 239, 0.72);
}

.mm-artist-card__cta {
  align-self: flex-start;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  min-height: 40px;
  border-radius: var(--site-radius-sm);
  border: 1px solid var(--kin-600);
  background: linear-gradient(180deg, var(--kin-400) 0%, var(--kin-500) 100%);
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  color: var(--ink-900);
  white-space: nowrap;
}

.mm-artist-card__badge {
  align-self: flex-start;
  display: inline-flex;
  padding: 6px 14px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: transparent;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  letter-spacing: 0.12em;
  color: rgba(248, 244, 239, 0.5);
}
</style>
