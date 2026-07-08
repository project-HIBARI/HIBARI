<script setup>
/**
 * ゆかりの地ギャラリー（プレミアム会員限定）
 */
import ModalShell from './ModalShell.vue'
import Photo from '../ui/Photo.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { MEMBERSHIP_LABELS } from '../../constants/membership.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'

const emit = defineEmits(['close'])

const { membership } = useMemberAccess()
const items = HIBARU_DATA.placeGallery
</script>

<template>
  <ModalShell title="✦ ゆかりの地ギャラリー" @close="emit('close')">
    <p class="gallery-modal__badge">{{ MEMBERSHIP_LABELS[membership] }}向け限定コンテンツ</p>
    <div class="gallery-modal__grid">
      <article v-for="item in items" :key="item.id" class="gallery-modal__card">
        <Photo :w="280" :h="180" :caption="item.title" variant="sepia" class="gallery-modal__ph" />
        <h3 class="gallery-modal__title">{{ item.title }}</h3>
        <p class="gallery-modal__caption">{{ item.caption }}</p>
      </article>
    </div>
  </ModalShell>
</template>

<style scoped>
.gallery-modal__badge {
  display: inline-block;
  margin: 0 0 16px;
  padding: 4px 12px;
  font-size: 11px;
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
}
.gallery-modal__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.gallery-modal__card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  overflow: hidden;
  background: var(--site-surface);
}
.gallery-modal__ph {
  width: 100% !important;
  height: 160px !important;
}
.gallery-modal__title {
  margin: 0;
  padding: 10px 12px 4px;
  font-family: var(--ff-mincho);
  font-size: 14px;
  color: var(--site-text);
}
.gallery-modal__caption {
  margin: 0;
  padding: 0 12px 12px;
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-muted);
}

@media (max-width: 600px) {
  .gallery-modal__grid {
    grid-template-columns: 1fr;
  }
}
</style>
