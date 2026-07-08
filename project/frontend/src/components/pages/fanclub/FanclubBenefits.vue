<script setup>
/**
 * 部品名: ファンクラブ 特典ハイライト
 * 用途: 会員特典一覧（クリックで各機能へ）
 */
import { useMemberAccess } from '../../../composables/useMemberAccess.js'
import { MEMBERSHIP_LABELS } from '../../../constants/membership.js'

const emit = defineEmits(['use-feature'])

const { canUse, isLoggedIn, membership, PERMISSION } = useMemberAccess()

const benefits = [
  { feature: 'news', icon: '✦', title: '月刊ニュースレター', desc: '会員向けの最新情報・コラムを毎月お届けします。', permission: PERMISSION.NEWSLETTER },
  { feature: 'events', icon: '★', title: 'チケット先行予約', desc: 'コンサートやイベントの先行予約にご利用いただけます。', permission: PERMISSION.TICKET_PREORDER },
  { feature: 'board', icon: '💬', title: '掲示板投稿', desc: '一般会員は月10回、プレミアムは無制限で投稿できます。', permission: PERMISSION.BOARD_POST },
  { feature: 'ai', icon: '♪', title: 'AIひばり対話', desc: '一般会員は月10回、プレミアム会員は無制限で対話できます。', permission: PERMISSION.AI_CHAT },
  { feature: 'disco', icon: '▶', title: 'プレミアム限定映像', desc: 'プレミアム会員だけの未公開映像・特別コンテンツ。', permission: PERMISSION.PREMIUM_VIDEO, premium: true },
  { feature: 'gallery', icon: '✧', title: '限定コンテンツ', desc: 'ハイレゾ音源や会員限定の特典コンテンツ。', permission: PERMISSION.EXCLUSIVE_CONTENT, premium: true },
  { feature: 'events', icon: '◎', title: '優先申込＋会員割引', desc: 'イベントの優先申込と会員割引価格がご利用いただけます。', permission: PERMISSION.PRIORITY_DISCOUNT, premium: true },
]

function status(b) {
  if (!isLoggedIn.value) return 'ログイン後に利用可能'
  if (canUse(b.permission)) return '利用可能'
  if (b.premium) return `${MEMBERSHIP_LABELS.premium}限定`
  return '会員登録が必要'
}

function onUse(b) {
  emit('use-feature', b.feature)
}
</script>

<template>
  <ul class="fc-benefits">
    <li
      v-for="(b, i) in benefits"
      :key="`${b.feature}-${i}`"
      class="fc-benefits__item"
      :class="{
        'fc-benefits__item--premium': b.premium,
        'fc-benefits__item--ready': isLoggedIn && canUse(b.permission),
      }"
    >
      <button type="button" class="fc-benefits__btn" @click="onUse(b)">
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
  padding: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-4);
}
.fc-benefits__item {
  border: 1px solid var(--site-border);
  border-radius: var(--site-radius-md);
  background: var(--site-surface);
  overflow: hidden;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.fc-benefits__item--premium {
  border-color: rgba(201, 169, 97, 0.45);
  background: linear-gradient(180deg, #fffaf6 0%, var(--site-surface) 100%);
}
.fc-benefits__item--ready {
  border-color: var(--murasaki-400);
}
.fc-benefits__item--ready:hover {
  box-shadow: var(--site-shadow-md);
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
  font-size: 20px;
}
.fc-benefits__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: 15px;
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
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--kin-600);
}
.fc-benefits__desc {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  line-height: 1.7;
  color: var(--site-text-muted);
}
.fc-benefits__status {
  font-size: 11px;
  font-weight: 700;
  color: var(--murasaki-700);
  letter-spacing: 0.06em;
}

@media (max-width: 1100px) {
  .fc-benefits {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 900px) {
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
