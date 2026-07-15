/**
 * SNS DM 未読件数（ポーリング）
 */
import { ref } from 'vue'
import { fetchDmUnreadCount } from '../api/sns.js'
import { useAuth } from './useAuth.js'

const POLL_MS = 15000

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
    const data = await fetchDmUnreadCount()
    unreadCount.value = data?.unread_count || 0
  } catch {
    // 取得失敗時は現状値を維持
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

export function useSnsDmUnread() {
  return { unreadCount, refresh, startPolling, stopPolling }
}
