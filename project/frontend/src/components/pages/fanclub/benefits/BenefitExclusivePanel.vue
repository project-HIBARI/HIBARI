<script setup>
/**
 * 会員特典: 限定コンテンツ（ギャラリー・ハイレゾ）
 */
import MemberGate from '../../../common/MemberGate.vue'
import Photo from '../../../ui/Photo.vue'
import { HIBARU_DATA } from '../../../../data/hibaruData.js'
import { MEMBERSHIP_LABELS, PERMISSION } from '../../../../constants/membership.js'
import { useMemberAccess } from '../../../../composables/useMemberAccess.js'

const emit = defineEmits(['need-auth'])

const { membership } = useMemberAccess()
const items = HIBARU_DATA.placeGallery
</script>

<template>
  <MemberGate
    :permission="PERMISSION.EXCLUSIVE_CONTENT"
    feature="限定コンテンツ（ギャラリー・ハイレゾ音源）"
    @login="emit('need-auth', 'login')"
    @register="emit('need-auth', 'register-premium')"
    @upgrade="emit('need-auth', 'register-premium')"
  >
    <p class="benefit-panel__badge">{{ MEMBERSHIP_LABELS[membership] }}向け限定コンテンツ</p>
    <p class="benefit-panel__lead">
      ゆかりの地フォトギャラリーと、会員限定のハイレゾ音源コンテンツをお楽しみいただけます。
    </p>
    <div class="benefit-panel__grid">
      <article v-for="item in items" :key="item.id" class="benefit-panel__card">
        <Photo :w="280" :h="180" :caption="item.title" variant="sepia" class="benefit-panel__ph" />
        <h3 class="benefit-panel__card-title">{{ item.title }}</h3>
        <p class="benefit-panel__caption">{{ item.caption }}</p>
      </article>
    </div>
  </MemberGate>
</template>

<style scoped>
.benefit-panel__badge {
  display: inline-block;
  margin: 0 0 8px;
  padding: 4px 12px;
  font-size: var(--font-size-caption);
  color: var(--murasaki-700);
  background: var(--murasaki-100);
  border: 1px solid var(--murasaki-400);
  border-radius: 999px;
}
.benefit-panel__lead {
  margin: 0 0 16px;
  font-size: var(--font-size-button);
  line-height: 1.7;
  color: var(--site-text-muted);
}
.benefit-panel__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.benefit-panel__card {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  overflow: hidden;
  background: var(--site-surface);
}
.benefit-panel__ph {
  width: 100% !important;
  height: 160px !important;
}
.benefit-panel__card-title {
  margin: 0;
  padding: 10px 12px 4px;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-small);
  color: var(--site-text);
}
.benefit-panel__caption {
  margin: 0;
  padding: 0 12px 12px;
  font-size: var(--font-size-caption);
  line-height: 1.6;
  color: var(--site-text-muted);
}

@media (max-width: 600px) {
  .benefit-panel__grid {
    grid-template-columns: 1fr;
  }
}
</style>
