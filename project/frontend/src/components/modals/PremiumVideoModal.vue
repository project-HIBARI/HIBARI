<script setup>
/**
 * プレミアム限定映像モーダル（会員限定・公開ページへは遷移しない）
 */
import { computed } from 'vue'
import ModalShell from './ModalShell.vue'
import UiIco from '../ui/UiIco.vue'
import MemberGate from '../common/MemberGate.vue'
import { HIBARU_DATA } from '../../data/hibaruData.js'
import { useMemberAccess } from '../../composables/useMemberAccess.js'
import { PERMISSION } from '../../constants/membership.js'

const emit = defineEmits(['close', 'need-auth'])

const { canUse, isLoggedIn, isPremium } = useMemberAccess()

const PREMIUM_PV_IDS = new Set(['pv-002', 'pv-003'])

const canView = computed(
  () => isLoggedIn.value && isPremium.value && canUse(PERMISSION.PREMIUM_VIDEO),
)

const premiumItems = computed(() =>
  HIBARU_DATA.featuredPv.filter((pv) => PREMIUM_PV_IDS.has(pv.id)),
)

function onPlay(pv) {
  if (!canView.value) return
  if (pv.youtubeId) {
    window.open(`https://www.youtube.com/watch?v=${pv.youtubeId}`, '_blank', 'noopener,noreferrer')
  }
}
</script>

<template>
  <ModalShell title="✦ プレミアム限定映像" wide @close="emit('close')">
    <MemberGate
      v-if="!canView"
      :permission="PERMISSION.PREMIUM_VIDEO"
      feature="プレミアム限定映像"
      @login="emit('need-auth', 'login'); emit('close')"
      @register="emit('need-auth', 'register-premium'); emit('close')"
      @upgrade="emit('need-auth', 'register-premium'); emit('close')"
    />
    <template v-else>
      <p class="premium-video__lead">プレミアム会員限定の未公開映像・特別コンテンツです。</p>
      <div class="premium-video__grid">
        <button
          v-for="pv in premiumItems"
          :key="pv.id"
          type="button"
          class="premium-video__card"
          @click="onPlay(pv)"
        >
          <div class="premium-video__thumb">
            <div v-if="!pv.youtubeId" class="premium-video__placeholder">
              <UiIco name="play" :size="28" color="var(--murasaki-700)" />
              <span>準備中</span>
            </div>
            <img
              v-else
              :src="`https://img.youtube.com/vi/${pv.youtubeId}/hqdefault.jpg`"
              :alt="pv.title"
              class="premium-video__img"
            />
            <span class="premium-video__badge">Premium</span>
          </div>
          <div class="premium-video__body">
            <span class="premium-video__year">{{ pv.year }}</span>
            <h3 class="premium-video__title">{{ pv.title }}</h3>
            <p v-if="pv.note" class="premium-video__note">{{ pv.note }}</p>
          </div>
        </button>
      </div>
    </template>
  </ModalShell>
</template>

<style scoped>
.premium-video__lead {
  margin: 0 0 16px;
  font-size: var(--font-size-button);
  line-height: 1.7;
  color: var(--site-text-muted);
}
.premium-video__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.premium-video__card {
  padding: 0;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface);
  overflow: hidden;
  cursor: pointer;
  text-align: left;
}
.premium-video__thumb {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--murasaki-100);
}
.premium-video__placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 8px;
  font-size: var(--font-size-caption);
  color: var(--site-text-muted);
}
.premium-video__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.premium-video__badge {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 3px 8px;
  font-size: var(--font-size-badge);
  font-weight: 700;
  color: #fff;
  background: var(--kin-600);
  border-radius: 4px;
}
.premium-video__body {
  padding: 12px 14px 14px;
}
.premium-video__year {
  font-size: var(--font-size-caption);
  color: var(--kin-600);
}
.premium-video__title {
  margin: 4px 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-small);
  color: var(--site-text);
}
.premium-video__note {
  margin: 0;
  font-size: var(--font-size-caption);
  line-height: 1.6;
  color: var(--site-text-muted);
}
@media (max-width: 767px) {
  .premium-video__grid {
    grid-template-columns: 1fr;
  }
}
</style>
