<script setup>
/**
 * ページ: 通知センター
 * 役割: いいね・コメント・フォロー・DM・ストーリー関連の通知一覧、既読管理、遷移先の解決
 */
import { ref, computed, onMounted } from 'vue'
import UiButton from '../ui/UiButton.vue'
import SnsEmptyState from './sns/SnsEmptyState.vue'
import SnsSkeletonCard from './sns/SnsSkeletonCard.vue'
import NotificationItem from './notifications/NotificationItem.vue'
import { fetchNotifications, markNotificationRead, markAllNotificationsRead } from '../../api/notifications.js'
import { resolveNotificationTarget } from '../../constants/notifications.js'
import { useSnsNotifications } from '../../composables/useSnsNotifications.js'

const emit = defineEmits(['navigate'])

const { refresh: refreshUnreadCount } = useSnsNotifications()

const notifications = ref([])
const loading = ref(false)
const loadingMore = ref(false)
const errorMessage = ref('')
const nextCursor = ref(null)
const markingAllRead = ref(false)

const DAY_MS = 24 * 60 * 60 * 1000

function groupKey(iso) {
  const created = new Date(iso)
  const now = new Date()
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  if (created >= startOfToday) return 'today'
  if (now - created < 7 * DAY_MS) return 'week'
  return 'older'
}

const groupedNotifications = computed(() => {
  const groups = { today: [], week: [], older: [] }
  for (const n of notifications.value) {
    groups[groupKey(n.created_at)].push(n)
  }
  return groups
})

const hasAny = computed(() => notifications.value.length > 0)

async function loadNotifications({ reset = true } = {}) {
  errorMessage.value = ''
  if (reset) {
    loading.value = true
    nextCursor.value = null
  }
  try {
    const data = await fetchNotifications(reset ? {} : { cursor: nextCursor.value })
    notifications.value = reset ? data.notifications : [...notifications.value, ...data.notifications]
    nextCursor.value = data.next_cursor
  } catch (err) {
    errorMessage.value = err?.message || '通知の取得に失敗しました'
  } finally {
    loading.value = false
  }
}

async function loadMore() {
  if (!nextCursor.value || loadingMore.value) return
  loadingMore.value = true
  try {
    const data = await fetchNotifications({ cursor: nextCursor.value })
    notifications.value = [...notifications.value, ...data.notifications]
    nextCursor.value = data.next_cursor
  } catch {
    // 追加読み込み失敗時は現状を維持
  } finally {
    loadingMore.value = false
  }
}

async function onOpen(notification) {
  if (!notification.is_read) {
    notification.is_read = true
    try {
      await markNotificationRead(notification.notification_id)
      refreshUnreadCount()
    } catch {
      // 既読化に失敗しても画面遷移は継続する
    }
  }
  const target = resolveNotificationTarget(notification)
  if (target) emit('navigate', target)
}

async function onMarkAllRead() {
  if (markingAllRead.value) return
  markingAllRead.value = true
  try {
    await markAllNotificationsRead()
    notifications.value = notifications.value.map((n) => ({ ...n, is_read: true }))
    refreshUnreadCount()
  } catch {
    // 失敗時は個別クリックでの既読化にフォールバック
  } finally {
    markingAllRead.value = false
  }
}

onMounted(() => {
  loadNotifications()
})
</script>

<template>
  <div class="sns-notifications">
    <header class="sns-notifications__head">
      <h1 class="sns-notifications__title">通知</h1>
      <UiButton
        variant="outline"
        size="sm"
        :disabled="markingAllRead || !hasAny"
        @click="onMarkAllRead"
      >
        すべて既読
      </UiButton>
    </header>

    <SnsSkeletonCard v-if="loading" variant="post" :count="4" />

    <template v-else-if="errorMessage">
      <div class="sns-notifications__error-card">
        <p class="sns-notifications__state sns-notifications__state--error">読み込みに失敗しました</p>
        <UiButton variant="outline" size="sm" @click="loadNotifications()">もう一度試す</UiButton>
      </div>
    </template>

    <SnsEmptyState
      v-else-if="!hasAny"
      icon="chat"
      title="通知はまだありません"
      message="いいね・コメント・フォロー・DM・ストーリーの反応がここに表示されます"
    />

    <template v-else>
      <section v-if="groupedNotifications.today.length" class="sns-notifications__group">
        <h2 class="sns-notifications__group-title">今日</h2>
        <NotificationItem
          v-for="n in groupedNotifications.today"
          :key="n.notification_id"
          :notification="n"
          @open="onOpen"
        />
      </section>

      <section v-if="groupedNotifications.week.length" class="sns-notifications__group">
        <h2 class="sns-notifications__group-title">過去7日間</h2>
        <NotificationItem
          v-for="n in groupedNotifications.week"
          :key="n.notification_id"
          :notification="n"
          @open="onOpen"
        />
      </section>

      <section v-if="groupedNotifications.older.length" class="sns-notifications__group">
        <h2 class="sns-notifications__group-title">それ以前</h2>
        <NotificationItem
          v-for="n in groupedNotifications.older"
          :key="n.notification_id"
          :notification="n"
          @open="onOpen"
        />
      </section>

      <UiButton v-if="nextCursor" variant="outline" size="sm" :disabled="loadingMore" @click="loadMore">
        {{ loadingMore ? '読み込み中…' : 'もっと見る' }}
      </UiButton>
    </template>
  </div>
</template>

<style scoped>
.sns-notifications {
  position: relative;
  max-width: 640px;
  margin: 0 auto;
  padding: 24px 16px calc(var(--bottom-nav-height, 66px) + env(safe-area-inset-bottom, 0px) + 32px);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sns-notifications__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.sns-notifications__title {
  margin: 0;
  font-family: var(--ff-mincho);
  font-size: clamp(1.35rem, 4vw, 1.75rem);
  color: var(--sns-ivory);
  letter-spacing: 0.06em;
}

.sns-notifications__group {
  display: flex;
  flex-direction: column;
}

.sns-notifications__group-title {
  margin: 0 0 8px;
  padding: 0 2px;
  font-family: var(--ff-sans-jp);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
  color: var(--sns-text-muted, rgba(248, 244, 239, 0.6));
}

.sns-notifications__state {
  margin: 0;
  padding: 24px 12px;
  text-align: center;
  font-size: 13px;
  color: var(--sns-text-muted);
}

.sns-notifications__state--error {
  color: #e08a8a;
}

.sns-notifications__error-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 32px 16px;
  border-radius: var(--site-radius-lg);
  border: 1px solid var(--sns-border);
  background: var(--sns-card);
}

@media (max-width: 767px) {
  .sns-notifications {
    padding-top: 18px;
  }
}
</style>
