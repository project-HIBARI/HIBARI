<script setup>
/**
 * 部品名: ゆかりの地 — ギャラリーパネル
 * 用途: 会員向け写真ギャラリーのプレースホルダ（クリックで認証モーダル誘導）
 */
import SectionTitle from '../../ui/SectionTitle.vue'
import Photo from '../../ui/Photo.vue'
import { HIBARU_DATA } from '../../../data/hibaruData.js'

const emit = defineEmits(['open-gallery'])

const items = HIBARU_DATA.placeGallery
</script>

<template>
  <!-- ゆかりの地ギャラリー（会員向けプレースホルダ） -->
  <section class="places-gallery" aria-label="ゆかりの地ギャラリー">
    <SectionTitle
      title="ゆかりの地ギャラリー"
      sub="Photo Gallery"
      size="md"
      link-label="もっと見る"
      @link-click="emit('open-gallery')"
    />

    <div class="places-gallery__grid">
      <button
        v-for="item in items"
        :key="item.id"
        type="button"
        class="places-gallery__card"
        :aria-label="item.title + 'の写真（会員限定）'"
        @click="emit('open-gallery')"
      >
        <Photo :w="200" :h="140" :caption="item.title" variant="sepia" class="places-gallery__ph" />
        <div class="places-gallery__body">
          <h3 class="places-gallery__title">{{ item.title }}</h3>
          <p class="places-gallery__caption">{{ item.caption }}</p>
          <span class="places-gallery__lock">会員限定</span>
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
.places-gallery__ph {
  width: 100% !important;
  height: 140px !important;
}
.places-gallery__body {
  padding: var(--sp-3) var(--sp-4) var(--sp-4);
  position: relative;
}
.places-gallery__title {
  margin: 0 0 4px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  font-weight: 700;
  color: var(--site-text);
}
.places-gallery__caption {
  margin: 0;
  font-size: 11px;
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
  font-size: 9px;
  letter-spacing: 0.1em;
  border-radius: 4px;
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
