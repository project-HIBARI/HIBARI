<script setup>
/**
 * 部品名: 通知一覧の1行
 * 役割: 通知内容の表示、クリック時に既読化と画面遷移をPageNotificationsへ委譲する
 */
import UiIco from '../../ui/UiIco.vue'
import { NOTIFICATION_ICON } from '../../../constants/notifications.js'

const props = defineProps({
  notification: { type: Object, required: true },
})

const emit = defineEmits(['open'])

function formatRelativeTime(iso) {
  const diffMs = Date.now() - new Date(iso).getTime()
  const min = Math.floor(diffMs / 60000)
  if (min < 1) return 'たった今'
  if (min < 60) return `${min}分前`
  const hour = Math.floor(min / 60)
  if (hour < 24) return `${hour}時間前`
  const day = Math.floor(hour / 24)
  if (day < 7) return `${day}日前`
  return new Date(iso).toLocaleDateString('ja-JP', { month: 'numeric', day: 'numeric' })
}
</script>

<template>
  <button
    type="button"
    class="notification-item"
    :class="{ 'notification-item--unread': !notification.is_read }"
    @click="emit('open', notification)"
  >
    <span class="notification-item__avatar" aria-hidden="true">
      <img v-if="notification.actor_avatar_path" :src="notification.actor_avatar_path" :alt="notification.actor_name" />
      <span v-else>{{ (notification.actor_name || '?').charAt(0) }}</span>
      <span class="notification-item__icon">
        <UiIco :name="NOTIFICATION_ICON[notification.notification_type] || 'chat'" :size="11" color="#fff" />
      </span>
    </span>

    <span class="notification-item__body">
      <span class="notification-item__message">{{ notification.message }}</span>
      <span class="notification-item__time">{{ formatRelativeTime(notification.created_at) }}</span>
      <span v-if="notification.target_deleted" class="notification-item__deleted">この投稿は削除されています</span>
    </span>

    <span v-if="notification.post_thumbnail_path && !notification.target_deleted" class="notification-item__thumb">
      <img :src="notification.post_thumbnail_path" alt="" loading="lazy" />
    </span>

    <span v-if="!notification.is_read" class="notification-item__dot" aria-hidden="true" />
  </button>
</template>

<style scoped>
.notification-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 64px;
  padding: 10px 14px;
  background: transparent;
  border: 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  cursor: pointer;
  text-align: left;
}

.notification-item--unread {
  background: rgba(228, 190, 99, 0.06);
}

.notification-item__avatar {
  position: relative;
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--sns-purple, var(--murasaki-700));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-family: var(--ff-sans-jp);
}

.notification-item__avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.notification-item__icon {
  position: absolute;
  right: -3px;
  bottom: -3px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--sns-purple, var(--murasaki-600));
  border: 2px solid var(--sns-bg, #1a1418);
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-item__body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.notification-item__message {
  font-size: 13px;
  line-height: 1.5;
  color: var(--sns-ivory, #f8f4ef);
  overflow-wrap: break-word;
}

.notification-item__time {
  font-size: 11px;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.5));
}

.notification-item__deleted {
  font-size: 11px;
  font-style: italic;
  color: rgba(248, 244, 239, 0.45);
}

.notification-item__thumb {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.06);
}

.notification-item__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.notification-item__dot {
  flex-shrink: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--sns-gold, var(--kin-500));
}
</style>
