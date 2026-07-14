<script setup>
/**
 * 部品名: Music Memory Book — プレミアム導線帯
 */
import UiButton from '../../ui/UiButton.vue'
import UiIco from '../../ui/UiIco.vue'

defineProps({
  compact: { type: Boolean, default: false },
})

const emit = defineEmits(['open-fanclub'])
</script>

<template>
  <section class="mmb-premium" :class="{ 'mmb-premium--compact': compact }" aria-label="プレミアム会員のご案内">
    <div class="mmb-premium__inner">
      <div class="mmb-premium__copy">
        <span class="mmb-premium__badge">
          <UiIco name="crown" :size="12" color="var(--kin-400)" />
          Premium
        </span>
        <h3 v-if="!compact" class="mmb-premium__title">
          プレミアム会員になると、すべての思い出をずっと保存できます。
        </h3>
        <p class="mmb-premium__desc">
          年別アルバムの無制限保存、思い出のPDF出力、特別な記念コンテンツなどをご利用いただけます。
        </p>
        <ul v-if="compact" class="mmb-premium__list">
          <li>思い出動画の作成</li>
          <li>PDF保存</li>
          <li>年別アルバムの長期保存</li>
          <li>AIによる振り返り</li>
        </ul>
      </div>
      <UiButton variant="gold" size="md" class="mmb-premium__btn" @click="emit('open-fanclub')">
        プレミアム会員の詳細を見る
      </UiButton>
    </div>
  </section>
</template>

<style scoped>
.mmb-premium {
  margin-top: var(--sp-8);
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(201, 169, 97, 0.35);
  background:
    radial-gradient(ellipse at 0% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 55%),
    linear-gradient(135deg, var(--murasaki-800) 0%, var(--murasaki-700) 100%);
  box-shadow: var(--site-shadow-md);
}

.mmb-premium__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-6);
  padding: var(--sp-6) var(--sp-7);
  flex-wrap: wrap;
}

.mmb-premium--compact .mmb-premium__inner {
  padding: var(--sp-5) var(--sp-6);
}

.mmb-premium__badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 999px;
  border: 1px solid rgba(201, 169, 97, 0.45);
  background: rgba(255, 255, 255, 0.1);
  font-family: var(--ff-latin);
  font-size: 11px;
  letter-spacing: 0.12em;
  color: var(--kin-400);
  margin-bottom: 12px;
}

.mmb-premium__title {
  margin: 0 0 8px;
  font-family: var(--ff-mincho);
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: var(--paper-50);
  line-height: 1.6;
}

.mmb-premium__desc {
  margin: 0;
  font-size: 13px;
  line-height: 1.85;
  color: rgba(255, 255, 255, 0.82);
  max-width: 560px;
}

.mmb-premium__list {
  margin: 12px 0 0;
  padding: 0;
  list-style: none;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px 16px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.78);
}

.mmb-premium__list li {
  padding-left: 14px;
  position: relative;
}

.mmb-premium__list li::before {
  content: '·';
  position: absolute;
  left: 0;
  color: var(--kin-400);
}

.mmb-premium__btn {
  flex-shrink: 0;
}
</style>
