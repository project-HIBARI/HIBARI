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
  <!-- サブスクリプションサービスの紹介カード -->
  <UiCard tone="purple" padding="lg" class="top-subscription">
    <span class="top-subscription__ribbon">おすすめ</span>
    <h2 class="top-subscription__title">サブスクリプションサービス</h2>
    <p class="top-subscription__desc">
      月額制で、ここだけの限定コンテンツをお楽しみいただけます。
    </p>

    <ul class="top-subscription__perks">
      <li v-for="p in perks" :key="p.label" class="top-subscription__perk">
        <span class="top-subscription__perk-icon">{{ p.icon }}</span>
        <span>{{ p.label }}</span>
      </li>
    </ul>

    <UiButton variant="gold" size="md" class="top-subscription__btn" @click="emit('open-detail')">
      サービスの詳細を見る
    </UiButton>
  </UiCard>
</template>

<style scoped>
.top-subscription {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.top-subscription__ribbon {
  position: absolute;
  top: 16px;
  left: -4px;
  padding: 4px 14px 4px 10px;
  background: var(--kin-500);
  color: var(--ink-900);
  font-family: var(--ff-mincho);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  border-radius: 0 4px 4px 0;
}
.top-subscription__title {
  margin: 28px 0 10px;
  font-family: var(--ff-mincho);
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #fff;
}
.top-subscription__desc {
  margin: 0 0 24px;
  font-size: 13px;
  line-height: 1.85;
  color: rgba(255, 255, 255, 0.88);
}
.top-subscription__perks {
  list-style: none;
  margin: 0 0 auto;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}
.top-subscription__perk {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.92);
}
.top-subscription__perk-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid rgba(201, 169, 97, 0.5);
  background: rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: var(--kin-400);
  flex-shrink: 0;
}
.top-subscription__btn {
  margin-top: 24px;
  align-self: flex-start;
}

@media (max-width: 767px) {
  .top-subscription__perks {
    grid-template-columns: 1fr;
  }
}
</style>
