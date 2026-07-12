/**
 * SNS DM 未読件数（ポーリング）
 */
import { ref } from 'vue'
import { fetchDmUnreadCount } from '../api/sns.js'
import { useAuth } from './useAuth.js'

const POLL_MS = 15000

const unreadCount = ref(0)
let pollTimer = null

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

function startPolling() {
  stopPolling()
  refresh()
  pollTimer = window.setInterval(refresh, POLL_MS)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
}

export function useSnsDmUnread() {
  return { unreadCount, refresh, startPolling, stopPolling }
}
