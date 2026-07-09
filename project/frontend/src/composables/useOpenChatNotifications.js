/**
 * オープンチャット通知（未読バッジ + ブラウザ通知）
 */
import { ref } from 'vue'
import { fetchOpenChatNotifications } from '../api/openChat.js'

const POLL_MS = 8000
const STORAGE_KEY = 'hibari_open_chat_notify'

const totalUnread = ref(0)
const roomUnreads = ref([])
const notificationsEnabled = ref(
  typeof localStorage !== 'undefined' && localStorage.getItem(STORAGE_KEY) === '1',
)
const notificationPermission = ref(
  typeof Notification !== 'undefined' ? Notification.permission : 'denied',
)

let pollTimer = null
let activeRoomId = null
let lastNotifiedByRoom = {}

export function useOpenChatNotifications() {
  function setActiveRoomId(roomId) {
    activeRoomId = roomId ?? null
  }

  function shouldSkipBrowserNotify(roomId, messageId) {
    if (activeRoomId === roomId && !document.hidden) {
      lastNotifiedByRoom[roomId] = messageId
      return true
    }
    const prev = lastNotifiedByRoom[roomId] || 0
    if (messageId <= prev) return true
    return false
  }

  function pushBrowserNotifications(rooms) {
    if (
      typeof Notification === 'undefined' ||
      !notificationsEnabled.value ||
      Notification.permission !== 'granted'
    ) {
      return
    }

    for (const room of rooms) {
      const latest = room.latest_unread
      if (!latest) continue
      if (shouldSkipBrowserNotify(room.room_id, latest.message_id)) continue

      const body = `${latest.author_name}: ${latest.preview}`
      try {
        new Notification(room.room_name, {
          body,
          tag: `open-chat-${room.room_id}-${latest.message_id}`,
          icon: '/images/misorahibari-logo-cropped.png',
        })
      } catch {
        // 通知非対応環境
      }
      lastNotifiedByRoom[room.room_id] = latest.message_id
    }
  }

  async function refresh() {
    try {
      const data = await fetchOpenChatNotifications()
      totalUnread.value = data?.total_unread || 0
      roomUnreads.value = data?.rooms || []
      pushBrowserNotifications(roomUnreads.value)
      return data
    } catch {
      return null
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

  async function enableNotifications() {
    if (typeof Notification === 'undefined') {
      return false
    }
    const permission = await Notification.requestPermission()
    notificationPermission.value = permission
    if (permission === 'granted') {
      notificationsEnabled.value = true
      localStorage.setItem(STORAGE_KEY, '1')
      return true
    }
    notificationsEnabled.value = false
    localStorage.removeItem(STORAGE_KEY)
    return false
  }

  function disableNotifications() {
    notificationsEnabled.value = false
    localStorage.removeItem(STORAGE_KEY)
  }

  function unreadForRoom(roomId) {
    const room = roomUnreads.value.find((r) => r.room_id === roomId)
    return room?.unread_count || 0
  }

  return {
    totalUnread,
    roomUnreads,
    notificationsEnabled,
    notificationPermission,
    setActiveRoomId,
    refresh,
    startPolling,
    stopPolling,
    enableNotifications,
    disableNotifications,
    unreadForRoom,
  }
}
