<script setup>
/**
 * 部品名: ファンクラブサイト用 会員ステータス表示
 * 用途: ログイン済み会員のプラン表示のみ（認証操作は Music Memories 側）
 */
import { computed } from 'vue'
import { MEMBERSHIP_LABELS } from '../../constants/membership.js'

const props = defineProps({
  userName: { type: String, default: '' },
  membership: { type: String, default: null },
  isFanclubMember: { type: Boolean, default: false },
})

const displayName = computed(() => props.userName || '会員')
const planLabel = computed(() => {
  if (!props.isFanclubMember) return '無料アカウント'
  return MEMBERSHIP_LABELS[props.membership] || '有料会員'
})
</script>

<template>
  <div class="fc-membership-badge" :title="`${displayName} さん（${planLabel}）`">
    <span class="fc-membership-badge__avatar" aria-hidden="true">{{ displayName.charAt(0) }}</span>
    <span class="fc-membership-badge__text">
      <span class="fc-membership-badge__name">{{ displayName }}</span>
      <span class="fc-membership-badge__plan">{{ planLabel }}</span>
    </span>
  </div>
</template>

<style scoped>
.fc-membership-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 200px;
  padding: 4px 12px 4px 4px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: #fff;
}
.fc-membership-badge__avatar {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--murasaki-700);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
}
.fc-membership-badge__text {
  display: flex;
  flex-direction: column;
  min-width: 0;
  line-height: 1.2;
}
.fc-membership-badge__name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: var(--ff-sans-jp);
  font-size: 11px;
  color: var(--site-text);
}
.fc-membership-badge__plan {
  font-family: var(--ff-sans-jp);
  font-size: 10px;
  color: var(--murasaki-700);
  letter-spacing: 0.04em;
}
</style>
