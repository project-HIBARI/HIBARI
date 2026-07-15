<script setup>
/**
 * 部品名: ファンクラブサイト用 会員ステータス表示
 * 用途: ログイン済み会員の表示・アカウント設定への導線
 */
import { computed } from 'vue'

const props = defineProps({
  userName: { type: String, default: '' },
  avatarPath: { type: String, default: '' },
})

defineEmits(['open-account'])

const displayName = computed(() => props.userName || '会員')
const hasAvatar = computed(() => Boolean(props.avatarPath))
</script>

<template>
  <button
    type="button"
    class="fc-membership-badge"
    :title="`${displayName} さん`"
    aria-haspopup="dialog"
    @click="$emit('open-account')"
  >
    <span class="fc-membership-badge__avatar" aria-hidden="true">
      <img
        v-if="hasAvatar"
        :src="avatarPath"
        :alt="displayName"
        class="fc-membership-badge__avatar-img"
      />
      <template v-else>{{ displayName.charAt(0) }}</template>
    </span>
    <span class="fc-membership-badge__name">{{ displayName }}</span>
    <span class="fc-membership-badge__chevron" aria-hidden="true">▾</span>
  </button>
</template>

<style scoped>
.fc-membership-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  max-width: 180px;
  margin: 0;
  padding: 4px 10px 4px 4px;
  border: 1px solid var(--site-border);
  border-radius: 999px;
  background: #fff;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
}

.fc-membership-badge:hover {
  background: #fffefb;
  border-color: rgba(93, 58, 107, 0.24);
  box-shadow: 0 2px 8px rgba(40, 30, 25, 0.08);
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
  font-size: var(--font-size-navigation);
  font-weight: 700;
  overflow: hidden;
}

.fc-membership-badge__avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.fc-membership-badge__name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: var(--ff-sans-jp);
  font-size: var(--font-size-navigation);
  color: var(--site-text);
}

.fc-membership-badge__chevron {
  flex-shrink: 0;
  font-size: var(--font-size-badge);
  color: var(--site-text-muted);
}
</style>
