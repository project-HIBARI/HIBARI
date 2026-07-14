<script setup>
/**
 * 会員特典: プレミアム限定映像
 */
import { computed } from 'vue'
import MemberGate from '../../../common/MemberGate.vue'
import UiIco from '../../../ui/UiIco.vue'
import { HIBARU_DATA } from '../../../../data/hibaruData.js'
import { useMemberAccess } from '../../../../composables/useMemberAccess.js'
import { PERMISSION } from '../../../../constants/membership.js'

const emit = defineEmits(['need-auth'])

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
  <MemberGate
    :permission="PERMISSION.PREMIUM_VIDEO"
    feature="プレミアム限定映像"
    @login="emit('need-auth', 'login')"
    @register="emit('need-auth', 'register-premium')"
    @upgrade="emit('need-auth', 'register-premium')"
  >
    <p class="benefit-panel__lead">プレミアム会員限定の未公開映像・特別コンテンツです。</p>
    <div class="benefit-panel__grid">
      <button
        v-for="pv in premiumItems"
        :key="pv.id"
        type="button"
        class="benefit-panel__video-card"
        @click="onPlay(pv)"
      >
        <div class="benefit-panel__thumb">
          <div v-if="!pv.youtubeId" class="benefit-panel__placeholder">
            <UiIco name="play" :size="28" color="var(--murasaki-700)" />
            <span>準備中</span>
          </div>
          <img
            v-else
            :src="`https://img.youtube.com/vi/${pv.youtubeId}/hqdefault.jpg`"
            :alt="pv.title"
            class="benefit-panel__img"
          />
          <span class="benefit-panel__premium-badge">Premium</span>
        </div>
        <div class="benefit-panel__body">
          <span class="benefit-panel__year">{{ pv.year }}</span>
          <h3 class="benefit-panel__video-title">{{ pv.title }}</h3>
          <p v-if="pv.note" class="benefit-panel__note">{{ pv.note }}</p>
        </div>
      </button>
    </div>
  </MemberGate>
</template>

<style scoped>
.benefit-panel__lead {
  margin: 0 0 16px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.benefit-panel__grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-4);
}
.benefit-panel__video-card {
  padding: 0;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface);
  overflow: hidden;
  cursor: pointer;
  text-align: left;
}
.benefit-panel__thumb {
  position: relative;
  aspect-ratio: 16 / 9;
  background: var(--murasaki-100);
}
.benefit-panel__placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 8px;
  font-size: 12px;
  color: var(--site-text-muted);
}
.benefit-panel__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.benefit-panel__premium-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  padding: 3px 8px;
  font-size: 9px;
  font-weight: 700;
  color: #fff;
  background: var(--kin-600);
  border-radius: 4px;
}
.benefit-panel__body {
  padding: 12px 14px 14px;
}
.benefit-panel__year {
  font-size: 11px;
  color: var(--kin-600);
}
.benefit-panel__video-title {
  margin: 4px 0;
  font-family: var(--ff-mincho);
  font-size: 14px;
  color: var(--site-text);
}
.benefit-panel__note {
  margin: 0;
  font-size: 11px;
  line-height: 1.6;
  color: var(--site-text-muted);
}

@media (max-width: 600px) {
  .benefit-panel__grid {
    grid-template-columns: 1fr;
  }
}
</style>
