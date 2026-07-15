<script setup>
/**
 * 部品名: ファンクラブ 特典ハイライト
 */
import { ref } from 'vue'
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { MEMBERSHIP_LABELS } from '../../../constants/membership.js'

const emit = defineEmits(['use-feature'])

const { canUse, isLoggedIn, isFanclubMember, PERMISSION } = useMemberAccess()

const benefits = [
  { feature: 'news', icon: '✦', title: '月刊ニュースレター', desc: '会員向けの最新情報・コラムを毎月お届けします。', permission: PERMISSION.NEWSLETTER },
  { feature: 'events', icon: '★', title: 'チケット先行予約', desc: 'コンサートやイベントの先行予約にご利用いただけます。', permission: PERMISSION.TICKET_PREORDER },
  { feature: 'board', icon: '💬', title: '掲示板投稿', desc: '一般会員は月10回、プレミアムは無制限で投稿できます。', permission: PERMISSION.BOARD_POST },
  { feature: 'open-chat', icon: '👥', title: 'オープンチャット', desc: 'ファン同士が参加できるグループチャット。リアルタイムで交流できます。', permission: PERMISSION.OPEN_CHAT },
  { feature: 'ai', icon: '♪', title: 'AIひばり対話', desc: '一般会員は月10回、プレミアム会員は無制限で対話できます。', permission: PERMISSION.AI_CHAT },
  { feature: 'disco', icon: '▶', title: 'プレミアム限定映像', desc: 'プレミアム会員だけの未公開映像・特別コンテンツ。', permission: PERMISSION.PREMIUM_VIDEO, premium: true },
  { feature: 'gallery', icon: '✧', title: '限定コンテンツ', desc: 'ハイレゾ音源や会員限定の特典コンテンツ。', permission: PERMISSION.EXCLUSIVE_CONTENT, premium: true },
  { feature: 'priority-events', icon: '◎', title: '優先申込＋会員割引', desc: 'イベントの優先申込と会員割引価格がご利用いただけます。', permission: PERMISSION.PRIORITY_DISCOUNT, premium: true },
]

/** DevTools スマホ表示でも浮かぶよう、:hover ではなくクラスで制御 */
const liftedFeature = ref(null)

function liftBenefit(feature) {
  liftedFeature.value = feature
}

function unliftBenefit(feature) {
  if (liftedFeature.value === feature) liftedFeature.value = null
}

function status(b) {
  if (!isFanclubMember.value) {
    return '有料会員限定'
  }
  if (canUse(b.permission)) return '利用可能'
  if (b.premium) return `${MEMBERSHIP_LABELS.premium}限定`
  return '会員登録が必要'
}

function onUse(b) {
  emit('use-feature', b.feature)
}
</script>

<template>
  <ul class="fc-benefits is-visible">
    <li
      v-for="b in benefits"
      :key="b.feature"
      class="fc-benefits__item motion-card"
      :class="{
        'fc-benefits__item--premium': b.premium,
        'fc-benefits__item--ready': isLoggedIn && canUse(b.permission),
        'fc-benefits__item--lifted': liftedFeature === b.feature,
      }"
      @pointerenter="liftBenefit(b.feature)"
      @pointerleave="unliftBenefit(b.feature)"
      @mouseenter="liftBenefit(b.feature)"
      @mouseleave="unliftBenefit(b.feature)"
    >
      <button
        type="button"
        class="fc-benefits__btn"
        @focus="liftBenefit(b.feature)"
        @blur="unliftBenefit(b.feature)"
        @click="onUse(b)"
      >
        <span class="fc-benefits__icon" aria-hidden="true">{{ b.icon }}</span>
        <h3 class="fc-benefits__title">
          {{ b.title }}
          <span v-if="b.premium" class="fc-benefits__tag">Premium</span>
        </h3>
        <p class="fc-benefits__desc">{{ b.desc }}</p>
        <span class="fc-benefits__status">{{ status(b) }} ›</span>
      </button>
    </li>
  </ul>
</template>

<style scoped>
.fc-benefits {
  list-style: none;
  margin: 0;
  padding: 14px 6px 28px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--sp-4);
}
.fc-benefits__item {
  position: relative;
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface);
  box-shadow: 0 2px 8px rgba(60, 40, 30, 0.06);
  overflow: visible;
  isolation: isolate;
  will-change: transform, box-shadow;
  transition:
    transform 0.22s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.22s cubic-bezier(0.22, 1, 0.36, 1),
    border-color 0.2s ease,
    background 0.2s ease;
}
.fc-benefits__item:hover,
.fc-benefits__item.motion-card:hover,
.fc-benefits__item:focus-within,
.fc-benefits__item--lifted,
.fc-benefits__item.motion-card.fc-benefits__item--lifted {
  transform: translateY(-10px) scale(1.02);
  box-shadow:
    0 18px 40px rgba(60, 40, 30, 0.26),
    0 6px 14px rgba(93, 58, 107, 0.18);
  border-color: var(--murasaki-500, #7a4d8a);
  background: linear-gradient(135deg, #fff 0%, var(--murasaki-100) 100%);
  z-index: 2;
}
.fc-benefits__item:active,
.fc-benefits__item.motion-card:active,
.fc-benefits__item--lifted:active {
  transform: translateY(-3px) scale(0.995);
  box-shadow: 0 8px 18px rgba(60, 40, 30, 0.16);
  border-color: var(--murasaki-500, #7a4d8a);
  z-index: 2;
}
.fc-benefits__item--premium {
  border-color: rgba(201, 169, 97, 0.45);
  background: linear-gradient(180deg, #fffaf6 0%, var(--site-surface) 100%);
}
.fc-benefits__item--premium:hover,
.fc-benefits__item--premium:focus-within,
.fc-benefits__item--premium.fc-benefits__item--lifted {
  border-color: var(--kin-500, #c9a961);
  background: linear-gradient(180deg, #fff 0%, #fffaf6 100%);
}
.fc-benefits__item--ready {
  border-color: var(--murasaki-400);
}
.fc-benefits__btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  width: 100%;
  padding: 24px 18px;
  border: 0;
  background: transparent;
  cursor: pointer;
  border-radius: inherit;
  -webkit-tap-highlight-color: transparent;
}
.fc-benefits__icon {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 1px solid var(--kin-500);
  background: var(--murasaki-100);
  color: var(--kin-600);
  font-size: var(--font-size-subtitle);
}
.fc-benefits__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--site-text);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}
.fc-benefits__tag {
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-badge);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--kin-600);
}
.fc-benefits__desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-caption);
  line-height: 1.7;
  color: var(--site-text-muted);
}
.fc-benefits__status {
  font-size: var(--font-size-caption);
  font-weight: 700;
  color: var(--murasaki-700);
  letter-spacing: 0.06em;
}

@media (max-width: 1100px) {
  .fc-benefits {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 480px) {
  .fc-benefits {
    grid-template-columns: 1fr;
  }
}
</style>
