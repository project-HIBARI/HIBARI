<script setup>

/**

 * 部品名: ページメインビジュアルカード

 * 用途: 透過PNG画像・タイトル・説明文を統一レイアウトで表示

 */

import { computed } from 'vue'

import { pageImageUrl } from '../../lib/pageImages.js'



const props = defineProps({

  /** ファイル名または /images/... 形式のパス */

  image: { type: String, required: true },

  title: { type: String, default: '' },

  description: { type: String, default: '' },

  alt: { type: String, default: '' },

  /** 画像を右・テキストを左に配置 */

  reverse: { type: Boolean, default: false },

  /** 画像のみ表示（導線カード等） */

  imageOnly: { type: Boolean, default: false },

  /** コンパクト表示（カテゴリカード内） */

  compact: { type: Boolean, default: false },

  /** cover | contain（透過PNGは contain 推奨） */

  fit: { type: String, default: 'contain' },

})



const src = computed(() =>

  props.image.startsWith('/') ? props.image : pageImageUrl(props.image),

)



const imgAlt = computed(() => props.alt || props.title || '')

</script>



<template>

  <article

    class="page-image-card"

    :class="{

      'page-image-card--reverse': reverse,

      'page-image-card--image-only': imageOnly,

      'page-image-card--compact': compact,

    }"

  >

    <div class="page-image-card__media">

      <img

        :src="src"

        :alt="imgAlt"

        class="page-image-card__img"

        :style="{ objectFit: fit }"

        decoding="async"

        draggable="false"

      />

    </div>

    <div v-if="!imageOnly && (title || description)" class="page-image-card__body">

      <h2 v-if="title" class="page-image-card__title">{{ title }}</h2>

      <p v-if="description" class="page-image-card__desc">{{ description }}</p>

      <slot />

    </div>

  </article>

</template>



<style scoped>

.page-image-card {

  display: grid;

  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);

  gap: var(--sp-6);

  align-items: center;

  padding: var(--sp-6);

  background: rgba(255, 254, 251, 0.95);

  border: 1px solid var(--kin-500);

  border-radius: var(--site-radius-lg);

  box-shadow: var(--site-shadow-md);

}

.page-image-card--reverse .page-image-card__media {

  order: 2;

}

.page-image-card--reverse .page-image-card__body {

  order: 1;

}

.page-image-card__media {

  display: flex;

  align-items: center;

  justify-content: center;

  width: 100%;

  aspect-ratio: var(--page-image-ratio);

  max-height: var(--page-image-display-h);

  padding: var(--sp-3);

  background: transparent;

  border-radius: var(--site-radius-md);

  overflow: hidden;

}

.page-image-card__img {

  width: 100%;

  height: 100%;

  max-width: 100%;

  max-height: 100%;

  object-position: center;

  display: block;

}

.page-image-card__body {

  display: flex;

  flex-direction: column;

  gap: var(--sp-3);

}

.page-image-card__title {

  margin: 0;

  font-family: var(--ff-mincho);

  font-size: clamp(24px, 3vw, 34px);

  font-weight: 800;

  letter-spacing: 0.1em;

  color: var(--murasaki-700);

  line-height: 1.35;

}

.page-image-card__desc {

  margin: 0;

  font-family: var(--ff-sans-jp);

  font-size: 14px;

  line-height: 1.85;

  letter-spacing: 0.04em;

  color: var(--site-text-muted);

}



/* 画像のみ */

.page-image-card--image-only {

  display: block;

  padding: 0;

  background: transparent;

  border: 0;

  box-shadow: none;

  border-radius: 0;

}

.page-image-card--image-only .page-image-card__media {

  max-height: var(--page-image-hero-h);

  padding: var(--sp-2);

  border: 0;

  box-shadow: none;

  background: transparent;

}

.page-image-card--image-only .page-image-card__img {

  max-height: 100%;

}



/* コンパクト（カテゴリ導線カード内） */

.page-image-card--compact.page-image-card--image-only .page-image-card__media {

  max-height: var(--page-image-compact-h);

  padding: var(--sp-1);

}

.page-image-card--compact.page-image-card--image-only .page-image-card__img {

  max-height: 100%;

}



@media (max-width: 767px) {

  .page-image-card:not(.page-image-card--image-only) {

    grid-template-columns: 1fr;

    gap: var(--sp-4);

    padding: var(--sp-5);

  }

  .page-image-card--reverse .page-image-card__media,

  .page-image-card--reverse .page-image-card__body {

    order: unset;

  }

  .page-image-card__media {

    max-height: 220px;

  }

}



@media (min-width: 768px) and (max-width: 1023px) {

  .page-image-card:not(.page-image-card--image-only) {

    padding: var(--sp-5);

    gap: var(--sp-5);

  }

  .page-image-card__media {

    max-height: 240px;

  }

}

</style>


