<script setup>
/**
 * 部品名: ホーム — サブスクリプションサービス紹介カード
 * 用途: ヒーロー下の会員向け特典・サブスク案内を表示する
 */
import UiCard from '../../ui/UiCard.vue'
import UiButton from '../../ui/UiButton.vue'

const emit = defineEmits(['open-detail'])

const perks = [
  { icon: '▶', label: '限定動画' },
  { icon: '♪', label: 'ハイレゾ音源' },
  { icon: '✦', label: '会員誌デジタル版' },
  { icon: '★', label: 'チケット先行予約' },
]
</script>

<template>
  <UiCard tone="purple" padding="lg" class="top-subscription">
    <span class="top-subscription__ribbon">おすすめ</span>
    <p class="top-subscription__lead">特別な体験を、あなたに。</p>
    <h2 class="top-subscription__title">サブスクリプションサービス</h2>
    <p class="top-subscription__desc">
      月額制で、ここだけの限定コンテンツをお楽しみいただけます。
    </p>

    <ul class="top-subscription__perks">
      <li v-for="p in perks" :key="p.label" class="top-subscription__perk">
        <span class="top-subscription__perk-icon">{{ p.icon }}</span>
        <span class="top-subscription__perk-label">{{ p.label }}</span>
      </li>
    </ul>

    <UiButton variant="gold" size="md" class="top-subscription__btn" @click="emit('open-detail')">
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
