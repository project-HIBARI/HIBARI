/**
 * ファンクラブ オープンチャット API
 */
import { apiRequest } from './client.js'

export function fetchOpenChatRooms() {
  return apiRequest('/api/open-chats')
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

export function sendOpenChatMessage(roomId, body) {
  return apiRequest(`/api/open-chats/${roomId}/messages`, {
    method: 'POST',
    body: JSON.stringify({ body }),
  })
}
