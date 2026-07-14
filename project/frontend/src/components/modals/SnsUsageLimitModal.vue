<script setup>
/**
 * 部品名: SNS週間投稿上限モーダル
 * 用途: 週間投稿回数の上限に達した際に表示する（プラン案内つき）
 */
import ModalShell from './ModalShell.vue'
import UiButton from '../ui/UiButton.vue'

const props = defineProps({
  membership: { type: String, default: null },
  nextResetLabel: { type: String, default: '' },
})

const emit = defineEmits(['close', 'view-plans'])
</script>

<template>
  <ModalShell title="投稿上限に達しました" @close="emit('close')">
    <div class="sns-limit">
      <p class="sns-limit__text">今週の投稿可能回数に達しました。</p>
      <p v-if="nextResetLabel" class="sns-limit__reset">次回リセット：{{ nextResetLabel }}</p>
      <p class="sns-limit__hint">
        <template v-if="membership === 'general'">
          プレミアム会員なら投稿回数が無制限になります。
        </template>
        <template v-else>
          月額500円会員なら週5回、プレミアム会員なら無制限で投稿できます。
        </template>
      </p>
      <div class="sns-limit__actions">
        <UiButton variant="gold" size="md" @click="emit('view-plans')">プランを見る</UiButton>
        <UiButton variant="ghost" size="md" @click="emit('close')">閉じる</UiButton>
      </div>
    </div>
  </ModalShell>
</template>

<style scoped>
.sns-limit {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.sns-limit__text {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--site-text);
}
.sns-limit__reset {
  margin: 0;
  font-size: 13px;
  color: var(--site-text-muted);
}
.sns-limit__hint {
  margin: 4px 0 0;
  font-size: 13px;
  line-height: 1.8;
  color: var(--site-text-muted);
}
.sns-limit__actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
  flex-wrap: wrap;
}
</style>
