<script setup>
/**
 * 部品名: SNS空状態カード
 * 用途: 投稿なし・ストーリーズなし・保存済みなし等の共通空表示
 */
import UiIco from '../../ui/UiIco.vue'
import UiButton from '../../ui/UiButton.vue'

defineProps({
  icon: { type: String, default: 'image' },
  title: { type: String, required: true },
  message: { type: String, default: '' },
  actionLabel: { type: String, default: '' },
})

defineEmits(['action'])
</script>

<template>
  <div class="sns-empty">
    <span class="sns-empty__icon" aria-hidden="true">
      <UiIco :name="icon" :size="28" color="var(--sns-gold-pale)" />
    </span>
    <p class="sns-empty__title">{{ title }}</p>
    <p v-if="message" class="sns-empty__message">{{ message }}</p>
    <UiButton v-if="actionLabel" variant="gold" size="sm" @click="$emit('action')">
      {{ actionLabel }}
    </UiButton>
  </div>
</template>

<style scoped>
.sns-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 40px 20px;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--sns-border);
  background: var(--sns-card);
  text-align: center;
}
.sns-empty__icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle, rgba(109, 61, 130, 0.5), rgba(33, 22, 35, 0.2));
  border: 1px solid rgba(228, 190, 99, 0.3);
}
.sns-empty__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: var(--font-size-body);
  color: var(--sns-ivory);
}
.sns-empty__message {
  margin: 0;
  max-width: 320px;
  font-size: var(--font-size-caption);
  line-height: 1.8;
  color: var(--sns-text-muted);
}
</style>
