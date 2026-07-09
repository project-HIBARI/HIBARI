<script setup>
/**
 * 部品名: ホーム — サブスクリプションサービス紹介カード
 * 用途: ヒーロー下の会員向け特典・サブスク案内を表示する（プラン別ロック表示）
 */
import { computed } from 'vue'
import PageImageCard from '../../common/PageImageCard.vue'
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'
import { PAGE_IMAGES } from '../../../lib/pageImages.js'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { PERMISSION } from '../../../constants/membership.js'

const emit = defineEmits(['open-detail', 'use-feature'])

const { canUse, isLoggedIn } = useMemberAccess()

const perks = [
  { icon: '▶', label: '限定動画', permission: PERMISSION.PREMIUM_VIDEO, feature: 'disco' },
  { icon: '♪', label: 'ハイレゾ音源', permission: PERMISSION.EXCLUSIVE_CONTENT, feature: 'gallery' },
  { icon: '✦', label: '会員誌デジタル版', permission: PERMISSION.NEWSLETTER, feature: 'news' },
  { icon: '★', label: 'チケット先行予約', permission: PERMISSION.TICKET_PREORDER, feature: 'events' },
]

const perkStates = computed(() =>
  perks.map((p) => ({
    ...p,
    unlocked: canUse(p.permission),
  })),
)
</script>

<template>
  <UiCard tone="purple" padding="lg" class="top-subscription">
    <div class="top-subscription__image">
      <PageImageCard
        :image="PAGE_IMAGES.benefits"
        title="会員特典"
        description="限定コンテンツや先行予約など、会員だけの特典をご用意しています。"
        alt="会員特典"
        image-only
        compact
        fit="contain"
      />
    </div>
    <span class="top-subscription__ribbon">おすすめ</span>
    <p class="top-subscription__lead">特別な体験を、あなたに。</p>
    <h2 class="top-subscription__title">サブスクリプションサービス</h2>
    <p class="top-subscription__desc">
      月額制で、ここだけの限定コンテンツをお楽しみいただけます。
    </p>

    <ul class="top-subscription__perks">
      <li
        v-for="p in perkStates"
        :key="p.label"
        class="top-subscription__perk"
        :class="{ 'top-subscription__perk--locked': !p.unlocked }"
      >
        <button type="button" class="top-subscription__perk-btn" @click="emit('use-feature', p.feature)">
          <span class="top-subscription__perk-icon">{{ p.icon }}</span>
          <span class="top-subscription__perk-label">{{ p.label }}</span>
          <span v-if="!p.unlocked" class="top-subscription__perk-lock">
            {{ isLoggedIn ? 'プレミアム' : '会員限定' }}
          </span>
        </button>
      </li>
    </ul>

    <UiButton variant="gold" size="md" class="top-subscription__btn home-cta-btn home-cta-btn--gold" @click="emit('open-detail')">
      サービスの詳細を見る ›
    </UiButton>
  </UiCard>
</template>

<style scoped>
.top-subscription {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 380px;
  overflow: hidden;
}
.top-subscription__image {
  position: absolute;
  top: 0;
  right: 0;
  width: 42%;
  height: 140px;
  opacity: 0.35;
  pointer-events: none;
}
.top-subscription__image :deep(.page-image-card__media) {
  border-color: rgba(255, 255, 255, 0.25);
  background: rgba(255, 255, 255, 0.08);
}
.top-subscription__ribbon {
  position: absolute;
  top: 18px;
  left: -4px;
  padding: 5px 16px 5px 12px;
  background: linear-gradient(135deg, var(--kin-400), var(--kin-500));
  color: var(--ink-900);
  font-family: var(--ff-mincho);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  border-radius: 0 4px 4px 0;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}
.top-subscription__lead {
  margin: 32px 0 6px;
  font-family: var(--ff-mincho);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: var(--kin-400);
}
.top-subscription__title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: clamp(20px, 2vw, 24px);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #fff;
  line-height: 1.45;
}
.top-subscription__desc {
  margin: 0 0 28px;
  font-size: 13px;
  line-height: 1.85;
  color: rgba(255, 255, 255, 0.88);
}
.top-subscription__perks {
  list-style: none;
  margin: 0 0 auto;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.top-subscription__perk {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-align: center;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.92);
  line-height: 1.4;
  position: relative;
}
.top-subscription__perk-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
}
.top-subscription__perk--locked {
  opacity: 0.55;
}
.top-subscription__perk-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(201, 169, 97, 0.55);
  background: rgba(0, 0, 0, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  color: var(--kin-400);
  flex-shrink: 0;
}
.top-subscription__perk-lock {
  font-size: 9px;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.65);
}
.top-subscription__btn {
  margin-top: 24px;
  width: 100%;
  justify-content: center;
}

@media (max-width: 900px) {
  .top-subscription__perks {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}
@media (max-width: 767px) {
  .top-subscription {
    min-height: auto;
  }
}
</style>
