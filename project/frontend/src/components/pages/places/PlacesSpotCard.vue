<script setup>
/**
 * 部品名: ゆかりの地 — スポットカード
 * 用途: 一覧グリッド内の1スポット分カード（写真・メタ・お気に入り・詳細展開）
 */
import { ref, computed } from 'vue'
import Photo from '../../ui/Photo.vue'
import UiIco from '../../ui/UiIco.vue'
import UiButton from '../../ui/UiButton.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { aosAttrs } from '../../../lib/aos.js'

const imageFailed = ref(false)

const props = defineProps({
  spot: { type: Object, required: true },
  isFavorite: { type: Boolean, default: false },
  index: { type: Number, default: 0 },
})

const emit = defineEmits(['toggle-favorite', 'select'])

const expanded = ref(false)

const categoryLabel = computed(() => {
  const c = HIBARU_DATA.placeCategories.find((x) => x.key === props.spot.category)
  return c ? c.label : 'その他'
})

const regionLabel = computed(() => {
  const r = HIBARU_DATA.placeRegions.find((x) => x.key === props.spot.region)
  return r ? r.label : ''
})

function onFavoriteClick(e) {
  e.stopPropagation()
  emit('toggle-favorite', props.spot.id)
}

function onShareClick(e) {
  e.stopPropagation()
  const text = `${props.spot.name} — ${props.spot.area}`
  const url = window.location.href
  if (navigator.share) {
    navigator.share({ title: props.spot.name, text, url }).catch(() => {})
    return
  }
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(`${text}\n${url}`)
  }
}
</script>

<template>
  <article class="places-spot-card motion-card" v-bind="aosAttrs(index * 80)">
    <div class="places-spot-card__photo motion-image">
      <img
        v-if="spot.image && !imageFailed"
        :src="spot.image"
        :alt="spot.name"
        class="places-spot-card__img"
        loading="lazy"
        decoding="async"
        @error="imageFailed = true"
      />
      <Photo
        v-else
        :w="320"
        :h="160"
        :caption="spot.name"
        variant="sepia"
        class="places-spot-card__ph"
      />
      <span class="places-spot-card__cat">{{ categoryLabel }}</span>
      <span v-if="spot.visitable" class="places-spot-card__badge places-spot-card__badge--open">見学可</span>
      <span v-else class="places-spot-card__badge places-spot-card__badge--closed">閉館</span>
    </div>

    <div class="places-spot-card__body">
      <h3 class="places-spot-card__title">{{ spot.name }}</h3>
      <p class="places-spot-card__location">{{ spot.area }}</p>
      <p class="places-spot-card__region">{{ regionLabel }} · {{ spot.prefecture }}</p>
      <p class="places-spot-card__desc">{{ spot.description || spot.note }}</p>
      <p v-if="spot.tips" class="places-spot-card__tips">
        <UiIco name="pin" :size="12" color="var(--kin-600)" />
        {{ spot.tips }}
      </p>

      <div v-if="expanded" class="places-spot-card__detail">
        <p class="places-spot-card__detail-text">{{ spot.note }}</p>
        <p v-if="spot.id === 'kinenkan'" class="places-spot-card__event">
          <strong>イベント情報</strong><br />
          4月29日《春と恋・愛のフィルムコンサート》<br />
          10:30〜12:00 / 13:30〜15:00 · 料金: ¥3,000（要予約）<br />
          TEL: 03-5422-3358
        </p>
      </div>

      <div class="places-spot-card__actions">
        <UiButton variant="outline" size="sm" class="motion-button" @click="expanded = !expanded">
          {{ expanded ? '閉じる' : '詳細を見る' }}
        </UiButton>
        <button type="button" class="places-spot-card__share" aria-label="共有" title="共有する" @click="onShareClick">
          <span class="places-spot-card__share-icon" aria-hidden="true">↗</span>
        </button>
        <button
          type="button"
          class="places-spot-card__fav"
          :class="{ 'places-spot-card__fav--on': isFavorite }"
          :aria-label="isFavorite ? 'お気に入りから外す' : 'お気に入りに追加'"
          :aria-pressed="isFavorite"
          @click="onFavoriteClick"
        >
          <UiIco name="heart" :size="16" :color="isFavorite ? 'var(--beni-600)' : 'var(--site-text-muted)'" />
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.places-spot-card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  overflow: hidden;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.places-spot-card:hover {
  border-color: rgba(122, 80, 136, 0.25);
  box-shadow: var(--site-shadow-md);
}
.places-spot-card__photo {
  position: relative;
  overflow: hidden;
  background: var(--site-surface-muted);
}
.places-spot-card__ph {
  width: 100% !important;
  height: 160px !important;
}
.places-spot-card__img {
  display: block;
  width: 100%;
  height: 160px;
  object-fit: cover;
  object-position: center;
}
.places-spot-card__cat {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 3px 10px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid var(--site-border);
  border-radius: 999px;
  font-size: 10px;
  letter-spacing: 0.08em;
  color: var(--murasaki-700);
}
.places-spot-card__badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 3px 8px;
  font-size: 9px;
  letter-spacing: 0.1em;
  border-radius: 4px;
}
.places-spot-card__badge--open {
  color: #2a7a5a;
  border: 1px solid #2a7a5a;
  background: rgba(255, 255, 255, 0.9);
}
.places-spot-card__badge--closed {
  color: var(--beni-600);
  border: 1px solid var(--beni-500);
  background: rgba(255, 255, 255, 0.9);
}
.places-spot-card__body {
  padding: var(--sp-4);
}
.places-spot-card__title {
  margin: 0 0 6px;
  font-family: var(--ff-mincho);
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
  line-height: 1.4;
}
.places-spot-card__location {
  margin: 0 0 2px;
  font-size: 12px;
  color: var(--site-text-muted);
  line-height: 1.5;
}
.places-spot-card__region {
  margin: 0 0 10px;
  font-family: var(--ff-mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  color: var(--kin-600);
}
.places-spot-card__desc {
  margin: 0 0 8px;
  font-size: 12px;
  line-height: 1.75;
  color: var(--site-text-muted);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.places-spot-card__tips {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin: 0 0 var(--sp-3);
  padding: var(--sp-3);
  background: var(--site-surface-muted);
  border-radius: var(--site-radius-sm);
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-muted);
}
.places-spot-card__detail {
  margin-bottom: var(--sp-3);
  padding: var(--sp-3);
  background: var(--murasaki-100);
  border-radius: var(--site-radius-sm);
  border: 1px solid rgba(122, 80, 136, 0.15);
}
.places-spot-card__detail-text {
  margin: 0 0 8px;
  font-size: 12px;
  line-height: 1.8;
  color: var(--site-text);
}
.places-spot-card__event {
  margin: 0;
  font-size: 11px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.places-spot-card__actions {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
}
.places-spot-card__share,
.places-spot-card__fav {
  margin-left: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-sm);
  background: var(--site-surface);
  cursor: pointer;
  transition: border-color 0.2s;
}
.places-spot-card__fav--on {
  border-color: var(--beni-500);
  background: rgba(192, 52, 47, 0.06);
}
.places-spot-card__share-icon {
  font-size: 14px;
  color: var(--site-text-muted);
  line-height: 1;
}
.places-spot-card__share:hover,
.places-spot-card__fav:hover {
  border-color: var(--murasaki-400);
}
.places-spot-card__share:focus-visible,
.places-spot-card__fav:focus-visible {
  outline: 2px solid var(--murasaki-500);
  outline-offset: 2px;
}
</style>
