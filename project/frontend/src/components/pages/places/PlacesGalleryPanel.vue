<script setup>
/**
 * 部品名: ゆかりの地 — ギャラリーパネル
 * 用途: プレミアム会員向け写真ギャラリー（権限に応じてロック表示）
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import Photo from '../../ui/Photo.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'

const emit = defineEmits(['open-gallery', 'need-auth'])

const { canUse, isLoggedIn, PERMISSION } = useMemberAccess()
const items = HIBARU_DATA.placeGallery
const unlocked = () => canUse(PERMISSION.EXCLUSIVE_CONTENT)

function placeImage(placeId) {
  return HIBARU_DATA.places.find((p) => p.id === placeId)?.image || ''
}

function onLinkClick() {
  if (unlocked()) emit('open-gallery')
  else if (!isLoggedIn.value) emit('need-auth', 'login')
  else emit('need-auth', 'register-premium')
}

function onCardClick() {
  onLinkClick()
}
</script>

<template>
  <section class="places-gallery" aria-label="ゆかりの地ギャラリー">
    <SectionTitle
      title="ゆかりの地ギャラリー"
      sub="Photo Gallery"
      size="md"
      link-label="もっと見る"
      @link-click="onLinkClick"
    />

    <div class="places-gallery__grid">
      <button
        v-for="item in items"
        :key="item.id"
        type="button"
        class="places-gallery__card"
        :class="{ 'places-gallery__card--locked': !unlocked() }"
        :aria-label="item.title + (unlocked() ? 'の写真' : '（プレミアム限定）')"
        @click="onCardClick"
      >
        <img
          v-if="placeImage(item.placeId)"
          :src="placeImage(item.placeId)"
          :alt="item.title"
          class="places-gallery__img"
          loading="lazy"
          decoding="async"
        />
        <Photo v-else :w="200" :h="140" :caption="item.title" variant="sepia" class="places-gallery__ph" />
        <div class="places-gallery__body">
          <h3 class="places-gallery__title">{{ item.title }}</h3>
          <p class="places-gallery__caption">{{ item.caption }}</p>
          <span class="places-gallery__lock">{{ unlocked() ? '閲覧可能' : 'プレミアム限定' }}</span>
        </div>
      </button>
    </div>
  </section>
</template>

<style scoped>
.places-gallery {
  margin-bottom: var(--sp-7);
}
.places-gallery__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
}
.places-gallery__card {
  padding: 0;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-lg);
  background: var(--site-surface);
  box-shadow: var(--site-shadow);
  overflow: hidden;
  cursor: pointer;
  text-align: left;
  transition: transform 0.2s, box-shadow 0.2s;
}
.places-gallery__card:hover {
  transform: translateY(-2px);
  box-shadow: var(--site-shadow-md);
}
.places-gallery__card--locked .places-gallery__ph {
  filter: grayscale(0.4) brightness(0.92);
}
.places-gallery__ph {
  width: 100% !important;
  height: 140px !important;
}
.places-gallery__img {
  display: block;
  width: 100%;
  height: 140px;
  object-fit: cover;
  object-position: center;
}
.places-gallery__card--locked .places-gallery__img {
  filter: grayscale(0.55) brightness(0.88);
}
.places-gallery__body {
  padding: var(--sp-3) var(--sp-4) var(--sp-4);
  position: relative;
}
.places-gallery__title {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-small);
  font-weight: 700;
  color: var(--site-text);
}
.places-gallery__caption {
  margin: 0;
  font-size: var(--font-size-caption);
  line-height: 1.5;
  color: var(--site-text-muted);
}
.places-gallery__lock {
  position: absolute;
  top: -100px;
  right: 10px;
  padding: 3px 8px;
  background: var(--murasaki-700);
  color: #fff;
  font-size: var(--font-size-badge);
  letter-spacing: 0.1em;
  border-radius: 4px;
}
.places-gallery__card--locked .places-gallery__lock {
  background: var(--kin-600);
}
.places-gallery__card:focus-visible {
  outline: 2px solid var(--murasaki-500);
  outline-offset: 2px;
}

@media (max-width: 1024px) {
  .places-gallery__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 480px) {
  .places-gallery__grid {
    grid-template-columns: 1fr;
  }
}
</style>
