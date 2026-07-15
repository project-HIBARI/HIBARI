import { apiRequest } from './client.js'

export function fetchNotifications({ cursor } = {}) {
  const qs = cursor ? `?cursor=${cursor}` : ''
  return apiRequest(`/api/notifications${qs}`)
}

export function fetchNotificationUnreadCount() {
  return apiRequest('/api/notifications/unread-count')
}

export function markNotificationRead(notificationId) {
  return apiRequest(`/api/notifications/${notificationId}/read`, { method: 'POST' })
}

export function markAllNotificationsRead() {
  return apiRequest('/api/notifications/read-all', { method: 'POST' })
}
