<script setup>
/**
 * 部品名: SNS投稿回数案内カード
 * 用途: 週間投稿可能回数（無制限 / 残り回数）と次回リセット日時を表示
 */
import UiIco from '../../ui/UiIco.vue'

defineProps({
  message: { type: String, required: true },
  nextResetLabel: { type: String, default: '' },
  unlimited: { type: Boolean, default: false },
})
</script>

<template>
  <div class="sns-usage-card" :class="{ 'sns-usage-card--unlimited': unlimited }">
    <span class="sns-usage-card__icon" aria-hidden="true">
      <UiIco name="crown" :size="18" color="var(--sns-gold)" />
    </span>
    <div class="sns-usage-card__text">
      <p class="sns-usage-card__message">{{ message }}</p>
      <p v-if="nextResetLabel" class="sns-usage-card__reset">次回リセット：{{ nextResetLabel }}</p>
    </div>
    <span class="sns-usage-card__deco" aria-hidden="true">♪</span>
  </div>
</template>

<style scoped>
.sns-usage-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--site-radius-lg);
  border: 1px solid rgba(228, 190, 99, 0.3);
  background: linear-gradient(135deg, rgba(109, 61, 130, 0.28), rgba(33, 22, 35, 0.6));
  overflow: hidden;
}
.sns-usage-card__icon {
  flex-shrink: 0;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(228, 190, 99, 0.14);
  border: 1px solid rgba(228, 190, 99, 0.4);
}
.sns-usage-card__text {
  flex: 1;
  min-width: 0;
}
.sns-usage-card__message {
  margin: 0;
  font-family: var(--ff-sans-jp);
  font-size: 13px;
  font-weight: 600;
  color: var(--sns-gold);
}
.sns-usage-card__reset {
  margin: 2px 0 0;
  font-size: 11px;
  color: var(--sns-text-muted);
}
.sns-usage-card__deco {
  position: absolute;
  right: 14px;
  bottom: -6px;
  font-size: 34px;
  color: rgba(228, 190, 99, 0.14);
  pointer-events: none;
}
</style>
