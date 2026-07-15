import { ref } from 'vue'
import { fetchNotificationUnreadCount } from '../api/notifications.js'
import { useAuth } from './useAuth.js'

const POLL_MS = 30000

const unreadCount = ref(0)
let pollTimer = null
let visibilityBound = false

async function refresh() {
  const { isLoggedIn } = useAuth()
  if (!isLoggedIn.value) {
    unreadCount.value = 0
    return
  }
  try {
    const data = await fetchNotificationUnreadCount()
    unreadCount.value = data?.unread_count || 0
  } catch {
    // 失敗時は直前の値を維持する
  }
}

function onVisibilityChange() {
  if (!document.hidden) refresh()
}

function startPolling() {
  stopPolling()
  refresh()
  pollTimer = window.setInterval(() => {
    if (document.hidden) return
    refresh()
  }, POLL_MS)
  if (!visibilityBound) {
    document.addEventListener('visibilitychange', onVisibilityChange)
    visibilityBound = true
  }
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
  if (visibilityBound) {
    document.removeEventListener('visibilitychange', onVisibilityChange)
    visibilityBound = false
  }
}

export function useSnsNotifications() {
  return { unreadCount, refresh, startPolling, stopPolling }
}
