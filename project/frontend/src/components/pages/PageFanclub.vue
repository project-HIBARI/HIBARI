<script setup>
/**
 * ページ: ファンクラブ特典紹介
 * 構成: 見出し / 特典ハイライト / プラン・料金 / 加入CTA
 * 導線: 「ファンクラブ加入」→ 新規会員登録（navigate: register）
 */
import PageHead from '../ui/PageHead.vue'
import SectionTitle from '../ui/SectionTitle.vue'
import FanclubBenefits from './fanclub/FanclubBenefits.vue'
import FanclubPlanCard from './fanclub/FanclubPlanCard.vue'
import FanclubJoinCta from './fanclub/FanclubJoinCta.vue'

const emit = defineEmits(['navigate'])

const plans = [
  {
    id: 'standard',
    name: '一般会員',
    price: '¥500',
    unit: '/ 月',
    features: ['月刊ニュースレター', 'チケット先行予約', '掲示板投稿', '月10回 AIひばり対話'],
    locked: ['限定コンテンツ', 'AI新曲制作支援', '優先申込'],
  },
  {
    id: 'premium',
    name: 'プレミアム会員',
    price: '¥1,500',
    unit: '/ 月',
    features: [
      '一般会員特典すべて',
      'プレミアム限定映像',
      '限定コンテンツ',
      'AI新曲制作支援',
      'AIひばり対話 無制限',
      '優先申込 + 会員割引',
    ],
    locked: [],
    recommended: true,
  },
]

function goRegister() {
  emit('navigate', 'register')
}
</script>

<template>
  <div class="page-fanclub">
    <PageHead kanji="會" title="ファンクラブ" sub="Fan Club · 会員特典とプランのご案内" />

    <p class="page-fanclub__intro">
      美空ひばりファンクラブは、限定コンテンツやイベント先行予約など、ファンのための特典をご用意しています。
      あなたにあったプランをお選びいただき、ひばりの世界をより深くお楽しみください。
    </p>

    <section class="page-fanclub__section">
      <SectionTitle title="会員特典" sub="Member Benefits" size="md" />
      <FanclubBenefits />
    </section>

    <section class="page-fanclub__section">
      <SectionTitle title="プラン・料金" sub="Plans &amp; Pricing" size="md" />
      <div class="page-fanclub__plans">
        <FanclubPlanCard
          v-for="plan in plans"
          :key="plan.id"
          :plan="plan"
          @join="goRegister"
        />
      </div>
    </section>

    <FanclubJoinCta class="page-fanclub__cta" @join="goRegister" />
  </div>
</template>

<style scoped>
.page-fanclub {
  color: var(--site-text);
}
.page-fanclub__intro {
  margin: 0 0 var(--sp-7);
  max-width: 760px;
  font-family: var(--ff-sans-jp);
  font-size: 14px;
  line-height: 1.9;
  color: var(--site-text-muted);
}
.page-fanclub__section {
  margin-bottom: var(--sp-8);
}
.page-fanclub__plans {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--sp-5);
  align-items: stretch;
}
.page-fanclub__cta {
  margin-top: var(--sp-7);
}

@media (max-width: 767px) {
  .page-fanclub__plans {
    grid-template-columns: 1fr;
  }
}
</style>
