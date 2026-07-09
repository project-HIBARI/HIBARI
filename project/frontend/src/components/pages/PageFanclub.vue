<script setup>
/**
 * ページ: ファンクラブ特典紹介
 * 構成: 見出し / 特典ハイライト / プラン・料金 / 加入CTA
 */
import { ref } from 'vue'
import PageHead from '../ui/PageHead.vue'
import SectionTitle from '../ui/SectionTitle.vue'
import FanclubBenefits from './fanclub/FanclubBenefits.vue'
import FanclubPlanCard from './fanclub/FanclubPlanCard.vue'
import FanclubJoinCta from './fanclub/FanclubJoinCta.vue'
import { MEMBERSHIP_PLANS } from '../../constants/membership.js'
import { useScrollReveal } from '../../composables/useScrollReveal.js'

const emit = defineEmits(['navigate', 'register'])

const pageRoot = ref(null)
useScrollReveal(pageRoot)

const plans = MEMBERSHIP_PLANS

function goRegister(plan) {
  emit('register', plan.id)
}
</script>

<template>
  <div ref="pageRoot" class="page-fanclub">
    <PageHead kanji="會" title="ファンクラブ" sub="Fan Club · 会員特典とプランのご案内" />

    <p class="page-fanclub__intro site-reveal">
      美空ひばりファンクラブは、限定コンテンツやイベント先行予約など、ファンのための特典をご用意しています。
      一般会員・プレミアム会員からお選びいただき、ひばりの世界をより深くお楽しみください。
    </p>

    <section class="page-fanclub__section site-reveal site-reveal--delay-1">
      <SectionTitle title="会員特典" sub="Member Benefits" size="md" />
      <FanclubBenefits />
    </section>

    <section class="page-fanclub__section site-reveal site-reveal--delay-2">
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

    <FanclubJoinCta class="page-fanclub__cta site-reveal site-reveal--delay-3" @join="() => goRegister(plans[0])" />
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
