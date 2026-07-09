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

const perkGroups = [
  {
    id: 'core',
    title: '会員基本特典',
    perks: [
      { icon: '✦', label: '会員誌デジタル版', permission: PERMISSION.NEWSLETTER, feature: 'news' },
      { icon: '★', label: 'チケット先行予約', permission: PERMISSION.TICKET_PREORDER, feature: 'events' },
      { icon: '💬', label: '掲示板投稿', permission: PERMISSION.BOARD_POST, feature: 'board' },
      { icon: '👥', label: 'オープンチャット', permission: PERMISSION.OPEN_CHAT, feature: 'open-chat' },
      { icon: '♪', label: 'AIひばり対話', permission: PERMISSION.AI_CHAT, feature: 'ai' },
    ],
  },
  {
    id: 'premium',
    title: 'プレミアム限定',
    perks: [
      { icon: '▶', label: '限定動画', permission: PERMISSION.PREMIUM_VIDEO, feature: 'disco', premium: true },
      { icon: '✧', label: 'ハイレゾ音源', permission: PERMISSION.EXCLUSIVE_CONTENT, feature: 'gallery', premium: true },
      { icon: '◎', label: '優先申込＋割引', permission: PERMISSION.PRIORITY_DISCOUNT, feature: 'priority-events', premium: true },
    ],
  },
]

const groups = computed(() =>
  perkGroups.map((group) => ({
    ...group,
    perks: group.perks.map((p) => ({
      ...p,
      unlocked: canUse(p.permission),
      lockLabel: perkLockLabel(p),
    })),
  })),
)

function perkLockLabel(perk) {
  if (canUse(perk.permission)) return ''
  if (!isLoggedIn.value) return '会員限定'
  if (perk.premium) return 'プレミアム'
  return '会員限定'
}
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
      月額制で、限定コンテンツのほか掲示板・オープンチャット・AI対話など、会員だけの体験をお楽しみいただけます。
    </p>

    <div class="top-subscription__groups">
      <section
        v-for="group in groups"
        :key="group.id"
        class="top-subscription__group"
        :class="`top-subscription__group--${group.id}`"
      >
        <h3 class="top-subscription__group-title">{{ group.title }}</h3>
        <ul class="top-subscription__perks">
          <li
            v-for="p in group.perks"
            :key="p.feature"
            class="top-subscription__perk"
            :class="{ 'top-subscription__perk--locked': !p.unlocked, 'top-subscription__perk--premium': p.premium }"
          >
            <button type="button" class="top-subscription__perk-btn" @click="emit('use-feature', p.feature)">
              <span class="top-subscription__perk-icon" aria-hidden="true">{{ p.icon }}</span>
              <span class="top-subscription__perk-label">{{ p.label }}</span>
              <span v-if="p.lockLabel" class="top-subscription__perk-lock">{{ p.lockLabel }}</span>
            </button>
          </li>
        </ul>
      </section>
    </div>

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
  min-height: 520px;
  overflow: hidden;
}
.top-subscription__image {
  position: absolute;
  top: 0;
  right: 0;
  width: 38%;
  height: 150px;
  opacity: 0.32;
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
  margin: 0 0 10px;
  font-family: var(--ff-mincho);
  font-size: clamp(20px, 2vw, 24px);
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #fff;
  line-height: 1.45;
}
.top-subscription__desc {
  margin: 0 0 20px;
  font-size: 13px;
  line-height: 1.85;
  color: rgba(255, 255, 255, 0.88);
  max-width: 36em;
}
.top-subscription__groups {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: auto;
}
.top-subscription__group {
  padding: 14px 14px 12px;
  border-radius: var(--site-radius-md);
  background: rgba(0, 0, 0, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.top-subscription__group--premium {
  background: rgba(0, 0, 0, 0.22);
  border-color: rgba(201, 169, 97, 0.28);
}
.top-subscription__group-title {
  margin: 0 0 12px;
  font-family: var(--ff-mincho);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: rgba(255, 255, 255, 0.72);
}
.top-subscription__group--premium .top-subscription__group-title {
  color: var(--kin-400);
}
.top-subscription__perks {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 10px;
}
.top-subscription__group--premium .top-subscription__perks {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
.top-subscription__perk {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  text-align: center;
  font-size: 10px;
  color: rgba(255, 255, 255, 0.92);
  line-height: 1.35;
  position: relative;
  min-width: 0;
}
.top-subscription__perk-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: 100%;
  min-height: 88px;
  padding: 8px 4px;
  border: 1px solid transparent;
  border-radius: var(--site-radius-sm);
  background: transparent;
  color: inherit;
  cursor: pointer;
  transition:
    background 0.25s ease,
    border-color 0.25s ease,
    transform 0.25s ease;
}
.top-subscription__perk-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(201, 169, 97, 0.35);
  transform: translateY(-2px);
}
.top-subscription__perk--locked {
  opacity: 0.62;
}
.top-subscription__perk--premium .top-subscription__perk-icon {
  border-color: rgba(201, 169, 97, 0.75);
  background: rgba(201, 169, 97, 0.12);
}
.top-subscription__perk-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(201, 169, 97, 0.55);
  background: rgba(0, 0, 0, 0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: var(--kin-400);
  flex-shrink: 0;
}
.top-subscription__perk-label {
  display: block;
  width: 100%;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.02em;
  word-break: keep-all;
  overflow-wrap: anywhere;
}
.top-subscription__perk-lock {
  font-size: 8px;
  letter-spacing: 0.08em;
  color: rgba(255, 255, 255, 0.65);
  padding: 2px 6px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.22);
}
.top-subscription__btn {
  margin-top: 20px;
  width: 100%;
  justify-content: center;
  flex-shrink: 0;
}

@media (max-width: 1100px) {
  .top-subscription__perks {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  .top-subscription__group--premium .top-subscription__perks {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
@media (max-width: 900px) {
  .top-subscription {
    min-height: auto;
  }
  .top-subscription__perks,
  .top-subscription__group--premium .top-subscription__perks {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }
}
@media (max-width: 767px) {
  .top-subscription__image {
    width: 46%;
    height: 120px;
  }
}
</style>
