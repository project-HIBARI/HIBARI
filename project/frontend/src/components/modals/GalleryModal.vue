<script setup>
/**
 * ゆかりの地ギャラリー（プレミアム会員限定）
 */
import { computed } from 'vue'
import ModalShell from './ModalShell.vue'
import Photo from '../ui/Photo.vue'
import MemberGate from '../common/MemberGate.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { MEMBERSHIP_LABELS } from '../../constants/membership.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'
import { PERMISSION } from '../../constants/membership.js'

const emit = defineEmits(['close', 'need-auth'])

const { membership, canUse, isLoggedIn, isPremium } = useMemberAccess()
const items = HIBARU_DATA.placeGallery

const canView = computed(
  () => isLoggedIn.value && isPremium.value && canUse(PERMISSION.EXCLUSIVE_CONTENT),
)
</script>

<template>
  <ModalShell title="✦ 限定コンテンツ" wide @close="emit('close')">
    <MemberGate
      v-if="!canView"
      :permission="PERMISSION.EXCLUSIVE_CONTENT"
      feature="限定コンテンツ（ギャラリー・ハイレゾ音源）"
      @login="emit('need-auth', 'login'); emit('close')"
      @register="emit('need-auth', 'register-premium'); emit('close')"
      @upgrade="emit('need-auth', 'register-premium'); emit('close')"
    />
    <template v-else>
      <p class="gallery-modal__badge">{{ MEMBERSHIP_LABELS[membership] }}向け限定コンテンツ</p>
      <p class="gallery-modal__lead">
        ゆかりの地フォトギャラリーと、会員限定のハイレゾ音源コンテンツをお楽しみいただけます。
      </p>
      <div class="gallery-modal__grid">
        <article v-for="item in items" :key="item.id" class="gallery-modal__card">
          <Photo :w="280" :h="180" :caption="item.title" variant="sepia" class="gallery-modal__ph" />
          <h3 class="gallery-modal__title">{{ item.title }}</h3>
          <p class="gallery-modal__caption">{{ item.caption }}</p>
        </article>
      </div>
    </template>
  </ModalShell>
</template>

<style scoped>
.gallery-modal__badge {
  display: inline-block;
  margin: 0 0 8px;
  padding: 4px 12px;
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
}
.gallery-modal__lead {
  margin: 0 0 16px;
  font-size: var(--font-size-button);
  line-height: 1.7;
  color: var(--site-text-muted);
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
  font-size: var(--font-size-small);
  color: var(--site-text);
}
.gallery-modal__caption {
  margin: 0;
  padding: 0 12px 12px;
  font-size: var(--font-size-caption);
  line-height: 1.6;
  color: var(--site-text-muted);
}

@media (max-width: 767px) {
  .gallery-modal__grid {
    grid-template-columns: 1fr;
  }
}
</style>
