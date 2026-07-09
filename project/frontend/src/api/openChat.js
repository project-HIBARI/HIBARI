/**
 * ファンクラブ オープンチャット API
 */
import { apiRequest } from './client.js'

export function fetchOpenChatRooms() {
  return apiRequest('/api/open-chats')
}

export function fetchOpenChatNotifications() {
  return apiRequest('/api/open-chats/notifications')
}

export function fetchOpenChatRoom(roomId) {
  return apiRequest(`/api/open-chats/${roomId}`)
}

export function joinOpenChatRoom(roomId) {
  return apiRequest(`/api/open-chats/${roomId}/join`, { method: 'POST' })
}

export function leaveOpenChatRoom(roomId) {
  return apiRequest(`/api/open-chats/${roomId}/leave`, { method: 'POST' })
}

export function fetchOpenChatMembers(roomId) {
  return apiRequest(`/api/open-chats/${roomId}/members`)
}

export function fetchOpenChatMessages(roomId, { afterId, limit } = {}) {
  const params = new URLSearchParams()
  if (afterId) params.set('after_id', String(afterId))
  if (limit) params.set('limit', String(limit))
  const query = params.toString()
  return apiRequest(`/api/open-chats/${roomId}/messages${query ? `?${query}` : ''}`)
}

export function sendOpenChatMessage(roomId, { body = '', message_type = 'text', media_path = null } = {}) {
  return apiRequest(`/api/open-chats/${roomId}/messages`, {
    method: 'POST',
    body: JSON.stringify({ body, message_type, media_path }),
  })
}

export async function uploadOpenChatMedia(roomId, file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`/api/open-chats/${roomId}/upload`, {
    method: 'POST',
    credentials: 'include',
    body: formData,
  })

  let data = null
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    data = await response.json()
  }

  if (!response.ok) {
    const message = data?.error || `アップロードに失敗しました（${response.status}）`
    const error = new Error(message)
    error.status = response.status
    error.data = data
    throw error
  }

  return data
}
